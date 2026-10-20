import sqlite3

conn = sqlite3.connect('storage/smart_cam.db')
cursor = conn.cursor()

# Check current
cursor.execute("SELECT min(start_time), max(start_time) FROM security_events")
print("BEFORE:", cursor.fetchone())

# Shift records that were saved in UTC (start_time > 03:00) by -3 hours
cursor.execute("UPDATE security_events SET start_time = datetime(start_time, '-3 hours'), end_time = datetime(end_time, '-3 hours') WHERE start_time >= '2026-10-20 03:00:00'")
print("UPDATED ROWS:", cursor.rowcount)
conn.commit()

cursor.execute("SELECT min(start_time), max(start_time) FROM security_events")
print("AFTER:", cursor.fetchone())
conn.close()
