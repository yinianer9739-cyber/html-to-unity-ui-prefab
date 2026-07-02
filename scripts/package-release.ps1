param(
    [string]$OutputDir = "release"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Resolve-Path (Join-Path $scriptDir "..")).Path
$versionFile = Join-Path $root "VERSION"

if (-not (Test-Path -LiteralPath $versionFile)) {
    throw "VERSION file is missing."
}

$version = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$') {
    throw "VERSION must be a semantic version, got '$version'."
}

$releaseDir = Join-Path $root $OutputDir
New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null

$stageRoot = Join-Path $env:TEMP ("html-to-unity-ui-prefab-release-" + [guid]::NewGuid().ToString("N"))
$stageSkill = Join-Path $stageRoot "html-to-unity-ui-prefab"
New-Item -ItemType Directory -Force -Path $stageSkill | Out-Null

$excludedDirs = @(".git", ".github", "release", "__pycache__", ".pytest_cache")
$excludedFiles = @()

Get-ChildItem -LiteralPath $root -Force | ForEach-Object {
    if (($excludedDirs -notcontains $_.Name) -and ($excludedFiles -notcontains $_.Name)) {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $stageSkill $_.Name) -Recurse -Force
    }
}

$stagedFiles = @(Get-ChildItem -LiteralPath $stageSkill -Recurse -Force | Where-Object { $_.PSIsContainer -eq $false })
if ($stagedFiles.Count -eq 0) {
    throw "Release staging directory is empty: $stageSkill"
}

Get-ChildItem -LiteralPath $stageSkill -Recurse -Force | Where-Object {
    ($_.PSIsContainer -and $_.Name -eq "__pycache__") -or
    ((-not $_.PSIsContainer) -and ($_.Extension -in @(".pyc", ".pyo")))
} | ForEach-Object {
    Remove-Item -LiteralPath $_.FullName -Recurse -Force
}

$zipPath = Join-Path $releaseDir ("html-to-unity-ui-prefab-v$version.zip")
if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}

[System.Reflection.Assembly]::LoadWithPartialName("System.IO.Compression") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("System.IO.Compression.FileSystem") | Out-Null
$zipStream = [System.IO.File]::Open($zipPath, [System.IO.FileMode]::CreateNew)
$archive = New-Object System.IO.Compression.ZipArchive($zipStream, [System.IO.Compression.ZipArchiveMode]::Create)
$entryCount = 0
try {
    Push-Location -LiteralPath $stageSkill
    try {
        Get-ChildItem -LiteralPath "." -Recurse -Force | Where-Object { $_.PSIsContainer -eq $false } | ForEach-Object {
            $relative = Resolve-Path -LiteralPath $_.FullName -Relative
            if ($relative.StartsWith(".\")) {
                $relative = $relative.Substring(2)
            }
            elseif ($relative.StartsWith("./")) {
                $relative = $relative.Substring(2)
            }
            elseif ($relative -eq ".") {
                $relative = ""
            }
            $entryName = "html-to-unity-ui-prefab/" + ($relative -replace "\\", "/")
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $_.FullName, $entryName) | Out-Null
            $entryCount += 1
        }
    }
    finally {
        Pop-Location
    }
    if ($entryCount -eq 0) {
        throw "No files were written to the release zip."
    }
}
finally {
    $archive.Dispose()
    $zipStream.Dispose()
}

Remove-Item -LiteralPath $stageRoot -Recurse -Force

if (-not (Test-Path -LiteralPath $zipPath)) {
    throw "Release zip was not created: $zipPath"
}

$archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    if ($archive.Entries.Count -eq 0) {
        throw "Release zip is empty: $zipPath"
    }
}
finally {
    $archive.Dispose()
}

Write-Output $zipPath
