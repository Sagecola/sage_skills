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

$flagCount = (@($Major, $Minor, $Patch) | Where-Object { $_ -eq $true } | Measure-Object).Count
if ($flagCount -gt 1) {
    throw "Use only one version flag: -Major, -Minor, or -Patch."
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    $pluginDir = ".claude-plugin"
    $marketplacePath = Join-Path $pluginDir "marketplace.json"
    $pluginManifestPath = Join-Path $pluginDir "plugin.json"

    if (-not (Test-Path $marketplacePath)) {
        if (-not (Test-Path $pluginDir)) {
            New-Item -ItemType Directory -Path $pluginDir -Force | Out-Null
        }

        $seed = @{
            name = "sage-skills"
            owner = @{
                name = "Sagecola"
                url = "https://github.com/Sagecola"
            }
            metadata = @{
                description = "Reusable cross-runtime skill library."
                version = "0.1.0"
            }
            plugins = @(
                @{
                    name = "sage-skills"
                    source = "./"
                    description = "Sage Skills marketplace bundle."
                    version = "0.1.0"
                }
            )
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
        Write-Host "- $marketplacePath"
        if (Test-Path $pluginManifestPath) {
            Write-Host "- $pluginManifestPath"
        }
        Write-Host ""
        Write-Host "No changes made. Run without -DryRun to execute."
        return
    }

    $marketplace.metadata.version = $nextVersion
    if ($marketplace.plugins) {
        foreach ($entry in $marketplace.plugins) {
            if ($entry.PSObject.Properties.Name -contains "version") {
                $entry.version = $nextVersion
            }
        }
    }
    $marketplace | ConvertTo-Json -Depth 8 | Set-Content -Path $marketplacePath -Encoding UTF8

    $filesToAdd = @($marketplacePath)

    if (Test-Path $pluginManifestPath) {
        $pluginManifest = Get-Content -Path $pluginManifestPath -Raw | ConvertFrom-Json
        if ($pluginManifest.PSObject.Properties.Name -contains "version") {
            $pluginManifest.version = $nextVersion
            $pluginManifest | ConvertTo-Json -Depth 8 | Set-Content -Path $pluginManifestPath -Encoding UTF8
            $filesToAdd += $pluginManifestPath
        }
    }

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
