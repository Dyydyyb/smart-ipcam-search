import hmac
import hashlib
import base64
import json
import time
import uuid
import datetime
import psycopg2
import psycopg2.extras
import bcrypt
from typing import Optional, Dict, Any, List
from loguru import logger
from core.config import settings

def get_db():
    """Retorna una conexión a Supabase PostgreSQL."""
    conn = psycopg2.connect(settings.SUPABASE_DB_URL, connect_timeout=10)
    conn.autocommit = True
    return conn

# ==========================================
# AUTENTICACIÓN Y SEGURIDAD JWT / TOKENS
# ==========================================
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False

def generate_token(user: Dict[str, Any], expires_in_seconds: int = 86400 * 7) -> str:
    """Genera un token de sesión seguro firmado con HMAC-SHA256."""
    payload = {
        "sub": str(user.get("id")),
        "username": user.get("username"),
        "role": user.get("role", "client"),
        "full_name": user.get("full_name", ""),
        "exp": int(time.time()) + expires_in_seconds
    }
    raw_payload = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    b64_payload = base64.urlsafe_b64encode(raw_payload).decode('utf-8').rstrip('=')
    
    signature = hmac.new(
        settings.JWT_SECRET.encode('utf-8'),
        b64_payload.encode('utf-8'),
        hashlib.sha256
    ).digest()
    b64_sig = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    
    return f"{b64_payload}.{b64_sig}"

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Valida la firma y expiración del token."""
    if not token or '.' not in token:
        return None
    try:
        b64_payload, b64_sig = token.split('.', 1)
        
        # Validar firma
        expected_sig = hmac.new(
            settings.JWT_SECRET.encode('utf-8'),
            b64_payload.encode('utf-8'),
            hashlib.sha256
        ).digest()
        actual_sig = base64.urlsafe_b64decode(b64_sig + '=' * (-len(b64_sig) % 4))
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
        
        # Decodificar payload
        payload_bytes = base64.urlsafe_b64decode(b64_payload + '=' * (-len(b64_payload) % 4))
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        # Validar expiración
        if payload.get("exp", 0) < int(time.time()):
            return None
            
        return payload
    except Exception as e:
        logger.warning(f"Error verificando token: {e}")
        return None

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Valida usuario y contraseña en Supabase."""
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                SELECT id, username, email, password_hash, full_name, role, is_active 
                FROM users 
                WHERE (username = %s OR email = %s) AND is_active = TRUE;
            """, (username.strip(), username.strip().lower()))
            row = cur.fetchone()
            if not row:
                return None
            if verify_password(password, row["password_hash"]):
                return {
                    "id": str(row["id"]),
                    "username": row["username"],
                    "email": row["email"],
                    "full_name": row["full_name"],
                    "role": row["role"]
                }
            return None
    finally:
        conn.close()

def create_client_user(username: str, password: str, full_name: str, email: str = "") -> str:
    """Crea una cuenta de acceso para un cliente en Supabase."""
    conn = get_db()
    try:
        with conn.cursor() as cur:
            pwd_hash = hash_password(password)
            cur.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role, is_active)
                VALUES (%s, %s, %s, %s, 'client', TRUE)
                ON CONFLICT (username) DO UPDATE 
                SET password_hash = EXCLUDED.password_hash, full_name = EXCLUDED.full_name
                RETURNING id;
            """, (username.strip(), email.strip().lower() or None, pwd_hash, full_name.strip()))
            return str(cur.fetchone()[0])
    finally:
        conn.close()

# ==========================================
# CLIENTES & CÁMARAS EN SUPABASE
# ==========================================
def get_clients(search: Optional[str] = None, status: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = "SELECT * FROM clients WHERE 1=1"
            params = []
            
            if user_id:
                query += " AND user_id = %s"
                params.append(user_id)
                
            if status and status != "all":
                if status in ["activo", "suspendido"]:
                    query += " AND service_status = %s"
                    params.append(status)
                elif status in ["al_dia", "vencido", "pendiente"]:
                    query += " AND payment_status = %s"
                    params.append(status)
                    
            if search:
                q = f"%{search.strip().lower()}%"
                query += " AND (LOWER(name) LIKE %s OR LOWER(phone) LIKE %s OR LOWER(address) LIKE %s OR LOWER(client_user) LIKE %s)"
                params.extend([q, q, q, q])
                
            query += " ORDER BY created_at DESC;"
            cur.execute(query, params)
            clients = [dict(r) for r in cur.fetchall()]
            
            # Formatear números y obtener cámaras de cada cliente
            for c in clients:
                c["installation_cost"] = float(c["installation_cost"] or 0.0)
                c["installation_paid"] = float(c["installation_paid"] or 0.0)
                c["monthly_fee"] = float(c["monthly_fee"] or 0.0)
                if c.get("created_at"):
                    c["created_at"] = c["created_at"].isoformat()
                if c.get("last_payment_date"):
                    c["last_payment_date"] = c["last_payment_date"].isoformat()
                    
                cur.execute("SELECT * FROM cameras WHERE client_id = %s ORDER BY created_at ASC;", (c["id"],))
                cams = [dict(cam) for cam in cur.fetchall()]
                for cam in cams:
                    if cam.get("created_at"):
                        cam["created_at"] = cam["created_at"].isoformat()
                c["cameras"] = cams
                
            return clients
    finally:
        conn.close()

def get_client(client_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM clients WHERE id = %s;", (client_id,))
            row = cur.fetchone()
            if not row:
                return None
            c = dict(row)
            c["installation_cost"] = float(c["installation_cost"] or 0.0)
            c["installation_paid"] = float(c["installation_paid"] or 0.0)
            c["monthly_fee"] = float(c["monthly_fee"] or 0.0)
            if c.get("created_at"):
                c["created_at"] = c["created_at"].isoformat()
            if c.get("last_payment_date"):
                c["last_payment_date"] = c["last_payment_date"].isoformat()
                
            cur.execute("SELECT * FROM cameras WHERE client_id = %s;", (client_id,))
            c["cameras"] = [dict(cam) for cam in cur.fetchall()]
            return c
    finally:
        conn.close()

def create_client(data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db()
    try:
        with conn.cursor() as cur:
            client_id = f"cli_{uuid.uuid4().hex[:8]}"
            user = data.get("client_user", "").strip() or f"user_{uuid.uuid4().hex[:5]}"
            pwd = data.get("client_pass", "").strip() or f"pass_{uuid.uuid4().hex[:5]}"
            
            # Crear cuenta de usuario asociada
            user_uuid = create_client_user(user, pwd, data.get("name", ""), data.get("email", ""))
            
            inst_cost = float(data.get("installation_cost", 0.0) or 0.0)
            inst_paid = float(data.get("installation_paid", 0.0) or 0.0)
            monthly = float(data.get("monthly_fee", 0.0) or 0.0)
            billing_day = int(data.get("billing_day", 10) or 10)
            
            cur.execute("""
                INSERT INTO clients (
                    id, user_id, name, business_type, phone, email, address, notes,
                    installation_cost, installation_paid, monthly_fee, billing_day,
                    payment_status, service_status, client_user, client_pass, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id;
            """, (
                client_id, user_uuid, data.get("name", "").strip(), data.get("business_type", "Comercio / Local"),
                data.get("phone", "").strip(), data.get("email", "").strip(), data.get("address", "").strip(),
                data.get("notes", "").strip(), inst_cost, inst_paid, monthly, billing_day,
                "al_dia" if inst_paid > 0 else "pendiente", data.get("service_status", "activo"),
                user, pwd
            ))
            
            # Insertar cámaras del cliente
            cameras = data.get("cameras", [])
            for i, cam in enumerate(cameras):
                cam_id = f"cam_{uuid.uuid4().hex[:6]}"
                cur.execute("""
                    INSERT INTO cameras (
                        id, client_id, name, location, ip, port, camera_user,
                        serial_number, safety_code, rtsp_sub, rtsp_main, stream_url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    cam_id, client_id, cam.get("name") or f"Cámara {i+1}", cam.get("location") or "General",
                    cam.get("ip") or "", cam.get("port") or 554, cam.get("user") or "admin",
                    cam.get("serial_number") or "", cam.get("safety_code") or "",
                    cam.get("rtsp") or cam.get("rtsp_sub") or "", cam.get("rtsp_main") or "",
                    cam.get("stream_url") or ""
                ))
                
            # Registrar cobro de instalación inicial si aplica
            if inst_paid > 0:
                cur.execute("""
                    INSERT INTO payments (id, client_id, type, amount, period, method, notes)
                    VALUES (%s, %s, 'instalacion', %s, 'Instalación', 'Efectivo', 'Pago inicial de instalación al dar de alta');
                """, (f"pay_{uuid.uuid4().hex[:6]}", client_id, inst_paid))
                
            logger.info(f"Cliente Supabase registrado: {data.get('name')} ({client_id})")
            return get_client(client_id)
    finally:
        conn.close()

def update_client(client_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor() as cur:
            fields = []
            params = []
            allowed = ["name", "business_type", "phone", "email", "address", "notes", "installation_cost", "installation_paid", "monthly_fee", "billing_day", "service_status", "client_user", "client_pass"]
            for k in allowed:
                if k in data and data[k] is not None:
                    fields.append(f"{k} = %s")
                    if k in ["installation_cost", "installation_paid", "monthly_fee"]:
                        params.append(float(data[k] or 0.0))
                    elif k == "billing_day":
                        params.append(int(data[k] or 10))
                    else:
                        params.append(str(data[k]).strip())
            
            if fields:
                params.append(client_id)
                cur.execute(f"UPDATE clients SET {', '.join(fields)} WHERE id = %s;", params)
                
            # Si cambió contraseña o usuario del cliente, sincronizar usuario en tabla users
            if "client_user" in data or "client_pass" in data:
                cur.execute("SELECT user_id FROM clients WHERE id = %s;", (client_id,))
                r = cur.fetchone()
                if r and r[0]:
                    user_id = r[0]
                    u_fields = []
                    u_params = []
                    if "client_user" in data and data["client_user"]:
                        u_fields.append("username = %s")
                        u_params.append(str(data["client_user"]).strip())
                    if "client_pass" in data and data["client_pass"]:
                        u_fields.append("password_hash = %s")
                        u_params.append(hash_password(str(data["client_pass"]).strip()))
                    if u_fields:
                        u_params.append(user_id)
                        cur.execute(f"UPDATE users SET {', '.join(u_fields)} WHERE id = %s;", u_params)
            
            # Si se enviaron cámaras actualizadas
            if "cameras" in data and isinstance(data["cameras"], list):
                cur.execute("DELETE FROM cameras WHERE client_id = %s;", (client_id,))
                for i, cam in enumerate(data["cameras"]):
                    cam_id = cam.get("id") or f"cam_{uuid.uuid4().hex[:6]}"
                    cur.execute("""
                        INSERT INTO cameras (
                            id, client_id, name, location, ip, port, camera_user,
                            serial_number, safety_code, rtsp_sub, rtsp_main, stream_url
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        cam_id, client_id, cam.get("name") or f"Cámara {i+1}", cam.get("location") or "General",
                        cam.get("ip") or "", cam.get("port") or 554, cam.get("user") or "admin",
                        cam.get("serial_number") or "", cam.get("safety_code") or "",
                        cam.get("rtsp") or cam.get("rtsp_sub") or "", cam.get("rtsp_main") or "",
                        cam.get("stream_url") or ""
                    ))
            
            return get_client(client_id)
    finally:
        conn.close()

def delete_client(client_id: str) -> bool:
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM clients WHERE id = %s;", (client_id,))
            return cur.rowcount > 0
    finally:
        conn.close()

def toggle_client_status(client_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE clients 
                SET service_status = CASE WHEN service_status = 'activo' THEN 'suspendido' ELSE 'activo' END
                WHERE id = %s
                RETURNING service_status;
            """, (client_id,))
            row = cur.fetchone()
            if not row:
                return None
            return get_client(client_id)
    finally:
        conn.close()

def record_client_payment(client_id: str, payment_type: str, amount: float, method: str = "Transferencia", period: str = "", notes: str = "") -> Optional[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor() as cur:
            now_period = period or datetime.datetime.now().strftime("%Y-%m")
            pay_id = f"pay_{uuid.uuid4().hex[:6]}"
            cur.execute("""
                INSERT INTO payments (id, client_id, type, amount, date, period, method, notes)
                VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s);
            """, (pay_id, client_id, payment_type, float(amount), now_period, method, notes))
            
            if payment_type == "instalacion":
                cur.execute("""
                    UPDATE clients 
                    SET installation_paid = installation_paid + %s, last_payment_date = NOW()
                    WHERE id = %s;
                """, (float(amount), client_id))
            else:
                cur.execute("""
                    UPDATE clients 
                    SET payment_status = 'al_dia', last_payment_date = NOW()
                    WHERE id = %s;
                """, (client_id,))
                
            return get_client(client_id)
    finally:
        conn.close()

# ==========================================
# VENTAS DE SOFTWARE EN SUPABASE
# ==========================================
def get_software_sales(search: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = "SELECT * FROM software_sales WHERE 1=1"
            params = []
            if status and status != "all":
                query += " AND payment_status = %s"
                params.append(status)
            if search:
                q = f"%{search.strip().lower()}%"
                query += " AND (LOWER(buyer_name) LIKE %s OR LOWER(buyer_company) LIKE %s OR LOWER(license_plan) LIKE %s OR LOWER(license_key) LIKE %s)"
                params.extend([q, q, q, q])
            query += " ORDER BY date DESC;"
            cur.execute(query, params)
            sales = [dict(r) for r in cur.fetchall()]
            for s in sales:
                s["price"] = float(s["price"] or 0.0)
                s["amount_paid"] = float(s["amount_paid"] or 0.0)
                if s.get("date"):
                    s["date"] = s["date"].isoformat()
            return sales
    finally:
        conn.close()

def create_software_sale(data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db()
    try:
        with conn.cursor() as cur:
            sale_id = f"sale_sw_{uuid.uuid4().hex[:6]}"
            key_raw = uuid.uuid4().hex[:8].upper()
            default_key = f"BADD-{data.get('license_plan', 'PRO')[:3].upper()}-{key_raw[:4]}-{key_raw[4:]}"
            license_key = data.get("license_key", "").strip() or default_key
            price = float(data.get("price", 0.0) or 0.0)
            amount_paid = float(data.get("amount_paid", price if data.get("payment_status") == "pagado" else 0.0) or 0.0)
            
            cur.execute("""
                INSERT INTO software_sales (
                    id, buyer_name, buyer_company, buyer_contact, buyer_email,
                    license_plan, licenses_count, price, amount_paid, currency,
                    payment_model, payment_method, payment_status, license_key, date, notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
                RETURNING id;
            """, (
                sale_id, data.get("buyer_name", "").strip(), data.get("buyer_company", "").strip(),
                data.get("buyer_contact", "").strip(), data.get("buyer_email", "").strip(),
                data.get("license_plan", "Licencia Servidor Pro"), int(data.get("licenses_count", 1) or 1),
                price, amount_paid, data.get("currency", "ARS"),
                data.get("payment_model", "Pago Único Perpetuo"), data.get("payment_method", "Transferencia Bancaria"),
                data.get("payment_status", "pagado"), license_key, data.get("notes", "").strip()
            ))
            
            return {
                "id": sale_id,
                "buyer_name": data.get("buyer_name"),
                "license_key": license_key,
                "price": price,
                "amount_paid": amount_paid,
                "payment_status": data.get("payment_status", "pagado")
            }
    finally:
        conn.close()

def get_software_sale(sale_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM software_sales WHERE id = %s;", (sale_id,))
            row = cur.fetchone()
            if not row:
                return None
            s = dict(row)
            s["price"] = float(s["price"] or 0.0)
            s["amount_paid"] = float(s["amount_paid"] or 0.0)
            if s.get("date"):
                s["date"] = s["date"].isoformat()
            return s
    finally:
        conn.close()

def update_software_sale(sale_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor() as cur:
            fields = []
            params = []
            allowed = ["buyer_name", "buyer_company", "buyer_contact", "buyer_email", "license_plan", "licenses_count", "price", "amount_paid", "currency", "payment_model", "payment_method", "payment_status", "license_key", "notes"]
            for k in allowed:
                if k in data and data[k] is not None:
                    fields.append(f"{k} = %s")
                    if k in ["price", "amount_paid"]:
                        params.append(float(data[k] or 0.0))
                    elif k == "licenses_count":
                        params.append(int(data[k] or 1))
                    else:
                        params.append(str(data[k]).strip())
            if fields:
                params.append(sale_id)
                cur.execute(f"UPDATE software_sales SET {', '.join(fields)} WHERE id = %s;", params)
            return get_software_sale(sale_id)
    finally:
        conn.close()

def delete_software_sale(sale_id: str) -> bool:
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM software_sales WHERE id = %s;", (sale_id,))
            return cur.rowcount > 0
    finally:
        conn.close()

def record_software_payment(sale_id: str, amount: float, method: str = "Transferencia Bancaria", notes: str = "") -> Optional[Dict[str, Any]]:
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT price, amount_paid FROM software_sales WHERE id = %s;", (sale_id,))
            row = cur.fetchone()
            if not row:
                return None
            new_paid = float(row["amount_paid"] or 0.0) + float(amount)
            new_status = "pagado" if new_paid >= float(row["price"] or 0.0) else "seña"
            cur.execute("""
                UPDATE software_sales 
                SET amount_paid = %s, payment_status = %s, payment_method = %s
                WHERE id = %s;
            """, (new_paid, new_status, method, sale_id))
            return {"id": sale_id, "amount_paid": new_paid, "status": new_status}
    finally:
        conn.close()

# ==========================================
# MÉTRICAS Y GRÁFICOS REALES DESDE SUPABASE
# ==========================================
def get_dashboard_stats() -> Dict[str, Any]:
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            now = datetime.datetime.now()
            current_period = now.strftime("%Y-%m")
            current_month_name = now.strftime("%B %Y")
            
            # Conteo de clientes
            cur.execute("SELECT count(*), count(*) FILTER (WHERE service_status = 'activo'), count(*) FILTER (WHERE service_status = 'suspendido') FROM clients;")
            r_cli = cur.fetchone()
            total_clients = r_cli[0] or 0
            active_clients = r_cli[1] or 0
            suspended_clients = r_cli[2] or 0
            
            # Cámaras
            cur.execute("SELECT count(*) FROM cameras;")
            total_cameras = cur.fetchone()[0] or 0
            
            # MRR
            cur.execute("SELECT COALESCE(SUM(monthly_fee), 0) FROM clients WHERE service_status = 'activo';")
            mrr = float(cur.fetchone()[0] or 0.0)
            
            # Pagos
            cur.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE type = 'instalacion';")
            total_inst_rev = float(cur.fetchone()[0] or 0.0)
            
            cur.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE type = 'cuota';")
            total_monthly_rev = float(cur.fetchone()[0] or 0.0)
            
            cur.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE type = 'cuota' AND period = %s;", (current_period,))
            current_month_collected = float(cur.fetchone()[0] or 0.0)
            
            # Software
            cur.execute("""
                SELECT 
                    COALESCE(SUM(amount_paid), 0), 
                    COALESCE(SUM(price), 0), 
                    count(*), 
                    COALESCE(SUM(licenses_count), 0),
                    count(*) FILTER (WHERE payment_status IN ('pagado', 'seña'))
                FROM software_sales;
            """)
            r_sw = cur.fetchone()
            total_sw_rev = float(r_sw[0] or 0.0)
            total_sw_billed = float(r_sw[1] or 0.0)
            sw_sales_count = r_sw[2] or 0
            sw_licenses_count = r_sw[3] or 0
            active_sw_clients = r_sw[4] or 0
            
            # Alertas
            cur.execute("SELECT count(*) FILTER (WHERE payment_status = 'al_dia'), count(*) FILTER (WHERE payment_status = 'vencido'), count(*) FILTER (WHERE payment_status = 'pendiente') FROM clients;")
            r_status = cur.fetchone()
            clients_al_dia = r_status[0] or 0
            clients_vencidos = r_status[1] or 0
            clients_pendientes = r_status[2] or 0
            
            progress_pct = round((current_month_collected / mrr * 100), 1) if mrr > 0 else 0.0
            total_business_rev = total_inst_rev + total_monthly_rev + total_sw_rev
            
            return {
                "total_clients": total_clients,
                "active_clients": active_clients,
                "suspended_clients": suspended_clients,
                "total_cameras": total_cameras,
                "mrr": round(mrr, 2),
                "total_installation_revenue": round(total_inst_rev, 2),
                "total_monthly_revenue": round(total_monthly_rev, 2),
                "current_month_collected": round(current_month_collected, 2),
                "current_month_expected": round(mrr, 2),
                "collection_progress_pct": min(progress_pct, 100.0),
                "clients_al_dia": clients_al_dia,
                "clients_vencidos": clients_vencidos,
                "clients_pendientes": clients_pendientes,
                "total_software_revenue": round(total_sw_rev, 2),
                "total_software_billed": round(total_sw_billed, 2),
                "total_software_sales_count": sw_sales_count,
                "total_software_licenses": sw_licenses_count,
                "active_software_clients": active_sw_clients,
                "total_business_revenue": round(total_business_rev, 2),
                "current_period": current_period,
                "current_month_name": current_month_name
            }
    finally:
        conn.close()

def get_balance_charts() -> Dict[str, Any]:
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            months = ["May 2026", "Jun 2026", "Jul 2026", "Ago 2026", "Sep 2026", "Oct 2026"]
            
            stats = get_dashboard_stats()
            tot_sub = stats["total_monthly_revenue"]
            tot_inst = stats["total_installation_revenue"]
            tot_sw = stats["total_software_revenue"]
            tot_all = tot_sub + tot_inst + tot_sw or 1.0
            
            subscriptions_series = [0.0, 0.0, 0.0, 0.0, 0.0, tot_sub]
            installations_series = [0.0, 0.0, 0.0, 0.0, 0.0, tot_inst]
            software_series = [0.0, 0.0, 0.0, 0.0, 0.0, tot_sw]
            total_monthly_flow = [s + i + sw for s, i, sw in zip(subscriptions_series, installations_series, software_series)]
            
            composition = {
                "labels": ["Abonos Mensuales Cámaras", "Instalaciones & Hardware", "Venta de Software & Licencias"],
                "values": [round(tot_sub, 2), round(tot_inst, 2), round(tot_sw, 2)],
                "percentages": [
                    round((tot_sub / tot_all) * 100, 1),
                    round((tot_inst / tot_all) * 100, 1),
                    round((tot_sw / tot_all) * 100, 1)
                ]
            }
            
            # Movimientos reales desde payments
            cur.execute("""
                SELECT p.date, p.type, p.amount, p.method, c.name as client_name
                FROM payments p
                JOIN clients c ON p.client_id = c.id
                ORDER BY p.date DESC
                LIMIT 10;
            """)
            rows = cur.fetchall()
            recent_transactions = []
            for r in rows:
                recent_transactions.append({
                    "date": r["date"].strftime("%Y-%m-%d") if r["date"] else "",
                    "concept": f"Cobro de {r['type']}",
                    "entity": r["client_name"],
                    "category": "Abono" if r["type"] == "cuota" else "Instalación",
                    "amount": float(r["amount"]),
                    "status": "Completado"
                })
                
            return {
                "months": months,
                "subscriptions": subscriptions_series,
                "installations": installations_series,
                "software": software_series,
                "total_monthly_flow": total_monthly_flow,
                "composition": composition,
                "recent_transactions": recent_transactions
            }
    finally:
        conn.close()

# ==========================================
# GESTIÓN DE CÁMARAS Y STREAMING SUPABASE
# ==========================================
def get_cameras_for_user(user: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Retorna las cámaras correspondientes según el rol del usuario (Admin ve todas, Cliente solo las suyas)."""
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            role = user.get("role", "client")
            if role == "admin":
                cur.execute("""
                    SELECT c.*, cl.name as client_name 
                    FROM cameras c 
                    LEFT JOIN clients cl ON c.client_id = cl.id
                    ORDER BY c.created_at ASC;
                """)
            else:
                user_id = str(user.get("sub") or user.get("id") or "")
                username = str(user.get("username") or "")
                cur.execute("""
                    SELECT c.*, cl.name as client_name 
                    FROM cameras c 
                    JOIN clients cl ON c.client_id = cl.id
                    WHERE (cl.user_id::text = %s OR cl.client_user = %s)
                    ORDER BY c.created_at ASC;
                """, (user_id, username))
            rows = cur.fetchall()
            cams = []
            for r in rows:
                c = dict(r)
                if c.get("created_at"):
                    c["created_at"] = c["created_at"].isoformat()
                cams.append(c)
            return cams
    finally:
        conn.close()

def add_camera_supabase(camera_data: Dict[str, Any], client_id: Optional[str] = None) -> Dict[str, Any]:
    """Registra una nueva cámara vinculada a un cliente en Supabase."""
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cam_id = f"cam_{uuid.uuid4().hex[:6]}"
            cur.execute("""
                INSERT INTO cameras (
                    id, client_id, name, location, ip, port, camera_user,
                    serial_number, safety_code, rtsp_sub, rtsp_main, stream_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                cam_id, client_id,
                camera_data.get("name") or "Cámara IP",
                camera_data.get("location") or "General",
                camera_data.get("ip") or "",
                camera_data.get("port") or 554,
                camera_data.get("user") or "admin",
                camera_data.get("serial_number") or "",
                camera_data.get("safety_code") or "",
                camera_data.get("rtsp_sub") or camera_data.get("rtsp") or "",
                camera_data.get("rtsp_main") or "",
                camera_data.get("stream_url") or ""
            ))
            return {
                "id": cam_id,
                "name": camera_data.get("name"),
                "location": camera_data.get("location"),
                "serial_number": camera_data.get("serial_number"),
                "safety_code": camera_data.get("safety_code")
            }
    finally:
        conn.close()

def delete_camera_supabase(cam_id: str) -> bool:
    """Elimina una cámara de Supabase."""
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cameras WHERE id = %s;", (cam_id,))
            return cur.rowcount > 0
    finally:
        conn.close()

