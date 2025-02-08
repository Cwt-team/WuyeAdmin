# db.py
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

# 创建全局 SQLAlchemy 实例
db = SQLAlchemy()

def init_db(app):
    """初始化数据库"""
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3326/wuye"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # 输出SQL语句，方便调试
    
    # 初始化 SQLAlchemy
    db.init_app(app)
    
    # 创建所有表
    with app.app_context():
        try:
            db.create_all()
            print("数据库表创建成功！")
        except Exception as e:
            print(f"数据库表创建失败：{str(e)}")
            raise e

def test_db_models():
    """测试数据库模型"""
    try:
        # 测试查询community_info表
        from models import CommunityInfo
        communities = CommunityInfo.query.all()
        print(f"成功查询到{len(communities)}个小区信息")
        
        # 测试查询admin_role表
        from models import AdminRole
        roles = AdminRole.query.all()
        print(f"成功查询到{len(roles)}个管理员角色")
        
        return True
    except Exception as e:
        print(f"数据库模型测试失败：{str(e)}")
        return False

# 创建一个示例模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    total_units = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    owners = db.relationship('Owner', backref='community', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'location': self.location,
            'totalUnits': self.total_units,
            'status': self.status,
            'createTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    id_card = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    remark = db.Column(db.String(200))
    owner_type = db.Column(db.String(20), nullable=False)
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'room': self.room,
            'name': self.name,
            'gender': self.gender,
            'idCard': self.id_card,
            'phone': self.phone,
            'remark': self.remark,
            'ownerType': self.owner_type,
            'updateTime': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }
