# Script de Registro de Tarea 24/7 en Windows para Baddgroup Vision AI
param (
    [switch]$Uninstall
)

$TaskName = "BaddgroupVisionAI_24x7"
$ScriptDir = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$WatchdogScript = Join-Path $ScriptDir "service_watchdog.py"

if (-not (Test-Path $PythonExe)) {
    $PythonExe = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
}

if ($Uninstall) {
    Write-Host "Desinstalando servicio 24/7 '$TaskName'..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "[OK] Servicio desinstalado." -ForegroundColor Green
    exit 0
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   BADDGROUP VISION AI - INSTALADOR DE SERVICIO 24/7" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Definir la Acción
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$WatchdogScript`"" -WorkingDirectory $ScriptDir

# 2. Definir el Disparador (Al encender el sistema)
$Trigger = New-ScheduledTaskTrigger -AtStartup

# 3. Definir Configuración de Resiliencia (Reinicio automático ante fallos)
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -Priority 4

# 4. Registrar la tarea con permisos elevados
try {
    # Intentar registrar a nivel de arranque del sistema
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -RunLevel Highest `
        -Force | Out-Null

    Write-Host "[OK] Tarea de inicio automático '$TaskName' registrada exitosamente." -ForegroundColor Green
    Write-Host "     El sistema se iniciará de forma 100% autónoma en cada arranque de la máquina." -ForegroundColor Gray
    
    # Iniciar la tarea de inmediato
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "[OK] Tarea iniciada en segundo plano ahora mismo." -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Se requieren permisos de Administrador para registrar la tarea en el inicio del sistema." -ForegroundColor Red
    Write-Host "Por favor ejecute PowerShell o este instalador como Administrador (clic derecho -> Ejecutar como administrador)." -ForegroundColor Yellow
}
