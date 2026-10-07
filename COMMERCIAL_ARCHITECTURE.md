# 🚀 Estrategia de Comercialización y Arquitectura para Escala (SaaS / Enterprise)

Este documento define la hoja de ruta para evolucionar la plataforma desde un **Proof of Concept (PoC) local** hacia un **producto comercializable (B2B SaaS / On-Premise Appliance)** para empresas, comercios, barrios privados o usuarios finales.

---

## 1. El Dilema del Video en la Nube y por qué el Streaming Puro Falla

Un error común al comercializar software de visión por computadora es pensar en:
> *"Enviar todos los streams RTSP de las cámaras de los clientes a un servidor en la nube con GPUs masivas."*

### Por qué ese modelo no es rentable:
1. **Saturación de Ancho de Banda (Upload del Cliente):**
   * Una cámara 1080p transmite ~2 a 4 Mbps continuos.
   * Un cliente con 8 cámaras requiere entre 16 y 32 Mbps de subida ininterrumpida. Si la conexión de internet del cliente fluctúa, el sistema se cae.
2. **Costo de GPU en la Nube Inviable:**
   * Procesar 50 o 100 streams 24/7 en la nube requeriría alquilar decenas de instancias con GPUs (AWS EC2 g5 / Azure / RunPod), costando miles de dólares al mes.
   * Sería imposible cobrar una suscripción mensual accesible ($15 - $40 USD / mes por cámara) con márgenes positivos.

---

## 2. La Solución Ganadora: Arquitectura Híbrida "Edge-to-Cloud"

Este es el modelo utilizado por empresas líderes de la industria (Verkada, Rhombus, Spot AI, Ambient.ai):

```
┌────────────────────────────────────────────────────────┐
│              EN EL CLIENTE (EDGE / LOCAL)              │
│                                                        │
│  [Cámara IP 1] ──┐                                     │
│  [Cámara IP 2] ──┼─> [ Mini PC / Hub Local / NVR ]     │
│  [Cámara IP N] ──┘         │                           │
│                            ├─ Ingesta RTSP local       │
│                            ├─ Detección YOLO ligera    │
│                            ├─ ByteTrack (Anti-Spam)    │
│                            ├─ Grabación local (Disco)  │
│                            └─ Extracción de Thumbnails │
└────────────────────────────┬───────────────────────────┘
                             │
                             │ Solo envía EVENTOS (JSON ~2KB)
                             │ y THUMBNAILS clave (~50KB)
                             │ vía HTTPS / WebSocket seguro
                             ▼
┌────────────────────────────────────────────────────────┐
│            EN EL SERVIDOR EN LA NUBE (SAAS)            │
│                                                        │
│   [ Backend Multi-Tenant (FastAPI / Node) ]            │
│   [ Base de Datos Centralizada (PostgreSQL / Supabase)]│
│   [ Panel Web & Móvil para Clientes (Next.js) ]        │
│                                                        │
│   ──> BÚSQUEDA INTELIGENTE POR TOKENS:                 │
│       * LLM de Búsqueda (Gemini Flash / GPT-4o-mini)   │
│         Traduce consultas naturales a filtros SQL.     │
│         Costo: $0.0001 USD por consulta.               │
│                                                        │
│       * VLM Opcional para Detalles Finos:              │
│         "¿Qué color de remera tenía la persona?"       │
│         Se envía SOLO el thumbnail del evento al VLM.  │
│         Costo: insignificante (centavos al mes).       │
└────────────────────────────────────────────────────────┘
```

---

## 3. Modelos de Negocio Comerciales

### Modelo A: SaaS Híbrido B2B (Suscripción Mensual - MRR)
* **A quién va dirigido:** Comercios, oficinas, gimnasios, clínicas, depósitos logísticos.
* **Cómo funciona:**
  * El cliente ya tiene cámaras IP (Hikvision, Dahua, Imou, etc.).
  * Se le provee un "Agent" (software instalado en una PC que ya tengan en el local o una Mini-PC económica tipo Intel N100 de $120 USD que se amortiza en el alta).
  * El cliente accede a una plataforma web centralizada (`app.tudominio.com`) desde su celular o PC para buscar eventos de todas sus sucursales.
  * **Tarificación:** $10 a $30 USD mensuales por cámara o por sucursal.

### Modelo B: Enterprise / On-Premise Appliance (Venta de Software + Hardware)
* **A quién va dirigido:** Barrios cerrados, fábricas, entidades financieras, empresas con políticas estrictas de privacidad (que no pueden subir video a internet).
* **Cómo funciona:**
  * Se vende la solución completa "llave en mano" instalada en un servidor local del cliente (usando Ollama local y base de datos local, exactamente igual al PoC que estamos armando ahora).
  * **Tarificación:** Pago inicial por setup + licencia de software + abono mensual de mantenimiento y soporte.

---

## 4. Uso Estratégico de Modelos de IA por Tokens en la Nube

Para comercializar con modelos de IA en la nube sin costos fijos astronómicos de servidores GPU dedicados:

1. **Uso de APIs por Tokens (Serverless):**
   * En lugar de alquilar una GPU en la nube 24/7 que cuesta $200-$500 USD/mes, se usan APIs como **Google Gemini 2.0 / 1.5 Flash** o **OpenAI GPT-4o-mini**.
   * Solo pagas cuando el usuario realmente hace una búsqueda:
     * Una búsqueda de texto cuesta menos de **$0.00005 USD**.
     * Si un cliente hace 500 búsquedas al mes, tu costo de IA en la nube es de **$0.025 USD (¡menos de 3 centavos de dólar al mes!)**.
2. **Capacidad Multimodal (VLM) bajo demanda:**
   * Si el usuario pregunta: *"Buscá personas con mochila negra o campera roja"*:
     1. El LLM filtra eventos de tipo `person`.
     2. Para los 5 o 10 eventos encontrados, se envían sus thumbnails al modelo multimodal (Gemini Flash Vision) para verificar si la persona lleva mochila o campera roja.
     3. Resultado: Precisión asombrosa a un costo casi nulo.

---

## 5. Cómo Diseñamos el Código Hoy para que la Migración Futura sea Inmediata

Para que lo que desarrollemos hoy en tu PC local sea 100% reutilizable mañana en el producto comercial:

1. **Separación Modular del Agente de Visión (`vision_agent/`):**
   * El código que captura el RTSP y corre YOLO corre como un proceso independiente. En el PoC guarda en el PostgreSQL local; en el SaaS, ese mismo módulo puede enviar los eventos a un endpoint HTTP remoto mediante un `API_KEY`.
2. **Esquema de Base de Datos Multi-Tenant Ready:**
   * Agregaremos desde ahora un campo `organization_id` o `account_id` en las tablas (`cameras`, `events`). En el PoC será `default`, pero el código ya estará listo para múltiples clientes.
3. **Adaptador de LLM Intercambiable (`llm_provider`):**
   * Crearemos una interfaz común:
     * `OllamaProvider` (para correr gratis localmente en tu Ryzen / GPU ahora).
     * `CloudTokenProvider` (para conectar Gemini Flash / OpenAI con una sola variable de entorno `.env` en el futuro).
