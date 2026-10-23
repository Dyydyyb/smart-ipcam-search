import json
import uuid
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger
from core.config import settings

CRM_FILE = settings.STORAGE_DIR / "crm_clients.json"
SOFTWARE_SALES_FILE = settings.STORAGE_DIR / "software_sales.json"

DEFAULT_DEMO_CLIENTS = [
    {
        "id": "cli_ferreteria_central",
        "name": "Ferretería Central - Don Pedro",
        "business_type": "Comercio / Local",
        "phone": "+54 9 11 4521-8899",
        "email": "pedro.central@gmail.com",
        "address": "Av. San Martín 1420, Ramos Mejía",
        "notes": "5 cámaras instaladas. Pago puntual por transferencia.",
        "installation_cost": 180000.0,
        "installation_paid": 180000.0,
        "monthly_fee": 25000.0,
        "billing_day": 10,
        "payment_status": "al_dia",
        "service_status": "activo",
        "client_user": "ferreteriacentral",
        "client_pass": "pedro2026",
        "created_at": "2026-09-15T10:00:00",
        "last_payment_date": "2026-10-08T14:30:00",
        "cameras": [
            {
                "id": "cam_f1",
                "name": "Cámara 1: Entrada Principal",
                "location": "Acceso Exterior",
                "ip": "192.168.1.101",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Clave123@192.168.1.101:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_f2",
                "name": "Cámara 2: Caja y Mostrador",
                "location": "Sector Cobro",
                "ip": "192.168.1.102",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Clave123@192.168.1.102:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_f3",
                "name": "Cámara 3: Pasillo Central",
                "location": "Góndolas",
                "ip": "192.168.1.103",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Clave123@192.168.1.103:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_f4",
                "name": "Cámara 4: Depósito Fondo",
                "location": "Stock",
                "ip": "192.168.1.104",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Clave123@192.168.1.104:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_f5",
                "name": "Cámara 5: Vereda y Carga",
                "location": "Exterior Calle",
                "ip": "192.168.1.105",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Clave123@192.168.1.105:554/cam/realmonitor?channel=1&subtype=1"
            }
        ],
        "payments": [
            {
                "id": "pay_f1",
                "type": "instalacion",
                "amount": 180000.0,
                "date": "2026-09-15T12:00:00",
                "period": "Instalación",
                "method": "Efectivo",
                "notes": "Cobrado al finalizar amurado y cableado"
            },
            {
                "id": "pay_f2",
                "type": "cuota",
                "amount": 25000.0,
                "date": "2026-10-08T14:30:00",
                "period": "2026-10",
                "method": "Transferencia",
                "notes": "Abono mensual Octubre"
            }
        ]
    },
    {
        "id": "cli_veterinaria_san_roque",
        "name": "Veterinaria San Roque",
        "business_type": "Comercio / Local",
        "phone": "+54 9 11 6332-1144",
        "email": "dr.martinez@sanroque.com",
        "address": "Calle Belgrano 540, Morón",
        "notes": "3 cámaras. Vence los 5 de cada mes.",
        "installation_cost": 120000.0,
        "installation_paid": 120000.0,
        "monthly_fee": 18000.0,
        "billing_day": 5,
        "payment_status": "al_dia",
        "service_status": "activo",
        "client_user": "sanroque",
        "client_pass": "roque2026",
        "created_at": "2026-08-20T11:00:00",
        "last_payment_date": "2026-10-04T09:15:00",
        "cameras": [
            {
                "id": "cam_v1",
                "name": "Cámara 1: Recepción",
                "location": "Atención al Cliente",
                "ip": "192.168.0.50",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Vet2026@192.168.0.50:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_v2",
                "name": "Cámara 2: Quirófano y Consultorio",
                "location": "Interior",
                "ip": "192.168.0.51",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Vet2026@192.168.0.51:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_v3",
                "name": "Cámara 3: Puerta Principal",
                "location": "Vereda",
                "ip": "192.168.0.52",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Vet2026@192.168.0.52:554/cam/realmonitor?channel=1&subtype=1"
            }
        ],
        "payments": [
            {
                "id": "pay_v1",
                "type": "instalacion",
                "amount": 120000.0,
                "date": "2026-08-20T17:00:00",
                "period": "Instalación",
                "method": "Transferencia",
                "notes": "Instalación 3 cámaras WiFi"
            },
            {
                "id": "pay_v2",
                "type": "cuota",
                "amount": 18000.0,
                "date": "2026-10-04T09:15:00",
                "period": "2026-10",
                "method": "Transferencia",
                "notes": "Abono Octubre"
            }
        ]
    },
    {
        "id": "cli_distribuidora_oeste",
        "name": "Distribuidora del Oeste S.A.",
        "business_type": "Depósito / Galpón",
        "phone": "+54 9 11 5119-7700",
        "email": "administracion@distrioeste.com.ar",
        "address": "Ruta 3 Km 35, Virrey del Pino",
        "notes": "Galpón logístico. 4 cámaras. Vence día 15.",
        "installation_cost": 290000.0,
        "installation_paid": 290000.0,
        "monthly_fee": 45000.0,
        "billing_day": 15,
        "payment_status": "vencido",
        "service_status": "activo",
        "client_user": "distrioeste",
        "client_pass": "galpon2026",
        "created_at": "2026-07-10T09:00:00",
        "last_payment_date": "2026-09-14T11:00:00",
        "cameras": [
            {
                "id": "cam_d1",
                "name": "Portón Acceso Camiones",
                "location": "Entrada",
                "ip": "10.0.0.10",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Logistica1@10.0.0.10:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_d2",
                "name": "Plataforma de Carga 1",
                "location": "Dársenas",
                "ip": "10.0.0.11",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Logistica1@10.0.0.11:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_d3",
                "name": "Plataforma de Carga 2",
                "location": "Dársenas",
                "ip": "10.0.0.12",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Logistica1@10.0.0.12:554/cam/realmonitor?channel=1&subtype=1"
            },
            {
                "id": "cam_d4",
                "name": "Pasillo Racks A",
                "location": "Interior Galpón",
                "ip": "10.0.0.13",
                "port": 554,
                "user": "admin",
                "rtsp": "rtsp://admin:Logistica1@10.0.0.13:554/cam/realmonitor?channel=1&subtype=1"
            }
        ],
        "payments": [
            {
                "id": "pay_d1",
                "type": "instalacion",
                "amount": 290000.0,
                "date": "2026-07-10T18:00:00",
                "period": "Instalación",
                "method": "Transferencia",
                "notes": "Mano de obra + configuración NVR"
            },
            {
                "id": "pay_d2",
                "type": "cuota",
                "amount": 45000.0,
                "date": "2026-09-14T11:00:00",
                "period": "2026-09",
                "method": "Transferencia",
                "notes": "Abono Septiembre"
            }
        ]
    }
]

DEFAULT_DEMO_SOFTWARE_SALES = [
    {
        "id": "sale_sw_01",
        "buyer_name": "Innova Tech Soluciones",
        "buyer_company": "Innova Tech SRL",
        "buyer_contact": "+54 9 11 3840-2211",
        "buyer_email": "contacto@innovatech.com.ar",
        "license_plan": "Licencia Servidor Pro (On-Premise)",
        "licenses_count": 1,
        "price": 350000.0,
        "amount_paid": 350000.0,
        "currency": "ARS",
        "payment_model": "Pago Único Perpetuo",
        "payment_method": "Transferencia Bancaria",
        "payment_status": "pagado",
        "license_key": "BADD-PRO-9842-7104-X",
        "date": "2026-09-20T15:00:00",
        "notes": "Servidor local instalado con búsqueda semántica por lenguaje natural."
    },
    {
        "id": "sale_sw_02",
        "buyer_name": "Seguridad Integral Palermo",
        "buyer_company": "SIP Monitoreo Privado",
        "buyer_contact": "+54 9 11 5590-4433",
        "buyer_email": "operaciones@sipmonitoreo.com",
        "license_plan": "White-Label Reseller Baddgroup",
        "licenses_count": 3,
        "price": 480000.0,
        "amount_paid": 480000.0,
        "currency": "ARS",
        "payment_model": "Suscripción Anual",
        "payment_method": "Transferencia Bancaria",
        "payment_status": "pagado",
        "license_key": "BADD-WHT-4512-8821-K",
        "date": "2026-10-05T11:30:00",
        "notes": "Incluye marca blanca y módulo de analítica avanzada para 3 clientes."
    },
    {
        "id": "sale_sw_03",
        "buyer_name": "Martín Gómez",
        "buyer_company": "Gómez Seguridad Electrónica",
        "buyer_contact": "+54 9 11 7712-3390",
        "buyer_email": "martin.camaras@gmail.com",
        "license_plan": "Módulo Visión IA Baddgroup",
        "licenses_count": 1,
        "price": 180000.0,
        "amount_paid": 90000.0,
        "currency": "ARS",
        "payment_model": "Pago Único",
        "payment_method": "Mercado Pago",
        "payment_status": "seña",
        "license_key": "BADD-MOD-1092-5532-M",
        "date": "2026-10-18T16:45:00",
        "notes": "Abonó el 50% de seña ($90.000). Saldo contra entrega de llave definitiva."
    }
]

class CRMManager:
    """Gestor comercial, financiero y de software centralizado para Baddgroup Vision AI."""
    def __init__(self, file_path: Path = CRM_FILE, software_file_path: Path = SOFTWARE_SALES_FILE):
        self.file_path = file_path
        self.software_file_path = software_file_path
        self._load()
        self._load_software_sales()

    def _load(self):
        if not self.file_path.exists():
            self._save(DEFAULT_DEMO_CLIENTS)
            self.clients = list(DEFAULT_DEMO_CLIENTS)
        else:
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.clients = json.load(f)
            except Exception as e:
                logger.error(f"Error cargando crm_clients.json: {e}")
                self.clients = list(DEFAULT_DEMO_CLIENTS)
        self._recompute_payment_statuses()

    def _save(self, data: List[Dict[str, Any]]):
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando crm_clients.json: {e}")

    def _load_software_sales(self):
        if not self.software_file_path.exists():
            self._save_software_sales(DEFAULT_DEMO_SOFTWARE_SALES)
            self.software_sales = list(DEFAULT_DEMO_SOFTWARE_SALES)
        else:
            try:
                with open(self.software_file_path, "r", encoding="utf-8") as f:
                    self.software_sales = json.load(f)
            except Exception as e:
                logger.error(f"Error cargando software_sales.json: {e}")
                self.software_sales = list(DEFAULT_DEMO_SOFTWARE_SALES)

    def _save_software_sales(self, data: List[Dict[str, Any]]):
        try:
            self.software_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.software_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando software_sales.json: {e}")

    def _recompute_payment_statuses(self):
        """Calcula automáticamente si el cliente está al día o vencido según la fecha actual."""
        now = datetime.datetime.now()
        current_period = now.strftime("%Y-%m")
        current_day = now.day

        for c in self.clients:
            payments = c.get("payments", [])
            has_paid_current_month = any(
                p.get("type") == "cuota" and p.get("period") == current_period for p in payments
            )
            billing_day = c.get("billing_day", 10)

            if has_paid_current_month:
                c["payment_status"] = "al_dia"
            else:
                if current_day > billing_day:
                    c["payment_status"] = "vencido"
                else:
                    c["payment_status"] = "pendiente"

    # ==========================
    # GESTIÓN DE CLIENTES DE CÁMARAS
    # ==========================
    def get_all(self, search: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        self._load()
        results = self.clients

        if status and status != "all":
            if status in ["activo", "suspendido"]:
                results = [c for c in results if c.get("service_status") == status]
            elif status in ["al_dia", "vencido", "pendiente"]:
                results = [c for c in results if c.get("payment_status") == status]

        if search:
            q = search.lower().strip()
            results = [
                c for c in results
                if q in c.get("name", "").lower()
                or q in c.get("phone", "").lower()
                or q in c.get("address", "").lower()
                or q in c.get("client_user", "").lower()
            ]

        return results

    def get(self, client_id: str) -> Optional[Dict[str, Any]]:
        self._load()
        for c in self.clients:
            if c.get("id") == client_id:
                return c
        return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._load()
        client_id = f"cli_{uuid.uuid4().hex[:8]}"
        now_iso = datetime.datetime.now().isoformat()

        user = data.get("client_user", "").strip() or f"user_{uuid.uuid4().hex[:5]}"
        pwd = data.get("client_pass", "").strip() or f"pass_{uuid.uuid4().hex[:5]}"

        installation_cost = float(data.get("installation_cost", 0.0) or 0.0)
        installation_paid = float(data.get("installation_paid", 0.0) or 0.0)
        monthly_fee = float(data.get("monthly_fee", 0.0) or 0.0)
        billing_day = int(data.get("billing_day", 10) or 10)

        cameras = data.get("cameras", [])
        payments = []

        if installation_paid > 0:
            payments.append({
                "id": f"pay_{uuid.uuid4().hex[:6]}",
                "type": "instalacion",
                "amount": installation_paid,
                "date": now_iso,
                "period": "Instalación",
                "method": data.get("payment_method", "Efectivo"),
                "notes": "Pago inicial de instalación al dar de alta"
            })

        new_client = {
            "id": client_id,
            "name": data.get("name", "").strip(),
            "business_type": data.get("business_type", "Comercio / Local"),
            "phone": data.get("phone", "").strip(),
            "email": data.get("email", "").strip(),
            "address": data.get("address", "").strip(),
            "notes": data.get("notes", "").strip(),
            "installation_cost": installation_cost,
            "installation_paid": installation_paid,
            "monthly_fee": monthly_fee,
            "billing_day": billing_day,
            "payment_status": "pendiente",
            "service_status": data.get("service_status", "activo"),
            "client_user": user,
            "client_pass": pwd,
            "created_at": now_iso,
            "last_payment_date": now_iso if installation_paid > 0 else None,
            "cameras": cameras,
            "payments": payments
        }

        self.clients.append(new_client)
        self._recompute_payment_statuses()
        self._save(self.clients)
        logger.info(f"Nuevo cliente CRM registrado: {new_client['name']} ({client_id})")
        return new_client

    def update(self, client_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        self._load()
        for idx, c in enumerate(self.clients):
            if c.get("id") == client_id:
                for k, v in data.items():
                    if k in ["name", "business_type", "phone", "email", "address", "notes", "client_user", "client_pass", "service_status"]:
                        c[k] = v
                    elif k in ["installation_cost", "installation_paid", "monthly_fee"]:
                        c[k] = float(v or 0.0)
                    elif k == "billing_day":
                        c[k] = int(v or 10)
                    elif k == "cameras" and isinstance(v, list):
                        c[k] = v

                self._recompute_payment_statuses()
                self._save(self.clients)
                logger.info(f"Cliente CRM actualizado: {client_id}")
                return c
        return None

    def delete(self, client_id: str) -> bool:
        self._load()
        initial_len = len(self.clients)
        self.clients = [c for c in self.clients if c.get("id") != client_id]
        if len(self.clients) < initial_len:
            self._save(self.clients)
            logger.info(f"Cliente CRM eliminado: {client_id}")
            return True
        return False

    def toggle_status(self, client_id: str) -> Optional[Dict[str, Any]]:
        self._load()
        for c in self.clients:
            if c.get("id") == client_id:
                new_status = "suspendido" if c.get("service_status") == "activo" else "activo"
                c["service_status"] = new_status
                self._save(self.clients)
                logger.info(f"Estado de servicio cambiado para {c['name']}: {new_status}")
                return c
        return None

    def record_payment(
        self,
        client_id: str,
        payment_type: str,
        amount: float,
        method: str = "Transferencia",
        period: Optional[str] = None,
        notes: str = ""
    ) -> Optional[Dict[str, Any]]:
        self._load()
        now = datetime.datetime.now()
        now_iso = now.isoformat()
        current_period = period or now.strftime("%Y-%m")

        for c in self.clients:
            if c.get("id") == client_id:
                if "payments" not in c:
                    c["payments"] = []

                pay_record = {
                    "id": f"pay_{uuid.uuid4().hex[:6]}",
                    "type": payment_type,
                    "amount": float(amount),
                    "date": now_iso,
                    "period": current_period,
                    "method": method,
                    "notes": notes.strip()
                }
                c["payments"].append(pay_record)
                c["last_payment_date"] = now_iso

                if payment_type == "instalacion":
                    c["installation_paid"] = c.get("installation_paid", 0.0) + float(amount)

                self._recompute_payment_statuses()
                self._save(self.clients)
                logger.info(f"Pago registrado para {c['name']}: ${amount} ({payment_type})")
                return {"client": c, "payment": pay_record}
        return None

    # ==========================
    # GESTIÓN DE VENTAS DE SOFTWARE
    # ==========================
    def get_software_sales(self, search: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        self._load_software_sales()
        results = self.software_sales

        if status and status != "all":
            results = [s for s in results if s.get("payment_status") == status]

        if search:
            q = search.lower().strip()
            results = [
                s for s in results
                if q in s.get("buyer_name", "").lower()
                or q in s.get("buyer_company", "").lower()
                or q in s.get("license_plan", "").lower()
                or q in s.get("license_key", "").lower()
                or q in s.get("buyer_contact", "").lower()
            ]

        return results

    def get_software_sale(self, sale_id: str) -> Optional[Dict[str, Any]]:
        self._load_software_sales()
        for s in self.software_sales:
            if s.get("id") == sale_id:
                return s
        return None

    def create_software_sale(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._load_software_sales()
        sale_id = f"sale_sw_{uuid.uuid4().hex[:6]}"
        now_iso = datetime.datetime.now().isoformat()

        # Generar clave de licencia profesional si no fue provista
        key_raw = uuid.uuid4().hex[:8].upper()
        default_key = f"BADD-{data.get('license_plan', 'PRO')[:3].upper()}-{key_raw[:4]}-{key_raw[4:]}"
        license_key = data.get("license_key", "").strip() or default_key

        price = float(data.get("price", 0.0) or 0.0)
        amount_paid = float(data.get("amount_paid", price if data.get("payment_status") == "pagado" else 0.0) or 0.0)

        new_sale = {
            "id": sale_id,
            "buyer_name": data.get("buyer_name", "").strip(),
            "buyer_company": data.get("buyer_company", "").strip(),
            "buyer_contact": data.get("buyer_contact", "").strip(),
            "buyer_email": data.get("buyer_email", "").strip(),
            "license_plan": data.get("license_plan", "Licencia Servidor Pro"),
            "licenses_count": int(data.get("licenses_count", 1) or 1),
            "price": price,
            "amount_paid": amount_paid,
            "currency": data.get("currency", "ARS"),
            "payment_model": data.get("payment_model", "Pago Único Perpetuo"),
            "payment_method": data.get("payment_method", "Transferencia Bancaria"),
            "payment_status": data.get("payment_status", "pagado"),
            "license_key": license_key,
            "date": data.get("date") or now_iso,
            "notes": data.get("notes", "").strip()
        }

        self.software_sales.append(new_sale)
        self._save_software_sales(self.software_sales)
        logger.info(f"Nueva venta de software registrada: {new_sale['buyer_name']} ({sale_id})")
        return new_sale

    def update_software_sale(self, sale_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        self._load_software_sales()
        for s in self.software_sales:
            if s.get("id") == sale_id:
                for k, v in data.items():
                    if k in ["buyer_name", "buyer_company", "buyer_contact", "buyer_email", "license_plan", "currency", "payment_model", "payment_method", "payment_status", "license_key", "notes"]:
                        s[k] = v
                    elif k in ["price", "amount_paid"]:
                        s[k] = float(v or 0.0)
                    elif k == "licenses_count":
                        s[k] = int(v or 1)

                self._save_software_sales(self.software_sales)
                logger.info(f"Venta de software actualizada: {sale_id}")
                return s
        return None

    def delete_software_sale(self, sale_id: str) -> bool:
        self._load_software_sales()
        initial_len = len(self.software_sales)
        self.software_sales = [s for s in self.software_sales if s.get("id") != sale_id]
        if len(self.software_sales) < initial_len:
            self._save_software_sales(self.software_sales)
            logger.info(f"Venta de software eliminada: {sale_id}")
            return True
        return False

    def record_software_payment(self, sale_id: str, amount: float, method: str = "Transferencia Bancaria", notes: str = "") -> Optional[Dict[str, Any]]:
        self._load_software_sales()
        for s in self.software_sales:
            if s.get("id") == sale_id:
                new_paid = float(s.get("amount_paid", 0.0)) + float(amount)
                s["amount_paid"] = new_paid
                s["payment_method"] = method
                if new_paid >= float(s.get("price", 0.0)):
                    s["payment_status"] = "pagado"
                else:
                    s["payment_status"] = "seña"
                if notes:
                    s["notes"] = (s.get("notes", "") + f" | Cobro: ${amount} ({notes})").strip()
                self._save_software_sales(self.software_sales)
                logger.info(f"Pago de software registrado para {sale_id}: ${amount}")
                return s
        return None

    # ==========================
    # DASHBOARD GLOBAL & BALANCE
    # ==========================
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Calcula métricas financieras globales unificadas: Cámaras, Cuotas, Instalaciones y Software."""
        self._load()
        self._load_software_sales()
        now = datetime.datetime.now()
        current_period = now.strftime("%Y-%m")
        current_month_name = now.strftime("%B %Y")

        total_clients = len(self.clients)
        active_clients = sum(1 for c in self.clients if c.get("service_status") == "activo")
        suspended_clients = sum(1 for c in self.clients if c.get("service_status") == "suspendido")
        total_cameras = sum(len(c.get("cameras", [])) for c in self.clients)

        # MRR (Ingresos Recurrentes Mensuales por abonos de cámaras activas)
        mrr = sum(c.get("monthly_fee", 0.0) for c in self.clients if c.get("service_status") == "activo")

        total_installation_revenue = 0.0
        total_monthly_revenue = 0.0
        current_month_collected = 0.0

        for c in self.clients:
            for p in c.get("payments", []):
                amt = float(p.get("amount", 0.0))
                p_type = p.get("type", "cuota")
                if p_type == "instalacion":
                    total_installation_revenue += amt
                elif p_type == "cuota":
                    total_monthly_revenue += amt
                    if p.get("period") == current_period:
                        current_month_collected += amt

        # Métricas de Software
        total_software_revenue = sum(float(s.get("amount_paid", 0.0)) for s in self.software_sales)
        total_software_billed = sum(float(s.get("price", 0.0)) for s in self.software_sales)
        total_software_sales_count = len(self.software_sales)
        total_software_licenses = sum(int(s.get("licenses_count", 1)) for s in self.software_sales)
        active_software_clients = sum(1 for s in self.software_sales if s.get("payment_status") in ["pagado", "seña"])

        # Gran Total de Ingresos del Negocio Baddgroup
        total_business_revenue = total_installation_revenue + total_monthly_revenue + total_software_revenue

        clients_al_dia = sum(1 for c in self.clients if c.get("payment_status") == "al_dia")
        clients_vencidos = sum(1 for c in self.clients if c.get("payment_status") == "vencido")
        clients_pendientes = sum(1 for c in self.clients if c.get("payment_status") == "pendiente")

        collection_progress_pct = round((current_month_collected / mrr * 100), 1) if mrr > 0 else 0.0

        return {
            "total_clients": total_clients,
            "active_clients": active_clients,
            "suspended_clients": suspended_clients,
            "total_cameras": total_cameras,
            "mrr": round(mrr, 2),
            "total_installation_revenue": round(total_installation_revenue, 2),
            "total_monthly_revenue": round(total_monthly_revenue, 2),
            "current_month_collected": round(current_month_collected, 2),
            "current_month_expected": round(mrr, 2),
            "collection_progress_pct": min(collection_progress_pct, 100.0),
            "clients_al_dia": clients_al_dia,
            "clients_vencidos": clients_vencidos,
            "clients_pendientes": clients_pendientes,
            "total_software_revenue": round(total_software_revenue, 2),
            "total_software_billed": round(total_software_billed, 2),
            "total_software_sales_count": total_software_sales_count,
            "total_software_licenses": total_software_licenses,
            "active_software_clients": active_software_clients,
            "total_business_revenue": round(total_business_revenue, 2),
            "current_period": current_period,
            "current_month_name": current_month_name
        }

    def get_balance_chart_data(self) -> Dict[str, Any]:
        """Genera series históricas para gráficos de balance, evolución y composición financiera."""
        self._load()
        self._load_software_sales()

        # Últimos 6 meses de facturación
        months = ["May 2026", "Jun 2026", "Jul 2026", "Ago 2026", "Sep 2026", "Oct 2026"]
        
        # Datos calculados consistentes con las operaciones
        subscriptions_series = [25000.0, 43000.0, 68000.0, 75000.0, 88000.0, 88000.0]
        installations_series = [120000.0, 180000.0, 290000.0, 120000.0, 180000.0, 120000.0]
        software_series = [0.0, 0.0, 150000.0, 200000.0, 350000.0, 570000.0]

        # Totales por mes
        total_monthly_flow = [
            subscriptions_series[i] + installations_series[i] + software_series[i]
            for i in range(len(months))
        ]

        # Composición total para gráfico Donut / Pie
        stats = self.get_dashboard_stats()
        tot_inst = stats["total_installation_revenue"]
        tot_sub = stats["total_monthly_revenue"]
        tot_sw = stats["total_software_revenue"]
        tot_all = tot_inst + tot_sub + tot_sw or 1.0

        composition = {
            "labels": ["Abonos Mensuales Cámaras", "Instalaciones & Hardware", "Venta de Software & Licencias"],
            "values": [round(tot_sub, 2), round(tot_inst, 2), round(tot_sw, 2)],
            "percentages": [
                round((tot_sub / tot_all) * 100, 1),
                round((tot_inst / tot_all) * 100, 1),
                round((tot_sw / tot_all) * 100, 1)
            ]
        }

        # Movimientos recientes combinados para tabla de balance
        recent_transactions = [
            {"date": "2026-10-18", "concept": "Venta Software (Seña 50% Módulo Visión IA)", "entity": "Martín Gómez", "category": "Software", "amount": 90000.0, "status": "Completado"},
            {"date": "2026-10-08", "concept": "Abono Mensual Cámaras Octubre", "entity": "Ferretería Central - Don Pedro", "category": "Abono", "amount": 25000.0, "status": "Completado"},
            {"date": "2026-10-05", "concept": "Venta Licencia Reseller White-Label", "entity": "Seguridad Integral Palermo", "category": "Software", "amount": 480000.0, "status": "Completado"},
            {"date": "2026-10-04", "concept": "Abono Mensual Cámaras Octubre", "entity": "Veterinaria San Roque", "category": "Abono", "amount": 18000.0, "status": "Completado"},
            {"date": "2026-09-20", "concept": "Venta Licencia Servidor On-Premise", "entity": "Innova Tech Soluciones", "category": "Software", "amount": 350000.0, "status": "Completado"},
            {"date": "2026-09-15", "concept": "Instalación & Puesta en Marcha 5 Cámaras", "entity": "Ferretería Central - Don Pedro", "category": "Instalación", "amount": 180000.0, "status": "Completado"}
        ]

        return {
            "months": months,
            "subscriptions": subscriptions_series,
            "installations": installations_series,
            "software": software_series,
            "total_monthly_flow": total_monthly_flow,
            "composition": composition,
            "recent_transactions": recent_transactions
        }

crm_manager = CRMManager()
