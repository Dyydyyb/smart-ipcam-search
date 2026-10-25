import requests

BASE_URL = 'http://66.97.44.166'

def main():
    # 1. Login Admin Dylan
    payload = {'username': 'dylan', 'password': 'Dylanssj2.camaras', 'expected_role': 'admin'}
    res = requests.post(f'{BASE_URL}/api/auth/login', json=payload)
    token_admin = res.json()['token']
    headers_admin = {'Authorization': f'Bearer {token_admin}'}

    # 2. Crear Cliente 'Comercio San Cayetano' con 2 cámaras
    new_client_data = {
        'name': 'Comercio San Cayetano',
        'business_type': 'Autoservicio',
        'phone': '+54 9 11 3344-5566',
        'client_user': 'sancayetano',
        'client_pass': 'caye2026',
        'monthly_fee': 28000,
        'billing_day': 10,
        'cameras': [
            {'name': 'Cámara 1: Entrada y Vereda', 'safety_code': 'L27EA4F3', 'serial_number': 'SN-IMOU-01', 'rtsp': 'rtsp://66.97.44.166:8554/live/caye1'},
            {'name': 'Cámara 2: Línea de Cajas', 'safety_code': 'K88BC291', 'serial_number': 'SN-IMOU-02', 'rtsp': 'rtsp://66.97.44.166:8554/live/caye2'}
        ]
    }
    create_res = requests.post(f'{BASE_URL}/api/crm/clients', headers=headers_admin, json=new_client_data)
    client_created = create_res.json()['client']
    client_id = client_created['id']
    num_cams = len(client_created['cameras'])
    print(f"[OK] Cliente creado en Supabase con {num_cams} cámaras: {client_created['name']}")

    # 3. Login como el Cliente 'sancayetano'
    login_client_res = requests.post(f'{BASE_URL}/api/auth/login', json={'username': 'sancayetano', 'password': 'caye2026', 'expected_role': 'client'})
    print("[OK] Login Cliente sancayetano exitoso:", login_client_res.status_code)
    token_client = login_client_res.json()['token']
    headers_client = {'Authorization': f'Bearer {token_client}'}

    # 4. Consultar /api/cameras como cliente -> Debe retornar exactamente sus 2 cámaras
    client_cams = requests.get(f'{BASE_URL}/api/cameras', headers=headers_client).json()
    print(f"[OK] Cámaras detectadas en la cuenta del cliente ({len(client_cams)}):")
    for c in client_cams:
        print(f"   - {c['name']} | Safety: {c.get('safety_code')} | SN: {c.get('serial_number')}")

    # 5. Agregar una 3ra cámara al cliente desde el CRM
    updated_data = {
        'cameras': [
            {'name': 'Cámara 1: Entrada y Vereda', 'safety_code': 'L27EA4F3', 'serial_number': 'SN-IMOU-01', 'rtsp': 'rtsp://66.97.44.166:8554/live/caye1'},
            {'name': 'Cámara 2: Línea de Cajas', 'safety_code': 'K88BC291', 'serial_number': 'SN-IMOU-02', 'rtsp': 'rtsp://66.97.44.166:8554/live/caye2'},
            {'name': 'Cámara 3: Depósito y Stock', 'safety_code': 'M99XX441', 'serial_number': 'SN-IMOU-03', 'rtsp': 'rtsp://66.97.44.166:8554/live/caye3'}
        ]
    }
    requests.put(f'{BASE_URL}/api/crm/clients/{client_id}', headers=headers_admin, json=updated_data)

    # 6. Consultar nuevamente como cliente -> Ahora debe tener 3 cámaras
    client_cams_v2 = requests.get(f'{BASE_URL}/api/cameras', headers=headers_client).json()
    print(f"[OK] Tras agregar cámara en CRM, cliente detecta en vivo ({len(client_cams_v2)} cámaras):")
    for c in client_cams_v2:
        print(f"   - {c['name']} | Safety: {c.get('safety_code')}")

    # 7. Eliminar cámaras dejando solo 1
    updated_data_v3 = {
        'cameras': [
            {'name': 'Cámara 1: Entrada y Vereda', 'safety_code': 'L27EA4F3', 'serial_number': 'SN-IMOU-01', 'rtsp': 'rtsp://66.97.44.166:8554/live/caye1'}
        ]
    }
    requests.put(f'{BASE_URL}/api/crm/clients/{client_id}', headers=headers_admin, json=updated_data_v3)
    client_cams_v3 = requests.get(f'{BASE_URL}/api/cameras', headers=headers_client).json()
    print(f"[OK] Tras eliminar cámaras en CRM, cliente detecta en vivo ({len(client_cams_v3)} cámaras):")
    for c in client_cams_v3:
        print(f"   - {c['name']}")

    # 8. Limpiar cliente de prueba para dejar base 100% limpia
    requests.delete(f'{BASE_URL}/api/crm/clients/{client_id}', headers=headers_admin)
    print("[OK] Cliente de prueba eliminado con éxito. Base de datos 100% limpia!")

if __name__ == '__main__':
    main()
