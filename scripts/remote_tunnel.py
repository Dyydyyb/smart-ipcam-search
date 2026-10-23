import os
import sys
import shutil
import urllib.request
import subprocess
from pathlib import Path
from loguru import logger

CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
TOOLS_DIR.mkdir(parents=True, exist_ok=True)
CLOUDFLARED_EXE = TOOLS_DIR / "cloudflared.exe"

def ensure_cloudflared():
    if CLOUDFLARED_EXE.exists():
        return CLOUDFLARED_EXE
    
    # Check if in system PATH
    sys_path = shutil.which("cloudflared")
    if sys_path:
        return Path(sys_path)
    
    logger.info("Descargando Cloudflare Tunnel para acceso remoto seguro...")
    try:
        urllib.request.urlretrieve(CLOUDFLARED_URL, str(CLOUDFLARED_EXE))
        logger.success(f"Cloudflare Tunnel descargado en {CLOUDFLARED_EXE}")
        return CLOUDFLARED_EXE
    except Exception as e:
        logger.error(f"Error descargando cloudflared: {e}")
        return None

def start_tunnel(port: int = 8000):
    exe = ensure_cloudflared()
    if not exe:
        logger.error("No se pudo iniciar el túnel. Descárguelo manualmente desde: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/")
        return

    logger.info(f"Iniciando túnel seguro HTTPS para http://localhost:{port}...")
    logger.info("Esto generará una URL pública segura (https://*.trycloudflare.com) para gestionar su cámara desde el celular o mostrar demos en vivo a clientes del extranjero.")
    
    proc = subprocess.Popen(
        [str(exe), "tunnel", "--url", f"http://localhost:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    for line in proc.stdout:
        print(line, end="")
        if "trycloudflare.com" in line:
            import re
            match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if match:
                url = match.group(0)
                logger.success("=================================================================")
                logger.success(f">> URL PÚBLICA ACTIVA PARA DEMOS Y ACCESO REMOTO:")
                logger.success(f">> {url}")
                logger.success("=================================================================")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_tunnel(port)
