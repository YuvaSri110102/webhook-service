import time
from datetime import datetime
from app.db import get_db_connection, release_db_connection

def process_transaction(transaction_id: str):
    try:
        time.sleep(30)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            update transactions
            set status = %s,
                processed_at = %s
            where transaction_id = %s
            """,
            ("PROCESSED", datetime.utcnow(), transaction_id),
        )
        conn.commit()
        cur.close()
        release_db_connection(conn)

    except Exception as e:
        print(f"Worker error for {transaction_id}: {e}")
