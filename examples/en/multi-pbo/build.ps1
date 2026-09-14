[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [ValidateNotNullOrEmpty()] [string]$ToolRoot,
    [Parameter(Mandatory = $true)] [ValidateNotNullOrEmpty()] [string]$WorkRoot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Require-File([string]$Path, [string]$Label) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "$Label was not found: $Path" }
    return (Resolve-Path -LiteralPath $Path).Path
}
function Get-NormalizedAbsolutePath([string]$Path) {
    return [IO.Path]::GetFullPath($Path).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
}
function Test-IsWithinDirectory([string]$Candidate, [string]$Directory) {
    $candidatePath = Get-NormalizedAbsolutePath $Candidate
    $directoryPath = (Get-NormalizedAbsolutePath $Directory) + [IO.Path]::DirectorySeparatorChar
    return $candidatePath.StartsWith($directoryPath, [StringComparison]::OrdinalIgnoreCase)
}
function ConvertTo-NormalizedVirtualPath([string]$Path) { return $Path.Trim().Replace('\', '/').TrimStart('/').ToLowerInvariant() }
function Invoke-Tool([string]$Exe, [string[]]$Arguments, [string]$LogPath, [string]$Label) {
    $text = (& $Exe @Arguments 2>&1 | Out-String)
    $exitCode = $LASTEXITCODE
    Set-Content -LiteralPath $LogPath -Value $text -Encoding utf8
    if ($exitCode -ne 0) { throw "$Label exited $exitCode. See $LogPath" }
    # Addon Builder has been observed to return 0 after fatal tool-path failures.
    if ($text -match '(?im)(?:^|[\r\n])\s*(?:\[[^\]]+\]\s*)?\[(?:FATAL|ERROR)\]|^\s*(?:FATAL|ERROR)\b') { throw "$Label emitted FATAL/ERROR text. See $LogPath" }
    return $text
}
function Get-BankRevMemberLines([string]$Text, [string]$Prefix, [string]$Component) {
    $normalizedPrefix = ConvertTo-NormalizedVirtualPath $Prefix
    $prefixBoundary = $normalizedPrefix + '/'
    $lines = @($Text -split "`r?`n" | ForEach-Object { $_.Trim() } | Where-Object { $_.Length -gt 0 })
    if ($lines.Count -eq 0) { throw "BankRev member table for $Component was empty." }
    $members = [System.Collections.Generic.List[object]]::new()
    foreach ($line in $lines) {
        $normalizedLine = ConvertTo-NormalizedVirtualPath $line
        if (-not $normalizedLine.StartsWith($prefixBoundary, [StringComparison]::OrdinalIgnoreCase)) { throw "BankRev member line for $Component is outside the exact manifest prefix boundary '$Prefix': $line" }
        $relativePath = $normalizedLine.Substring($prefixBoundary.Length)
        if ([string]::IsNullOrWhiteSpace($relativePath)) { throw "BankRev member line for $Component has no member path after prefix '$Prefix': $line" }
        $members.Add([PSCustomObject]@{ line = $line; normalized_path = $normalizedLine })
    }
    return $members
}
function Assert-ExhaustiveDSCheck([string]$Text, [object[]]$ExpectedSignatures, [string]$Package) {
    $expected = @($ExpectedSignatures | ForEach-Object { Get-NormalizedAbsolutePath $_ })
    $actual = [System.Collections.Generic.List[string]]::new()
    $lines = @($Text -split "`r?`n" | ForEach-Object { $_.Trim() } | Where-Object { $_.Length -gt 0 })
    if ($lines.Count -eq 0) { throw "DSCheckSignatures ($Package) emitted no signature-result lines." }
    foreach ($line in $lines) {
        $match = [regex]::Match($line, '^Signature\s+(.+?)\s+is OK$')
        if (-not $match.Success) { throw "DSCheckSignatures ($Package) emitted unexpected or non-OK output: $line" }
        $actual.Add((Get-NormalizedAbsolutePath $match.Groups[1].Value))
    }
    $duplicateActual = @($actual | Group-Object | Where-Object Count -gt 1)
    if ($duplicateActual.Count -gt 0) { throw "DSCheckSignatures ($Package) reported a signature more than once: $($duplicateActual[0].Name)" }
    $missing = @($expected | Where-Object { $_ -notin $actual })
    $unexpected = @($actual | Where-Object { $_ -notin $expected })
    if ($missing.Count -gt 0 -or $unexpected.Count -gt 0 -or $actual.Count -ne $expected.Count) { throw "DSCheckSignatures ($Package) did not produce a one-to-one set of expected OK results. Missing: $($missing -join '; '). Unexpected: $($unexpected -join '; ')." }
    return @($actual)
}

$root = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$requestedWorkRoot = Get-NormalizedAbsolutePath $WorkRoot
if ($requestedWorkRoot -eq $root -or (Test-IsWithinDirectory $requestedWorkRoot $root)) { throw 'WorkRoot must be outside the versioned examples/en/multi-pbo fixture tree.' }
$manifestPath = Join-Path $root 'manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ((Resolve-Path -LiteralPath $ToolRoot).Path -eq $root) { throw 'ToolRoot must be the installed DayZ Experimental Tools directory, not this fixture.' }

$addonBuilder = Require-File (Join-Path $ToolRoot 'Bin\AddonBuilder\AddonBuilder.exe') 'Addon Builder'
$bankRev = Require-File (Join-Path $ToolRoot 'Bin\PboUtils\BankRev.exe') 'BankRev'
$dsCreateKey = Require-File (Join-Path $ToolRoot 'Bin\DsUtils\DSCreateKey.exe') 'DSCreateKey'
$dsSignFile = Require-File (Join-Path $ToolRoot 'Bin\DsUtils\DSSignFile.exe') 'DSSignFile'
$dsCheck = Require-File (Join-Path $ToolRoot 'Bin\DsUtils\DSCheckSignatures.exe') 'DSCheckSignatures'
$toolHashes = @{}
@($addonBuilder, $bankRev, $dsCreateKey, $dsSignFile, $dsCheck) | ForEach-Object { $toolHashes[$_] = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash }

New-Item -ItemType Directory -Force -Path $requestedWorkRoot | Out-Null
$runId = 'pboexample-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [Guid]::NewGuid().ToString('N').Substring(0, 8)
$runRoot = Join-Path $requestedWorkRoot $runId
$tempRoot = Join-Path $runRoot 'temp'; $buildRoot = Join-Path $runRoot 'build'; $releaseRoot = Join-Path $runRoot 'release'; $logsRoot = Join-Path $runRoot 'logs'; $keysRoot = Join-Path $runRoot 'keys'
@($tempRoot, $buildRoot, $releaseRoot, $logsRoot, $keysRoot) | ForEach-Object { New-Item -ItemType Directory -Force -Path $_ | Out-Null }

# Phase 1: all PBOs are built, finally named, BankRev-inspected, and collision-collected before any hash or signature exists.
$records = [System.Collections.Generic.List[object]]::new(); $virtualPaths = [System.Collections.Generic.List[object]]::new()
foreach ($component in $manifest.components) {
    $source = Require-File (Join-Path $root (Join-Path $component.source 'config.cpp')) "$($component.id) config.cpp"
    $sourceRoot = Split-Path -Parent $source; $componentTemp = Join-Path $tempRoot $component.id; $componentBuild = Join-Path $buildRoot $component.id
    New-Item -ItemType Directory -Force -Path $componentTemp, $componentBuild | Out-Null
    $addonLog = Join-Path $logsRoot "$($component.id)-addon-builder.log"
    $addonArgs = @($sourceRoot, $componentBuild, '-packonly', '-clear', "-temp=$componentTemp", "-prefix=$($component.prefix)", "-toolsDirectory=$ToolRoot")
    Invoke-Tool $addonBuilder $addonArgs $addonLog "Addon Builder ($($component.id))" | Out-Null
    $builtPbos = @(Get-ChildItem -LiteralPath $componentBuild -File -Filter '*.pbo')
    if ($builtPbos.Count -ne 1 -or $builtPbos[0].Length -le 0) { throw "Addon Builder ($($component.id)) did not create exactly one non-empty PBO in $componentBuild." }
    $addonsRoot = Join-Path (Join-Path $releaseRoot $component.package) 'Addons'; New-Item -ItemType Directory -Force -Path $addonsRoot | Out-Null
    $finalPbo = Join-Path $addonsRoot $component.pbo; Move-Item -LiteralPath $builtPbos[0].FullName -Destination $finalPbo
    if (-not (Test-Path -LiteralPath $finalPbo -PathType Leaf)) { throw "Final manifest name was not created: $finalPbo" }
    $propertiesLog = Join-Path $logsRoot "$($component.id)-bankrev-properties.log"; $properties = Invoke-Tool $bankRev @('-properties', $finalPbo) $propertiesLog "BankRev properties ($($component.id))"
    $prefixPattern = '(?i)(?<!\S)' + [regex]::Escape($component.prefix).Replace('/', '[\\/]') + '(?:[\\/]+)?(?=\s|$)'
    if ($properties -notmatch $prefixPattern) { throw "BankRev properties for $($component.id) did not show manifest prefix $($component.prefix)." }
    $membersLog = Join-Path $logsRoot "$($component.id)-bankrev-members.log"
    $members = @(Get-BankRevMemberLines (Invoke-Tool $bankRev @('-logFull', $finalPbo) $membersLog "BankRev members ($($component.id))") $component.prefix $component.id)
    foreach ($member in $members) { $virtualPaths.Add([PSCustomObject]@{ component = $component.id; line = $member.line; path = $member.normalized_path }) }
    $records.Add([PSCustomObject]@{ id = $component.id; source = $component.source; package = $component.package; pbo = $component.pbo; prefix = $component.prefix; addon = $component.addon; command = @($addonBuilder) + $addonArgs; final_pbo = $finalPbo; member_count_observed = $members.Count; bankrev_member_lines = @($members | ForEach-Object line) })
}
$duplicatePaths = @($virtualPaths | Group-Object path | Where-Object Count -gt 1)
if ($duplicatePaths.Count -gt 0) { $detail = $duplicatePaths | ForEach-Object { $_.Name + ' (' + (($_.Group.component) -join ', ') + ')' }; throw 'Normalized virtual-path collision rejected before hashing or signing: ' + ($detail -join '; ') }

# Phase 2: only the collision-clean final PBO set is hashed, signed, and verified.
$authority = $manifest.authority
Push-Location $keysRoot; try { Invoke-Tool $dsCreateKey @($authority) (Join-Path $logsRoot 'dscreatekey.log') 'DSCreateKey' | Out-Null } finally { Pop-Location }
$privateKey = Require-File (Join-Path $keysRoot "$authority.biprivatekey") 'Generated private key'; $publicKey = Require-File (Join-Path $keysRoot "$authority.bikey") 'Generated public key'
foreach ($record in $records) {
    $beforeSignHash = (Get-FileHash -LiteralPath $record.final_pbo -Algorithm SHA256).Hash; $signLog = Join-Path $logsRoot "$($record.id)-sign.log"
    Invoke-Tool $dsSignFile @($privateKey, $record.final_pbo) $signLog "DSSignFile ($($record.id))" | Out-Null
    $afterSignHash = (Get-FileHash -LiteralPath $record.final_pbo -Algorithm SHA256).Hash
    if ($beforeSignHash -ne $afterSignHash) { throw "DSSignFile unexpectedly changed final PBO bytes for $($record.id)." }
    $bisigns = @(Get-ChildItem -LiteralPath (Split-Path -Parent $record.final_pbo) -File | Where-Object { $_.Name -like "$($record.pbo).*" -and $_.Extension -eq '.bisign' })
    if ($bisigns.Count -ne 1) { throw "DSSignFile ($($record.id)) did not create exactly one expected bisign beside the final PBO." }
    $record | Add-Member -NotePropertyName pbo_sha256 -NotePropertyValue $afterSignHash; $record | Add-Member -NotePropertyName bisign -NotePropertyValue $bisigns[0].Name; $record | Add-Member -NotePropertyName bisign_path -NotePropertyValue $bisigns[0].FullName; $record | Add-Member -NotePropertyName bisign_sha256 -NotePropertyValue ((Get-FileHash -LiteralPath $bisigns[0].FullName -Algorithm SHA256).Hash)
}
Copy-Item -LiteralPath (Join-Path $root 'package\Shared\mod.cpp') -Destination (Join-Path $releaseRoot '@PBOExample\mod.cpp'); Copy-Item -LiteralPath (Join-Path $root 'package\Server\mod.cpp') -Destination (Join-Path $releaseRoot '@PBOExampleServer\mod.cpp')
New-Item -ItemType Directory -Force -Path (Join-Path $releaseRoot '@PBOExample\Keys') | Out-Null; Copy-Item -LiteralPath $publicKey -Destination (Join-Path $releaseRoot "@PBOExample\Keys\$authority.bikey")

$checkResults = [System.Collections.Generic.List[object]]::new()
foreach ($package in @('@PBOExample', '@PBOExampleServer')) {
    $addons = Join-Path $releaseRoot "$package\Addons"; $checkLog = Join-Path $logsRoot (($package.TrimStart('@')) + '-dscheck.log')
    $checkText = Invoke-Tool $dsCheck @($addons, (Join-Path $releaseRoot '@PBOExample\Keys')) $checkLog "DSCheckSignatures ($package)"
    $expected = @($records | Where-Object package -eq $package | ForEach-Object bisign_path); $actual = @(Assert-ExhaustiveDSCheck $checkText $expected $package)
    $checkResults.Add([PSCustomObject]@{ package = $package; expected_bisigns = $expected; ok_bisigns = $actual; stdout = $checkText.Trim(); log = $checkLog })
}
$receipt = [PSCustomObject]@{ schema_version = 2; fixture = $manifest.example; run_root = $runRoot; tool_root = (Resolve-Path -LiteralPath $ToolRoot).Path; tool_sha256 = $toolHashes; manifest_sha256 = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash; workflow = @('build/final-name/BankRev/member-collision for all components', 'hash/sign only after global collision pass', 'exhaustive DSCheck one-to-one OK matching'); components = $records; normalized_virtual_paths = $virtualPaths; duplicate_path_policy = 'case-insensitive normalized virtual paths; fail before hashing or signing; fixture release policy, not an engine-law claim'; dscheck = $checkResults; runtime_not_tested = @('DayZ boot', 'client join and folder-level serverMod distribution', 'cross-PBO CfgMods path resolution', 'requiredAddons runtime resolution', 'verifySignatures=2 enforcement including changed/missing/wrong-key cases', 'whether serverMod-only PBO signatures are operationally checked') }
$receiptPath = Join-Path $runRoot 'receipt.json'; $receipt | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $receiptPath -Encoding utf8
Write-Output "SUCCESS: isolated release and receipt created at $runRoot"; Write-Output "Receipt: $receiptPath"
