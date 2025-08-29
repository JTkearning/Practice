
// API基础URL配置 - 根据环境自动选择
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://127.0.0.1:5000'  // 本地开发环境
    : '/api';  // 生产环境使用相对路径

// 给"查询分数"按钮绑定点击事件
document.getElementById('searchBtn').onclick = function() {
	const id = document.getElementById('studentId').value.trim();
	const resultDiv = document.getElementById('result');
	const searchBtn = document.getElementById('searchBtn');
	
	if (!id) {
		resultDiv.textContent = '请输入学号';
		resultDiv.style.color = '#ff6b6b';
		return;
	}
	
	// 显示加载状态
	searchBtn.disabled = true;
	searchBtn.textContent = '查询中...';
	resultDiv.textContent = '正在查询...';
	resultDiv.style.color = '#666';
	
	fetch(`${API_BASE_URL}/score?id=${id}`)
		.then(response => {
			if (!response.ok) {
				throw new Error(`HTTP ${response.status}`);
			}
			return response.json();
		})
		.then(data => {
			if (data.score !== undefined) {
				resultDiv.textContent = `学号：${data.id}，分数：${data.score}`;
				resultDiv.style.color = '#28a745';
			} else {
				resultDiv.textContent = data.error || '查询失败';
				resultDiv.style.color = '#ff6b6b';
			}
		})
		.catch(error => {
			console.error('查询错误:', error);
			resultDiv.textContent = '无法连接服务器，请检查网络连接';
			resultDiv.style.color = '#ff6b6b';
		})
		.finally(() => {
			// 恢复按钮状态
			searchBtn.disabled = false;
			searchBtn.textContent = '查询分数';
		});
};

// 给"添加/修改成绩"按钮绑定点击事件
document.getElementById('addBtn').onclick = function() {
	// 获取输入的学号和分数
	const id = document.getElementById('addId').value.trim();
	const score = document.getElementById('addScore').value.trim();
	const resultDiv = document.getElementById('result');
	const addBtn = document.getElementById('addBtn');

	// 校验输入
	if (!id || score === '') {
		resultDiv.textContent = '请输入学号和分数';
		resultDiv.style.color = '#ff6b6b';
		return;
	}

	// 验证分数格式
	const scoreNum = Number(score);
	if (isNaN(scoreNum) || scoreNum < 0 || scoreNum > 100) {
		resultDiv.textContent = '分数必须是0-100之间的数字';
		resultDiv.style.color = '#ff6b6b';
		return;
	}

	// 显示加载状态
	addBtn.disabled = true;
	addBtn.textContent = '提交中...';
	resultDiv.textContent = '正在处理...';
	resultDiv.style.color = '#666';

	// 发送 POST 请求到后端，添加或修改成绩
	fetch(`${API_BASE_URL}/score`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ id, score: scoreNum })
	})
	.then(response => {
		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}
		return response.json();
	})
	.then(data => {
		if (data.score !== undefined) {
			resultDiv.textContent = `${data.msg}：学号 ${data.id}，分数 ${data.score}`;
			resultDiv.style.color = '#28a745';
			// 清空输入框
			document.getElementById('addId').value = '';
			document.getElementById('addScore').value = '';
		} else {
			resultDiv.textContent = data.error || '操作失败';
			resultDiv.style.color = '#ff6b6b';
		}
	})
	.catch(error => {
		console.error('提交错误:', error);
		resultDiv.textContent = '无法连接服务器，请检查网络连接';
		resultDiv.style.color = '#ff6b6b';
	})
	.finally(() => {
		// 恢复按钮状态
		addBtn.disabled = false;
		addBtn.textContent = '添加/修改成绩';
	});
};
