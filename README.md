
# 学生成绩查询系统

## 项目结构
- api/index.py：后端 Flask Serverless 服务（Vercel 部署）
- requirements.txt：后端依赖声明
- vercel.json：Vercel 配置文件
- frontend/index.html：前端页面，输入学号查询分数、添加/修改成绩
- frontend/style.css：前端样式
- frontend/script.js：前端交互脚本

## 本地启动方法
1. 安装 Flask 及依赖：`pip3 install --break-system-packages flask flask-cors`
2. 初始化数据库：`python3 backend/init_db.py`
3. 运行后端：`python3 backend/app.py`
4. 用浏览器打开 `frontend/index.html`，输入学号查询分数或添加/修改成绩

## 已修复的问题
- ✅ 修复了backend/app.py中的重复import语句
- ✅ 增强了前端的错误处理和用户体验
- ✅ 添加了加载状态显示和分数验证
- ✅ 改进了API端点配置，支持本地和生产环境
- ✅ 增强了后端的输入验证和错误处理
- ✅ 优化了界面样式，支持按钮禁用状态

## Vercel 部署方法
1. 将项目推送到 GitHub
2. 登录 Vercel，导入仓库，自动识别 Python Serverless API
3. 前端静态页面可放在根目录或 Vercel 静态托管
4. 注意：Serverless 环境数据库为临时文件，仅适合演示

## API 说明
- GET /score?id=学号：查询成绩
- POST /score：添加或修改成绩，提交 JSON，如 `{"id": "学号", "score": 分数}`
- 返回：`{"id": "学号", "score": 分数}` 或 `{"error": "未找到该学号"}`
