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

cur.execute("SELECT id, username, role FROM users")
print("USERS:", cur.fetchall())

cur.execute("SELECT id, user_id, name, client_user FROM clients")
print("CLIENTS:", cur.fetchall())

cur.execute("SELECT id, client_id, name, safety_code FROM cameras")
print("CAMERAS:", cur.fetchall())
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
