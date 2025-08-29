
// 给"查询分数"按钮绑定点击事件
document.getElementById('searchBtn').onclick = function() {
	const id = document.getElementById('studentId').value.trim();
	const resultDiv = document.getElementById('result');
	if (!id) {
		resultDiv.textContent = '请输入学号';
		return;
	}
	fetch(`/score?id=${id}`)
		.then(res => res.json())
		.then(data => {
			if (data.score !== undefined) {
				resultDiv.textContent = `学号：${data.id}，分数：${data.score}`;
			} else {
				resultDiv.textContent = data.error || '查询失败';
			}
		})
		.catch(() => {
			resultDiv.textContent = '无法连接服务器';
		});
};

// 给"添加/修改成绩"按钮绑定点击事件
document.getElementById('addBtn').onclick = function() {
	// 获取输入的学号和分数
	const id = document.getElementById('addId').value.trim();
	const score = document.getElementById('addScore').value.trim();
	const resultDiv = document.getElementById('result');

	// 校验输入
	if (!id || score === '') {
		resultDiv.textContent = '请输入学号和分数';
		return;
	}

	// 发送 POST 请求到后端，添加或修改成绩
	fetch('/score', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ id, score: Number(score) })
	})
	.then(res => res.json())
	.then(data => {
		if (data.score !== undefined) {
			resultDiv.textContent = `${data.msg}：学号 ${data.id}，分数 ${data.score}`;
		} else {
			resultDiv.textContent = data.error || '操作失败';
		}
	})
	.catch(() => {
		resultDiv.textContent = '无法连接服务器';
	});
};
