import sys
import uvicorn

# Configurar UTF-8 para stdout en Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.config import settings

if __name__ == "__main__":
    print("=" * 64)
    print(">> Iniciando Smart IP Camera AI Search Platform")
    print(f">> Camara RTSP: {settings.CAMERA_RTSP_SUB.split('@')[-1]}")
    print(f">> Panel Web: http://localhost:{settings.PORT}")
    print("=" * 64)
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=False)
