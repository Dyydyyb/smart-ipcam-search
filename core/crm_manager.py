import json
import uuid
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger
from core.config import settings

CRM_FILE = settings.STORAGE_DIR / "crm_clients.json"

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
        "notes": "Galpón logístico. 8 cámaras. Vence día 15.",
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

class CRMManager:
    """Gestor comercial y financiero centralizado para Baddgroup Vision AI."""
    def __init__(self, file_path: Path = CRM_FILE):
        self.file_path = file_path
        self._load()

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

        # Generar usuario / contraseña si no se indicaron
        user = data.get("client_user", "").strip() or f"user_{uuid.uuid4().hex[:5]}"
        pwd = data.get("client_pass", "").strip() or f"pass_{uuid.uuid4().hex[:5]}"

        installation_cost = float(data.get("installation_cost", 0.0) or 0.0)
        installation_paid = float(data.get("installation_paid", 0.0) or 0.0)
        monthly_fee = float(data.get("monthly_fee", 0.0) or 0.0)
        billing_day = int(data.get("billing_day", 10) or 10)

        cameras = data.get("cameras", [])
        payments = []

        # Registrar pago de instalación si fue abonado al ingresar
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
                    "type": payment_type,  # 'cuota' o 'instalacion'
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

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Calcula métricas financieras globales y KPIs de clientes."""
        self._load()
        now = datetime.datetime.now()
        current_period = now.strftime("%Y-%m")
        current_month_name = now.strftime("%B %Y")

        total_clients = len(self.clients)
        active_clients = sum(1 for c in self.clients if c.get("service_status") == "activo")
        suspended_clients = sum(1 for c in self.clients if c.get("service_status") == "suspendido")
        total_cameras = sum(len(c.get("cameras", [])) for c in self.clients)

        # MRR (Ingresos Recurrentes Mensuales esperados por clientes activos)
        mrr = sum(c.get("monthly_fee", 0.0) for c in self.clients if c.get("service_status") == "activo")

        # Total histórico recaudado
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
            "current_period": current_period,
            "current_month_name": current_month_name
        }

crm_manager = CRMManager()
