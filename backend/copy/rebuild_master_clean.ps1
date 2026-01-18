# Script de Build Limpo - Master Sender
# Executa limpeza completa e rebuild

Write-Host "CLEAN REBUILD - MASTER SENDER" -ForegroundColor Cyan
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

# 2. Limpar cache do Tauri
Write-Host "2. Cleaning Tauri cache..." -ForegroundColor Yellow
$targetPath = "master_sender\gui\src-tauri\target"
if (Test-Path $targetPath) {
    Remove-Item -Recurse -Force $targetPath -ErrorAction SilentlyContinue
    Write-Host "   SUCCESS: Cache removed" -ForegroundColor Green
} else {
    Write-Host "   INFO: Cache already clean" -ForegroundColor Gray
}

# 3. Build completo
Write-Host "3. Starting full build..." -ForegroundColor Yellow
Write-Host "   WAIT: This will take 3-5 minutes..." -ForegroundColor Gray

Set-Location master_sender\gui

# Build
npm run tauri build

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: BUILD COMPLETE" -ForegroundColor Green
    Write-Host "Executable generated at:" -ForegroundColor Cyan
    Write-Host "   src-tauri\target\release\master-sender.exe" -ForegroundColor White
} else {
    Write-Host "ERROR: BUILD FAILED" -ForegroundColor Red
}

Set-Location ..\..
