from db import db
from datetime import datetime
import json

class MaintenanceRequest(db.Model):
    """维修请求模型（对应维修请求表）"""
    __tablename__ = 'maintenance_request'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_number = db.Column(db.String(50), unique=True, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)  # 社区ID
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False)         # 房屋ID
    
    reporter_name = db.Column(db.String(50), nullable=False)
    reporter_phone = db.Column(db.String(20), nullable=False)
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), default='normal')
    expected_time = db.Column(db.DateTime)
    images = db.Column(db.Text)
    
    status = db.Column(db.String(20), default='pending')
    report_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    assign_time = db.Column(db.DateTime)
    process_time = db.Column(db.DateTime)
    complete_time = db.Column(db.DateTime)
    
    handler_name = db.Column(db.String(50))
    handler_phone = db.Column(db.String(20))
    repair_type = db.Column(db.String(20))
    cost = db.Column(db.DECIMAL(10,2), default=0.00)
    is_paid = db.Column(db.Boolean, default=False)
    payment_time = db.Column(db.DateTime)
    payment_method = db.Column(db.String(20))
    notes = db.Column(db.Text)
    
    evaluation_score = db.Column(db.Integer)
    evaluation_content = db.Column(db.Text)
    evaluation_time = db.Column(db.DateTime)
    evaluation_images = db.Column(db.Text)
    
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    community = db.relationship('CommunityInfo', backref='maintenance_requests')
    house = db.relationship('HouseInfo', backref='maintenance_requests')

    def to_dict(self):
        """转换为字典格式"""
        try:
            return {
                'id': self.id,
                'request_number': self.request_number, # 报修单号
                'communityId': self.community_id,
                'communityName': self.community.community_name if self.community else None,
                'houseId': self.house_id,
                'house_full_name': self.house.house_full_name if self.house else None,
                'reporter_name': self.reporter_name,   #报修人
                'reporter_phone': self.reporter_phone,   #报修人电话
                'title': self.title,
                'description': self.description,
                'type': self.type,
                'priority': self.priority,
                'expectedTime': self.expected_time.strftime('%Y-%m-%d %H:%M:%S') if self.expected_time else None,
                'images': json.loads(self.images) if self.images else [],
                'status': self.status,
                'report_time': self.report_time.strftime('%Y-%m-%d %H:%M:%S') if self.report_time else None,
                'assignTime': self.assign_time.strftime('%Y-%m-%d %H:%M:%S') if self.assign_time else None,
                'processTime': self.process_time.strftime('%Y-%m-%d %H:%M:%S') if self.process_time else None,
                'completeTime': self.complete_time.strftime('%Y-%m-%d %H:%M:%S') if self.complete_time else None,
                'handlerName': self.handler_name,
                'handlerPhone': self.handler_phone,
                'repairType': self.repair_type,
                'cost': float(self.cost) if self.cost else 0.00,
                'isPaid': bool(self.is_paid),
                'paymentTime': self.payment_time.strftime('%Y-%m-%d %H:%M:%S') if self.payment_time else None,
                'paymentMethod': self.payment_method,
                'notes': self.notes,
                'evaluationScore': self.evaluation_score,
                'evaluationContent': self.evaluation_content,
                'evaluationTime': self.evaluation_time.strftime('%Y-%m-%d %H:%M:%S') if self.evaluation_time else None,
                'evaluationImages': json.loads(self.evaluation_images) if self.evaluation_images else [],
                'isDeleted': bool(self.is_deleted),
                'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
                'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
            }
        except Exception as e:
            print(f"转换维修请求数据出错: {str(e)}")
            return {} 