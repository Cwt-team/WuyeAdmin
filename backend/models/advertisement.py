from db import db
from datetime import datetime

class Advertisement(db.Model):
    __tablename__ = 'door_machine_content_management'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    orientation = db.Column(db.String(20), nullable=False)  # horizontal/vertical
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'title': self.title,
            'imageUrl': self.image_url,
            'orientation': self.orientation,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } 