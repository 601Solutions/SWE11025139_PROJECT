import sqlite3
from passlib.hash import bcrypt

def get_connection():
    conn = sqlite3.connect("pet_healthcare.db", check_same_thread=False)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    # 유저 테이블 (id, username, email, hashed_password)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    ''')
    # 강아지 테이블 (id, name, breed, age, weight, health, owner_id(FK))
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            breed TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight REAL NOT NULL,
            health TEXT,
            owner_id INTEGER,
            FOREIGN KEY (owner_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = bcrypt.hash(password)
    cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
                   (username, email, hashed_pw))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        hashed_pw = row[0]
        return bcrypt.verify(password, hashed_pw)
    return False

def user_exists(username, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ? OR email = ?", (username, email))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def add_dog(name, breed, age, weight, health, owner_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO dogs (name, breed, age, weight, health, owner_id) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, breed, age, weight, health, owner_id))
    conn.commit()
    conn.close()
