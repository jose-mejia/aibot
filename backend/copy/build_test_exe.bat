@echo off
setlocal enabledelayedexpansion

echo ===========================================
echo   AIBOT TRADE COPIER - COMPLETE BUILD
echo ===========================================
echo.

set "ROOT_DIR=%CD%"
set "MASTER_DIR=%ROOT_DIR%\master_sender"
set "CLIENT_DIR=%ROOT_DIR%\client_copier"
set "DIST_DIR=%ROOT_DIR%\dist_test"
set "API_DIR=%ROOT_DIR%\api_server"

:: Create dist directory
if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"

echo ============================================
echo STEP 1: Installing Python Dependencies
echo ============================================
pip install pyinstaller requests websockets MetaTrader5 sqlalchemy
if errorlevel 1 (
    echo ✗ Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✓ Python dependencies installed
echo.

echo ============================================
echo STEP 2: Building Rust API Server
echo ============================================
cd "%API_DIR%"
cargo build --release
if errorlevel 1 (
    echo ✗ Failed to build Rust API server
    pause
    exit /b 1
)
echo ✓ Rust API server built successfully
echo.

echo ============================================
echo STEP 3: Building Master Sender EXE
echo ============================================
cd "%MASTER_DIR%"

pyinstaller --noconfirm --onefile --console ^
 --name "master_sender" ^
 --add-data "config_sender.json;." ^
 --hidden-import "MetaTrader5" ^
 --hidden-import "requests" ^
 --hidden-import "json" ^
 --hidden-import "logging" ^
 --hidden-import "time" ^
 --hidden-import "numpy" ^
 --hidden-import "numpy._core" ^
 --hidden-import "numpy._core.multiarray" ^
 --collect-all "numpy" ^
 main_sender.py

if exist "dist\master_sender.exe" (
    copy "dist\master_sender.exe" "%DIST_DIR%\master_sender.exe" >nul
    echo ✓ Master Sender EXE created
) else (
    echo ✗ Failed to create Master Sender EXE
    pause
    exit /b 1
)
echo.

echo ============================================
echo STEP 4: Building Client Copier EXE
echo ============================================
cd "%CLIENT_DIR%"

pyinstaller --noconfirm --onefile --console ^
 --name "client_copier" ^
 --add-data "config_client.json;." ^
 --hidden-import "MetaTrader5" ^
 --hidden-import "websockets" ^
 --hidden-import "asyncio" ^
 --hidden-import "json" ^
 --hidden-import "logging" ^
 --hidden-import "numpy" ^
 --hidden-import "numpy._core" ^
 --hidden-import "numpy._core.multiarray" ^
 --collect-all "numpy" ^
 main_client.py

if exist "dist\client_copier.exe" (
    copy "dist\client_copier.exe" "%DIST_DIR%\client_copier.exe" >nul
    echo ✓ Client Copier EXE created
) else (
    echo ✗ Failed to create Client Copier EXE
    pause
    exit /b 1
)
echo.

echo ============================================
echo STEP 5: Creating Configuration Files
echo ============================================

:: Create config_sender.json
(
echo {
echo     "api": {
echo         "url": "http://127.0.0.1:8000",
echo         "username": "master_user",
echo         "password": "secret_password"
echo     },
echo     "mt5": {
echo         "login": 12345678,
echo         "password": "YOUR_MT5_PASSWORD_HERE",
echo         "server": "YOUR_BROKER_SERVER_HERE"
echo     }
echo }
) > "%DIST_DIR%\config_sender.json"

:: Create config_client.json
(
echo {
echo     "api": {
echo         "url": "http://127.0.0.1:8000",
echo         "ws_url": "ws://127.0.0.1:8000",
echo         "username": "client_user",
echo         "password": "client_password"
echo     },
echo     "mt5": {
echo         "login": 87654321,
echo         "password": "YOUR_MT5_PASSWORD_HERE",
echo         "server": "YOUR_BROKER_SERVER_HERE"
echo     },
echo     "trade_copy": {
echo         "mode": "fix",
echo         "fixed_lot": 0.01,
echo         "multiplier": 1.0,
echo         "magic_number_copier": 123456,
echo         "max_slippage_points": 50,
echo         "max_spread_points": 20,
echo         "max_exposure_trades": 5,
echo         "max_exposure_lots": 10.0
echo     },
echo     "paths": {
echo         "db_file": "client_db.json"
echo     },
echo     "safety": {
echo         "max_drawdown_percent": 10
echo     }
echo }
) > "%DIST_DIR%\config_client.json"

:: Create README
(
echo # AIBOT Trade Copier - Test Distribution
echo.
echo ## Files Included
echo - master_sender.exe - Monitors Master MT5 account and sends orders to API
echo - client_copier.exe - Receives orders from API and copies to Client MT5
echo - config_sender.json - Configuration for Master Sender
echo - config_client.json - Configuration for Client Copier
echo.
echo ## Setup Instructions
echo.
echo ### 1. Configure Master Sender
echo Edit config_sender.json and update:
echo - mt5.login: Your Master MT5 account number
echo - mt5.password: Your Master MT5 password
echo - mt5.server: Your broker server name
echo.
echo ### 2. Configure Client Copier
echo Edit config_client.json and update:
echo - mt5.login: Your Client MT5 account number
echo - mt5.password: Your Client MT5 password
echo - mt5.server: Your broker server name
echo.
echo ### 3. Start the API Server
echo The Rust API server must be running first.
echo From the main directory, run: cd api_server ^&^& cargo run --release
echo.
echo ### 4. Run Master Sender
echo Double-click master_sender.exe or run from command line
echo.
echo ### 5. Run Client Copier
echo Double-click client_copier.exe or run from command line
echo.
echo ## Testing
echo 1. Open a trade in your Master MT5 account
echo 2. Watch the console output of master_sender.exe
echo 3. Watch the console output of client_copier.exe
echo 4. Verify the trade appears in your Client MT5 account
echo.
echo ## Logs
echo - sender.log - Master Sender logs
echo - client.log - Client Copier logs
echo.
echo ## Troubleshooting
echo - Make sure MT5 is running and logged in
echo - Make sure API server is running on port 8000
echo - Check the log files for errors
echo - Verify your MT5 credentials are correct
) > "%DIST_DIR%\README.txt"

echo ✓ Configuration files created
echo.

echo ============================================
echo STEP 6: Copying API Server Executable
echo ============================================
copy "%API_DIR%\target\release\api_server.exe" "%DIST_DIR%\api_server.exe" >nul 2>&1
if exist "%DIST_DIR%\api_server.exe" (
    echo ✓ API Server executable copied
) else (
    echo ⚠ API Server executable not found - you'll need to run it from api_server directory
)
echo.

echo ===========================================
echo          BUILD COMPLETE!
echo ===========================================
echo.
echo Distribution folder: %DIST_DIR%
echo.
echo Files created:
dir /b "%DIST_DIR%"
echo.
echo ===========================================
echo Next Steps:
echo ===========================================
echo 1. Go to dist_test folder
echo 2. Edit config_sender.json with your Master MT5 credentials
echo 3. Edit config_client.json with your Client MT5 credentials
echo 4. Read README.txt for testing instructions
echo.
echo Quick Test:
echo   Run: quick_test.bat
echo.
pause
