import time
from datetime import datetime
from app.db import conn

def process_transaction(transaction_id: str):
    try:
        time.sleep(30)

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

    except Exception as e:
        print(f"Worker error for {transaction_id}: {e}")
