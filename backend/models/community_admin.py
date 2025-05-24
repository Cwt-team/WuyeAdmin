from backend.db import db
from datetime import datetime

class CommunityAdmin(db.Model):
    """小区管理员表"""
    __tablename__ = 'community_manager'
    
    id = db.Column(db.BigInteger, primary_key=True, comment='管理员ID')
    community_id = db.Column(db.Integer, nullable=False, comment='关联的小区ID')
    other_name = db.Column(db.String(50), nullable=False, comment='别名')
    account_number = db.Column(db.String(50), nullable=False, unique=True, comment='账号')
    character_type = db.Column(db.String(50), nullable=False, comment='角色')
    phone_number = db.Column(db.String(20), nullable=False, comment='手机号码')
    password = db.Column(db.String(100), nullable=False, default='', comment='登录密码')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': str(self.id),
            'communityId': self.community_id,
            'nickname': self.other_name,  # 返回时使用nickname以保持前端兼容
            'username': self.account_number,  # 返回时使用username以保持前端兼容
            'role': self.character_type,
            'phone': self.phone_number,  # 返回时使用phone以保持前端兼容
            'createTime': str(int(self.created_at.timestamp() * 1000)) if self.created_at else ''
        } 