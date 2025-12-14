from fastapi import FastAPI, Request
from datetime import datetime
from fastapi.responses import JSONResponse
from app.routes.webhook import router as webhook_router
from app.routes.transactions import router as transactions_router
app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        },
    )

@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.utcnow().isoformat()
    }

app.include_router(webhook_router, prefix="/v1/webhooks")
app.include_router(transactions_router, prefix="/v1")

