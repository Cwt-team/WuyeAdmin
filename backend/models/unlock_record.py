from backend.db import db
from datetime import datetime

class UnlockRecord(db.Model):
    __tablename__ = 'unlocking_record'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False)
    device_type = db.Column(db.Enum('Entrance Machine', 'Fencing Machine', 'Other'))
    device_info = db.Column(db.String(200))
    unlocking_type = db.Column(db.String(50))
    unlocker = db.Column(db.String(100))
    unlocking_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    house = db.relationship('HouseInfo', backref='unlock_records')

    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'houseId': self.house_id,
            'deviceType': self.device_type,
            'doorInfo': self.device_info,
            'unlockingType': self.unlocking_type,
            'unlocker': self.unlocker,
            'unlockingTime': self.unlocking_time.strftime('%Y-%m-%d %H:%M:%S'),
            'houseName': self.house.house_full_name if self.house else None
        } 