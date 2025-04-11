# 从 db 模块中导入 SQLAlchemy 实例 db，用于定义数据模型
from backend.db import db
# 导入 datetime 模块中的 datetime 类，用于设置默认的日期和时间
from datetime import datetime


# 定义一个名为 CommunityNotification 的模型类，继承自 db.Model
# 该类对应数据库中的一张表，存储社区通知信息
class CommunityNotification(db.Model):
    # 指定数据库中对应的表名为 'community_notification'
    __tablename__ = 'community_notification'

    # 定义 id 字段，类型为 BigInteger，设为主键并且自增
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # 定义 community_id 字段，类型为 Integer，该字段为外键，
    # 关联 community_info 表中的 id 字段，且不能为空
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)

    # 定义 title 字段，类型为 String，长度限制为 100 字符，不能为空
    title = db.Column(db.String(100), nullable=False)

    # 定义 content 字段，类型为 Text，用于存储通知的具体内容，不能为空
    content = db.Column(db.Text, nullable=False)

    # 定义 display_start_time 字段，类型为 Date，用于存储通知开始显示的日期
    display_start_time = db.Column(db.Date)

    # 定义 display_end_time 字段，类型为 Date，用于存储通知结束显示的日期
    display_end_time = db.Column(db.Date)

    # 定义 created_at 字段，类型为 DateTime，不能为空，默认值为当前日期时间
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 定义 updated_at 字段，类型为 TIMESTAMP，不能为空，默认值为当前日期时间
    # 并在记录更新时自动更新该字段的值
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 定义一个实例方法 to_dict，将模型对象转换为字典格式，便于序列化（例如返回 JSON 数据）
    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'title': self.title,
            'content': self.content,
            # 如果 display_start_time 不为空，则格式化为 'YYYY-MM-DD' 字符串，否则返回 None
            'displayStartTime': self.display_start_time.strftime('%Y-%m-%d') if self.display_start_time else None,
            # 如果 display_end_time 不为空，则格式化为 'YYYY-MM-DD' 字符串，否则返回 None
            'displayEndTime': self.display_end_time.strftime('%Y-%m-%d') if self.display_end_time else None,
            # created_at 字段格式化为 'YYYY-MM-DD HH:MM:SS' 字符串
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
