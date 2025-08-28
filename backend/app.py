# 学生成绩查询系统后端

# 学生成绩查询系统后端（数据库版）
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'students.db')

# 查询成绩
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

# 添加或修改成绩
@app.route('/score', methods=['POST'])
def add_or_update_score():
	data = request.get_json()
	student_id = data.get('id')
	score = data.get('score')
	if not student_id or score is None:
		return jsonify({"error": "参数缺失"}), 400
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

if __name__ == '__main__':
	app.run(debug=True)
