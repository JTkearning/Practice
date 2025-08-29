
# 学生成绩查询系统

一个简单的学生成绩查询和管理系统，支持查询成绩、添加和修改成绩功能。

## 项目结构
```
New/
├── api/index.py              # Vercel Serverless API
├── backend/
│   ├── app.py               # Flask 后端服务
│   ├── init_db.py           # 数据库初始化脚本
│   └── students.db          # SQLite 数据库
├── frontend/
│   ├── index.html           # 前端页面
│   ├── style.css            # 前端样式
│   ├── script.js            # 前端脚本（Vercel版）
│   └── script-render.js     # 前端脚本（Render版）
├── index.html               # 根目录入口页面（Vercel部署用）
├── index-render.html        # Render部署入口页面
├── requirements.txt         # Python依赖
├── vercel.json             # Vercel配置
├── render.yaml             # Render配置
└── README.md               # 项目说明
```

## 🚀 部署方法

### 方案一：Vercel 部署（推荐）

**优势**：免费、支持Serverless、自动HTTPS、全球CDN

1. **准备代码**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **部署到Vercel**
   - 访问 [Vercel](https://vercel.com)
   - 使用GitHub账号登录
   - 点击 "New Project"
   - 导入您的GitHub仓库
   - Vercel会自动检测配置并部署

3. **访问应用**
   - 部署完成后，Vercel会提供一个类似 `https://your-project.vercel.app` 的链接
   - 前端页面：`https://your-project.vercel.app`
   - API接口：`https://your-project.vercel.app/api/score`

### 方案二：Render 部署

**优势**：支持持久化数据库、免费750小时/月

1. **准备代码**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **部署到Render**
   - 访问 [Render](https://render.com)
   - 使用GitHub账号登录
   - 点击 "New +"，选择 "Web Service"
   - 连接您的GitHub仓库
   - Render会根据 `render.yaml` 自动配置

3. **访问应用**
   - 部署完成后，Render会提供一个链接
   - 应用地址：`https://your-app-name.onrender.com`

## 🛠️ 本地开发

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **初始化数据库**
   ```bash
   python backend/init_db.py
   ```

3. **启动后端服务**
   ```bash
   python backend/app.py
   ```

4. **访问应用**
   - 打开浏览器访问：`http://localhost:5000`

## 📋 API 说明

### 查询成绩
- **URL**: `GET /score?id={学号}`
- **示例**: `GET /score?id=202301`
- **返回**:
  ```json
  {"id": "202301", "score": 95}
  ```

### 添加/修改成绩
- **URL**: `POST /score`
- **Content-Type**: `application/json`
- **请求体**:
  ```json
  {"id": "202301", "score": 88}
  ```
- **返回**:
  ```json
  {"id": "202301", "score": 88, "msg": "成绩已更新"}
  ```

## 🔧 配置说明

### Vercel 配置 (vercel.json)
```json
{
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/index.py"
    }
  ]
}
```

### Render 配置 (render.yaml)
```yaml
services:
  - type: web
    name: student-score-system
    env: python
    buildCommand: "pip install -r requirements.txt && python backend/init_db.py"
    startCommand: "gunicorn --bind 0.0.0.0:$PORT backend.app:app"
    autoDeploy: true
    plan: free
```

## 📝 默认测试数据

系统预设了以下测试数据：
- 学号: 202301, 分数: 95
- 学号: 202302, 分数: 88  
- 学号: 202303, 分数: 76
- 学号: 202304, 分数: 100

## 🔒 注意事项

1. **Vercel部署**：数据库是临时的，每次冷启动会重置数据
2. **Render部署**：免费版应用休眠后重启可能较慢
3. **生产环境**：建议使用外部数据库服务（如PostgreSQL）替换SQLite
4. **安全性**：当前版本没有身份验证，请根据需要添加安全措施

## 🆘 故障排除

### 部署失败
- 检查 `requirements.txt` 中的依赖版本
- 确保代码已推送到GitHub
- 查看部署日志中的错误信息

### API无法访问
- 检查API路径是否正确
- 确认CORS设置
- 查看浏览器开发者工具的Network标签

### 数据丢失（Vercel）
- 这是正常现象，Serverless函数是无状态的
- 考虑集成外部数据库服务
