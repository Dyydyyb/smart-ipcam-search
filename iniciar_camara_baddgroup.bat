@echo off
title Baddgroup Vision AI - Transmisor de Camara IP
echo ==============================================================================
echo BADDGROUP VISION AI - TRANSMISOR DE CAMARA A NUBE (CLOUD BRIDGE)
echo ==============================================================================
echo Conectando camara IMOU local al servidor seguro de Baddgroup...
cd /d "%~dp0"

:loop
.venv\Scripts\python.exe -u scripts\camera_stream_bridge.py
echo.
echo [ALERTA] Conexion reiniciandose en 3 segundos...
timeout /t 3 /nobreak >nul
goto loop
