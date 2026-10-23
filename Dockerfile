# BADDGROUP VISION AI - Dockerfile de Producción
FROM public.ecr.aws/docker/library/python:3.12-slim

# Instalar dependencias del sistema requeridas por OpenCV y FFmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir greenlet

# Copiar el código fuente de la plataforma
COPY . .

# Crear directorios de almacenamiento persistente
RUN mkdir -p storage/clips storage/thumbnails storage/models snapshots

# Exponer el puerto de la plataforma web y API
EXPOSE 8000

# Healthcheck de monitoreo
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/api/status || exit 1

# Comando de inicio en producción
CMD ["python", "run_server.py"]
