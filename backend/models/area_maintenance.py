from db import db
from datetime import datetime

class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenance_requests'
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, nullable=False)
    district_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CommunityReview(db.Model):
    __tablename__ = 'community_reviews'
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('personal_info.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    images = db.Column(db.Text, comment='图片路径，多个路径用逗号分隔')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reply = db.Column(db.Text, comment='物业回复内容')
    reply_time = db.Column(db.DateTime, comment='回复时间')
    status = db.Column(db.Integer, default=0, comment='状态：0-未回复 1-已回复')
    
    # 关联关系
    community = db.relationship('CommunityInfo', backref='reviews')
    user = db.relationship('PersonalInfo', backref='reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'community_id': self.community_id,
            'community_name': self.community.community_name if self.community else None,
            'user_id': self.user_id,
            'user_name': self.user.nickname if self.user else None,
            'rating': self.rating,
            'comment': self.comment,
            'images': self.images.split(',') if self.images else [],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'reply': self.reply,
            'reply_time': self.reply_time.strftime('%Y-%m-%d %H:%M:%S') if self.reply_time else None,
            'status': self.status,
            'replied': self.status == 1
        } 