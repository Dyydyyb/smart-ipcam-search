import paramiko
import time
import socket
import threading
import concurrent.futures

def find_camera_ip():
    def check(ip):
        s = socket.socket()
        s.settimeout(0.2)
        if s.connect_ex((ip, 554)) == 0:
            s.close()
            return ip
        s.close()
        return None

    ips = [f'192.168.100.{i}' for i in range(1, 255)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
        for res in ex.map(check, ips):
            if res:
                return res
    return "192.168.100.198"

def test_vps_opencv():
    cam_ip = find_camera_ip()
    print(f"Cámara detectada en LAN: {cam_ip}:554")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('66.97.44.166', port=5199, username='root', password='Dylanssj2.camaras', timeout=15)
    
    transport = ssh.get_transport()
    transport.set_keepalive(10)
    print("Estableciendo Reverse Tunnel en VPS 127.0.0.1:18554 -> Cámara LAN...")
    transport.request_port_forward('', 18554)
    
    stop_event = threading.Event()
    
    def handler(channel):
        sock = socket.socket()
        sock.connect((cam_ip, 554))
        
        def forward(source, destination):
            try:
                while not stop_event.is_set():
                    data = source.recv(8192)
                    if not data:
                        break
                    destination.sendall(data)
            except Exception:
                pass
            finally:
                source.close()
                destination.close()
                
        threading.Thread(target=forward, args=(channel, sock), daemon=True).start()
        threading.Thread(target=forward, args=(sock, channel), daemon=True).start()
        
    def accept_thread():
        while not stop_event.is_set():
            try:
                chan = transport.accept(1.0)
                if chan is not None:
                    handler(chan)
            except Exception:
                break
                
    t = threading.Thread(target=accept_thread, daemon=True)
    t.start()
    
    time.sleep(2)
    print("Probando captura con OpenCV dentro del contenedor Docker en el VPS...")
    cmd = "docker exec baddgroup-vision-ai python -c \"import cv2, os; os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS']='rtsp_transport;tcp'; cap=cv2.VideoCapture('rtsp://admin:L27EA4F3@host.docker.internal:18554/cam/realmonitor?channel=1&subtype=1'); print('VPS OPENCV OPENED:', cap.isOpened()); ret, frame = cap.read(); print('VPS READ FRAME:', ret, 'SHAPE:', frame.shape if ret else None); cap.release()\""
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print("OUTPUT DESDE EL VPS:\n", out)
    if err:
        print("STDERR:\n", err)
        
    stop_event.set()
    ssh.close()

if __name__ == '__main__':
    test_vps_opencv()
