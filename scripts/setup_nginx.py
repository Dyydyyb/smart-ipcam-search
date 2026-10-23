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

nginx_conf = """server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
"""

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=10)
    print("[OK] Conectado a DonWeb vía SSH.")

    sftp = ssh.open_sftp()
    with sftp.file("/etc/nginx/sites-available/default", "w") as f:
        f.write(nginx_conf)
    sftp.close()
    print("[OK] Configuración Nginx escrita en /etc/nginx/sites-available/default.")

    commands = [
        "nginx -t",
        "systemctl restart nginx",
        "systemctl status nginx --no-pager",
        "curl -s -i http://localhost/api/status"
    ]

    for cmd in commands:
        print(f"\n[EXEC] >>> {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        for line in stdout:
            print(line, end="", flush=True)
        err = stderr.read().decode("utf-8", errors="replace")
        if err and "warning" not in err.lower():
            print(f"[STDERR] {err}", flush=True)

    ssh.close()
    print("\n[OK] Nginx proxy inverso 80 -> 8000 activo.")

if __name__ == "__main__":
    main()
