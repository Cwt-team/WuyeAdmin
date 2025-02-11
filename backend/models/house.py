from db import db
from datetime import datetime

class HouseInfo(db.Model):
    __tablename__ = 'house_info'
    
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    district_number = db.Column(db.String(10))
    building_number = db.Column(db.String(10))
    unit_number = db.Column(db.String(10))
    house_full_name = db.Column(db.String(100), nullable=False)
    house_level = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 关联关系
    community = db.relationship('CommunityInfo', backref='houses')
    parent = db.relationship('HouseInfo', remote_side=[id], backref='children')
    
    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'districtNumber': self.district_number,
            'buildingNumber': self.building_number,
            'unitNumber': self.unit_number,
            'fullName': self.house_full_name,
            'level': self.house_level,
            'parentId': self.parent_id,
            'createTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'count': len(self.children) if self.children else 0
        } 