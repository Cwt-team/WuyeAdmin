from backend.db import db
from datetime import datetime

# 设备表
class Device(db.Model):
    __tablename__ = 'device'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='设备ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False, comment='关联的小区ID')
    device_code = db.Column(db.String(50), nullable=False, unique=True, comment='设备编码，唯一值')
    device_sn = db.Column(db.String(100), unique=True, comment='设备唯一序列号')
    name = db.Column(db.String(100), comment='设备名称')
    soft_ver = db.Column(db.String(50), comment='软件版本号')
    device_type = db.Column(db.Enum('门口机', '围栏机', '人脸识别机', '其他'), default='其他', comment='设备类型')
    status = db.Column(db.Enum('在线', '离线'), default='离线', comment='设备状态')
    last_heart_time = db.Column(db.DateTime, comment='最后心跳时间')
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='创建时间')
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')
    
    # 关联的关系
    community = db.relationship('CommunityInfo', backref='devices')
    # 关联的照片
    photos = db.relationship('DevicePhoto', backref='device', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'deviceCode': self.device_code,
            'deviceSn': self.device_sn,
            'name': self.name,
            'softVer': self.soft_ver,
            'deviceType': self.device_type,
            'status': self.status,
            'lastHeartTime': self.last_heart_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_heart_time else None,
            'communityName': self.community.name if self.community else None,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# 设备照片记录表
class DevicePhoto(db.Model):
    __tablename__ = 'device_photo'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='照片ID')
    device_id = db.Column(db.BigInteger, db.ForeignKey('device.id', ondelete='CASCADE'), nullable=False, comment='关联的设备ID')
    photo_url = db.Column(db.String(255), nullable=False, comment='照片URL')
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='创建时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'deviceId': self.device_id,
            'photoUrl': self.photo_url,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# 设备人脸记录表
class DeviceFace(db.Model):
    __tablename__ = 'device_face'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='人脸记录ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False, comment='关联的小区ID')
    phone = db.Column(db.String(20), nullable=False, comment='用户手机号')
    room_number = db.Column(db.String(20), comment='房间号')
    unit_id = db.Column(db.String(20), comment='楼栋单元号')
    image_url = db.Column(db.String(255), comment='图片下载地址')
    zip_url = db.Column(db.String(255), comment='人脸特征码下载地址')
    state = db.Column(db.String(2), comment='状态 10新增 20修改 30删除 40无效图片 50有效图片')
    create_time = db.Column(db.BigInteger, comment='记录的时间戳')
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='创建时间')
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'phone': self.phone,
            'roomNumber': self.room_number,
            'unitId': self.unit_id,
            'imageUrl': self.image_url,
            'zipUrl': self.zip_url,
            'state': self.state,
            'createTime': self.create_time,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# SIP配置表
class SipConfig(db.Model):
    __tablename__ = 'sip_config'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='SIP配置ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False, comment='关联的小区ID')
    unit_id = db.Column(db.String(20), nullable=False, comment='楼栋单元号')
    room_number = db.Column(db.String(20), nullable=False, comment='房间号')
    device_code = db.Column(db.String(50), nullable=False, comment='设备编号')
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=True, comment='关联房屋ID')
    owner_id = db.Column(db.BigInteger, db.ForeignKey('owner_info.id', ondelete='SET NULL'), nullable=True, comment='关联的业主ID')
    phone = db.Column(db.String(20), nullable=False, comment='电话号码')
    sip_host = db.Column(db.String(100), nullable=False, comment='SIP服务器地址')
    sip_port = db.Column(db.String(10), nullable=False, default='5060', comment='SIP端口')
    sip_user = db.Column(db.String(50), nullable=False, comment='SIP账号（短号）')
    sip_password = db.Column(db.String(50), nullable=False, comment='SIP密码')
    sip_domain = db.Column(db.String(100), nullable=False, comment='注册域')
    is_enabled = db.Column(db.Boolean, nullable=False, default=True, comment='是否启用：0-禁用，1-启用')
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='创建时间')
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')
    
    # 关联关系
    house = db.relationship('HouseInfo', backref='sip_configs')
    owner = db.relationship('OwnerInfo', backref='sip_configs')
    community = db.relationship('CommunityInfo', backref='sip_configs')
    
    __table_args__ = (
        db.UniqueConstraint('sip_user', name='uk_sip_user'),
        db.UniqueConstraint('community_id', 'unit_id', 'room_number', 'device_code', name='uk_unit_room_device'),
        db.Index('idx_device_search', 'community_id', 'unit_id', 'room_number', 'device_code'),
        db.Index('idx_device_code', 'device_code'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'unitId': self.unit_id,
            'roomNumber': self.room_number,
            'deviceCode': self.device_code,
            'houseId': self.house_id,
            'ownerId': self.owner_id,
            'phone': self.phone,
            'sipHost': self.sip_host,
            'sipPort': self.sip_port,
            'sipUser': self.sip_user, 
            'sipPassword': self.sip_password,
            'sipDomain': self.sip_domain,
            'isEnabled': self.is_enabled,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
