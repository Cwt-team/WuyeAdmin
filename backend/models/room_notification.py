from db import db
from datetime import datetime

class RoomNotification(db.Model):
    __tablename__ = 'room_notification'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    display_start_time = db.Column(db.Date)
    display_end_time = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'houseId': self.house_id,
            'title': self.title,
            'content': self.content,
            'displayStartTime': self.display_start_time.strftime('%Y-%m-%d') if self.display_start_time else None,
            'displayEndTime': self.display_end_time.strftime('%Y-%m-%d') if self.display_end_time else None,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } 