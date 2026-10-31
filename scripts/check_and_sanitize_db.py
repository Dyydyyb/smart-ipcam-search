import paramiko

def main():
    print("Conectando al VPS DonWeb para verificar base de datos Supabase...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('66.97.44.166', port=5199, username='root', password='Dylanssj2.camaras', timeout=15)

    python_code = '''
from core.supabase_db import get_db
conn = get_db()
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'cameras'")
cols = [r[0] for r in cur.fetchall()]
print("COLUMNAS DE CAMERAS:", cols)

cur.execute("SELECT * FROM cameras")
rows = cur.fetchall()
print("CAMARAS ACTUALES:", rows)

cur.execute("UPDATE cameras SET safety_code = 'BG-SEC-01' WHERE safety_code ILIKE '%L27EA4F3%'")
cur.execute("UPDATE cameras SET rtsp_sub = REPLACE(rtsp_sub, 'L27EA4F3', 'BG-SEC-01') WHERE rtsp_sub ILIKE '%L27EA4F3%'")
cur.execute("UPDATE cameras SET rtsp_main = REPLACE(rtsp_main, 'L27EA4F3', 'BG-SEC-01') WHERE rtsp_main ILIKE '%L27EA4F3%'")
cur.execute("UPDATE cameras SET stream_url = REPLACE(stream_url, 'L27EA4F3', 'BG-SEC-01') WHERE stream_url ILIKE '%L27EA4F3%'")
conn.commit()

cur.execute("SELECT id, name, safety_code, rtsp_sub FROM cameras")
print("CAMARAS SANITIZADAS:", cur.fetchall())
'''

    # Escribir script temporal dentro del contenedor
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/sanitize_db.py', 'w') as f:
        f.write(python_code)
    sftp.close()

    stdin, stdout, stderr = ssh.exec_command('docker cp /tmp/sanitize_db.py baddgroup-vision-ai:/app/sanitize_db.py && docker exec baddgroup-vision-ai python /app/sanitize_db.py')
    print("OUT:\n", stdout.read().decode())
    print("ERR:\n", stderr.read().decode())
    ssh.close()

if __name__ == "__main__":
    main()
