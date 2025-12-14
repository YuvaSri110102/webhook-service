import time
from datetime import datetime
from app.db import conn

def process_transaction(transaction_id: str):
    """
    Simulates external API processing with a 30-second delay,
    then marks the transaction as PROCESSED.
    """
    time.sleep(30)

    cur = conn.cursor()
    try:
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
    finally:
        cur.close()
