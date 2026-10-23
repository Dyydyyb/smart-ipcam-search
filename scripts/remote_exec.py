import sys
import paramiko

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HOST = "66.97.44.166"
PORT = 5199
USER = "root"
PASSWORD = "Dylanssj2.camaras"

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "docker ps"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=10)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    for line in stdout:
        print(line, end="", flush=True)
    err = stderr.read().decode("utf-8", errors="replace")
    if err and "warning" not in err.lower():
        print(f"[STDERR] {err}", flush=True)
    exit_status = stdout.channel.recv_exit_status()
    print(f"\n[STATUS] Exit code: {exit_status}", flush=True)
    ssh.close()

if __name__ == "__main__":
    main()
