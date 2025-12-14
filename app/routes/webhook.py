from fastapi import APIRouter, status, BackgroundTasks
from pydantic import BaseModel
from psycopg2.errors import UniqueViolation
from app.db import get_db_connection, release_db_connection
from app.workers import process_transaction

router = APIRouter()

class TransactionWebhook(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str

@router.post("/transactions", status_code=status.HTTP_202_ACCEPTED)
def receive_webhook(
    payload: TransactionWebhook,
    background_tasks: BackgroundTasks
):
    conn = get_db_connection()
    cur = conn.cursor()
    is_new = False

    try:
        cur.execute(
            """
            insert into transactions
            (transaction_id, source_account, destination_account, amount, currency, status)
            values (%s, %s, %s, %s, %s, %s)
            """,
            (
                payload.transaction_id,
                payload.source_account,
                payload.destination_account,
                payload.amount,
                payload.currency,
                "PROCESSING",
            ),
        )
        conn.commit()
        is_new = True

    except Exception:
        conn.rollback()
        
    finally:
        cur.close()
        conn.close()
        release_db_connection(conn)

    if is_new:
        background_tasks.add_task(
            process_transaction, payload.transaction_id
        )

    return {"message": "Webhook accepted"}
