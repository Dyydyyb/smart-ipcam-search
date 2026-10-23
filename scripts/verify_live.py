import requests

def test_live_server():
    print("Iniciando verificación en el servidor DonWeb Cloud (66.97.44.166)...")
    
    # 1. Verificar HTML servido
    r_html = requests.get('http://66.97.44.166/')
    assert r_html.status_code == 200, f"Error cargando HTML: {r_html.status_code}"
    assert 'data-theme="light"' in r_html.text, "Falta data-theme=light en HTML!"
    assert 'id="liveMosaicCard"' in r_html.text, "Falta liveMosaicCard en HTML!"
    assert 'id="aiCameraSelect"' in r_html.text, "Falta aiCameraSelect en HTML!"
    print(">> 1. HTML Verification PASSED: Inicia en Modo Claro por defecto, con Mosaico Multi-Cámara y Selector IA Obligatorio.")

    # 2. Agregar segunda cámara si solo hay una
    cams = requests.get('http://66.97.44.166/api/cameras').json()
    if len(cams) < 2:
        add_res = requests.post('http://66.97.44.166/api/cameras', json={
            'name': 'Cámara Entrada Negocio',
            'location': 'Acceso Principal',
            'ip': '192.168.100.210',
            'port': 554,
            'user': 'admin'
        })
        print(">> Cámara agregada:", add_res.status_code, add_res.json())

    # 3. Listar cámaras
    cams = requests.get('http://66.97.44.166/api/cameras').json()
    print(f">> 2. Cámaras registradas en el servidor ({len(cams)}):")
    for c in cams:
        print(f"   - [{c['id']}] {c['name']} ({c['location']}) | IP: {c['ip']}:{c['port']}")

    # 4. Validar búsquedas con IA
    r_no_cam = requests.post('http://66.97.44.166/api/search', json={'query': 'personas'})
    assert r_no_cam.status_code == 400, "Debería dar 400 sin cámara"
    print(f">> 3. Validación de búsqueda sin cámara: HTTP {r_no_cam.status_code} - {r_no_cam.json()['detail']}")

    r_all_cam = requests.post('http://66.97.44.166/api/search', json={'query': 'personas', 'camera_id': 'all'})
    assert r_all_cam.status_code == 400, "Debería dar 400 con cámara=all"
    print(f">> 4. Validación de búsqueda en todas las cámaras: HTTP {r_all_cam.status_code} - {r_all_cam.json()['detail']}")

    r_specific = requests.post('http://66.97.44.166/api/search', json={'query': 'movimiento de brazos', 'camera_id': cams[0]['id']})
    assert r_specific.status_code == 200, f"Error en búsqueda con cámara específica: {r_specific.status_code}"
    data = r_specific.json()
    print(f">> 5. Búsqueda IA con cámara específica exitosa: HTTP 200 | Cámara: {data.get('camera_name')} | Eventos: {data.get('total_results')}")

    print("\nTODAS LAS VERIFICACIONES TÉCNICAS PASARON AL 100% EN PRODUCCIÓN.")

if __name__ == '__main__':
    test_live_server()
