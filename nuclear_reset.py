import psycopg2
import os
from dotenv import load_dotenv

DB_HOST = os.environ.get("DB_HOST")
# Put your real database password below:
DB_PASS = os.environ.get("DB_PASS")

try:
    conn = psycopg2.connect(host=DB_HOST, database="postgres", user="postgres", password=DB_PASS)
    cur = conn.cursor()
    
    # 1. Destroy the broken table completely
    cur.execute("DROP TABLE IF EXISTS news_sentiment;")
    
    # 2. Rebuild it forcing the FLOAT (decimal) type
    cur.execute("""
        CREATE TABLE news_sentiment (
            title TEXT,
            url TEXT UNIQUE,
            published_at TIMESTAMP,
            sentiment_score FLOAT,
            category TEXT
        );
    """)
    conn.commit()
    print("✅ SUCCESS: Old table vaporized. New decimal table created!")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
finally:
    if 'conn' in locals():
        conn.close()