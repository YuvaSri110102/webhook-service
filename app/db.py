import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set")

conn = psycopg2.connect(DATABASE_URL)

cur = conn.cursor()
cur.execute("select 1") 
print("DB connected successfully")