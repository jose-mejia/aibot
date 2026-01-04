@echo off
echo Building Sidecars...

REM Build Master Sender
echo Building Master Sender...
cd master_sender
pyinstaller ^
    --name=sender-service ^
    --onefile ^
    --windowed ^
    --hidden-import=sender_service ^
    --hidden-import=mt5_connector ^
    --hidden-import=numpy ^
    --hidden-import=MetaTrader5 ^
    --hidden-import=requests ^
    --collect-all=numpy ^
    --collect-all=MetaTrader5 ^
    --add-data="config_sender.json;." ^
    main_sender.py

move /Y "dist\sender-service.exe" "gui\src-tauri\sender-service-x86_64-pc-windows-msvc.exe"
cd ..

REM Build Client Copier
echo Building Client Copier...
cd client_copier
pyinstaller ^
    --name=client-service ^
    --onefile ^
    --windowed ^
    --hidden-import=client_service ^
    --hidden-import=mt5_connector ^
    --hidden-import=db_utils ^
    --hidden-import=safety ^
    --hidden-import=utils ^
    --hidden-import=numpy ^
    --hidden-import=MetaTrader5 ^
    --hidden-import=websockets ^
    --hidden-import=requests ^
    --collect-all=numpy ^
    --collect-all=MetaTrader5 ^
    --add-data="config_client.json;." ^
    main_client.py

move /Y "dist\client-service.exe" "gui\src-tauri\client-service-x86_64-pc-windows-msvc.exe"
cd ..

echo DONE. Sidecars built and moved to Tauri binaries folder.
pause
