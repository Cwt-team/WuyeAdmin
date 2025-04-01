from flask import Flask
from routes.maintenance import maintenance_bp

def create_app():
    app = Flask(__name__)
    # ... 其他配置 ...
    
    # 注册蓝图
    app.register_blueprint(maintenance_bp)
    
    return app 