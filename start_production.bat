@echo off
title Baddgroup Vision AI - Servidor de Produccion
echo ===================================================================
echo             BADDGROUP VISION AI - PLATAFORMA DE PRODUCCION
echo ===================================================================
echo Iniciando servidor de monitoreo y busqueda con IA...
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    echo [OK] Entorno virtual detectado. Iniciando aplicacion...
    start http://localhost:8000
    .venv\Scripts\python.exe run_server.py
) else (
    echo [INFO] Buscando Python en el sistema...
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        start http://localhost:8000
        python run_server.py
    ) else (
        echo [ERROR] No se detecto instalacion de Python.
        echo Por favor instale Python 3.12 o utilice Docker:
        echo    docker compose up -d
        pause
    )
)
pause
