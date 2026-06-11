import psycopg2
import os
from dotenv import load_dotenv

DB_HOST = os.environ.get("DB_HOST")
DB_PASS = os.environ.get("DB_PASS")

conn = psycopg2.connect(host=DB_HOST, database="postgres", user="postgres", password=DB_PASS)
cur = conn.cursor()

# This command upgrades the column to allow decimals permanently
cur.execute("ALTER TABLE news_sentiment ALTER COLUMN sentiment_score TYPE FLOAT;")
conn.commit()

print("Database column successfully upgraded to decimals!")
conn.close()