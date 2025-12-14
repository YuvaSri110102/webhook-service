from fastapi import APIRouter, HTTPException
from app.db import conn

router = APIRouter()

@router.get("/transactions/{transaction_id}")
def get_transaction_status(transaction_id: str):
    try:
        cur = conn.cursor()
        cur.execute(
            """
            select transaction_id, source_account, destination_account,
                   amount, currency, status, created_at, processed_at
            from transactions
            where transaction_id = %s
            """,
            (transaction_id,),
        )

        row = cur.fetchone()
        cur.close()

        if not row:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return {
            "transaction_id": row[0],
            "source_account": row[1],
            "destination_account": row[2],
            "amount": float(row[3]),
            "currency": row[4],
            "status": row[5],
            "created_at": row[6],
            "processed_at": row[7],
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to fetch transaction"
        )
