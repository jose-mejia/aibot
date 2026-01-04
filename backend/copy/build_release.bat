@echo off
echo ===========================================
echo      AIBOT TRADE COPIER - BUILD SYSTEM
echo ===========================================
echo.

:: 0. Setup
set "ROOT_DIR=%CD%"
set "MASTER_DIR=%ROOT_DIR%\master_sender"
set "CLIENT_DIR=%ROOT_DIR%\client_copier"
set "TARGET_TRIPLE=x86_64-pc-windows-msvc"

echo [1/5] Installing Dependencies...
pip install pyinstaller pyarmor fastapi uvicorn websockets requests MetaTrader5 sqlalchemy 
call npm install -g @tauri-apps/cli

:: 1. PROTECT & COMPILE: MASTER SENDER
echo.
echo [2/5] Building Master Sender (Protected)...
cd "%MASTER_DIR%"
:: Use PyInstaller encryption key for basic protection
pyinstaller --noconfirm --onefile --windowed ^
 --name "sender_service" ^
 --key "MySecretKey123" ^
 --add-data "config_sender.json;." ^
 --hidden-import "MetaTrader5" ^
 --hidden-import "requests" ^
 main_sender.py

:: Prepare Tauri Binaries folder
if not exist "gui\src-tauri\binaries" mkdir "gui\src-tauri\binaries"
copy "dist\sender_service.exe" "gui\src-tauri\binaries\sender_service-%TARGET_TRIPLE%.exe"

:: 2. PROTECT & COMPILE: CLIENT COPIER
echo.
echo [3/5] Building Client Copier (Protected)...
cd "%CLIENT_DIR%"

pyinstaller --noconfirm --onefile --windowed ^
 --name "client_service" ^
 --key "MySecretKeyClient456" ^
 --add-data "config_client.json;." ^
 --add-data "client_db.json;." ^
 --hidden-import "MetaTrader5" ^
 --hidden-import "websockets" ^
 --hidden-import "asyncio" ^
 main_client.py

:: Prepare Tauri Binaries folder
if not exist "gui\src-tauri\binaries" mkdir "gui\src-tauri\binaries"
copy "dist\client_service.exe" "gui\src-tauri\binaries\client_service-%TARGET_TRIPLE%.exe"

:: 3. BUILD UI: MASTER
echo.
echo [4/5] Building Master UI Installer...
cd "%MASTER_DIR%\gui"
call npm install
call npm run tauri build

:: 4. BUILD UI: CLIENT
echo.
echo [5/5] Building Client UI Installer...
cd "%CLIENT_DIR%\gui"
call npm install
call npm run tauri build

echo.
echo ===========================================
echo          BUILD COMPLETE!
echo ===========================================
echo Installers are located in:
echo   - Master: %MASTER_DIR%\gui\src-tauri\target\release\bundle\msi
echo   - Client: %CLIENT_DIR%\gui\src-tauri\target\release\bundle\msi
echo ===========================================
pause
