import sqlite3
from pathlib import Path

db_path = Path("storage/smart_cam.db")
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("PRAGMA table_info(security_events)")
    cols = [row[1] for row in c.fetchall()]
    print("Columnas existentes:", cols)

    if "camera_id" not in cols:
        print("Agregando columna camera_id...")
        c.execute("ALTER TABLE security_events ADD COLUMN camera_id TEXT DEFAULT 'cam_1'")

    if "camera_name" not in cols:
        print("Agregando columna camera_name...")
        c.execute("ALTER TABLE security_events ADD COLUMN camera_name TEXT DEFAULT 'Cámara Poste Principal'")

    conn.commit()
    c.execute("PRAGMA table_info(security_events)")
    print("Columnas finales:", [row[1] for row in c.fetchall()])
    conn.close()
    print("Migración SQLite exitosa.")
