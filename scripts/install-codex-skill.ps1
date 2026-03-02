param(
    [string]$SkillName,
    [switch]$All,
    [string]$Dest = "$HOME/.codex/skills",
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$mainInstaller = Join-Path $PSScriptRoot 'install-skills.ps1'
$tempConfig = Join-Path $repoRoot '.tmp-codex-targets.json'

@"
{
  "targets": [
    {
      "name": "codex",
      "enabled": true,
      "path": "$Dest"
    }
  ]
}
"@ | Set-Content -Path $tempConfig -Encoding UTF8

try {
    $argsList = @('-ExecutionPolicy','Bypass','-File', $mainInstaller, '-ConfigPath', $tempConfig)

    if ($All) {
        $argsList += '-All'
    }
    else {
        if ([string]::IsNullOrWhiteSpace($SkillName)) {
            throw 'Specify -SkillName <name> or use -All'
        }
        $argsList += @('-SkillName', $SkillName)
    }

    if ($DryRun) {
        $argsList += '-DryRun'
    }

    & powershell @argsList
}
finally {
    Remove-Item -Path $tempConfig -Force -ErrorAction SilentlyContinue
}
