import os
import pymysql
import re
from dotenv import load_dotenv

def migrate():
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("DATABASE_URL not found")
        return

    # Simple regex for mysql+pymysql://user:pass@host:port/db
    match = re.match(r'mysql\+pymysql://([^:]*):?([^@]*)@([^:/]*):?(\d*)/([^?]*)', db_url)
    if not match:
        print("Invalid DATABASE_URL format")
        return

    user, password, host, port, db_name = match.groups()
    
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=int(port) if port else 3306,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("SHOW COLUMNS FROM user_files LIKE 'file_size'")
        if not cursor.fetchone():
            print("Adding file_size column to user_files table...")
            cursor.execute("ALTER TABLE user_files ADD COLUMN file_size INT NULL AFTER file_path")
            print("Column added successfully.")
        else:
            print("Column 'file_size' already exists.")
            
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
