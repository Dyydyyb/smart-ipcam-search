import paramiko
import time
import socket

def test():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('66.97.44.166', port=5199, username='root', password='Dylanssj2.camaras', timeout=15)
    
    # Abrir reverse port forwarding: en el VPS puerto 18554 hacia 192.168.100.198:554
    transport = ssh.get_transport()
    print("Solicitando reverse port forward en VPS puerto 18554 -> 192.168.100.198:554...")
    transport.request_port_forward('', 18554)
    
    # Desde el VPS, hacer un curl o netcat a 127.0.0.1:18554
    cmd = "python3 -c \"import socket; s=socket.socket(); s.settimeout(3); s.connect(('127.0.0.1', 18554)); s.sendall(b'OPTIONS rtsp://127.0.0.1:18554 RTSP/1.0\\r\\nCSeq: 1\\r\\n\\r\\n'); print('RTSP RESPONSE FROM HOME CAMERA THROUGH VPS TUNNEL:', s.recv(512).decode('latin1', errors='ignore')); s.close()\""
    
    def handler(channel, origin, server):
        sock = socket.socket()
        sock.connect(('192.168.100.198', 554))
        
        import threading
        def forward(source, destination):
            try:
                while True:
                    data = source.recv(4096)
                    if len(data) == 0:
                        break
                    destination.sendall(data)
            except Exception:
                pass
            finally:
                source.close()
                destination.close()
                
        threading.Thread(target=forward, args=(channel, sock), daemon=True).start()
        threading.Thread(target=forward, args=(sock, channel), daemon=True).start()
        
    transport.set_keepalive(10)
    
    import threading
    def accept_thread():
        while True:
            chan = transport.accept(2.0)
            if chan is not None:
                handler(chan, None, None)
                
    t = threading.Thread(target=accept_thread, daemon=True)
    t.start()
    
    time.sleep(1)
    print("Ejecutando prueba desde el VPS...")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('latin1', errors='ignore')
    err = stderr.read().decode('latin1', errors='ignore')
    print("SALIDA:", out)
    if err:
        print("ERR:", err)
        
    ssh.close()

if __name__ == '__main__':
    test()
