import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("cityhall.db")
cur = conn.cursor()

# floors テーブル作成
cur.execute(
    """
CREATE TABLE IF NOT EXISTS floors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)
"""
)

# users テーブル作成
cur.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
"""
)

# 初期ユーザーが存在しない場合のみ追加
cur.execute("SELECT * FROM users WHERE username = ?", ("admin",))
if cur.fetchone() is None:
    hashed_pw = generate_password_hash("admin123")
    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", ("admin", hashed_pw)
    )
    print("ユーザー 'admin' を作成しました")
else:
    print("ユーザー 'admin' はすでに存在します")

conn.commit()
conn.close()
