[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [ValidateNotNullOrEmpty()] [string]$ToolRoot,
    [Parameter(Mandatory = $true)] [ValidateNotNullOrEmpty()] [string]$WorkRoot,
    [Parameter(Mandatory = $true)] [ValidateSet('v1', 'v2', 'matrix')] [string]$Variant
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
function Test-IsSamePath([string]$Left, [string]$Right) {
    return (Get-NormalizedAbsolutePath $Left).Equals((Get-NormalizedAbsolutePath $Right), [StringComparison]::OrdinalIgnoreCase)
}
function Test-IsReparsePoint([string]$Path) {
    return ((Get-Item -LiteralPath $Path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
}
function Assert-OrdinaryDirectory([string]$Path, [string]$Label) {
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) { throw "$Label is not a directory: $Path" }
    if (Test-IsReparsePoint $Path) { throw "$Label must not be a reparse point: $Path" }
    return (Resolve-Path -LiteralPath $Path).Path
}
function Ensure-OrdinaryDirectoryChain([string]$BasePath, [string]$CandidatePath, [string]$Label) {
    $base = Assert-OrdinaryDirectory $BasePath "$Label base"
    $candidate = Get-NormalizedAbsolutePath $CandidatePath
    if (-not ((Test-IsSamePath $candidate $base) -or (Test-IsWithinDirectory $candidate $base))) { throw "$Label escapes its approved base: $candidate" }

    $relative = $candidate.Substring($base.Length).TrimStart([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $current = $base
    if (-not [string]::IsNullOrWhiteSpace($relative)) {
        foreach ($segment in ($relative -split '[\\/]')) {
            if ([string]::IsNullOrWhiteSpace($segment)) { continue }
            $current = Join-Path $current $segment
            if (-not (Test-Path -LiteralPath $current)) {
                New-Item -ItemType Directory -Path $current -ErrorAction Stop | Out-Null
            }
            $current = Assert-OrdinaryDirectory $current "$Label path component"
        }
    }
    return (Assert-OrdinaryDirectory $current $Label)
}
function Assert-CaseInsensitiveUnique([string[]]$Names, [string]$Label) {
    $seen = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($name in $Names) {
        if (-not $seen.Add($name)) { throw "$Label contains a case-insensitive duplicate: $name" }
    }
}
function Invoke-Tool([string]$Exe, [string[]]$Arguments, [string]$LogPath, [string]$Label) {
    $text = (& $Exe @Arguments 2>&1 | Out-String)
    $exitCode = $LASTEXITCODE
    Set-Content -LiteralPath $LogPath -Value $text -Encoding utf8
    if ($exitCode -ne 0) { throw "$Label exited $exitCode. See $LogPath" }
    if ($text -match '(?im)(?:^|[\r\n])\s*(?:\[[^\]]+\]\s*)?\[(?:FATAL|ERROR)\]|^\s*(?:FATAL|ERROR)\b') { throw "$Label emitted FATAL/ERROR text. See $LogPath" }
    return $text
}

$root = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$repositoryRoot = [IO.Directory]::GetParent($root).FullName
$repositoryRoot = [IO.Directory]::GetParent($repositoryRoot).FullName
$repositoryRoot = [IO.Directory]::GetParent($repositoryRoot).FullName
$repositoryRoot = Assert-OrdinaryDirectory $repositoryRoot 'Repository root'
$temporaryRoot = Ensure-OrdinaryDirectoryChain $repositoryRoot (Join-Path $repositoryRoot 'TEMP') 'TEMP'
$disposableRoot = Join-Path $temporaryRoot 'entity-persistence-repair'
$requestedWorkRoot = Get-NormalizedAbsolutePath $WorkRoot
if ((Test-IsSamePath $requestedWorkRoot $repositoryRoot) -or (Test-IsWithinDirectory $repositoryRoot $requestedWorkRoot)) { throw 'WorkRoot must not be the repository root or an ancestor of it.' }
if ((Test-IsSamePath $requestedWorkRoot $root) -or (Test-IsWithinDirectory $requestedWorkRoot $root)) { throw 'WorkRoot must be outside the versioned fixture tree.' }
if (-not ((Test-IsSamePath $requestedWorkRoot $disposableRoot) -or (Test-IsWithinDirectory $requestedWorkRoot $disposableRoot))) { throw "WorkRoot must be the explicitly disposable path $disposableRoot or one of its children." }
$toolRootResolved = (Resolve-Path -LiteralPath $ToolRoot).Path
if ($toolRootResolved -eq $root) { throw 'ToolRoot must be the installed DayZ Experimental Tools directory, not this fixture.' }

$addonBuilder = Require-File (Join-Path $toolRootResolved 'Bin\AddonBuilder\AddonBuilder.exe') 'Addon Builder'
$bankRev = Require-File (Join-Path $toolRootResolved 'Bin\PboUtils\BankRev.exe') 'BankRev'
$variantRoot = Join-Path $root (Join-Path 'variants' $Variant)
$config = Require-File (Join-Path $variantRoot 'config.cpp') "$Variant config.cpp"
$script = Require-File (Join-Path $variantRoot 'scripts\4_World\EntityPersistenceFixture\EntityPersistenceFixtureBattery.c') "$Variant 4_World script"
$manifestPath = Require-File (Join-Path $root 'manifest.json') 'fixture manifest'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($Variant -notin @($manifest.variants)) { throw "Variant $Variant is not declared by manifest.json." }
$expectedPboName = [IO.Path]::GetFileName([string]$manifest.pbo)
if ([string]::IsNullOrWhiteSpace($expectedPboName) -or $expectedPboName -ne [string]$manifest.pbo -or [IO.Path]::GetExtension($expectedPboName) -ine '.pbo') { throw 'manifest.json pbo must be one canonical .pbo file name without a directory.' }

$disposableRoot = Ensure-OrdinaryDirectoryChain $temporaryRoot $disposableRoot 'Disposable fixture root'
$workRootResolved = Ensure-OrdinaryDirectoryChain $disposableRoot $requestedWorkRoot 'WorkRoot'
if (-not ((Test-IsSamePath $workRootResolved $disposableRoot) -or (Test-IsWithinDirectory $workRootResolved $disposableRoot))) { throw 'Resolved WorkRoot escapes the disposable path.' }
$runRoot = Join-Path $workRootResolved ('entity-persistence-' + $Variant + '-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [Guid]::NewGuid().ToString('N').Substring(0, 8))
if (Test-Path -LiteralPath $runRoot) { throw "Generated run directory unexpectedly already exists: $runRoot" }
New-Item -ItemType Directory -Path $runRoot -ErrorAction Stop | Out-Null
$runRoot = Assert-OrdinaryDirectory $runRoot 'Generated run directory'
$buildRoot = Ensure-OrdinaryDirectoryChain $runRoot (Join-Path $runRoot 'build') 'Build directory'
$addonTempRoot = Ensure-OrdinaryDirectoryChain $runRoot (Join-Path $runRoot 'temp') 'Addon Builder temporary directory'
$logsRoot = Ensure-OrdinaryDirectoryChain $runRoot (Join-Path $runRoot 'logs') 'Logs directory'
$inspectRoot = Ensure-OrdinaryDirectoryChain $runRoot (Join-Path $runRoot 'inspect') 'Inspection directory'
if (-not (Test-IsWithinDirectory $runRoot $workRootResolved) -or -not (Test-IsWithinDirectory $addonTempRoot $runRoot)) { throw 'Generated run or Addon Builder -clear path is outside the disposable run root.' }
Assert-OrdinaryDirectory $runRoot 'Generated run directory' | Out-Null
Assert-OrdinaryDirectory $addonTempRoot 'Addon Builder -clear path' | Out-Null

$addonLog = Join-Path $logsRoot 'addon-builder.log'
$addonArgs = @($variantRoot, $buildRoot, '-packonly', '-clear', "-temp=$addonTempRoot", "-prefix=$($manifest.prefix)", "-toolsDirectory=$toolRootResolved")
Invoke-Tool $addonBuilder $addonArgs $addonLog 'Addon Builder (package-only)' | Out-Null
$pboFiles = @(Get-ChildItem -LiteralPath $buildRoot -File -Filter '*.pbo')
if ($pboFiles.Count -ne 1 -or $pboFiles[0].Length -le 0) { throw 'Addon Builder did not create exactly one non-empty PBO.' }
$pbo = $pboFiles[0]
$canonicalPbo = Join-Path $buildRoot $expectedPboName
if ($pbo.Name -ine $expectedPboName) {
    Move-Item -LiteralPath $pbo.FullName -Destination $canonicalPbo -ErrorAction Stop
}
$pbo = Get-Item -LiteralPath $canonicalPbo -ErrorAction Stop
if ($pbo.Name -ine $expectedPboName -or $pbo.Length -le 0) { throw "Canonical manifest PBO was not produced: $expectedPboName" }

$propertiesLog = Join-Path $logsRoot 'bankrev-properties.log'
$properties = Invoke-Tool $bankRev @('-properties', $pbo.FullName) $propertiesLog 'BankRev properties'
$prefixPattern = '(?i)(?<!\S)' + [regex]::Escape($manifest.prefix).Replace('/', '[\\/]') + '(?:[\\/]+)?(?=\s|$)'
if ($properties -notmatch $prefixPattern) { throw "BankRev did not show requested prefix $($manifest.prefix)." }
$membersLog = Join-Path $logsRoot 'bankrev-members.log'
$membersText = Invoke-Tool $bankRev @('-logFull', $pbo.FullName) $membersLog 'BankRev member listing'
$members = @($membersText -split "`r?`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ })
if ($members.Count -eq 0) { throw 'BankRev member table was empty.' }
$expectedMembers = @(Get-ChildItem -LiteralPath $variantRoot -File -Recurse | Sort-Object FullName | ForEach-Object {
    $relativePath = $_.FullName.Substring($variantRoot.Length).TrimStart([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar).Replace('/', '\')
    "$($manifest.prefix)\$relativePath"
})
$normalizedMembers = @($members | ForEach-Object { $_.Replace('/', '\') })
Assert-CaseInsensitiveUnique $expectedMembers 'Expected source-member list'
Assert-CaseInsensitiveUnique $normalizedMembers 'BankRev member listing'
if ($normalizedMembers.Count -ne $expectedMembers.Count) { throw "BankRev member count $($normalizedMembers.Count) does not equal expected source-member count $($expectedMembers.Count)." }
foreach ($required in $expectedMembers) {
    if (-not ($normalizedMembers | Where-Object { $_ -ieq $required })) { throw "BankRev member listing lacks $required." }
}
foreach ($actual in $normalizedMembers) {
    if (-not ($expectedMembers | Where-Object { $_ -ieq $actual })) { throw "BankRev member listing has unexpected member $actual." }
}

$sourceFiles = @(Get-ChildItem -LiteralPath $variantRoot -File -Recurse | Sort-Object FullName | ForEach-Object { [PSCustomObject]@{ path = $_.FullName; sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash } })
$receipt = [PSCustomObject]@{
    schema_version = 1
    fixture = $manifest.fixture
    variant = $Variant
    run_root = $runRoot
    archive_result = 'passed'
    compilation_result = 'not attempted; Addon Builder -packonly is archive packaging, not Enforce Script compilation'
    runtime_result = 'not run by fixture policy'
    command = @($addonBuilder) + $addonArgs
    tool = @{
        addon_builder = @{ path = $addonBuilder; file_version = (Get-Item -LiteralPath $addonBuilder).VersionInfo.FileVersion; sha256 = (Get-FileHash -LiteralPath $addonBuilder -Algorithm SHA256).Hash }
        bankrev = @{ path = $bankRev; file_version = (Get-Item -LiteralPath $bankRev).VersionInfo.FileVersion; sha256 = (Get-FileHash -LiteralPath $bankRev -Algorithm SHA256).Hash }
    }
    manifest_sha256 = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash
    source_sha256 = $sourceFiles
    pbo = [PSCustomObject]@{ expected_name = $expectedPboName; path = $pbo.FullName; sha256 = (Get-FileHash -LiteralPath $pbo.FullName -Algorithm SHA256).Hash; bytes = $pbo.Length }
    bankrev = [PSCustomObject]@{ prefix = $manifest.prefix; properties_log = $propertiesLog; members_log = $membersLog; members = $normalizedMembers; expected_members = $expectedMembers }
    log_sha256 = @{ addon_builder = (Get-FileHash -LiteralPath $addonLog -Algorithm SHA256).Hash; bankrev_properties = (Get-FileHash -LiteralPath $propertiesLog -Algorithm SHA256).Hash; bankrev_members = (Get-FileHash -LiteralPath $membersLog -Algorithm SHA256).Hash }
    excluded = @('signing', 'keys', 'production mod configuration', 'storage data', 'DayZ/client/server process launch')
}
$receiptPath = Join-Path $runRoot 'receipt.json'
$receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $receiptPath -Encoding utf8
Write-Output "SUCCESS: package-only archive and inspection receipt: $receiptPath"
