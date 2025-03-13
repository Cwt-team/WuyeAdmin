from datetime import datetime
from db import db

class DistrictInfo(db.Model):
    __tablename__ = 'district_info'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='区域ID')
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False, comment='所属社区ID')
    district_name = db.Column(db.String(100), nullable=False, comment='区域名称')
    district_number = db.Column(db.String(10), nullable=False, comment='区域编号')
    building_count = db.Column(db.Integer, default=0, comment='楼栋数量')
    house_count = db.Column(db.Integer, default=0, comment='房屋数量')
    status = db.Column(db.Integer, default=1, comment='状态：0-禁用，1-启用')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    community = db.relationship('CommunityInfo', backref='districts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'communityName': self.community.community_name if self.community else None,
            'districtName': self.district_name,
            'districtNumber': self.district_number,
            'buildingCount': self.building_count,
            'houseCount': self.house_count,
            'status': self.status,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 