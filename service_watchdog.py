import os
import sys
import time
import subprocess
import urllib.request
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PYTHON_EXE = BASE_DIR / ".venv" / "Scripts" / "python.exe"
if not PYTHON_EXE.exists():
    PYTHON_EXE = Path(sys.executable)

LOG_FILE = BASE_DIR / "storage" / "service_watchdog.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [WATCHDOG 24/7] {msg}"
    print(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def is_ollama_running() -> bool:
    try:
        req = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        return req.getcode() == 200
    except Exception:
        return False

def ensure_ollama():
    if is_ollama_running():
        return
    log("Iniciando servidor local Ollama...")
    ollama_path = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe"
    if ollama_path.exists():
        subprocess.Popen([str(ollama_path), "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
    else:
        log("Ollama no encontrado en ruta predeterminada; continuando con motor de producción...")

def is_server_healthy() -> bool:
    try:
        req = urllib.request.urlopen("http://localhost:8000/api/status", timeout=5)
        if req.getcode() == 200:
            data = json.loads(req.read().decode())
            return "camera" in data
        return False
    except Exception:
        return False

def main():
    log("=======================================================")
    log("   BADDGROUP VISION AI - SUPERVISOR DE PRODUCCIÓN 24/7")
    log("=======================================================")
    log(f"Ejecutable Python: {PYTHON_EXE}")

    ensure_ollama()

    server_process = None
    failures = 0

    def start_server():
        nonlocal server_process
        log("Iniciando proceso principal del servidor Baddgroup Vision AI...")
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        server_process = subprocess.Popen(
            [str(PYTHON_EXE), str(BASE_DIR / "run_server.py")],
            cwd=str(BASE_DIR),
            env=env
        )
        time.sleep(6)

    start_server()

    while True:
        try:
            time.sleep(15)

            # Verificar si el proceso sigue vivo
            if server_process.poll() is not None:
                log(f"ALERTA: El proceso del servidor se cerró con código {server_process.returncode}. Reiniciando de inmediato...")
                ensure_ollama()
                start_server()
                failures = 0
                continue

            # Verificar respuesta HTTP del backend
            if is_server_healthy():
                failures = 0
            else:
                failures += 1
                log(f"ADVERTENCIA: Fallo de verificación de salud ({failures}/3)...")
                if failures >= 3:
                    log("CRÍTICO: El servidor no responde a las solicitudes de estado. Terminando y reiniciando proceso...")
                    try:
                        server_process.terminate()
                        server_process.wait(timeout=5)
                    except Exception:
                        server_process.kill()
                    ensure_ollama()
                    start_server()
                    failures = 0

        except KeyboardInterrupt:
            log("Supervisor detenido por el usuario.")
            if server_process:
                server_process.terminate()
            break
        except Exception as e:
            log(f"Error en ciclo de supervisión: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
