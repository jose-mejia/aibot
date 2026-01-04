# Script para testar integração completa (Frontends + Backend)

Write-Host "=== AIBOT INTEGRATION TEST ===" -ForegroundColor Cyan
Write-Host "Starting services..."

# 1. Start Backend (Rust or Mock)
Write-Host "1. Attempting to start API Server..."
if (Test-Path "api_server\target\release\api_server.exe") {
    Write-Host "Rust Binary found. Starting Rust API Server..." -ForegroundColor Green
    Start-Process -FilePath "api_server\target\release\api_server.exe" -NoNewWindow
} else {
    Write-Host "Rust Binary NOT found (compilation issue). Starting Python MOCK Server..." -ForegroundColor Yellow
    # Ensure uvicorn/fastapi are installed
    pip install fastapi uvicorn
    Start-Process -FilePath "python" -ArgumentList "api_server\mock_server.py" -NoNewWindow
}

Start-Sleep -Seconds 5

# 2. Start Admin Panel
Write-Host "2. Starting Admin Panel (Web)..." -ForegroundColor Magenta
Set-Location "api_server\admin_panel"
Start-Process "cmd" -ArgumentList "/c npm run dev"
Set-Location "..\.."

# 3. Start Master Sender GUI
Write-Host "3. Starting Master Sender GUI (Desktop)..." -ForegroundColor Magenta
Set-Location "master_sender\gui"
Start-Process "cmd" -ArgumentList "/c npm run dev"
# Nota: Para rodar como desktop real use 'npm run tauri dev', mas requer setup Rust/Tauri environment intacto.
# 'npm run dev' vai abrir no browser para validação visual rápida.
Set-Location "..\.."

# 4. Start Client Copier GUI
Write-Host "4. Starting Client Copier GUI (Desktop)..." -ForegroundColor Magenta
Set-Location "client_copier\gui"
Start-Process "cmd" -ArgumentList "/c npm run dev"
Set-Location "..\.."

Write-Host "All services started!" -ForegroundColor Green
Write-Host "Admin Panel: http://localhost:3000"
Write-Host "Master Sender: http://localhost:1420"
Write-Host "Client Copier: http://localhost:1421"
