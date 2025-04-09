from backend.db import db
from datetime import datetime
from backend.models import HouseInfo
from backend.models.community_info import CommunityInfo

class OwnerInfo(db.Model):
    """业主信息表"""
    __tablename__ = 'owner_info'
    
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='业主ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.CHAR(1), nullable=False, comment='性别：M-男 F-女')
    phone_number = db.Column(db.String(20), nullable=False, unique=True, comment='手机号码')
    id_card = db.Column(db.String(18), unique=True, comment='身份证号')
    email = db.Column(db.String(100), comment='邮箱')
    city = db.Column(db.String(50), comment='户籍城市')
    address = db.Column(db.String(200), comment='详细地址')
    owner_type = db.Column(db.String(20), nullable=False, default='业主', comment='业主类型')
    face_image = db.Column(db.String(200), comment='人脸图片路径')
    face_status = db.Column(db.Integer, default=0, comment='人脸状态：0-未录入 1-已录入')
    account = db.Column(db.String(50), unique=True, comment='账号')
    password = db.Column(db.String(100), comment='密码')
    wx_openid = db.Column(db.String(50), unique=True, comment='微信OpenID')
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # 关联关系
    community = db.relationship('CommunityInfo', backref='owners')
    house = db.relationship('HouseInfo', backref='owners')
    permissions = db.relationship('OwnerPermission', backref='owner', lazy='dynamic')

    def to_dict(self):
        return {
            'id': str(self.id),  # 将 id 转为字符串返回
            'communityId': self.community_id,  # 返回所属社区的 ID
            'houseId': self.house_id,  # 返回所属房屋的 ID
            'houseName': self.house.house_full_name if self.house else '',  # 如果关联的房屋存在，则返回房屋的完整名称，否则返回空字符串
            'name': self.name,  # 返回业主姓名
            'gender': self.gender,  # 返回业主性别
            'phone': self.phone_number,  # 返回手机号码
            'idCard': self.id_card or '',  # 返回身份证号码，若为空则返回空字符串
            'email': self.email or '',  # 返回邮箱，若为空则返回空字符串
            'city': self.city or '',  # 返回户籍城市，若为空则返回空字符串
            'address': self.address or '',  # 返回详细地址，若为空则返回空字符串
            'ownerType': self.owner_type,  # 返回业主类型
            'faceImage': self.face_image or '',  # 返回人脸图片路径，若为空则返回空字符串
            'faceStatus': self.face_status,  # 返回人脸状态（0或1）
            'updateTime': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')  # 格式化返回更新时间
        }

class OwnerPermission(db.Model):
    """业主权限表"""
    __tablename__ = 'owner_permission'
    
    __table_args__ = {'extend_existing': True}
    
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
            'id': str(self.id),                    # 将权限记录的ID转换为字符串返回
            'ownerId': str(self.owner_id),           # 将业主ID转换为字符串返回
            'houseId': self.house_id,                # 返回关联的房屋ID
            'status': self.permission_status,        # 返回权限状态
            'validPeriod': self.valid_period,        # 返回权限有效期
            'callingEnabled': self.calling_enabled,  # 返回呼叫功能是否启用的状态
            'pstnEnabled': self.pstn_enabled,        # 返回手机转接功能是否启用的状态
            'updateTime': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')  # 格式化返回更新时间
        }