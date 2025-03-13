from flask import Flask
from db import db, metadata
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/wuye'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

def reset_metadata():
    """重置SQLAlchemy元数据"""
    with app.app_context():
        # 清除所有表定义
        metadata.clear()
        
        # 重新导入所有模型
        from models import CommunityInfo, DistrictInfo, BuildingInfo, UnitInfo, RoomNotification
        
        # 重新创建所有表
        # db.create_all()  # 注释掉这一行，因为表已经存在
        
        print("元数据已重置")

if __name__ == '__main__':
    reset_metadata() 