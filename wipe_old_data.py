import psycopg2
import os
from dotenv import load_dotenv

# Put your actual password here
DB_HOST = os.environ.get("DB_HOST")
DB_PASS = os.environ.get("DB_PASS")

conn = psycopg2.connect(host=DB_HOST, database="postgres", user="postgres", password=DB_PASS)
cur = conn.cursor()

# This command instantly deletes all rows in the table without deleting the table itself
cur.execute("TRUNCATE TABLE news_sentiment;")
conn.commit()

print("Old integer data successfully wiped!")
conn.close()