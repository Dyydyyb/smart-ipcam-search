import socket
import json
import time

def find_cameras():
    print("Escaneando red local por cámaras Dahua / Imou / ONVIF...")
    
    # 1. Dahua / Imou Broadcast
    msg = json.dumps({"method": "DHDiscover.search", "params": {"mac": ""}}).encode('utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(2.0)
    
    found = []
    try:
        s.sendto(msg, ('239.255.255.251', 37810))
        s.sendto(msg, ('255.255.255.255', 37810))
        while True:
            data, addr = s.recvfrom(4096)
            text = data.decode('utf-8', errors='ignore')
            print(f"[DAHUA/IMOU DETECTADA] IP: {addr[0]} | Datos: {text[:200]}")
            found.append(addr[0])
    except socket.timeout:
        pass
    finally:
        s.close()
        
    # 2. WS-Discovery (ONVIF estándar)
    ws_msg = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<Envelope xmlns="http://www.w3.org/2003/05/soap-envelope">'
        '<Header><Action xmlns="http://schemas.xmlsoap.org/ws/2005/04/addressing">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</Action></Header>'
        '<Body><Probe xmlns="http://schemas.xmlsoap.org/ws/2005/04/discovery"><Types>dn:NetworkVideoTransmitter</Types></Probe></Body>'
        '</Envelope>'
    ).encode('utf-8')
    
    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s2.settimeout(2.0)
    try:
        s2.sendto(ws_msg, ('239.255.255.250', 3702))
        while True:
            data, addr = s2.recvfrom(4096)
            text = data.decode('utf-8', errors='ignore')
            print(f"[ONVIF DETECTADA] IP: {addr[0]}")
            found.append(addr[0])
    except socket.timeout:
        pass
    finally:
        s2.close()

    if not found:
        print("[INFO] No se detectó ninguna cámara respondiendo por broadcast UDP.")
    else:
        print(f"[EXITO] Cámaras encontradas en la red: {set(found)}")

if __name__ == "__main__":
    find_cameras()
