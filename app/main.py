from fastapi import FastAPI
from datetime import datetime
from app.routes.webhook import router as webhook_router
from app.routes.transactions import router as transactions_router
app = FastAPI()

@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.utcnow().isoformat()
    }

app.include_router(webhook_router, prefix="/v1/webhooks")
app.include_router(transactions_router, prefix="/v1")

