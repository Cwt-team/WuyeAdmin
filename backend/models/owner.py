from db import db
from datetime import datetime

class OwnerInfo(db.Model):
    """业主信息表"""
    __tablename__ = 'owner_info'
    
    id = db.Column(db.BigInteger, primary_key=True, comment='业主ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.String(1), nullable=False, comment='性别：M-男 F-女')
    phone_number = db.Column(db.String(20), nullable=False, unique=True, comment='手机号码')
    id_card = db.Column(db.String(18), unique=True, comment='身份证号')
    email = db.Column(db.String(100), comment='邮箱')
    city = db.Column(db.String(50), comment='户籍城市')
    address = db.Column(db.String(200), comment='详细地址')
    owner_type = db.Column(db.String(20), nullable=False, default='业主', comment='业主类型')
    face_image = db.Column(db.String(200), comment='人脸图片路径')
    face_status = db.Column(db.Integer, default=0, comment='人脸状态：0-未录入 1-已录入')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    community = db.relationship('CommunityInfo', backref='owners')
    house = db.relationship('HouseInfo', backref='owners')
    permissions = db.relationship('OwnerPermission', backref='owner', lazy='dynamic')

    def to_dict(self):
        return {
            'id': str(self.id),
            'communityId': self.community_id,
            'houseId': self.house_id,
            'houseName': self.house.house_full_name if self.house else '',
            'name': self.name,
            'gender': self.gender,
            'phone': self.phone_number,
            'idCard': self.id_card or '',
            'email': self.email or '',
            'city': self.city or '',
            'address': self.address or '',
            'ownerType': self.owner_type,
            'faceImage': self.face_image or '',
            'faceStatus': self.face_status,
            'updateTime': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class OwnerPermission(db.Model):
    """业主权限表"""
    __tablename__ = 'owner_permission'
    
    id = db.Column(db.BigInteger, primary_key=True, comment='权限ID')
    owner_id = db.Column(db.BigInteger, db.ForeignKey('owner_info.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False)
    permission_status = db.Column(db.String(20), nullable=False, default='正常', comment='权限状态')
    valid_period = db.Column(db.String(20), nullable=False, default='永久有效', comment='有效期')
    calling_enabled = db.Column(db.Boolean, default=True, comment='呼叫功能启用状态')
    pstn_enabled = db.Column(db.Boolean, default=False, comment='手机转接(PSTN)启用状态')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'ownerId': str(self.owner_id),
            'houseId': self.house_id,
            'status': self.permission_status,
            'validPeriod': self.valid_period,
            'callingEnabled': self.calling_enabled,
            'pstnEnabled': self.pstn_enabled,
            'updateTime': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 