# 数据库初始化脚本
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'students.db')

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE scores (
            id TEXT PRIMARY KEY,
            score INTEGER
        )''')
        # 插入一些初始数据
        c.executemany('INSERT INTO scores (id, score) VALUES (?, ?)', [
            ("202301", 95),
            ("202302", 88),
            ("202303", 76),
            ("202304", 100)
        ])
        conn.commit()
        conn.close()
        print('数据库已初始化')
    else:
        print('数据库已存在，无需初始化')

if __name__ == '__main__':
    init_db()
