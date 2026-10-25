import paramiko

def check():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('66.97.44.166', port=5199, username='root', password='Dylanssj2.camaras', timeout=15)
    
    commands = [
        "docker exec baddgroup-vision-ai head -n 20 /app/storage/cameras.json",
        "docker exec baddgroup-vision-ai python -c \"import sqlite3; c=sqlite3.connect('/app/storage/smart_cam.db'); print('DB Events:', c.cursor().execute('SELECT COUNT(*) FROM security_events').fetchone()); c.close()\"",
        "docker exec baddgroup-vision-ai grep -n 'escapeHtml' /app/frontend/index.html | head -n 5",
        "docker exec baddgroup-vision-ai grep -n 'Cámara Poste' /app/frontend/index.html | head -n 5",
        "docker exec baddgroup-vision-ai grep -n 'get_camera_by_id' /app/backend/main.py | head -n 5"
    ]
    
    for cmd in commands:
        print(f"=== {cmd} ===")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode('utf-8', errors='replace'))
        err = stderr.read().decode('utf-8', errors='replace')
        if err:
            print("ERR:", err)
            
    ssh.close()

if __name__ == '__main__':
    check()
