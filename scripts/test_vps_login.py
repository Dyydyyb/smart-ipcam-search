import paramiko

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('66.97.44.166', port=5199, username='root', password='Dylanssj2.camaras', timeout=10)
    
    cmd = 'curl -k -s -X POST https://127.0.0.1/api/auth/login -H "Host: vision.baddgroup.com" -H "Content-Type: application/json" -d "{\\"username\\":\\"BaddgroupDylan\\",\\"password\\":\\"1169957772\\"}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print("LOGIN RESPONSE VIA NGINX HTTPS:")
    print(out)
    if err:
        print("ERR:", err)
    
    ssh.close()

if __name__ == "__main__":
    main()
