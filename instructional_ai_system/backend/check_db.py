import sqlite3
import bcrypt

conn = sqlite3.connect('instructional_design.db')
c = conn.cursor()

c.execute('SELECT id, email, hashed_password FROM users')
users = c.fetchall()

print("CURRENT USERS:")
for u in users:
    print(u)
    
password_to_test = "password123" # try common password 
# print(f"Testing {password_to_test} against hash: {bcrypt.checkpw(password_to_test.encode('utf-8'), u[2].encode('utf-8'))}")

conn.close()
