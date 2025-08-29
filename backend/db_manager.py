#!/usr/bin/env python3
# 数据库管理工具
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'students.db')
EXPORT_FILE = os.path.join(os.path.dirname(__file__), 'data_export.json')

def export_data():
    """导出数据库数据到JSON文件"""
    if not os.path.exists(DB_PATH):
        print("数据库不存在")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM scores')
    rows = c.fetchall()
    conn.close()
    
    data = []
    for row in rows:
        data.append({"id": row[0], "score": row[1]})
    
    with open(EXPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已导出到 {EXPORT_FILE}")
    print(f"共导出 {len(data)} 条记录")

def import_data():
    """从JSON文件导入数据到数据库"""
    if not os.path.exists(EXPORT_FILE):
        print(f"导入文件 {EXPORT_FILE} 不存在")
        return
    
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 创建表（如果不存在）
    c.execute('''CREATE TABLE IF NOT EXISTS scores (
        id TEXT PRIMARY KEY,
        score INTEGER
    )''')
    
    # 清空现有数据
    c.execute('DELETE FROM scores')
    
    # 导入新数据
    for item in data:
        c.execute('INSERT INTO scores (id, score) VALUES (?, ?)', 
                 (item['id'], item['score']))
    
    conn.commit()
    conn.close()
    
    print(f"数据已导入，共导入 {len(data)} 条记录")

def show_data():
    """显示当前数据库中的所有数据"""
    if not os.path.exists(DB_PATH):
        print("数据库不存在")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY id')
    rows = c.fetchall()
    conn.close()
    
    print("\n当前数据库中的数据：")
    print("-" * 30)
    for row in rows:
        print(f"学号: {row[0]}, 分数: {row[1]}")
    print("-" * 30)
    print(f"总计: {len(rows)} 条记录\n")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print("用法:")
        print("  python db_manager.py export  # 导出数据")
        print("  python db_manager.py import  # 导入数据")
        print("  python db_manager.py show    # 显示数据")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'export':
        export_data()
    elif command == 'import':
        import_data()
    elif command == 'show':
        show_data()
    else:
        print("无效命令，支持的命令: export, import, show")
