from backend.db import db
from datetime import datetime
from backend.models import *

class OwnerApplication(db.Model):
    __tablename__ = 'owner_application'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='申请ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False, comment='关联的小区ID')
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False, comment='关联的房屋ID')
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.String(1), nullable=False, comment='性别：M-男 F-女')
    id_card = db.Column(db.String(18), unique=True, comment='身份证号')
    phone_number = db.Column(db.String(20), unique=True, nullable=False, comment='手机号码')
    application_status = db.Column(db.String(20), nullable=False, comment='申请状态')
    owner_type = db.Column(db.String(20), nullable=False, default='业主', comment='业主类型')
    application_time = db.Column(db.DateTime, nullable=False, comment='申请时间')
    information_photo = db.Column(db.String(200), comment='信息照片路径')
    callback_message = db.Column(db.String(200), comment='打回信息')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关联关系
    community = db.relationship('CommunityInfo', backref='applications')
    house = db.relationship('HouseInfo', backref='applications')

    def to_dict(self):
        house_info = f"{self.house.district_number or ''}区{self.house.building_number or ''}栋{self.house.unit_number or ''}单元"
        return {
            'id': self.id,  # 申请ID
            'room': house_info,  # 通过关联的房屋信息构造出的房间信息字符串，例如 "1区1栋1单元"
            'name': self.name,  # 申请人的姓名
            'gender': self.gender,  # 性别（M 或 F）
            'idCard': self.id_card,  # 身份证号
            'phone': self.phone_number,  # 手机号码
            'status': self.application_status,  # 申请状态
            'ownerType': self.owner_type,  # 业主类型
            'applyTime': self.application_time.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化后的申请时间
            'callbackMessage': self.callback_message  # 如果有打回信息，返回该信息
        }
