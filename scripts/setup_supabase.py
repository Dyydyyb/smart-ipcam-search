import psycopg2
import urllib.parse
import bcrypt
import sys

# Supabase Credentials
PROJECT_ID = "foghkrwrxqoqrkvdipnn"
PASSWORD_RAW = "1569957772Db!"
PASSWORD_ENC = urllib.parse.quote_plus(PASSWORD_RAW)
HOST = f"db.{PROJECT_ID}.supabase.co"
PORT = 5432
DATABASE = "postgres"
DB_URL = f"postgresql://postgres:{PASSWORD_ENC}@{HOST}:{PORT}/{DATABASE}?sslmode=require"

SCHEMA_SQL = """
-- Habilitar extensión pgcrypto para UUIDs
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. TABLA DE USUARIOS (AUTENTICACIÓN CON ROLES)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150),
    role VARCHAR(20) NOT NULL DEFAULT 'client', -- 'admin' (Dylan) o 'client' (cliente)
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. TABLA DE CLIENTES (CRM BADDGROUP)
CREATE TABLE IF NOT EXISTS clients (
    id VARCHAR(50) PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(200) NOT NULL,
    business_type VARCHAR(100) DEFAULT 'Comercio / Local',
    phone VARCHAR(50),
    email VARCHAR(150),
    address TEXT,
    notes TEXT,
    installation_cost NUMERIC(12, 2) DEFAULT 0.0,
    installation_paid NUMERIC(12, 2) DEFAULT 0.0,
    monthly_fee NUMERIC(12, 2) DEFAULT 0.0,
    billing_day INT DEFAULT 10,
    payment_status VARCHAR(30) DEFAULT 'pendiente',
    service_status VARCHAR(30) DEFAULT 'activo',
    client_user VARCHAR(80),
    client_pass VARCHAR(80),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_payment_date TIMESTAMPTZ
);

-- 3. TABLA DE CÁMARAS Y ENLACES RTSP / IMOU
CREATE TABLE IF NOT EXISTS cameras (
    id VARCHAR(50) PRIMARY KEY,
    client_id VARCHAR(50) REFERENCES clients(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(150),
    ip VARCHAR(100),
    port INT DEFAULT 554,
    camera_user VARCHAR(80) DEFAULT 'admin',
    serial_number VARCHAR(100), -- Para IMOU / Dahua P2P Cloud
    safety_code VARCHAR(100),   -- Clave de seguridad (ej: L27EA4F3)
    rtsp_sub TEXT,
    rtsp_main TEXT,
    stream_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. TABLA DE PAGOS Y COBRANZAS
CREATE TABLE IF NOT EXISTS payments (
    id VARCHAR(50) PRIMARY KEY,
    client_id VARCHAR(50) REFERENCES clients(id) ON DELETE CASCADE,
    type VARCHAR(30) NOT NULL, -- 'cuota' o 'instalacion'
    amount NUMERIC(12, 2) NOT NULL,
    date TIMESTAMPTZ DEFAULT NOW(),
    period VARCHAR(20),        -- '2026-10'
    method VARCHAR(50) DEFAULT 'Transferencia',
    notes TEXT
);

-- 5. TABLA DE VENTAS DE SOFTWARE Y LICENCIAS
CREATE TABLE IF NOT EXISTS software_sales (
    id VARCHAR(50) PRIMARY KEY,
    buyer_name VARCHAR(150) NOT NULL,
    buyer_company VARCHAR(150),
    buyer_contact VARCHAR(80),
    buyer_email VARCHAR(150),
    license_plan VARCHAR(100) NOT NULL,
    licenses_count INT DEFAULT 1,
    price NUMERIC(12, 2) NOT NULL,
    amount_paid NUMERIC(12, 2) DEFAULT 0.0,
    currency VARCHAR(10) DEFAULT 'ARS',
    payment_model VARCHAR(50) DEFAULT 'Pago Único Perpetuo',
    payment_method VARCHAR(50) DEFAULT 'Transferencia Bancaria',
    payment_status VARCHAR(30) DEFAULT 'pagado',
    license_key VARCHAR(100) UNIQUE NOT NULL,
    date TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT
);

-- 6. TABLA DE EVENTOS DE SEGURIDAD CON IA
CREATE TABLE IF NOT EXISTS security_events (
    id VARCHAR(50) PRIMARY KEY,
    camera_id VARCHAR(50) REFERENCES cameras(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    event_type VARCHAR(50) NOT NULL,
    confidence NUMERIC(4, 2),
    description TEXT,
    snapshot_path TEXT,
    clip_path TEXT
);

-- INDICES PARA RENDIMIENTO ALTO
CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(payment_status, service_status);
CREATE INDEX IF NOT EXISTS idx_cameras_client ON cameras(client_id);
CREATE INDEX IF NOT EXISTS idx_payments_client ON payments(client_id, period);
CREATE INDEX IF NOT EXISTS idx_security_events_cam ON security_events(camera_id, timestamp DESC);
"""

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def main():
    print(f"Conectando a Supabase PostgreSQL ({HOST})...")
    conn = psycopg2.connect(DB_URL, connect_timeout=10)
    conn.autocommit = True
    cur = conn.cursor()

    print("Creando tablas de producción (users, clients, cameras, payments, software_sales, security_events)...")
    cur.execute(SCHEMA_SQL)
    print("[OK] Tablas creadas exitosamente en Supabase.")

    # Crear o actualizar usuario SuperAdmin Dylan
    admin_user = "dylan"
    admin_email = "dylan@baddgroup.com"
    admin_pass = "Dylanssj2.camaras"
    admin_pass_hash = hash_password(admin_pass)

    cur.execute("SELECT id FROM users WHERE username = %s;", (admin_user,))
    row = cur.fetchone()
    if row:
        cur.execute("""
            UPDATE users 
            SET password_hash = %s, role = 'admin', is_active = TRUE 
            WHERE username = %s;
        """, (admin_pass_hash, admin_user))
        print(f"[OK] Usuario Administrador '{admin_user}' actualizado.")
    else:
        cur.execute("""
            INSERT INTO users (username, email, password_hash, full_name, role, is_active)
            VALUES (%s, %s, %s, %s, 'admin', TRUE);
        """, (admin_user, admin_email, admin_pass_hash, "Dylan - Baddgroup"))
        print(f"[OK] Usuario Administrador '{admin_user}' creado con éxito.")

    # Verificación de tablas limpias (sin mock data)
    cur.execute("SELECT count(*) FROM clients;")
    n_clients = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM cameras;")
    n_cams = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM software_sales;")
    n_sw = cur.fetchone()[0]
    print(f"[INFO ESTADO BASE LIMPIA]: Clientes: {n_clients} | Cámaras: {n_cams} | Ventas Software: {n_sw}")

    cur.close()
    conn.close()
    print("\n¡Configuración de Supabase completada al 100%!")

if __name__ == "__main__":
    main()
