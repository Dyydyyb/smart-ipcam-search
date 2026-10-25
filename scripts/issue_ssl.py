import sys
import time
import socket
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

def check_dns(max_retries=1, delay=3):
    print(f"[*] Comprobando resolución DNS para {DOMAIN}...")
    for i in range(max_retries):
        try:
            ip = socket.gethostbyname(DOMAIN)
            print(f"[✓] {DOMAIN} resuelve a IP: {ip}")
            if ip == HOST:
                return True
            else:
                print(f"[!] {DOMAIN} resuelve a {ip}, pero se esperaba {HOST}")
        except socket.gaierror:
            print(f"[-] Intento {i+1}/{max_retries}: {DOMAIN} aún no responde en DNS.")
        if i < max_retries - 1:
            time.sleep(delay)
    return False

def issue_certificate():
    print(f"[*] Conectando al VPS DonWeb ({HOST}:{PORT}) para emitir certificado SSL...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=15)

    cmd = f"certbot --nginx -d {DOMAIN} --non-interactive --agree-tos -m dylan@baddgroup.com --redirect"
    print(f"[EXEC] >>> {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    
    print("OUTPUT:\n", out)
    if err and "warning" not in err.lower():
        print("STDERR:\n", err)
        
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print(f"\n[✓] Certificado SSL Let's Encrypt instalado con éxito para {DOMAIN}!")
    else:
        print(f"\n[!] Certbot finalizó con código {exit_status}.")

    ssh.close()

if __name__ == "__main__":
    if check_dns():
        issue_certificate()
    else:
        print("\n[INFO] El registro DNS aún no fue detectado. Dylan debe añadir el registro A en DonWeb.")
