import os
import sys
import time
import socket
import urllib.request
import cv2
import numpy as np

# Configurar RTSP TCP
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

CAMERA_IP = "192.168.100.198"
CAMERA_USER = "admin"
CAMERA_PASS = "L27EA4F3"
VPS_PUSH_URL = "http://66.97.44.166/api/stream/push"

def find_camera():
    global CAMERA_IP
    # Probar IP actual primero
    s = socket.socket()
    s.settimeout(0.3)
    if s.connect_ex((CAMERA_IP, 554)) == 0:
        s.close()
        return CAMERA_IP
    s.close()
    
    # Escanear subred
    print("[BRIDGE] Buscando IP de la cámara en 192.168.100.x...")
    import concurrent.futures
    def check(ip):
        sock = socket.socket()
        sock.settimeout(0.2)
        if sock.connect_ex((ip, 554)) == 0:
            sock.close()
            return ip
        sock.close()
        return None

    ips = [f"192.168.100.{i}" for i in range(1, 255)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
        for res in ex.map(check, ips):
            if res:
                CAMERA_IP = res
                return res
    return CAMERA_IP

def run_bridge():
    cam_ip = find_camera()
    rtsp_url = f"rtsp://{CAMERA_USER}:{CAMERA_PASS}@{cam_ip}:554/cam/realmonitor?channel=1&subtype=1"
    print(f"[BRIDGE] Conectando a cámara física en {cam_ip}:554...")
    
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("[BRIDGE ERROR] No se pudo abrir el stream RTSP de la cámara.")
        return False
        
    print(f"[BRIDGE OK] Cámara conectada! Transmitiendo frames a {VPS_PUSH_URL}...")
    
    frame_count = 0
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("[BRIDGE] Pérdida de frame. Reconectando...")
                time.sleep(1)
                break
                
            frame_count += 1
            # Redimensionar a 640x480 si no lo está
            if frame.shape[1] != 640 or frame.shape[0] != 480:
                frame = cv2.resize(frame, (640, 480))
                
            ret_enc, buffer = cv2.imencode('.jpg', frame, encode_param)
            if not ret_enc:
                continue
                
            # Enviar frame por HTTP POST rápido
            req = urllib.request.Request(
                VPS_PUSH_URL,
                data=buffer.tobytes(),
                headers={'Content-Type': 'application/octet-stream'},
                method='POST'
            )
            try:
                with urllib.request.urlopen(req, timeout=1.0) as resp:
                    pass
            except Exception as e:
                pass
                
            if frame_count % 30 == 0:
                print(f"[BRIDGE] {frame_count} fotogramas enviados exitosamente al servidor Cloud.")
                
            time.sleep(0.066) # ~15 FPS
            
    finally:
        cap.release()

if __name__ == '__main__':
    while True:
        try:
            run_bridge()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[BRIDGE RETRY] Error: {e}. Reintentando en 3s...")
            time.sleep(3)
