@echo off
echo ===========================================
echo   AIBOT TRADE COPIER - CLEAN BUILD
echo ===========================================
echo.
echo This will delete all build artifacts:
echo   - PyInstaller dist and build folders
echo   - Rust target folder
echo   - dist_test folder
echo   - Log files
echo.
pause

set "ROOT_DIR=%CD%"
set "MASTER_DIR=%ROOT_DIR%\master_sender"
set "CLIENT_DIR=%ROOT_DIR%\client_copier"
set "API_DIR=%ROOT_DIR%\api_server"
set "DIST_DIR=%ROOT_DIR%\dist_test"

echo.
echo [1/5] Cleaning Master Sender build files...
if exist "%MASTER_DIR%\dist" (
    rmdir /s /q "%MASTER_DIR%\dist"
    echo ✓ Removed master_sender\dist
)
if exist "%MASTER_DIR%\build" (
    rmdir /s /q "%MASTER_DIR%\build"
    echo ✓ Removed master_sender\build
)
if exist "%MASTER_DIR%\*.spec" (
    del /q "%MASTER_DIR%\*.spec"
    echo ✓ Removed master_sender\*.spec
)

echo.
echo [2/5] Cleaning Client Copier build files...
if exist "%CLIENT_DIR%\dist" (
    rmdir /s /q "%CLIENT_DIR%\dist"
    echo ✓ Removed client_copier\dist
)
if exist "%CLIENT_DIR%\build" (
    rmdir /s /q "%CLIENT_DIR%\build"
    echo ✓ Removed client_copier\build
)
if exist "%CLIENT_DIR%\*.spec" (
    del /q "%CLIENT_DIR%\*.spec"
    echo ✓ Removed client_copier\*.spec
)

echo.
echo [3/5] Cleaning Rust API Server build files...
if exist "%API_DIR%\target" (
    echo This may take a while...
    rmdir /s /q "%API_DIR%\target"
    echo ✓ Removed api_server\target
)

echo.
echo [4/5] Cleaning distribution folder...
if exist "%DIST_DIR%" (
    rmdir /s /q "%DIST_DIR%"
    echo ✓ Removed dist_test
)

echo.
echo [5/5] Cleaning log files...
if exist "%ROOT_DIR%\*.log" (
    del /q "%ROOT_DIR%\*.log"
    echo ✓ Removed root log files
)
if exist "%MASTER_DIR%\*.log" (
    del /q "%MASTER_DIR%\*.log"
    echo ✓ Removed master_sender log files
)
if exist "%CLIENT_DIR%\*.log" (
    del /q "%CLIENT_DIR%\*.log"
    echo ✓ Removed client_copier log files
)

echo.
echo ===========================================
echo          CLEAN COMPLETE!
echo ===========================================
echo.
echo All build artifacts have been removed.
echo You can now run build_test_exe.bat for a fresh build.
echo.
pause
