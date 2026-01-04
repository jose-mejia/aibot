@echo off
echo ===========================================
echo   AIBOT TRADE COPIER - QUICK TEST
echo ===========================================
echo.

set "ROOT_DIR=%CD%"
set "DIST_DIR=%ROOT_DIR%\dist_test"

:: Check if executables exist
if not exist "%DIST_DIR%\master_sender.exe" (
    echo ✗ Executables not found!
    echo Please run build_test_exe.bat first
    pause
    exit /b 1
)

echo This script will start:
echo   1. API Server (Rust)
echo   2. Master Sender
echo   3. Client Copier
echo.
echo Make sure you have configured:
echo   - dist_test/config_sender.json
echo   - dist_test/config_client.json
echo.
echo IMPORTANT: Make sure MT5 is running and logged in!
echo.
pause

:: Start API Server in new window
echo.
echo [1/3] Starting API Server...
start "API Server" cmd /k "cd api_server && cargo run --release"
echo Waiting for API server to start...
timeout /t 8 /nobreak

:: Start Master Sender in new window
echo.
echo [2/3] Starting Master Sender...
start "Master Sender" cmd /k "cd dist_test && master_sender.exe"
echo Waiting for Master Sender to initialize...
timeout /t 4 /nobreak

:: Start Client Copier in new window
echo.
echo [3/3] Starting Client Copier...
start "Client Copier" cmd /k "cd dist_test && client_copier.exe"

echo.
echo ===========================================
echo          ALL SERVICES STARTED!
echo ===========================================
echo.
echo Three windows should now be open:
echo   1. API Server (Rust) - http://localhost:8000
echo   2. Master Sender - Monitoring MT5 Master
echo   3. Client Copier - Copying to MT5 Client
echo.
echo To test:
echo   - Open a trade in your Master MT5 account
echo   - Watch the logs in all three windows
echo   - Check if the trade appears in Client MT5
echo.
echo To stop: Close each window individually
echo.
pause
