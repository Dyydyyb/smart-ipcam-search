@echo off
title Baddgroup Vision AI - Instalador de Servicio 24/7
echo ===================================================================
echo     BADDGROUP VISION AI - INSTALADOR DE SERVICIO 24/7 EN WINDOWS
echo ===================================================================
echo Registrando el sistema de monitoreo e IA para inicio automatico
echo con el arranque de la maquina y reinicio automatico ante caidas...
echo.

cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\setup_autostart_task.ps1"

echo.
echo Presione cualquier tecla para finalizar...
pause >nul
