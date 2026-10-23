import sys
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

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=10)
        print("[OK] Conectado a DonWeb.")
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    commands = [
        "cd /opt/baddgroup-vision && git fetch origin && git reset --hard origin/main",
        "cd /opt/baddgroup-vision && docker compose up -d --build",
        "sleep 5",
        "docker ps",
        "curl -s -i http://localhost:8000/api/status"
    ]

    for cmd in commands:
        print(f"\n--- EXEC: {cmd} ---")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        print(out)
        if err:
            print("[STDERR]", err)

    ssh.close()

if __name__ == "__main__":
    main()
