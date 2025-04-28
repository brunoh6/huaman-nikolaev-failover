import time
import psycopg2
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'port': 5434,
    'dbname': 'postgres',
    'user': 'postgres',
    'password': ''
}

LOG_FILE = 'failover_log.csv'
was_success = True

with open(LOG_FILE, 'w') as log:
    log.write('timestamp,status,message\n')

print("[INFO] Приложение запущено. Попытка подключения каждые 2 секунды...")

while True:
    timestamp = datetime.now().isoformat()
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        message = f"Connected: {result[0]}"
        status = "success"
        cur.close()
        conn.close()
        was_success = True
    except Exception as e:
        message = str(e).replace('\n', ' ')
        status = "error"
        if was_success:
            message = "FAILOVER DETECTED: " + message
            was_success = False

    print(f"{timestamp} | {status.upper()} | {message}")
    with open(LOG_FILE, 'a') as log:
        log.write(f"{timestamp},{status},{message}\n")

    time.sleep(2)
