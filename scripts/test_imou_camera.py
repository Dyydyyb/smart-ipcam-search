"""
Script de Diagnóstico y Prueba de Conexión RTSP - Cámara Imou (Fase 0)
====================================================================
Este script verifica:
1. Conectividad de red a nivel socket TCP al puerto RTSP (554).
2. Apertura del stream de video usando OpenCV con transporte TCP.
3. Extracción de metadatos (resolución nativa, FPS, estabilidad).
4. Captura y almacenamiento de un fotograma de prueba (snapshot).

Uso:
    python scripts/test_imou_camera.py --ip 192.168.1.50 --password TU_SAFETY_CODE
o configurando un archivo .env
"""

import os
import sys
import time
import socket
import argparse
from pathlib import Path

# Configurar OpenCV para usar RTSP sobre TCP (evita paquetes perdidos y artefactos en Wi-Fi)
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"


def check_tcp_port(ip: str, port: int = 554, timeout: float = 3.0) -> bool:
    """Verifica si el puerto TCP 554 está abierto en la cámara."""
    print(f"[*] Comprobando conexión TCP con {ip}:{port}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        print(f"[✓] Puerto TCP {port} abierto y respondiendo.")
        return True
    except socket.timeout:
        print(f"[✗] Tiempo de espera agotado al conectar a {ip}:{port}.")
        print("    -> Verifica que la cámara esté encendida y conectada a la misma red Wi-Fi / LAN.")
        return False
    except Exception as e:
        print(f"[✗] Error al conectar al puerto {port}: {e}")
        return False


def test_rtsp_stream(rtsp_url: str, output_image_path: Path, max_test_frames: int = 60):
    """Prueba la captura de frames mediante OpenCV."""
    try:
        import cv2
    except ImportError:
        print("[✗] Error: OpenCV no está instalado. Ejecuta: pip install opencv-python-headless")
        sys.exit(1)

    # Ocultar la contraseña al imprimir en consola para seguridad
    safe_url = rtsp_url
    if "@" in rtsp_url:
        protocol_and_auth, rest = rtsp_url.split("@", 1)
        protocol, auth = protocol_and_auth.split("://", 1)
        user = auth.split(":", 1)[0]
        safe_url = f"{protocol}://{user}:******@{rest}"

    print(f"\n[*] Intentando abrir stream RTSP:")
    print(f"    URL: {safe_url}")

    start_time = time.time()
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print("[✗] No se pudo abrir el stream RTSP.")
        print("\n🔍 Posibles causas en cámaras Imou:")
        print(" 1. La contraseña no es la de la cuenta Imou Life, sino el 'Safety Code' impreso debajo de la cámara.")
        print(" 2. El usuario por defecto siempre es 'admin'.")
        print(" 3. En algunas versiones de firmware, ONVIF / RTSP debe activarse en la app Imou Life o Dahua ConfigTool.")
        print(" 4. La URL puede requerir canal o subtipo diferente:")
        print("    - Mainstream: /cam/realmonitor?channel=1&subtype=0")
        print("    - Substream:  /cam/realmonitor?channel=1&subtype=1")
        return False

    connect_duration = time.time() - start_time
    print(f"[✓] ¡Stream conectado exitosamente en {connect_duration:.2f} segundos!")

    # Obtener propiedades del stream
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print("\n📊 Información del Stream detectada:")
    print(f"    - Resolución: {width}x{height} píxeles")
    print(f"    - FPS reportados: {fps:.1f}")

    print(f"\n[*] Leyendo {max_test_frames} fotogramas para comprobar estabilidad...")
    frames_read = 0
    test_start = time.time()
    last_frame = None

    for i in range(max_test_frames):
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"[!] Fallo al leer frame #{i + 1}")
            break
        frames_read += 1
        last_frame = frame
        if (i + 1) % 15 == 0:
            print(f"    -> {i + 1}/{max_test_frames} frames procesados...")

    cap.release()
    elapsed = time.time() - test_start
    effective_fps = frames_read / elapsed if elapsed > 0 else 0

    print(f"\n[✓] Lectura finalizada: {frames_read} frames en {elapsed:.2f}s (FPS reales: {effective_fps:.1f})")

    if last_frame is not None:
        output_image_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_image_path), last_frame)
        print(f"[✓] Fotograma de prueba guardado en: {output_image_path.resolve()}")
        print("\n🎉 FASE 0 COMPLETADA CON ÉXITO: Tu cámara Imou está lista para el pipeline de IA.")
        return True
    else:
        print("[✗] No se pudo obtener ningún frame válido.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Prueba de conexión RTSP para cámara Imou")
    parser.add_argument("--ip", help="Dirección IP de la cámara (ej: 192.168.1.150)")
    parser.add_argument("--port", type=int, default=554, help="Puerto RTSP (default: 554)")
    parser.add_argument("--user", default="admin", help="Usuario RTSP (default: admin)")
    parser.add_argument("--password", help="Contraseña o Safety Code de la cámara")
    parser.add_argument("--subtype", type=int, default=0, choices=[0, 1],
                        help="Subtipo: 0 para Mainstream (Alta res), 1 para Substream (Baja res)")
    parser.add_argument("--output", default="snapshots/camera_test.jpg", help="Ruta donde guardar la foto de prueba")

    args = parser.parse_args()

    # Intentar leer desde .env si existe
    env_file = Path(".env")
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass

    ip = args.ip or os.getenv("CAMERA_IP")
    port = args.port or int(os.getenv("CAMERA_PORT", "554"))
    user = args.user or os.getenv("CAMERA_USER", "admin")
    password = args.password or os.getenv("CAMERA_PASSWORD")
    subtype = args.subtype

    if not ip or not password:
        print("=" * 70)
        print("⚠️  Faltan parámetros de conexión")
        print("=" * 70)
        print("Puedes ejecutarnos pasando argumentos:")
        print("  python scripts/test_imou_camera.py --ip <IP> --password <SAFETY_CODE>")
        print("\nO crear el archivo .env a partir de .env.example:")
        print("  cp .env.example .env")
        print("  (y editar CAMERA_IP y CAMERA_PASSWORD)\n")

        if not ip:
            ip = input("Introduce la IP local de la cámara (ej: 192.168.1.50): ").strip()
        if not password:
            password = input("Introduce el Safety Code / Contraseña de la cámara: ").strip()

    if not ip or not password:
        print("[✗] Error: Se requieren IP y contraseña para continuar.")
        sys.exit(1)

    # 1. Verificar socket TCP
    if not check_tcp_port(ip, port):
        sys.exit(1)

    # 2. Construir URL RTSP estándar de Dahua / Imou
    rtsp_url = f"rtsp://{user}:{password}@{ip}:{port}/cam/realmonitor?channel=1&subtype={subtype}"
    output_path = Path(args.output)

    # 3. Probar captura de video
    success = test_rtsp_stream(rtsp_url, output_path)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
