# Webhook Transaction Processing Service

This project is a backend service builts a real-world **webhook-based transaction processing system** with
asynchronous background processing, idempotency handling, and persistent storage.

---

## 🚀 Live API Endpoint

**Base URL (Deployed on Cloud):** 
https://webhook-backend-u5hv.onrender.com

---

## 📌 Features

- Webhook endpoint that responds instantly with **HTTP 202 Accepted**
- Asynchronous background processing with a **30-second delay**
- Idempotent handling of duplicate webhooks
- Persistent transaction storage using PostgreSQL
- Transaction status retrieval API
- Publicly deployed backend service

---

## 🛠 Tech Stack

- **Language:** Python 3
- **Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Database:** PostgreSQL (Supabase)
- **Deployment Platform:** Render

---

## 🧠 Technical Design Choices

### FastAPI
FastAPI was chosen for its high performance, async support, and suitability for
webhook-based systems.

### Background Processing
FastAPI’s `BackgroundTasks` is used to simulate external API processing with a
30-second delay without blocking the webhook response.

### Idempotency
- `transaction_id` is enforced as **UNIQUE** at the database level
- Duplicate webhooks always return `202 Accepted` but **do not trigger reprocessing**

### Database
PostgreSQL is used for persistence. Supabase’s **transaction pooler** is used to
ensure reliable cloud connectivity with SSL.

---

## 📡 API Endpoints

### 1. Health Check
GET /

Response:
```json
{
  "status": "HEALTHY",
  "current_time": "ISO_TIMESTAMP"
}

```
### 2. Webhook Endpoint
POST /v1/webhooks/transactions
Request:
```json

{
  "transaction_id": "txn_123",
  "source_account": "acc_user_1",
  "destination_account": "acc_merchant_1",
  "amount": 1000,
  "currency": "INR"
}
```
Response:
```json
{
    "message": "Webhook accepted"
}
```

### 3. Transaction Status API
GET /v1/transactions/{transaction_id}

Response:
```json
{
  "transaction_id": "txn_123",
  "source_account": "acc_user_1",
  "destination_account": "acc_merchant_1",
  "amount": 1000,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "ISO_TIMESTAMP",
  "processed_at": "ISO_TIMESTAMP"
}
```

status can be PROCESSING or PROCESSED
processed_at is null while processing

Run Locally

1. Clone Repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2. Create Virtual Environment
python -m venv venv

Activate:
Windows
>>> venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Environment Variables
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/postgres?sslmode=require

5. Run the Server
uvicorn app.main:app --reload

Server will be available at:
http://127.0.0.1:8000

6. How to Test the Service

Send a POST request to the webhook endpoint
Receive immediate 202 Accepted response
Call the status API → PROCESSING
After ~30 seconds → PROCESSED
Sending the same webhook again does not reprocess the transaction

