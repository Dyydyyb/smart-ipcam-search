# GUÍA MAESTRA DE PRODUCCIÓN 24/7 Y COMERCIALIZACIÓN
## Baddgroup Vision AI Platform

---

## 1. Puesta en Marcha 24/7 en tu Casa ("Prueba de Fuego")

Tu instalación personal en el poste es la prueba de concepto real que demostrará la estabilidad del sistema antes de venderlo. Para que funcione 24/7 sin interrupciones:

### A. Servicio Automático en Windows (Arranque con el Sistema)
Para que el sistema se inicie automáticamente cada vez que enciendes la computadora o tras un reinicio de Windows, sin necesidad de iniciar sesión:
1. Haz clic derecho en [`install_windows_service.bat`](file:///C:/Users/dylan/.gemini/antigravity-ide/scratch/smart-ipcam-search/install_windows_service.bat) y selecciona **"Ejecutar como Administrador"**.
2. Esto registra la tarea `BaddgroupVisionAI_24x7` en el Programador de Tareas de Windows con privilegios elevados (`SYSTEM / Highest`) y política de reinicio automático ante caídas cada 60 segundos.

### B. Supervisor Auto-Healing ([`service_watchdog.py`](file:///C:/Users/dylan/.gemini/antigravity-ide/scratch/smart-ipcam-search/service_watchdog.py))
- Supervisa el servidor cada 15 segundos mediante healthchecks HTTP a `/api/status`.
- Si el proceso del backend o de la IA se traba o cae, lo termina limpiamente y lo levanta en menos de 5 segundos.
- Inicia el servidor local de Ollama automáticamente si no está corriendo.
- Guarda el registro de eventos en [`storage/service_watchdog.log`](file:///C:/Users/dylan/.gemini/antigravity-ide/scratch/smart-ipcam-search/storage/service_watchdog.log).

### C. Protección de Disco y Retención Automática ([`engine/storage_manager.py`](file:///C:/Users/dylan/.gemini/antigravity-ide/scratch/smart-ipcam-search/engine/storage_manager.py))
- **Problema resuelto:** Los sistemas NVR tradicionales colapsan cuando el disco se llena.
- **Solución Baddgroup:** Un worker en segundo plano purga automáticamente grabaciones con más de 14 días de antigüedad o cuando el almacenamiento supera los 40 GB, garantizando que el disco jamás se sature.

---

## 2. Acceso Remoto Seguro & Demos en Vivo para Clientes

Para gestionar tu cámara desde tu teléfono celular o mostrarle una **demostración en vivo a clientes del extranjero**:

1. Ejecuta [`start_remote_tunnel.bat`](file:///C:/Users/dylan/.gemini/antigravity-ide/scratch/smart-ipcam-search/start_remote_tunnel.bat).
2. Se iniciará un túnel cifrado mediante **Cloudflare Tunnel**, el cual generará una URL pública segura como:
   ```
   https://tu-identificador-unico.trycloudflare.com
   ```
3. **Ventajas:**
   - Cero apertura de puertos en tu router (no necesitas tocar el módem ni pagar por IP fija).
   - Funciona detrás de CGNAT y redes de fibra óptica residenciales.
   - Tráfico protegido con certificado SSL y CDN global de Cloudflare.
   - *(Opcional)* Puedes vincularlo a tu propio dominio: `vision.baddgroup.com`.

---

## 3. Modelo de Negocio 1: Mercado Regional / Local (Kit Cámara + IA)

### La Propuesta de Valor:
En tu ciudad o región, los clientes (casas, comercios, talleres, fábricas, condominios) están acostumbrados a cámaras analógicas o DVRs viejos donde revisar una grabación toma horas. Tu oferta es:
> *"No te vendo solo una cámara que graba: te vendo una cámara inteligente que responde preguntas en segundos ('¿A qué hora entró el repartidor?', '¿Quién se acercó al portón?')."*

### Hardware Recomendado para el Cliente Local:
- **Cámara IP:** Imou Cruiser / Dahua IP 2K / 4K PoE o Wi-Fi ($45 - $70 USD de costo).
- **Unidad de Procesamiento (Baddgroup AI Box):** 
  - Mini-PC Intel N100 (4 núcleos, 16GB RAM, 512GB SSD) o Mini-PC Ryzen 5 ($130 - $180 USD de costo).
  - Consume apenas 15W de energía eléctrica, silencioso y compacto.
  - Soporta de 4 a 8 cámaras simultáneas procesando con YOLO11 y buffering circular.

### Estructura de Precios Sugerida:
1. **Kit 1 Cámara Inteligente + AI Box Instalado:**
   - Costo de equipos: ~$180 USD.
   - Precio de venta al cliente: **$390 - $550 USD** (Margen bruto: ~$210 - $370 USD por instalación).
2. **Kit 4 Cámaras Inteligentes + AI Box Instalado:**
   - Costo de equipos: ~$360 USD.
   - Precio de venta al cliente: **$750 - $980 USD**.
3. **Abono Mensual de Mantenimiento y Respaldo Cloud (Ingreso Recurrente):**
   - **$25 - $45 USD / mes por cliente** (incluye soporte, alertas por WhatsApp/Telegram y actualizaciones del software de IA). Con 30 clientes locales generas **$750 - $1,350 USD mensuales fijos**.

---

## 4. Modelo de Negocio 2: Mercado Extranjero (Software / Licenciamiento / SaaS)

Para vender en el extranjero sin necesidad de enviar hardware físico:

### A. Modalidad SaaS (Baddgroup Cloud Vision)
- **Cómo funciona:** Alojas la plataforma en un VPS Cloud con aceleración por GPU (Hetzner Cloud, DigitalOcean, RunPod o AWS EC2).
- El cliente extranjero ingresa a tu web (`app.baddgroup.com`), ingresa la URL RTSP de sus cámaras existentes (no necesita comprarte cámaras) y procesa todo en tu nube.
- **Precios de Mercado:**
  - **Plan Pro:** $15 USD / cámara / mes.
  - **Plan Enterprise (5 cámaras):** $59 USD / mes.
  - Búsqueda en lenguaje natural con Gemini 1.5 Flash integrada.

### B. Modalidad On-Premise (Docker License)
- Para empresas, fábricas o barrios privados en el extranjero que no pueden subir sus videos a internet por normativas de privacidad.
- **Cómo se entrega:** Les entregas el archivo [`docker-compose.yml`](file:///C:/Users/dylan/.gemini/antigravity-ide/scratch/smart-ipcam-search/docker-compose.yml) y una clave de licencia.
- Ejecutan un único comando en su servidor:
  ```bash
  docker compose up -d
  ```
- **Precios de Mercado:**
  - Licencia de software perpetua o anual: **$600 - $1,500 USD / año** por servidor.

---

## 5. Activación de la IA Multimodal (Google Gemini 1.5 Flash)

Para que las búsquedas analicen **los fotogramas directamente con visión humana** (colores de vestimenta, movimientos de brazos, objetos en mano):

1. Obtén tu clave en [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Añádela en tu archivo `.env`:
   ```ini
   GEMINI_API_KEY=AIzaSy...
   GEMINI_MODEL=gemini-1.5-flash
   ```
3. El sistema evaluará las miniaturas capturadas con Gemini 1.5 Flash cuando haya internet, y usará automáticamente Ollama Qwen 2.5 local como respaldo si la conexión se interrumpe.

---

## 6. Lista de Verificación para tu Prueba de Fuego (1 Semana)

- [x] Cámara IP conectada y transmitiendo por RTSP continuo.
- [x] Pipeline de tracking YOLO11 segmentando clips de video al detectar movimiento.
- [x] Supervisor [`service_watchdog.py`](file:///C:/Users/dylan/.gemini/antigravity-ide/scratch/smart-ipcam-search/service_watchdog.py) activo para auto-recuperación 24/7.
- [x] Retención automática en disco ([`engine/storage_manager.py`](file:///C:/Users/dylan/.gemini/antigravity-ide/scratch/smart-ipcam-search/engine/storage_manager.py)) para evitar desbordes de espacio.
- [x] Multi-cámara habilitada para añadir más cámaras desde la interfaz.
- [x] Contenedor Docker y scripts de despliegue listos para distribución.
- [x] Acceso remoto para celulares y demostraciones mediante Cloudflare Tunnel.
