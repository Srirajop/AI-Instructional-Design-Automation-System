import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")
# parse url: mysql+pymysql://root:@localhost:3306/storyboard_db
# host=localhost, user=root, password="", db=storyboard_db, port=3306
try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='storyboard_db',
        port=3306
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, storyboard FROM projects")
    projects = cursor.fetchall()
    with open('storyboard_audit_dump.md', 'w', encoding='utf-8') as f:
        for p in projects:
            f.write(f"# Project ID: {p[0]} - Title: {p[1]}\n")
            content = p[2] if p[2] is not None else "[EMPTY STORYBOARD]"
            f.write(content)
            f.write("\n\n" + "="*50 + "\n\n")
    print("DUMP SUCCESS")
except Exception as e:
    print(f"DUMP FAILED: {e}")
finally:
    if 'conn' in locals():
        conn.close()
