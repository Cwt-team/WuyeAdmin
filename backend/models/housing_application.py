from backend.db import db
from datetime import datetime

class HousingApplication(db.Model):
    """
    业主房屋绑定申请表
    """
    __tablename__ = 'owner_application'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='申请ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=True, comment='关联的小区ID')
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=True, comment='关联的房屋ID')
    
    # 临时房屋信息（用于申请过程）
    building_name = db.Column(db.String(100), nullable=True, comment='楼栋名称')
    unit_name = db.Column(db.String(100), nullable=True, comment='单元名称')
    house_number = db.Column(db.String(100), nullable=True, comment='房间号')
    
    # 业主基本信息
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.String(10), nullable=False, comment='性别：M-男 F-女')
    id_card = db.Column(db.String(18), comment='身份证号')
    phone_number = db.Column(db.String(20), nullable=False, comment='手机号码')
    
    # 申请状态和审批信息
    application_status = db.Column(db.String(20), nullable=False, default='待审核', comment='申请状态')
    owner_type = db.Column(db.String(20), nullable=False, default='业主', comment='业主类型')
    application_time = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='申请时间')
    callback_message = db.Column(db.String(500), comment='审核反馈信息')
    
    # 证明材料
    information_photo = db.Column(db.String(500), comment='信息照片路径')
    
    # 记录时间
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    community = db.relationship('CommunityInfo', backref='housing_applications')
    house = db.relationship('HouseInfo', backref='housing_applications')
    
    def __repr__(self):
        return f"<HousingApplication {self.id}: {self.name}>"
        
    def to_dict(self):
        return {
            'id': self.id,
            'community_id': self.community_id,
            'house_id': self.house_id,
            'building_name': self.building_name,
            'unit_name': self.unit_name,
            'house_number': self.house_number,
            'name': self.name,
            'gender': self.gender,
            'id_card': self.id_card,
            'phone_number': self.phone_number,
            'application_status': self.application_status,
            'owner_type': self.owner_type,
            'application_time': self.application_time.strftime('%Y-%m-%d %H:%M:%S') if self.application_time else None,
            'callback_message': self.callback_message,
            'information_photo': self.information_photo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 