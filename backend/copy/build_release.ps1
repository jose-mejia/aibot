# ZulFinance Build Script
# 1. Compiles Python Service (PyInstaller)
# 2. Moves Binary to Tauri Sidecar folder
# 3. Builds Tauri App

param(
    [switch]$ClientOnly,
    [switch]$MasterOnly,
    [switch]$SkipPython # Skip PyInstaller step (if already built)
)

$ErrorActionPreference = "Stop"

function Build-Python-Service {
    param($AppDir, $ScriptName, $BinaryName)
    Write-Host "🐍 Building Python Service: $BinaryName..." -ForegroundColor Yellow
    Push-Location $AppDir
    try {
        pyinstaller --clean --noconfirm --onefile --noconsole --name $BinaryName $ScriptName
        
        # Move to Tauri Binaries
        $destDir = "gui/src-tauri/binaries"
        if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Force -Path $destDir | Out-Null }
        
        Copy-Item "dist/$BinaryName.exe" "$destDir/$BinaryName.exe" -Force
        # Also copy for x86_64 Triple convention if needed by Tauri (Safety)
        Copy-Item "dist/$BinaryName.exe" "$destDir/${BinaryName}-x86_64-pc-windows-msvc.exe" -Force
        
        Write-Host "✅ Python Service Built: $destDir/$BinaryName.exe" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python Build Failed: $_" -ForegroundColor Red
        throw $_
    } finally {
        Pop-Location
    }
}

function Build-Tauri-App {
    param($AppDir, $AppName)
    Write-Host "🦀 Building Tauri App: $AppName..." -ForegroundColor Yellow
    Push-Location "$AppDir/gui"
    try {
        npm install
        npm run build
        npm run tauri build
        
        # Copy Release
        $srcExe = "src-tauri/target/release/${AppName}.exe"
        if (Test-Path $srcExe) {
            $releasesDir = "../../releases"
            if (-not (Test-Path $releasesDir)) { New-Item -ItemType Directory -Force -Path $releasesDir | Out-Null }
            Copy-Item $srcExe "$releasesDir/${AppName}_v1.0.0.exe" -Force
            Write-Host "🎉 Final Executable: releases/${AppName}_v1.0.0.exe" -ForegroundColor Cyan
        } else {
            Write-Host "❌ Executable not found at $srcExe" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Tauri Build Failed: $_" -ForegroundColor Red
    } finally {
        Pop-Location
    }
}

Write-Host "🚀 Starting ZulFinance Build..." -ForegroundColor Cyan

# --- CLIENT ---
if (-not $MasterOnly) {
    if (-not $SkipPython) {
        Build-Python-Service -AppDir "client_copier" -ScriptName "main_client.py" -BinaryName "client_service"
    }
    Build-Tauri-App -AppDir "client_copier" -AppName "ZulFinance_Client"
}

# --- MASTER ---
if (-not $ClientOnly) {
    if (-not $SkipPython) {
        Build-Python-Service -AppDir "master_sender" -ScriptName "main_sender.py" -BinaryName "sender_service"
    }
    Build-Tauri-App -AppDir "master_sender" -AppName "ZulFinance_Master"
}

Write-Host "`n✅ Build Process Finished." -ForegroundColor Green
