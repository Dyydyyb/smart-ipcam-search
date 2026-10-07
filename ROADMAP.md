# 🗺️ Roadmap y Plan de Implementación: Smart IP Camera AI Search

Este roadmap organiza el desarrollo del PoC en fases incrementales y verificables. **Ninguna fase avanza si la anterior no cumple sus criterios de éxito.**

---

## 🧭 Resumen de Fases

| Fase | Título | Objetivo Principal | Entregable Clave |
|---|---|---|---|
| **Fase 0** | **Validación de Cámara Imou & RTSP** | Descubrir la cámara, verificar credenciales y probar reproducción RTSP local. | Script de prueba con diagnóstico de codec, FPS y resolución. |
| **Fase 1** | **Ingesta Robusta & Pipeline de Visión** | Capturar frames sin lag, ejecutar YOLO11 con tracking y agrupar eventos sin spam. | Worker de detección con tracking ByteTrack y generador de thumbnails. |
| **Fase 2** | **Almacenamiento & Grabación Continua** | Configurar PostgreSQL y servicio de rotación de video segmentado (FFmpeg). | DB configurada y buffer de video sincronizado con los eventos detectados. |
| **Fase 3** | **Motor de Lenguaje Natural (FastAPI + Ollama)** | Conectar LLM local (Qwen 2.5) para traducir consultas naturales en filtros SQL. | API REST probada con endpoints de búsqueda y reproducción. |
| **Fase 4** | **Interfaz Web Inteligente (Next.js)** | Crear dashboard con buscador conversacional, línea de tiempo y reproductor de video. | Frontend interactivo listo para usar en localhost o red local. |
| **Fase 5** | **Estabilización 24/7 y Modo Continuo** | Auto-reconexión ante caídas de red, purga de video antiguo y métricas de consumo. | PoC funcional operando 24/7 de forma autónoma. |

---

## 📌 Detalle Paso a Paso por Fase

### 🔴 FASE 0 — Verificación de Cámara Imou & Conectividad RTSP
* **Objetivo:** Garantizar que la cámara está accesible en la red local y que el stream RTSP puede leerse sin problemas antes de escribir código complejo.
* **Tareas:**
  1. [ ] **Identificar IP y Credenciales:**
     * Encontrar la IP asignada por el router a la cámara Imou.
     * Localizar el **Safety Code** (Código de Seguridad / Device Password de 6-8 caracteres) en la etiqueta inferior de la cámara.
  2. [ ] **Verificar Formato de URL RTSP Dahua/Imou:**
     * Mainstream: `rtsp://admin:<SAFETY_CODE>@<IP_CAMARA>:554/cam/realmonitor?channel=1&subtype=0`
     * Substream: `rtsp://admin:<SAFETY_CODE>@<IP_CAMARA>:554/cam/realmonitor?channel=1&subtype=1`
  3. [ ] **Desarrollar Script de Prueba Mínimo (`scripts/test_imou_camera.py`):**
     * Conexión con OpenCV / FFmpeg.
     * Lectura de metadatos del stream (Codec H.264/H.265, FPS, Ancho x Alto).
     * Captura de un frame de prueba (`snapshots/camera_test.jpg`).
     * Medición de latencia de conexión.
* **Criterio de Aceptación:** Ver una captura nítida de la cámara guardada en disco y confirmar que el stream corre de forma continua durante al menos 60 segundos sin desconexión.

---

### 🟡 FASE 1 — Captura del Stream y Pipeline de Visión por Computadora
* **Objetivo:** Procesar el video de forma continua, detectar objetos de interés (personas, vehículos) y rastrearlos temporalmente.
* **Tareas:**
  1. [ ] **Diseño del Ingestion Worker Asíncrono:**
     * Hilo dedicado para lectura RTSP en buffer no bloqueante (evita acumulación de frames y desfase temporal).
     * Muestreo inteligente (Decimation a 5 FPS para ahorrar cómputo).
  2. [ ] **Integración de YOLO11 / YOLO8:**
     * Configuración con exportación ONNX DirectML para aprovechar la GPU AMD Radeon RX 7600 en Windows, o PyTorch CPU AVX2.
     * Filtrado estricto de clases de seguridad: `person`, `car`, `truck`, `bus`, `motorcycle`, `bicycle`, `dog`, `cat`.
  3. [ ] **Implementación de Tracking (ByteTrack / BoT-SORT):**
     * Asignación de ID persistente a cada objeto mientras se mantenga en cuadro.
     * Filtro temporal: evitar registrar un nuevo evento por cada segundo que una persona camina frente a la cámara.
  4. [ ] **Agregador de Eventos & Extracción de Thumbnails:**
     * Seleccionar el cuadro donde el objeto tuvo el área y confianza más alta para usarlo como miniatura.
* **Criterio de Aceptación:** Si una persona camina frente a la cámara durante 15 segundos, el sistema genera **1 solo evento consolidado** con su hora de inicio, hora de fin, clase "person", confianza y una foto de previsualización.

---

### 🟢 FASE 2 — Base de Datos y Grabación Sincronizada de Video
* **Objetivo:** Persistir los eventos estructurados en PostgreSQL y almacenar el video en archivos rotativos para reproducción posterior.
* **Tareas:**
  1. [ ] **Instalación y Configuración de PostgreSQL:**
     * Crear base de datos `smart_cam_db` y tablas (`cameras`, `video_segments`, `events`).
     * Índices temporales y por tipo de objeto.
  2. [ ] **Servicio de Grabación de Chunks (FFmpeg):**
     * Grabar el Mainstream en segmentos rotativos de 1 a 5 minutos (`.mp4`) usando copia directa de stream (`-c copy`) para consumir 0% de CPU en recodificación.
     * Registrar cada segmento en la tabla `video_segments` con sus timestamps exactos.
  3. [ ] **Vínculo Evento ↔ Segmento de Video:**
     * Asociar cada evento finalizado al segmento de video correspondiente con el offset en segundos para saltar directamente al momento de la acción.
* **Criterio de Aceptación:** Poder consultar en PostgreSQL un evento y obtener la ruta del archivo de video junto al segundo exacto en que ocurrió la detección.

---

### 🔵 FASE 3 — Motor de Búsqueda con LLM Local (Ollama + FastAPI)
* **Objetivo:** Permitir que el usuario consulte en lenguaje natural y obtener los eventos correspondientes en menos de 2 segundos.
* **Tareas:**
  1. [ ] **Instalación y Configuración de Ollama en Local:**
     * Descarga del modelo `qwen2.5:3b` o `qwen2.5:7b` (excelente soporte en español y alta velocidad en CPU/Vulkan).
  2. [ ] **Diseño del Prompt y Esquema JSON Estructurado:**
     * Traducción determinista de intenciones del usuario a filtros (clase, rango horario, duración).
     * Validación con Pydantic para prevenir alucinaciones de formato.
  3. [ ] **API Backend con FastAPI:**
     * `GET /api/stream/status` — Estado de la cámara.
     * `GET /api/events` — Listado con filtros manuales.
     * `POST /api/search` — Endpoint de búsqueda en lenguaje natural.
     * `GET /api/video/playback/{event_id}` — Endpoint de streaming de video parcial para reproducción web.
* **Criterio de Aceptación:** Escribir `"Mostrame autos y personas entre las 8 y las 10 de la mañana"` y recibir la respuesta estructurada de la base de datos con miniaturas y enlaces de video válidos.

---

### 🟣 FASE 4 — Frontend Web Inteligente (Next.js / React)
* **Objetivo:** Proveer una experiencia de usuario fluida, moderna y agradable.
* **Tareas:**
  1. [ ] **Interfaz Moderna (Dark Mode con diseño minimalista):**
     * Barra de búsqueda prominente en lenguaje natural con sugerencias rápidas.
     * Indicador de estado de la cámara en vivo (Online / Offline / FPS / Latencia).
  2. [ ] **Feed de Resultados y Galería:**
     * Tarjetas de eventos con thumbnail, etiqueta de objeto, duración y hora relativa ("hace 20 min").
     * Filtros rápidos por chips: `Todas`, `Personas`, `Vehículos`, `Hoy`, `Última hora`.
  3. [ ] **Reproductor de Video Integrado:**
     * Modal de reproducción que inicia automáticamente en el segundo exacto del evento detectado.
     * Controles de reproducción y descarga de clip.
* **Criterio de Aceptación:** El usuario ingresa a la aplicación web desde su navegador, busca un evento, ve la miniatura y al hacer clic reproduce el video instantáneamente.

---

### ⚪ FASE 5 — Operación Continua 24/7 y Robustez
* **Objetivo:** Garantizar que el sistema pueda dejarse encendido días enteros sin fugas de memoria ni colapso de disco.
* **Tareas:**
  1. [ ] **Watchdog de Reconexión RTSP:**
     * Si la cámara se reinicia o pierde Wi-Fi, el worker reintenta con backoff exponencial sin cerrar la aplicación.
  2. [ ] **Política de Retención de Disco:**
     * Servicio de limpieza automática: mantener solo los últimos N días de video o borrar los segmentos más antiguos si el disco supera el 85% de capacidad.
  3. [ ] **Métricas de Rendimiento:**
     * Monitoreo de uso de CPU, RAM y temperatura de la GPU RX 7600.
* **Criterio de Aceptación:** 48 horas continuas de funcionamiento sin reinicio manual ni degradación de memoria.
