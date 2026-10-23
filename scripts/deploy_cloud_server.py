import sys
import time
import paramiko

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HOST = "66.97.44.166"
PORT = 5199
USER = "root"
PASSWORD = "Dylanssj2.camaras"

def run_cmd(ssh, cmd, timeout=600):
    print(f"\n[REMOTE EXEC] >>> {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    
    # Stream output safely
    for line in stdout:
        try:
            print(line, end="", flush=True)
        except Exception:
            try:
                print(line.encode("ascii", errors="replace").decode("ascii"), end="", flush=True)
            except Exception:
                pass
    try:
        err = stderr.read().decode("utf-8", errors="replace")
    except Exception:
        err = ""
    if err and "warning" not in err.lower() and "debconf" not in err.lower():
        print(f"[STDERR] {err}")
    exit_status = stdout.channel.recv_exit_status()
    print(f"[STATUS] Exit code: {exit_status}")
    return exit_status

def main():
    print("===================================================================")
    print(f" Conectando a DonWeb Cloud Server: {HOST}:{PORT} como {USER}...")
    print("===================================================================")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=15)
        print("[OK] Conexión SSH establecida exitosamente con DonWeb.")
    except Exception as e:
        print(f"[ERROR] No se pudo conectar vía SSH: {e}")
        sys.exit(1)

    # 1. Verificar sistema operativo y recursos
    run_cmd(ssh, "uname -a && cat /etc/os-release | grep PRETTY_NAME && nproc && free -h")

    # 2. Actualizar repositorios e instalar Docker
    print("\n[PASO 1] Instalando Docker y dependencias del sistema...")
    run_cmd(ssh, "DEBIAN_FRONTEND=noninteractive apt-get update -y && apt-get install -y git curl ufw ca-certificates")

    # Instalar Docker oficial si no está presente
    run_cmd(ssh, "which docker || curl -fsSL https://get.docker.com | sh")
    run_cmd(ssh, "systemctl enable --now docker")

    # Verificar docker compose
    run_cmd(ssh, "docker compose version || apt-get install -y docker-compose-plugin")

    # 3. Descargar el repositorio del proyecto
    print("\n[PASO 2] Clonando/Actualizando repositorio Baddgroup Vision AI...")
    run_cmd(ssh, "mkdir -p /opt && if [ -d '/opt/baddgroup-vision' ]; then cd /opt/baddgroup-vision && git fetch origin && git reset --hard origin/main; else git clone https://github.com/Dyydyyb/smart-ipcam-search.git /opt/baddgroup-vision; fi")

    # 4. Configurar .env de producción en el servidor
    print("\n[PASO 3] Configurando variables de entorno de producción...")
    env_content = """CAMERA_IP=192.168.100.209
CAMERA_PORT=554
CAMERA_USER=admin
CAMERA_PASSWORD=L27EA4F3
CAMERA_RTSP_SUB=rtsp://admin:L27EA4F3@192.168.100.209:554/cam/realmonitor?channel=1&subtype=1
CAMERA_RTSP_MAIN=rtsp://admin:L27EA4F3@192.168.100.209:554/cam/realmonitor?channel=1&subtype=0
GEMINI_API_KEY=
GEMINI_MODEL=gemini-1.5-flash
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=qwen2.5:3b
DETECTION_FPS=5
RETENTION_DAYS=14
MAX_STORAGE_GB=25.0
"""
    sftp = ssh.open_sftp()
    with sftp.file("/opt/baddgroup-vision/.env", "w") as f:
        f.write(env_content)
    sftp.close()
    print("[OK] Archivo /opt/baddgroup-vision/.env configurado.")

    # 5. Asegurar puertos en firewall (abrir 8000, 80, 5199)
    print("\n[PASO 4] Configurando Firewall y puertos...")
    run_cmd(ssh, "ufw allow 5199/tcp && ufw allow 8000/tcp && ufw allow 80/tcp && ufw allow 443/tcp && ufw --force enable || true")

    # 6. Levantar la plataforma con Docker Compose
    print("\n[PASO 5] Levantando Baddgroup Vision AI con Docker Compose...")
    run_cmd(ssh, "cd /opt/baddgroup-vision && docker compose down || true")
    run_cmd(ssh, "cd /opt/baddgroup-vision && docker compose up -d --build", timeout=600)

    # 7. Verificar estado de los contenedores
    time.sleep(6)
    print("\n[PASO 6] Verificando salud del servidor...")
    run_cmd(ssh, "docker ps")
    run_cmd(ssh, "curl -s http://localhost:8000/api/status || echo 'Aun levantando servidor...'")

    ssh.close()
    print("\n===================================================================")
    print(" ¡DESPLIEGUE FINALIZADO EXITOSAMENTE EN DONWEB CLOUD!")
    print(f" URL Web Pública de Producción: http://{HOST}:8000")
    print("===================================================================")

if __name__ == "__main__":
    main()
