param(
    [string]$SkillName,
    [switch]$All,
    [string[]]$Tool,
    [string]$ConfigPath = "",
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$skillsRoot = Join-Path $repoRoot 'skills'

if (-not (Test-Path $skillsRoot)) {
    throw "skills directory not found: $skillsRoot"
}

if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    $defaultConfig = Join-Path $PSScriptRoot 'targets.json'
    $exampleConfig = Join-Path $PSScriptRoot 'targets.example.json'

    if (Test-Path $defaultConfig) {
        $ConfigPath = $defaultConfig
    }
    elseif (Test-Path $exampleConfig) {
        $ConfigPath = $exampleConfig
    }
    else {
        throw 'No targets config found. Create scripts/targets.json first.'
    }
}

if (-not (Test-Path $ConfigPath)) {
    throw "Config file not found: $ConfigPath"
}

function Resolve-UserPath([string]$rawPath) {
    if ([string]::IsNullOrWhiteSpace($rawPath)) {
        return $rawPath
    }

    $expanded = [Environment]::ExpandEnvironmentVariables($rawPath)

    if ($expanded.StartsWith('~')) {
        $expanded = $expanded -replace '^~', $HOME
    }

    if ($expanded.Contains('$HOME')) {
        $expanded = $expanded.Replace('$HOME', $HOME)
    }

    return $expanded
}

$config = Get-Content -Path $ConfigPath -Raw | ConvertFrom-Json
if (-not $config.targets) {
    throw "Invalid config: missing 'targets'"
}

$targets = @($config.targets | Where-Object { $_.enabled -eq $true })

if ($Tool -and $Tool.Count -gt 0) {
    $toolSet = @{}
    foreach ($t in $Tool) {
        $toolSet[$t.ToLowerInvariant()] = $true
    }

    $targets = @($targets | Where-Object {
        $toolSet.ContainsKey($_.name.ToLowerInvariant())
    })
}

if ($targets.Count -eq 0) {
    throw 'No enabled targets selected.'
}

$skillDirs = @()
if ($All) {
    $skillDirs = @(Get-ChildItem -Path $skillsRoot -Directory)
}
else {
    if ([string]::IsNullOrWhiteSpace($SkillName)) {
        throw 'Specify -SkillName <name> or use -All'
    }

    $source = Join-Path $skillsRoot $SkillName
    if (-not (Test-Path $source)) {
        throw "Skill not found: $source"
    }

    $skillDirs = @((Get-Item $source))
}

foreach ($target in $targets) {
    $targetRoot = Resolve-UserPath $target.path

    if ([string]::IsNullOrWhiteSpace($targetRoot)) {
        throw "Target path is empty for runtime: $($target.name)"
    }

    if (-not (Test-Path $targetRoot)) {
        if ($DryRun) {
            Write-Host "[DryRun] Create directory: $targetRoot"
        }
        else {
            New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
        }
    }

    foreach ($dir in $skillDirs) {
        $dest = Join-Path $targetRoot $dir.Name
        if ($DryRun) {
            Write-Host "[DryRun] $($dir.FullName) -> $dest"
        }
        else {
            Copy-Item -Path $dir.FullName -Destination $dest -Recurse -Force
            Write-Host "Installed [$($target.name)]: $($dir.Name) -> $dest"
        }
    }
}
