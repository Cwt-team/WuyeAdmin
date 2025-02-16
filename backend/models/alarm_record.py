from db import db
from datetime import datetime
from models.house import HouseInfo

class AlarmRecord(db.Model):
    __tablename__ = 'alarm_record'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False)
    alarm_type = db.Column(db.String(50), nullable=False)
    first_alarm_time = db.Column(db.DateTime, nullable=False)
    latest_alarm_time = db.Column(db.DateTime)
    alarm_description = db.Column(db.Text)
    alarm_status = db.Column(db.Enum('Pending', 'Resolved', 'Processing'), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    house = db.relationship('HouseInfo', backref='alarm_records')

    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'houseId': self.house_id,
            'houseName': self.house.house_full_name if self.house else None,
            'alarmType': self.alarm_type,
            'firstAlarmTime': self.first_alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
            'latestAlarmTime': self.latest_alarm_time.strftime('%Y-%m-%d %H:%M:%S') if self.latest_alarm_time else None,
            'alarmDescription': self.alarm_description,
            'alarmStatus': self.alarm_status
        } 