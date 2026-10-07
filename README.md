# 🔍 Smart IP Camera AI Search (PoC)

> Plataforma de búsqueda inteligente para cámaras IP convencionales mediante IA local, visión por computadora (YOLO + Tracking), procesamiento de lenguaje natural (Ollama) y base de datos relacional (PostgreSQL).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12-brightgreen.svg)](https://www.python.org/)
[![Hardware: AMD RX 7600 & Ryzen 5700G](https://img.shields.io/badge/Hardware-AMD%20Radeon%20RX%207600-red.svg)](https://www.amd.com/)
[![Local AI: Ollama](https://img.shields.io/badge/LLM-Ollama%20(Local)-orange.svg)](https://ollama.ai/)

---

## 🎯 Objetivo del Proyecto

Permitir que cualquier cámara IP convencional conectada por **RTSP** se vuelva **buscable mediante lenguaje natural**, como por ejemplo:
* *"¿Cuándo pasó un camión de basura?"*
* *"Mostrame las personas que aparecieron entre las 4 y las 6 AM."*
* *"¿Cuándo pasó un auto negro o rojo?"*
* *"Buscá personas cerca de la entrada ayer por la tarde."*

El sistema analiza continuamente la transmisión en tiempo real con un modelo de visión liviano, genera **eventos estructurados** en PostgreSQL, y traduce las búsquedas del usuario con un LLM local sin enviar nunca video continuo a un modelo masivo ni depender de servicios en la nube de pago.

---

## 💻 Hardware Objetivo y Compatibilidad

* **CPU:** AMD Ryzen 7 5700G (8c/16t, AVX2)
* **GPU:** AMD Radeon RX 7600 (8 GB VRAM, RDNA 3) — **Aceleración vía DirectML / ONNX Runtime** o ejecución CPU AVX2 optimizada.
* **RAM:** 16 GB DDR4.
* **Cámara de Prueba:** Imou (plataforma Dahua) Wi-Fi/Ethernet.
* **Sin requerimiento de NVIDIA CUDA ni servidores en la nube.**

---

## 🏗️ Arquitectura en Resumen

```
[ Cámara Imou RTSP ]
         │
         ├── Substream (640x360) ──> [ OpenCV Ingestion Worker (5 FPS) ]
         │                                       │
         │                               [ YOLO11 + ByteTrack ]
         │                                       │
         │                              (Generación de Eventos)
         │                                       │
         │                                       ▼
         ├── Mainstream (1080p)  ──> [ FFmpeg Segmenter ] ──> [ Archivos .mp4 ]
                                                 │
                                                 ▼
                                     [ PostgreSQL Database ]
                                                 ▲
                                                 │ (Filtro SQL)
[ Frontend Next.js ] ──> [ FastAPI Backend ] ──> [ Ollama (Qwen 2.5) ]
  (Búsqueda en lenguaje natural)
```

Para más detalles, consulta la documentación completa en [ARCHITECTURE.md](ARCHITECTURE.md) y el plan de etapas en [ROADMAP.md](ROADMAP.md).

---

## 📋 Requisitos Previos

Para ejecutar el entorno local en Windows, necesitarás:

1. **Python 3.11 o 3.12** (Recomendado para compatibilidad total con PyTorch y OpenCV).
2. **FFmpeg** (Instalable con `winget install Gyan.FFmpeg`).
3. **PostgreSQL 15 o superior** (O Docker para correr PostgreSQL local).
4. **Ollama** (Instalable con `winget install Ollama.Ollama`).
5. **Node.js 18+** (Para el frontend en Next.js).

---

## 🚀 Fase 0: Verificación de la Cámara Imou

Antes de iniciar el backend o la base de datos, debemos verificar la conexión con la cámara física.

### 1. Formato de URL RTSP en cámaras Imou:
```text
rtsp://admin:<SAFETY_CODE>@<IP_CAMARA>:554/cam/realmonitor?channel=1&subtype=0  (Mainstream - 1080p)
rtsp://admin:<SAFETY_CODE>@<IP_CAMARA>:554/cam/realmonitor?channel=1&subtype=1  (Substream - Baja resolución)
```

> ⚠️ **Nota Importante sobre la Contraseña:**
> En las cámaras Imou, la contraseña para el usuario `admin` suele ser el **Safety Code** (Código de Seguridad) impreso en la etiqueta pegada debajo de la cámara (cerca del código QR). No es necesariamente la contraseña de tu cuenta de la app Imou Life.

### 2. Ejecutar la prueba de conexión:
Copia el archivo de configuración de ejemplo:
```powershell
cp .env.example .env
```
Edita `.env` con la IP de tu cámara y el Safety Code, y ejecuta el script de diagnóstico:
```powershell
python scripts/test_imou_camera.py
```

El script verificará:
* Conexión TCP al puerto 554.
* Negociación RTSP.
* Resolución, FPS y codec detectados.
* Guardará una imagen de prueba en `snapshots/camera_test.jpg`.

---

## 📂 Estructura del Repositorio

```text
smart-ipcam-search/
├── .gitignore
├── ARCHITECTURE.md          # Especificación técnica detallada
├── ROADMAP.md               # Plan de desarrollo paso a paso
├── README.md                # Este archivo
├── requirements.txt         # Dependencias Python
├── .env.example             # Plantilla de variables de entorno
├── scripts/
│   └── test_imou_camera.py  # Script de diagnóstico para la Fase 0
├── backend/                 # Backend FastAPI (Fase 2-3)
├── frontend/                # Aplicación Next.js (Fase 4)
└── storage/                 # Directorio para clips y snapshots (ignorado en git)
```

---

## 📜 Licencia
Proyecto distribuido bajo la licencia MIT.
