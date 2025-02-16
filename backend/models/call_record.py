from db import db
from datetime import datetime

class CallRecord(db.Model):
    __tablename__ = 'call_record'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False)
    door_access_info = db.Column(db.String(200))
    call_start_time = db.Column(db.DateTime, nullable=False)
    call_duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    house = db.relationship('HouseInfo', backref='call_records')

    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'houseId': self.house_id,
            'doorAccessInfo': self.door_access_info,
            'callStartTime': self.call_start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'callDuration': self.call_duration,
            'houseName': self.house.house_full_name if self.house else None
        }