from backend.db import db
from datetime import datetime
import logging

class Complaint(db.Model):
    __tablename__ = 'complaint_suggestions'
    
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('owner_info.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # complaint: 投诉, suggestion: 建议
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text)  # 图片路径，多个用逗号分隔
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, rejected
    reply = db.Column(db.Text)  # 回复内容
    reply_time = db.Column(db.DateTime)  # 回复时间
    reply_by = db.Column(db.BigInteger, db.ForeignKey('property_manager.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    community = db.relationship('CommunityInfo', backref='complaints')
    user = db.relationship('OwnerInfo', backref='owner_complaints')
    
    def to_dict(self):
        try:
            community_name = self.community.community_name if self.community else None
            user_name = self.user.name if self.user else None
        except Exception as e:
            logging.error(f"获取关联数据失败: {str(e)}")
            community_name = None
            user_name = None
        
        return {
            'id': self.id,
            'communityId': self.community_id,
            'communityName': community_name,
            'userId': self.user_id,
            'userName': user_name,
            'type': self.type,
            'content': self.content,
            'status': self.status,
            'images': self.images.split(',') if self.images else [],
            'reply': self.reply,
            'replyTime': self.reply_time.strftime('%Y-%m-%d %H:%M:%S') if self.reply_time else None,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 