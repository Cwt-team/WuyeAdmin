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
        # 将当前 RoomNotification 对象转换为字典格式，便于序列化（例如转换为 JSON 数据返回给前端）
        return {
            'id': self.id,  # 返回通知的唯一标识 id
            'communityId': self.community_id,  # 返回所属社区的 ID
            'houseId': self.house_id,  # 返回关联房屋的 ID（如果有）
            'title': self.title,  # 返回通知标题
            'content': self.content,  # 返回通知内容
            # 如果 display_start_time 不为空，则使用 strftime 格式化为 'YYYY-MM-DD' 字符串；否则返回 None
            'displayStartTime': self.display_start_time.strftime('%Y-%m-%d') if self.display_start_time else None,
            # 如果 display_end_time 不为空，则使用 strftime 格式化为 'YYYY-MM-DD' 字符串；否则返回 None
            'displayEndTime': self.display_end_time.strftime('%Y-%m-%d') if self.display_end_time else None,
            # 将 created_at 字段格式化为 'YYYY-MM-DD HH:MM:SS' 格式的字符串返回
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
