# Vercel Serverless Flask API
import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'students.db')

# 每次 cold start 自动初始化数据库（仅适合演示）
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE scores (
            id TEXT PRIMARY KEY,
            score INTEGER
        )''')
        c.executemany('INSERT INTO scores (id, score) VALUES (?, ?)', [
            ("202301", 95),
            ("202302", 88),
            ("202303", 76),
            ("202304", 100)
        ])
        conn.commit()
        conn.close()

init_db()

@app.route('/score', methods=['GET'])
def get_score():
    student_id = request.args.get('id')
    if not student_id:
        return jsonify({"error": "缺少学号参数"}), 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT score FROM scores WHERE id=?', (student_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({"id": student_id, "score": row[0]})
    else:
        return jsonify({"error": "未找到该学号"}), 404

@app.route('/score', methods=['POST'])
def add_or_update_score():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请求数据格式错误"}), 400
            
        student_id = data.get('id')
        score = data.get('score')
        
        # 输入验证
        if not student_id or score is None:
            return jsonify({"error": "学号和分数不能为空"}), 400
        
        # 验证学号格式
        if not str(student_id).strip():
            return jsonify({"error": "学号不能为空"}), 400
            
        # 验证分数范围
        try:
            score = float(score)
            if score < 0 or score > 100:
                return jsonify({"error": "分数必须在0-100之间"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "分数必须是有效数字"}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # 判断是否已存在
        c.execute('SELECT score FROM scores WHERE id=?', (student_id,))
        if c.fetchone():
            c.execute('UPDATE scores SET score=? WHERE id=?', (score, student_id))
            msg = "成绩已更新"
        else:
            c.execute('INSERT INTO scores (id, score) VALUES (?, ?)', (student_id, score))
            msg = "成绩已添加"
        
        conn.commit()
        conn.close()
        
        return jsonify({"id": student_id, "score": score, "msg": msg})
        
    except sqlite3.Error as e:
        return jsonify({"error": f"数据库操作失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

# Vercel Serverless 必须暴露 app 变量
handler = app
