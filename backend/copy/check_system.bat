@echo off
echo ===========================================
echo   AIBOT TRADE COPIER - SYSTEM CHECK
echo ===========================================
echo.
echo Checking system prerequisites...
echo.

set "ERRORS=0"

:: Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python NOT found
    echo    Please install Python 3.8 or higher from python.org
    set /a ERRORS+=1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    echo ✓ Python found: !PYTHON_VER!
)
echo.

:: Check Rust
echo [2/6] Checking Rust...
rustc --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Rust NOT found
    echo    Please install Rust from rustup.rs
    set /a ERRORS+=1
) else (
    for /f "tokens=2" %%i in ('rustc --version 2^>^&1') do set RUST_VER=%%i
    echo ✓ Rust found: !RUST_VER!
)
echo.

:: Check Cargo
echo [3/6] Checking Cargo...
cargo --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Cargo NOT found
    echo    Cargo should come with Rust installation
    set /a ERRORS+=1
) else (
    for /f "tokens=2" %%i in ('cargo --version 2^>^&1') do set CARGO_VER=%%i
    echo ✓ Cargo found: !CARGO_VER!
)
echo.

:: Check pip
echo [4/6] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ✗ pip NOT found
    echo    pip should come with Python installation
    set /a ERRORS+=1
) else (
    echo ✓ pip found
)
echo.

:: Check MT5
echo [5/6] Checking MetaTrader 5...
if exist "C:\Program Files\MetaTrader 5\terminal64.exe" (
    echo ✓ MT5 found in default location
) else if exist "C:\Program Files (x86)\MetaTrader 5\terminal64.exe" (
    echo ✓ MT5 found in Program Files (x86)
) else (
    echo ⚠ MT5 NOT found in default locations
    echo    Please ensure MetaTrader 5 is installed
    echo    You can still proceed if MT5 is installed elsewhere
)
echo.

:: Check Python packages
echo [6/6] Checking Python packages...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ⚠ pyinstaller not installed (will be installed during build)
) else (
    echo ✓ pyinstaller installed
)

pip show MetaTrader5 >nul 2>&1
if errorlevel 1 (
    echo ⚠ MetaTrader5 package not installed (will be installed during build)
) else (
    echo ✓ MetaTrader5 package installed
)
echo.

:: Check directory structure
echo Checking directory structure...
if exist "api_server" (
    echo ✓ api_server directory found
) else (
    echo ✗ api_server directory NOT found
    set /a ERRORS+=1
)

if exist "master_sender" (
    echo ✓ master_sender directory found
) else (
    echo ✗ master_sender directory NOT found
    set /a ERRORS+=1
)

if exist "client_copier" (
    echo ✓ client_copier directory found
) else (
    echo ✗ client_copier directory NOT found
    set /a ERRORS+=1
)
echo.

:: Summary
echo ===========================================
echo              SUMMARY
echo ===========================================
echo.

if %ERRORS% EQU 0 (
    echo ✅ All critical checks passed!
    echo.
    echo You are ready to build the Trade Copier.
    echo.
    echo Next steps:
    echo   1. Run: build_test_exe.bat
    echo   2. Configure: dist_test/config_sender.json
    echo   3. Configure: dist_test/config_client.json
    echo   4. Test: quick_test.bat
    echo.
    echo See QUICKSTART.md for detailed instructions.
) else (
    echo ❌ %ERRORS% critical error(s) found!
    echo.
    echo Please fix the errors above before proceeding.
    echo.
    echo Installation guides:
    echo   Python: https://www.python.org/downloads/
    echo   Rust: https://rustup.rs/
    echo   MT5: https://www.metatrader5.com/
)

echo.
echo ===========================================
pause
