import paramiko

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('66.97.44.166', port=5199, username='root', password='Dylanssj2.camaras', timeout=10)
    
    # Probar autenticación directa en python dentro del contenedor
    cmd = '''docker exec baddgroup-vision-ai python -c "
from core import supabase_db
print('DB URL:', supabase_db.settings.SUPABASE_DB_URL)
user = supabase_db.authenticate_user('dylan', 'Dylanssj2.camaras')
print('AUTHENTICATE USER:', user)
token = supabase_db.generate_token(user) if user else None
print('TOKEN:', token)
"'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("OUTPUT:\n", stdout.read().decode('utf-8', errors='replace'))
    print("ERR:\n", stderr.read().decode('utf-8', errors='replace'))
    
    ssh.close()

if __name__ == "__main__":
    main()
