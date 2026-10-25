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
DOMAIN = "vision.baddgroup.com"

nginx_conf = f"""server {{
    listen 80;
    listen [::]:80;
    server_name {DOMAIN};

    client_max_body_size 100M;

    # Certbot ACME challenge
    location /.well-known/acme-challenge/ {{
        root /var/www/html;
    }}

    location / {{
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
        proxy_send_timeout 86400;
        proxy_buffering off;
    }}
}}
"""

def main():
    print(f"[*] Conectando al VPS DonWeb ({HOST}:{PORT})...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=12)
    print("[✓] Conectado exitosamente por SSH.")

    sftp = ssh.open_sftp()
    remote_path = f"/etc/nginx/sites-available/{DOMAIN}"
    print(f"[*] Escribiendo archivo de configuración en {remote_path}...")
    with sftp.file(remote_path, "w") as f:
        f.write(nginx_conf)
    sftp.close()
    print("[✓] Archivo Nginx guardado.")

    commands = [
        "mkdir -p /var/www/html",
        f"ln -sf /etc/nginx/sites-available/{DOMAIN} /etc/nginx/sites-enabled/{DOMAIN}",
        "nginx -t",
        "systemctl reload nginx",
        "systemctl status nginx --no-pager"
    ]

    for cmd in commands:
        print(f"\n[EXEC] >>> {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        if out:
            print(out.strip())
        if err and "warning" not in err.lower():
            print(f"[STDERR] {err.strip()}")

    ssh.close()
    print(f"\n[✓] Configuración de {DOMAIN} lista y activa en Nginx.")

if __name__ == "__main__":
    main()
