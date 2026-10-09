<#
Build the InflataDepot runtime fuel lock against YOUR legally installed KSP1 files.
No game DLLs are redistributed or uploaded. This generates only InflataDepotPlugin.dll.
Run from the extracted developer kit. Requires .NET Framework C# compiler (Windows).
#>
param([string]$KSPDir = "")
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrWhiteSpace($KSPDir)) { $KSPDir = $env:KSP_DIR }
if ([string]::IsNullOrWhiteSpace($KSPDir)) {
    $candidates = @(
        "${env:ProgramFiles(x86)}\Steam\steamapps\common\Kerbal Space Program",
        "$env:ProgramFiles\Steam\steamapps\common\Kerbal Space Program",
        "C:\Games\Kerbal Space Program"
    )
    foreach ($candidate in $candidates) {
        if ((-not [string]::IsNullOrWhiteSpace($candidate)) -and (Test-Path (Join-Path $candidate 'KSP_x64_Data\Managed\Assembly-CSharp.dll'))) {
            $KSPDir = $candidate; break
        }
    }
}
if ([string]::IsNullOrWhiteSpace($KSPDir)) { $KSPDir = Read-Host 'Full path to your Kerbal Space Program installation folder' }
if ($KSPDir) { $KSPDir = $KSPDir.Trim('"') }
$managed = Join-Path $KSPDir 'KSP_x64_Data\Managed'
if (-not (Test-Path (Join-Path $managed 'Assembly-CSharp.dll'))) { throw "Could not find Assembly-CSharp.dll under $managed. Check the KSP path." }
$csc = Join-Path $env:windir 'Microsoft.NET\Framework\v4.0.30319\csc.exe'
if (-not (Test-Path $csc)) { throw "Missing Microsoft .NET Framework C# compiler: $csc" }
$src = Join-Path $root 'Source\InflataDepotPlugin\ModuleInflataFuelLock.cs'
$plugins = Join-Path $root 'GameData\InflataDepot\Plugins'
New-Item -ItemType Directory -Force -Path $plugins | Out-Null
$output = Join-Path $plugins 'InflataDepotPlugin.dll'
# KSP/Unity splits engine types across modules. In particular, Assembly-CSharp
# exposes UI event interfaces from UnityEngine.UI.dll even though this mod does
# not directly call them. Include every installed UnityEngine module to satisfy
# those transitive compile-time references across supported KSP 1.12 builds.
$assemblyCSharp = Join-Path $managed 'Assembly-CSharp.dll'
$unityAssemblies = @(Get-ChildItem -LiteralPath $managed -Filter 'UnityEngine*.dll' -File | Sort-Object -Property Name)
$unityUi = Join-Path $managed 'UnityEngine.UI.dll'
if (-not (Test-Path -LiteralPath $unityUi)) {
    throw "Required Unity UI reference not found: $unityUi. Check your KSP 1.12.x installation."
}
if ($unityAssemblies.Count -eq 0) { throw "UnityEngine DLLs not found in $managed" }

# Avoid treating a stale DLL from an earlier build as proof of success.
if (Test-Path -LiteralPath $output) { Remove-Item -LiteralPath $output -Force }
$argsCsc = @('/nologo','/target:library','/optimize+')
$argsCsc += "/out:$output"
$argsCsc += "/reference:$assemblyCSharp"
foreach ($asm in $unityAssemblies) {
    $argsCsc += "/reference:$($asm.FullName)"
}
Write-Host ("KSP game assembly: " + $assemblyCSharp) -ForegroundColor Gray
Write-Host ("Unity references: " + $unityAssemblies.Count + " (includes UnityEngine.UI.dll)") -ForegroundColor Gray
Write-Host 'Building deployment lock against your local KSP assemblies...' -ForegroundColor Cyan
& $csc @argsCsc $src
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $output)) { throw 'Compilation failed. Review compiler errors above; do not publish a mod without the DLL.' }
Write-Host "SUCCESS: $output" -ForegroundColor Green
Write-Host 'Next: replace GameData/InflataDepot in the KSP installation with the folder in this kit.'
Write-Host 'In-game, right-click a tank and verify Depot storage reports LOCKED while stowed.'
