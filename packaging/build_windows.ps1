# Build the Windows desktop app: portable zip + (if Inno Setup is installed) an installer.
# Run from anywhere:  powershell -ExecutionPolicy Bypass -File packaging\build_windows.ps1

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$VenvPython = Join-Path $Root "thorlabs_env\Scripts\python.exe"
if (Test-Path $VenvPython) {
    $Python = $VenvPython
} else {
    $PythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $PythonCmd) {
        throw "Python is not on PATH. Use the development environment that has the project dependencies installed."
    }
    $Python = $PythonCmd.Source
}

Write-Host "Using Python: $Python"
& $Python -c "from version import __version__, APP_NAME; print(APP_NAME, __version__)"
$Version = (& $Python -c "from version import __version__; print(__version__)").Trim()

Write-Host "Installing/updating PyInstaller..."
& $Python -m pip install -r requirements-build.txt

Write-Host "Running PyInstaller..."
& $Python -m PyInstaller --noconfirm --clean --distpath dist --workpath build packaging\ThorlabsDataOverview.spec
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed."
}

$AppDir = Join-Path $Root "dist\ThorlabsDataOverview"
if (-not (Test-Path (Join-Path $AppDir "ThorlabsDataOverview.exe"))) {
    throw "Expected ThorlabsDataOverview.exe under $AppDir"
}

$Readme = Join-Path $AppDir "README.txt"
@"
Thorlabs Data Overview $Version (portable)

Double-click ThorlabsDataOverview.exe
No Python install is required.

1. Choose the parent folder that contains Thorlabs recordings
2. Click Run
3. Open the generated overview.pdf when finished

Existing stacks/averages are skipped. The PDF is rewritten each run.
"@ | Set-Content -Path $Readme -Encoding UTF8

$ReleaseDir = Join-Path $Root "dist\release"
New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

$ZipPath = Join-Path $ReleaseDir "ThorlabsDataOverview-$Version-windows-portable.zip"
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

Write-Host "Creating portable zip..."
Compress-Archive -Path $AppDir -DestinationPath $ZipPath -Force

$IsccCandidates = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe"
)
$Iscc = $IsccCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($Iscc) {
    Write-Host "Building installer with $Iscc"
    & $Iscc "/DMyAppVersion=$Version" (Join-Path $Root "packaging\installer.iss")
    if ($LASTEXITCODE -ne 0) {
        throw "Inno Setup failed."
    }
} else {
    Write-Host "Inno Setup 6 not found. Portable zip was created; skip the installer or install Inno Setup and re-run."
}

Write-Host ""
Write-Host "Release files in dist\release :"
Get-ChildItem $ReleaseDir | ForEach-Object { Write-Host " - $($_.Name)" }
