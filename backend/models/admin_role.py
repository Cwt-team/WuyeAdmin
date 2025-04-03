from backend.db import db
from datetime import datetime

class AdminRole(db.Model):
    """管理员角色表"""
    __tablename__ = 'admin_role'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='角色标识ID')
    role_name = db.Column(db.String(50), nullable=False, unique=True, comment='角色名称')
    sort_number = db.Column(db.Integer, nullable=False, comment='排序编号')
    description = db.Column(db.String(200), comment='角色描述')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': str(self.id),
            'name': self.role_name,
            'sortNo': self.sort_number,
            'description': self.description or '',
            'createTime': str(int(self.created_at.timestamp() * 1000))
        } 