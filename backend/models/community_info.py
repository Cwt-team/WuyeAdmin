from db import db
from datetime import datetime

class CommunityInfo(db.Model):
    __tablename__ = 'community_info'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    community_number = db.Column(db.String(50), unique=True, nullable=False, default='', comment='小区编号')
    community_name = db.Column(db.String(100), nullable=False, default='', comment='小区名称')
    community_city = db.Column(db.String(50), nullable=False, default='', comment='所在城市')
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='小区建档时间')
    is_enabled = db.Column(db.Integer, nullable=False, default=1, comment='启用状态')
    management_machine_quantity = db.Column(db.Integer, nullable=False, default=0, comment='管理机数量')
    indoor_machine_quantity = db.Column(db.Integer, nullable=False, default=0, comment='室内机数量')
    access_card_type = db.Column(db.String(20), nullable=False, default='NFC', comment='门禁卡类型')
    app_record_face = db.Column(db.Integer, nullable=False, default=0, comment='APP人脸录入')
    is_same_step = db.Column(db.Integer, nullable=False, default=0, comment='配置同步状态')
    is_record_upload = db.Column(db.Integer, nullable=False, default=0, comment='记录上传开关')
    community_password = db.Column(db.String(32), nullable=False, default='', comment='密码')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')

    def to_dict(self):
        return {
            'id': self.id,
            'communityNumber': self.community_number,
            'communityName': self.community_name,
            'communityCity': self.community_city,
            'creationTime': self.creation_time.strftime('%Y-%m-%d %H:%M:%S') if self.creation_time else None,
            'isEnabled': self.is_enabled,
            'managementMachineQuantity': self.management_machine_quantity,
            'indoorMachineQuantity': self.indoor_machine_quantity,
            'accessCardType': self.access_card_type,
            'appRecordFace': self.app_record_face,
            'isSameStep': self.is_same_step,
            'isRecordUpload': self.is_record_upload,
            'communityPassword': self.community_password,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        } 