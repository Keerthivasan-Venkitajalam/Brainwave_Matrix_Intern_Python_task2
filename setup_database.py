import sqlite3
from werkzeug.security import generate_password_hash

# Create database and users table
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
