import paramiko

def enable():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('66.97.44.166', port=5199, username='root', password='Dylanssj2.camaras', timeout=15)
    
    cmd = "sed -i 's/^#*GatewayPorts.*/GatewayPorts yes/' /etc/ssh/sshd_config && systemctl restart ssh"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("OUTPUT:", stdout.read().decode())
    print("ERR:", stderr.read().decode())
    
    stdin, stdout, stderr = ssh.exec_command("grep GatewayPorts /etc/ssh/sshd_config")
    print("NEW CONFIG:", stdout.read().decode())
    ssh.close()

if __name__ == '__main__':
    enable()
