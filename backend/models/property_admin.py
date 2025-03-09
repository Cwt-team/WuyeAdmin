from db import db
from datetime import datetime

class PropertyAdmin(db.Model):
    """物业管理员表"""
    __tablename__ = 'property_manager'
    
    id = db.Column(db.BigInteger, primary_key=True, comment='管理员ID')
    community_id = db.Column(db.Integer, nullable=False, comment='关联的小区ID')
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    phone_number = db.Column(db.String(20), nullable=False, unique=True, comment='手机号码')
    remark = db.Column(db.String(200), comment='备注')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    face_image = db.Column(db.String(200), comment='人脸图片路径')
    face_status = db.Column(db.Integer, default=0, comment='人脸状态：0-暂无数据 1-已录入')

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': str(self.id),  # 将管理员ID转换为字符串返回
            'communityId': self.community_id,  # 返回关联的小区ID
            'name': self.name,  # 返回管理员姓名
            'phone': self.phone_number,  # 返回手机号码，前端使用字段名“phone”
            'remark': self.remark or '',  # 返回备注，若为空则返回空字符串
            'updateTime': str(int(self.updated_at.timestamp() * 1000)) if self.updated_at else '',
            # 将更新时间转换为时间戳（毫秒），若为空返回空字符串
            'faceImage': self.face_image or '',  # 返回人脸图片路径，若为空则返回空字符串
            'faceStatus': self.face_status  # 返回人脸状态（0 或 1）
        }
