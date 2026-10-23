@echo off
title Baddgroup Vision AI - Acceso Remoto Seguro & Demos
echo ===================================================================
echo     BADDGROUP VISION AI - ACCESO REMOTO SEGURO PARA CLIENTES
echo ===================================================================
echo Generando enlace publico HTTPS con Cloudflare Tunnel...
echo Podras abrir este enlace desde tu telefono o enviarlo a clientes
echo en el extranjero para hacer demostraciones en vivo de la IA.
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe scripts\remote_tunnel.py
) else (
    python scripts\remote_tunnel.py
)

pause
