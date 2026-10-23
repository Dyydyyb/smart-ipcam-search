#!/usr/bin/env bash
# ===================================================================
# BADDGROUP VISION AI - SCRIPT DE INICIO PARA LINUX / SERVIDORES
# ===================================================================

cd "$(dirname "$0")"

echo "==================================================================="
echo "         BADDGROUP VISION AI - PLATAFORMA DE PRODUCCION"
echo "==================================================================="

# Si docker compose está disponible y se pasa --docker
if [ "$1" == "--docker" ]; then
    echo "[INFO] Iniciando mediante Docker Compose..."
    docker compose up -d --build
    echo "[OK] Plataforma iniciada en segundo plano en http://localhost:8000"
    exit 0
fi

if [ -f ".venv/bin/python" ]; then
    echo "[OK] Entorno virtual detectado (.venv). Iniciando supervisor 24/7..."
    .venv/bin/python service_watchdog.py
elif command -v python3 &>/dev/null; then
    echo "[OK] Ejecutando con python3 del sistema..."
    python3 service_watchdog.py
else
    echo "[INFO] Python no encontrado en PATH, ejecutando con Docker..."
    docker compose up -d
fi
