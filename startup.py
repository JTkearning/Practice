#!/usr/bin/env python3
"""
Render部署启动脚本
确保应用正确初始化并启动
"""
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 导入并启动应用
try:
    from backend.app import app, ensure_db_exists
    
    # 确保数据库存在
    print("正在初始化数据库...")
    ensure_db_exists()
    print("数据库初始化完成")
    
    # 健康检查
    print("应用健康检查...")
    with app.test_client() as client:
        response = client.get('/health')
        if response.status_code == 200:
            print("应用健康检查通过")
        else:
            print(f"应用健康检查失败: {response.status_code}")
    
    print("应用准备就绪")
    
except Exception as e:
    print(f"启动失败: {e}")
    sys.exit(1)

# 为gunicorn提供app对象
application = app

if __name__ == "__main__":
    # 开发模式直接运行
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
