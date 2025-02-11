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
            'id': str(self.id),
            'communityId': self.community_id,
            'name': self.name,
            'phone': self.phone_number,  # 返回时使用phone以保持前端兼容
            'remark': self.remark or '',
            'updateTime': str(int(self.updated_at.timestamp() * 1000)) if self.updated_at else '',
            'faceImage': self.face_image or '',
            'faceStatus': self.face_status
        } 