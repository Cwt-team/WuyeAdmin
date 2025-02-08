from db import db
from datetime import datetime

class CommunityInfo(db.Model):
    __tablename__ = 'community_info'
    
    id = db.Column(db.Integer, primary_key=True)
    community_number = db.Column(db.String(20), nullable=False)
    community_name = db.Column(db.String(100), nullable=False)
    community_city = db.Column(db.String(50), nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    is_enabled = db.Column(db.Integer, nullable=False)
    management_machine_quantity = db.Column(db.Integer, nullable=False)
    indoor_machine_quantity = db.Column(db.Integer, nullable=False)
    access_card_type = db.Column(db.String(20), nullable=False)
    app_record_face = db.Column(db.Integer, nullable=False)
    is_same_step = db.Column(db.Integer, nullable=False)
    is_record_upload = db.Column(db.Integer, nullable=False)
    community_password = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.community_number,
            'name': self.community_name,
            'location': self.community_city,
            'createTime': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'isEnabled': self.is_enabled,
            'managerMachineCount': self.management_machine_quantity,
            'indoorMachineCount': self.indoor_machine_quantity,
            'accessCardType': self.access_card_type,
            'appRecordFace': self.app_record_face,
            'isSameStep': self.is_same_step,
            'isRecordUpload': self.is_record_upload
        } 