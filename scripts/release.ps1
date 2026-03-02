param(
    [switch]$DryRun,
    [switch]$Major,
    [switch]$Minor,
    [switch]$Patch
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-NextVersion {
    param(
        [string]$Current,
        [ValidateSet("major", "minor", "patch")]
        [string]$Bump
    )

    $parts = $Current.Split(".")
    if ($parts.Count -ne 3) {
        throw "Invalid semantic version: $Current"
    }

    $major = [int]$parts[0]
    $minor = [int]$parts[1]
    $patch = [int]$parts[2]

    switch ($Bump) {
        "major" { return "{0}.0.0" -f ($major + 1) }
        "minor" { return "{0}.{1}.0" -f $major, ($minor + 1) }
        default { return "{0}.{1}.{2}" -f $major, $minor, ($patch + 1) }
    }
}

function Get-ChangedFiles {
    param([string]$LastTag)

    $files = @()
    if (-not [string]::IsNullOrWhiteSpace($LastTag)) {
        $files += @(git diff --name-only "$LastTag..HEAD")
    }
    $files += @(git diff --name-only)
    $files += @(git diff --name-only --cached)
    $files += @(git ls-files --others --exclude-standard)

    return @($files | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
}

function Build-SectionLines {
    param(
        [string]$Title,
        [string[]]$Items
    )

    if (-not $Items -or $Items.Count -eq 0) {
        return @()
    }

    $lines = @("### $Title")
    foreach ($item in $Items) {
        $lines += "- $item"
    }
    $lines += ""
    return $lines
}

function Insert-ChangelogEntry {
    param(
        [string]$Path,
        [string]$Version,
        [string]$DateText,
        [hashtable]$Sections,
        [string[]]$SectionOrder
    )

    $entryLines = @("## [$Version] - $DateText", "")
    foreach ($name in $SectionOrder) {
        $entryLines += Build-SectionLines -Title $name -Items $Sections[$name]
    }
    $entryText = ($entryLines -join "`r`n").TrimEnd() + "`r`n`r`n"

    if (-not (Test-Path $Path)) {
        $header = @(
            "# Changelog",
            "",
            "## [Unreleased]",
            "",
            $entryText.TrimEnd()
        ) -join "`r`n"
        Set-Content -Path $Path -Encoding UTF8 -Value ($header + "`r`n")
        return
    }

    $lines = Get-Content -Path $Path
    $existing = @($lines | Where-Object { $_ -match "^## \[$([regex]::Escape($Version))\]\b" })
    if ($existing.Count -gt 0) {
        return
    }

    $firstVersionIdx = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^## \[(?!Unreleased\])') {
            $firstVersionIdx = $i
            break
        }
    }

    if ($firstVersionIdx -lt 0) {
        $updated = ($lines -join "`r`n").TrimEnd() + "`r`n`r`n" + $entryText
    }
    else {
        $top = @()
        if ($firstVersionIdx -gt 0) {
            $top = $lines[0..($firstVersionIdx - 1)]
        }
        $bottom = $lines[$firstVersionIdx..($lines.Count - 1)]
        $updated = ($top -join "`r`n").TrimEnd() + "`r`n`r`n" + $entryText + ($bottom -join "`r`n").TrimEnd() + "`r`n"
    }

    Set-Content -Path $Path -Encoding UTF8 -Value $updated
}

$flagCount = (@($Major, $Minor, $Patch) | Where-Object { $_ -eq $true } | Measure-Object).Count
if ($flagCount -gt 1) {
    throw "Use only one version flag: -Major, -Minor, or -Patch."
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    $marketplacePath = if (Test-Path ".claude-plugin/marketplace.json") {
        ".claude-plugin/marketplace.json"
    }
    elseif (Test-Path "marketplace.json") {
        "marketplace.json"
    }
    else {
        "marketplace.json"
    }

    if (-not (Test-Path $marketplacePath)) {
        $seed = @{
            metadata = @{
                name = "sage_skills"
                displayName = "Sage Skills"
                description = "Reusable cross-runtime skill library."
                author = "Sagecola"
                version = "0.1.0"
            }
            repository = "https://github.com/Sagecola/sage_skills"
            skillsDir = "skills"
        }
        $seed | ConvertTo-Json -Depth 8 | Set-Content -Path $marketplacePath -Encoding UTF8
    }

    $marketplace = Get-Content -Path $marketplacePath -Raw | ConvertFrom-Json
    if (-not $marketplace.metadata) {
        $marketplace | Add-Member -MemberType NoteProperty -Name metadata -Value ([pscustomobject]@{})
    }
    if (-not $marketplace.metadata.version) {
        $marketplace.metadata | Add-Member -MemberType NoteProperty -Name version -Value "0.1.0"
    }

    $currentVersion = [string]$marketplace.metadata.version
    $lastTag = (git tag --sort=-v:refname | Select-Object -First 1)
    if ($lastTag) {
        $lastTag = $lastTag.Trim()
    }
    else {
        $lastTag = ""
    }

    $logRange = if ([string]::IsNullOrWhiteSpace($lastTag)) { "HEAD" } else { "$lastTag..HEAD" }
    $commitLines = @(git log $logRange --oneline)
    $changedFiles = Get-ChangedFiles -LastTag $lastTag

    if (($commitLines.Count -eq 0) -and ($changedFiles.Count -eq 0)) {
        throw "No changes detected to release."
    }

    $newSkills = @()
    foreach ($path in $changedFiles) {
        if ($path -match '^skills/([^/]+)/') {
            $newSkills += $matches[1]
        }
    }
    $newSkills = @($newSkills | Sort-Object -Unique)

    $hasFeat = $false
    foreach ($line in $commitLines) {
        if ($line -match 'feat(\(.+\))?:') { $hasFeat = $true }
    }

    $bump = if ($Major) {
        "major"
    }
    elseif ($Minor) {
        "minor"
    }
    elseif ($Patch) {
        "patch"
    }
    elseif ($hasFeat -or $newSkills.Count -gt 0) {
        "minor"
    }
    else {
        "patch"
    }

    $nextVersion = Get-NextVersion -Current $currentVersion -Bump $bump
    $today = Get-Date -Format "yyyy-MM-dd"

    $featuresEn = @()
    $fixesEn = @()
    $docsEn = @()
    $otherEn = @()
    $featuresZh = @()
    $fixesZh = @()
    $docsZh = @()
    $otherZh = @()

    foreach ($line in $commitLines) {
        $message = ($line -replace '^[a-f0-9]+\s+', '').Trim()
        if ($message -match '^feat(\(.+\))?:') {
            $featuresEn += $message
            $featuresZh += $message
        }
        elseif ($message -match '^fix(\(.+\))?:') {
            $fixesEn += $message
            $fixesZh += $message
        }
        elseif ($message -match '^docs(\(.+\))?:') {
            $docsEn += $message
            $docsZh += $message
        }
        else {
            $otherEn += $message
            $otherZh += $message
        }
    }

    foreach ($skill in $newSkills) {
        $featuresEn += "`$$skill`: skill updates included in this release"
        $featuresZh += "`$$skill`: ben ci fa bu bao han gai ji neng geng xin"
    }

    if (($changedFiles -contains "README.md") -or ($changedFiles -contains "README.zh.md")) {
        $docsEn += "README updated for release"
        $docsZh += "README wen dang yi tong bu geng xin"
    }
    if ($changedFiles -contains "scripts/release.ps1") {
        $otherEn += "release automation script added or updated"
        $otherZh += "xin zeng huo geng xin release zi dong hua jiao ben"
    }
    if (($changedFiles -contains "marketplace.json") -or ($changedFiles -contains ".claude-plugin/marketplace.json")) {
        $otherEn += "marketplace metadata updated"
        $otherZh += "marketplace yuan shu ju yi geng xin"
    }

    $featuresEn = @($featuresEn | Sort-Object -Unique)
    $fixesEn = @($fixesEn | Sort-Object -Unique)
    $docsEn = @($docsEn | Sort-Object -Unique)
    $otherEn = @($otherEn | Sort-Object -Unique)
    $featuresZh = @($featuresZh | Sort-Object -Unique)
    $fixesZh = @($fixesZh | Sort-Object -Unique)
    $docsZh = @($docsZh | Sort-Object -Unique)
    $otherZh = @($otherZh | Sort-Object -Unique)

    if (
        $featuresEn.Count -eq 0 -and
        $fixesEn.Count -eq 0 -and
        $docsEn.Count -eq 0 -and
        $otherEn.Count -eq 0
    ) {
        $otherEn = @("maintenance updates")
        $otherZh = @("wei hu xing geng xin")
    }

    $sectionsEn = @{
        "Features" = $featuresEn
        "Fixes" = $fixesEn
        "Documentation" = $docsEn
        "Other" = $otherEn
    }
    $sectionsZh = @{
        "Gong Neng" = $featuresZh
        "Xiu Fu" = $fixesZh
        "Wen Dang" = $docsZh
        "Qi Ta" = $otherZh
    }

    if ($DryRun) {
        Write-Host "=== DRY RUN MODE ==="
        Write-Host ""
        if ([string]::IsNullOrWhiteSpace($lastTag)) {
            Write-Host "Last tag: (none)"
        }
        else {
            Write-Host "Last tag: $lastTag"
        }
        Write-Host "Current version: v$currentVersion"
        Write-Host "Proposed version: v$nextVersion"
        Write-Host "Bump type: $bump"
        Write-Host ""
        Write-Host "Changed files:"
        foreach ($f in $changedFiles) {
            Write-Host "- $f"
        }
        Write-Host ""
        Write-Host "Files to modify:"
        Write-Host "- CHANGELOG.md"
        Write-Host "- CHANGELOG.zh.md"
        Write-Host "- $marketplacePath"
        Write-Host ""
        Write-Host "No changes made. Run without -DryRun to execute."
        return
    }

    $marketplace.metadata.version = $nextVersion
    $marketplace | ConvertTo-Json -Depth 8 | Set-Content -Path $marketplacePath -Encoding UTF8

    Insert-ChangelogEntry -Path "CHANGELOG.md" -Version $nextVersion -DateText $today -Sections $sectionsEn -SectionOrder @("Features", "Fixes", "Documentation", "Other")
    Insert-ChangelogEntry -Path "CHANGELOG.zh.md" -Version $nextVersion -DateText $today -Sections $sectionsZh -SectionOrder @("Gong Neng", "Xiu Fu", "Wen Dang", "Qi Ta")

    $filesToAdd = @("CHANGELOG.md", "CHANGELOG.zh.md", $marketplacePath)
    if (Test-Path "README.md") { $filesToAdd += "README.md" }
    if (Test-Path "README.zh.md") { $filesToAdd += "README.zh.md" }

    git add -- $filesToAdd
    $staged = @(git diff --cached --name-only)
    if ($staged.Count -eq 0) {
        throw "No staged release changes after update."
    }

    git commit -m "chore: release v$nextVersion"
    git tag "v$nextVersion"

    Write-Host "Release v$nextVersion created locally."
    Write-Host ""
    Write-Host "To publish:"
    Write-Host "  git push origin main"
    Write-Host "  git push origin v$nextVersion"
}
finally {
    Pop-Location
}
