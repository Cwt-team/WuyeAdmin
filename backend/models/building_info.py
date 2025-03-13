from datetime import datetime
from db import db

class BuildingInfo(db.Model):
    __tablename__ = 'building_info'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='楼栋ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False, comment='所属社区ID')
    district_id = db.Column(db.Integer, db.ForeignKey('district_info.id'), nullable=False, comment='所属区域ID')
    building_name = db.Column(db.String(100), nullable=False, comment='楼栋名称')
    building_number = db.Column(db.String(10), nullable=False, comment='楼栋编号')
    floor_count = db.Column(db.Integer, default=0, comment='楼层数量')
    unit_count = db.Column(db.Integer, default=0, comment='单元数量')
    house_count = db.Column(db.Integer, default=0, comment='房屋数量')
    status = db.Column(db.Integer, default=1, comment='状态：0-禁用，1-启用')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    community = db.relationship('CommunityInfo', backref='buildings')
    district = db.relationship('DistrictInfo', backref='buildings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'communityName': self.community.community_name if self.community else None,
            'districtId': self.district_id,
            'districtName': self.district.district_name if self.district else None,
            'buildingName': self.building_name,
            'buildingNumber': self.building_number,
            'floorCount': self.floor_count,
            'unitCount': self.unit_count,
            'houseCount': self.house_count,
            'status': self.status,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 