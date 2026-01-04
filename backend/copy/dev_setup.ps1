# Script de Manutencao e Inicializacao do AIBOT
# Caminho Raiz: c:\Users\josemejia\dev\python\aibot\backend\copy

Write-Host "--- AIBOT ENVIRONMENT RESET AND START ---" -ForegroundColor Cyan

# 1. LIMPEZA DE PROCESSOS
Write-Host "Cleaning processes..." -ForegroundColor Yellow
$processes = @("sender-service", "client-service", "master-sender", "client-copier", "node", "cargo", "rustc", "python")
foreach ($proc in $processes) {
    Get-Process -Name $proc -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2

# 2. LIMPEZA DE BANCO DE DADOS
Write-Host "Resetting database files..." -ForegroundColor Red
if (Test-Path "aibot.db") { Remove-Item "aibot.db" -Force }
if (Test-Path "copier.db") { Remove-Item "copier.db" -Force }
if (Test-Path "api_server/aibot.db") { Remove-Item "api_server/aibot.db" -Force }
if (Test-Path "api_server/copier.db") { Remove-Item "api_server/copier.db" -Force }

Write-Host "Environment Clean. DB will be created in api_server/aibot.db" -ForegroundColor Green

# 3. LANCAMENTO DOS COMPONENTES
Write-Host "Starting windows..." -ForegroundColor Green

$cmdApi = "cd api_server; `$env:DATABASE_URL='sqlite:aibot.db'; Write-Host '--- API SERVER ---' -ForegroundColor Magenta; cargo run"
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass", "-NoExit", "-Command", "$cmdApi"

$cmdDash = "cd api_server/admin_panel; Write-Host '--- DASHBOARD WEB ---' -ForegroundColor Cyan; npm run dev"
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass", "-NoExit", "-Command", "$cmdDash"

$cmdMaster = "cd master_sender/gui; Write-Host '--- MASTER APP ---' -ForegroundColor Yellow; npm run tauri dev"
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass", "-NoExit", "-Command", "$cmdMaster"

$cmdClient = "cd client_copier/gui; Write-Host '--- CLIENT APP ---' -ForegroundColor Blue; npm run tauri dev"
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass", "-NoExit", "-Command", "$cmdClient"

Write-Host "Success! DB is in api_server/aibot.db" -ForegroundColor White
Write-Host "Login: admin / admin123" -ForegroundColor Gray
