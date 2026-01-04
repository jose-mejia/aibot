@echo off
echo.
echo ==========================================
echo   INICIAR PYTHON MASTER SENDER (TESTE)
echo ==========================================
echo.
echo 1. Faca login no App Desktop Master ou Web Admin.
echo 2. Copie o 'access_token' (voce pode ver no console do navegador ou Network tab).
echo.
set /p TOKEN=">> Cole o Token JWT aqui: "
echo.
echo Iniciando servico Python com o token fornecido...
cd master_sender
python main_sender.py --token %TOKEN%
pause
