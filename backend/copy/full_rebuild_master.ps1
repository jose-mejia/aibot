# Script de Build Completo - Master Sender (Python + Tauri)
Write-Host "FULL REBUILD - MASTER SENDER" -ForegroundColor Cyan
Write-Host "============================"

# 1. Matar processos
Write-Host "1. Killing processes..." -ForegroundColor Yellow
Get-Process | Where-Object {
    $_.ProcessName -like "*master*" -or 
    $_.ProcessName -like "*sender*" -or 
    $_.ProcessName -like "*python*" -or 
    $_.ProcessName -like "*node*" -or
    $_.ProcessName -like "*vite*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

# 2. Rebuild Python Sidecar
Write-Host "2. Rebuilding Python Sidecar..." -ForegroundColor Yellow
Set-Location master_sender
pyinstaller sender-service.spec --clean --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: PyInstaller Failed" -ForegroundColor Red
    exit 1
}

# 3. Copiar Sidecar para Tauri
Write-Host "3. Copying Sidecar..." -ForegroundColor Yellow
$sidecarSource = "dist\sender-service.exe"
$sidecarDest = "gui\src-tauri\sender-service-x86_64-pc-windows-msvc.exe"
$sidecarDestSimple = "gui\src-tauri\sender-service.exe"

Copy-Item -Force $sidecarSource $sidecarDest
Copy-Item -Force $sidecarSource $sidecarDestSimple

Write-Host "   Sidecar copied to $sidecarDest" -ForegroundColor Green

# 4. Limpar cache do Tauri
Write-Host "4. Cleaning Tauri cache..." -ForegroundColor Yellow
$targetPath = "gui\src-tauri\target"
if (Test-Path $targetPath) {
    Remove-Item -Recurse -Force $targetPath -ErrorAction SilentlyContinue
    Write-Host "   SUCCESS: Cache removed" -ForegroundColor Green
}

# 5. Build Tauri
Write-Host "5. Starting Tauri Build..." -ForegroundColor Yellow
Set-Location gui
npm run tauri build

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: MASTER BUILD COMPLETE" -ForegroundColor Green
} else {
    Write-Host "ERROR: MASTER BUILD FAILED" -ForegroundColor Red
}

Set-Location ..\..
