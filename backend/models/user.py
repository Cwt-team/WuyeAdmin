from datetime import datetime
from db import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(50), nullable=False, unique=True, comment='用户名')
    password = db.Column(db.String(100), nullable=False, comment='密码')
    real_name = db.Column(db.String(50), comment='真实姓名')
    phone = db.Column(db.String(20), comment='手机号')
    email = db.Column(db.String(100), comment='邮箱')
    avatar = db.Column(db.String(255), comment='头像URL')
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), comment='关联的房屋ID')
    role = db.Column(db.String(20), default='user', comment='角色：admin-管理员，user-普通用户')
    status = db.Column(db.Integer, default=1, comment='状态：0-禁用，1-启用')
    last_login_time = db.Column(db.DateTime, comment='最后登录时间')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'realName': self.real_name,
            'phone': self.phone,
            'email': self.email,
            'avatar': self.avatar,
            'houseId': self.house_id,
            'role': self.role,
            'status': self.status,
            'lastLoginTime': self.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_login_time else None,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }