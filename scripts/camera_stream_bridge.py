import os
import sys
import time
import socket
import threading
import requests
import cv2
import numpy as np

# Configurar RTSP sobre TCP y buffer mínimo de FFmpeg para latencia cero
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|buffer_size;102400|max_delay;500000|reorder_queue_size;0"

CAMERA_IP = "192.168.100.198"
CAMERA_USER = "admin"
SAFETY_CODE = os.environ.get("SAFETY_CODE", sys.argv[1] if len(sys.argv) > 1 else "L27EA4F3").strip().upper()
CAMERA_PASS = SAFETY_CODE
VPS_PUSH_URL = f"http://66.97.44.166/api/stream/push?safety_code={SAFETY_CODE}"

def find_camera():
    global CAMERA_IP
    s = socket.socket()
    s.settimeout(0.3)
    if s.connect_ex((CAMERA_IP, 554)) == 0:
        s.close()
        return CAMERA_IP
    s.close()

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

class UltraFastBridge:
    def __init__(self, rtsp_url, push_url):
        self.rtsp_url = rtsp_url
        self.push_url = push_url
        self.latest_frame = None
        self.lock = threading.Lock()
        self.running = True
        self.connected = False
        self.session = requests.Session()
        # Pool HTTP persistente con Keep-Alive para eliminar latencia de handshake
        adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1, max_retries=0)
        self.session.mount("http://", adapter)
        self.session.headers.update({"Content-Type": "application/octet-stream"})

    def capture_loop(self):
        """Hilo de captura desacoplado: lee continuamente de la cámara descartando frames viejos."""
        while self.running:
            cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            if not cap.isOpened():
                print(f"[BRIDGE] Esperando conexión RTSP con la cámara...")
                time.sleep(2.0)
                continue

            self.connected = True
            print(f"[BRIDGE OK] Enlace RTSP activo con hardware de cámara.")
            try:
                while self.running:
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        print("[BRIDGE] Pérdida de señal RTSP. Reconectando...")
                        break
                    with self.lock:
                        self.latest_frame = frame
            finally:
                self.connected = False
                cap.release()
                time.sleep(1.0)

    def push_loop(self):
        """Hilo de transmisión: toma el frame más reciente y lo envía con conexión persistente."""
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        frame_count = 0
        target_fps = 15.0
        frame_interval = 1.0 / target_fps
        print(f"[BRIDGE] Transmitiendo a servidor Cloud ({self.push_url}) a {target_fps} FPS fluidos...")

        while self.running:
            start_t = time.time()
            frame_to_send = None

            with self.lock:
                if self.latest_frame is not None:
                    frame_to_send = self.latest_frame
                    self.latest_frame = None

            if frame_to_send is None:
                time.sleep(0.01)
                continue

            # Redimensionar a 640x480 si fuera necesario
            if frame_to_send.shape[1] != 640 or frame_to_send.shape[0] != 480:
                frame_to_send = cv2.resize(frame_to_send, (640, 480))

            ret_enc, buffer = cv2.imencode('.jpg', frame_to_send, encode_param)
            if not ret_enc:
                continue

            try:
                # POST directo con sesión reutilizada (5-10ms)
                resp = self.session.post(self.push_url, data=buffer.tobytes(), timeout=0.8)
                if resp.status_code == 200:
                    frame_count += 1
                    if frame_count % 60 == 0:
                        print(f"[BRIDGE CLOUD] {frame_count} fotogramas entregados fluidamente (Keep-Alive Activo).")
            except Exception:
                pass

            elapsed = time.time() - start_t
            sleep_time = max(0.005, frame_interval - elapsed)
            time.sleep(sleep_time)

    def start(self):
        t_cap = threading.Thread(target=self.capture_loop, daemon=True, name="Bridge-Capture")
        t_cap.start()

        # Esperar primer frame
        for _ in range(50):
            if self.latest_frame is not None:
                break
            time.sleep(0.1)

        self.push_loop()

def run_bridge():
    cam_ip = find_camera()
    rtsp_url = f"rtsp://{CAMERA_USER}:{CAMERA_PASS}@{cam_ip}:554/cam/realmonitor?channel=1&subtype=1"
    bridge = UltraFastBridge(rtsp_url, VPS_PUSH_URL)
    bridge.start()

if __name__ == '__main__':
    while True:
        try:
            run_bridge()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[BRIDGE RETRY] Error: {e}. Reintentando en 2s...")
            time.sleep(2)
