@echo off
echo Killing all related processes...

REM Kill Python sidecars
taskkill /F /IM sender-service-x86_64-pc-windows-msvc.exe 2>nul
taskkill /F /IM client-service-x86_64-pc-windows-msvc.exe 2>nul

REM Kill Tauri apps
taskkill /F /IM master-sender.exe 2>nul
taskkill /F /IM client-copier.exe 2>nul

REM Kill any Node/NPM processes
taskkill /F /IM node.exe 2>nul

REM Kill Cargo/Rust processes
taskkill /F /IM cargo.exe 2>nul
taskkill /F /IM rustc.exe 2>nul

REM Wait a bit for Windows to release file handles
timeout /t 2 /nobreak >nul

echo Done! All processes killed.
pause
