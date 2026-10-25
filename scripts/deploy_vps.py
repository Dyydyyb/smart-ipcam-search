import paramiko
import sys

def main():
    print("Conectando al VPS DonWeb (66.97.44.166:5199)...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('66.97.44.166', port=5199, username='root', password='Dylanssj2.camaras', timeout=15)

    # 1. Buscar la ruta donde se clonó el repo
    stdin, stdout, stderr = ssh.exec_command('find / -name "run_server.py" 2>/dev/null')
    locations = stdout.read().decode().strip().split("\n")
    print("Ubicaciones de run_server.py:", locations)

    # Filtrar ruta en host (no dentro de /var/lib/docker/overlay2)
    host_repo_dir = None
    for loc in locations:
        if "overlay2" not in loc and loc:
            host_repo_dir = loc.rsplit('/', 1)[0]
            break
            
    print("Directorio del repo en host:", host_repo_dir)

    if host_repo_dir:
        # Actualizar repo vía git pull
        cmd = f"cd {host_repo_dir} && git pull origin main"
        print(f"Ejecutando: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("GIT PULL OUT:", stdout.read().decode())
        print("GIT PULL ERR:", stderr.read().decode())

    # 2. Copiar archivos clave directamente al contenedor Docker activo
    print("Copiando archivos directamente al contenedor baddgroup-vision-ai...")
    
    # Usar sftp para subir los archivos actualizados a /tmp en el VPS
    sftp = ssh.open_sftp()
    
    files_to_sync = [
        ("core/supabase_db.py", "/tmp/supabase_db.py", "/app/core/supabase_db.py"),
        ("core/camera_manager.py", "/tmp/camera_manager.py", "/app/core/camera_manager.py"),
        ("core/config.py", "/tmp/config.py", "/app/core/config.py"),
        ("engine/stream_capture.py", "/tmp/stream_capture.py", "/app/engine/stream_capture.py"),
        ("engine/vision_pipeline.py", "/tmp/vision_pipeline.py", "/app/engine/vision_pipeline.py"),
        ("backend/main.py", "/tmp/main.py", "/app/backend/main.py"),
        ("frontend/login.html", "/tmp/login.html", "/app/frontend/login.html"),
        ("frontend/crm.html", "/tmp/crm.html", "/app/frontend/crm.html"),
        ("frontend/index.html", "/tmp/index.html", "/app/frontend/index.html"),
        ("storage/cameras.json", "/tmp/cameras.json", "/app/storage/cameras.json"),
        (".env", "/tmp/.env", "/app/.env")
    ]
    
    for local_f, remote_tmp, container_dest in files_to_sync:
        print(f"Subiendo {local_f} -> {remote_tmp}...")
        sftp.put(local_f, remote_tmp)
        # Copiar al contenedor
        cp_cmd = f"docker cp {remote_tmp} baddgroup-vision-ai:{container_dest}"
        stdin, stdout, stderr = ssh.exec_command(cp_cmd)
        err = stderr.read().decode()
        if err:
            print(f"Error copiando {local_f} al contenedor: {err}")
        else:
            print(f"[OK] {container_dest} actualizado en el contenedor.")
            
    sftp.close()

    # 3. Instalar psycopg2-binary y bcrypt dentro del contenedor si hicieran falta
    print("Verificando librerías psycopg2 y bcrypt dentro del contenedor...")
    stdin, stdout, stderr = ssh.exec_command("docker exec baddgroup-vision-ai pip install psycopg2-binary bcrypt")
    print(stdout.read().decode())

    # 4. Reiniciar el contenedor
    print("Reiniciando contenedor baddgroup-vision-ai...")
    stdin, stdout, stderr = ssh.exec_command("docker restart baddgroup-vision-ai")
    print("RESTART:", stdout.read().decode())

    # 5. Comprobar salud y logs
    stdin, stdout, stderr = ssh.exec_command("sleep 3 && docker logs --tail 25 baddgroup-vision-ai")
    print("LOGS DEL CONTENEDOR:\n", stdout.read().decode())

    # 5b. Comprobar CPU y Memoria
    stdin, stdout, stderr = ssh.exec_command("docker stats --no-stream")
    print("DOCKER STATS:\n", stdout.read().decode())

    # 6. Comprobar status de mediamtx
    stdin, stdout, stderr = ssh.exec_command("systemctl status mediamtx --no-pager")
    status_text = stdout.read().decode('utf-8', errors='replace')[:300].encode('ascii', errors='replace').decode('ascii')
    print("MEDIAMTX STATUS:\n", status_text)

    # 7. Actualizar repositorio del host
    stdin, stdout, stderr = ssh.exec_command("cd /opt/baddgroup-vision && git pull origin main")
    print("HOST REPO PULL:", stdout.read().decode('utf-8', errors='replace'))

    ssh.close()
    print("\nDespliegue completado con éxito!")

if __name__ == "__main__":
    main()
