from backend.db import db
from datetime import datetime
from backend.models.house import HouseInfo  # 改为使用完整的导入路径


# 报警记录模型类（对应数据库alarm_record表）
class AlarmRecord(db.Model):
    __tablename__ = 'alarm_record'  # 数据库表名

    # 主键ID（自增大整数类型）
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # 所属社区ID（外键关联community_info表的id字段）
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)

    # 关联房屋ID（外键关联house_info表的id字段）
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'), nullable=False)

    # 报警类型（字符串类型，如烟雾报警、入侵报警等）
    alarm_type = db.Column(db.String(50), nullable=False)

    # 首次报警时间（日期时间类型，不可为空）
    first_alarm_time = db.Column(db.DateTime, nullable=False)

    # 最近报警时间（日期时间类型，记录最后一次触发时间）
    latest_alarm_time = db.Column(db.DateTime)

    # 报警描述（文本类型，详细说明报警情况）
    alarm_description = db.Column(db.Text)

    # 报警状态（枚举类型：待处理/已解决/处理中，默认待处理）
    alarm_status = db.Column(
        db.Enum('Pending', 'Resolved', 'Processing'),
        nullable=False,
        default='Pending'
    )

    # 记录创建时间（自动设置为记录插入时间）
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 记录更新时间（每次更新自动设置为当前时间）
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now
    )

    # 关联关系 - 与HouseInfo模型的一对多关系
    # 通过house属性可访问关联的房屋对象
    # HouseInfo模型可通过alarm_records属性访问关联的报警记录
    house = db.relationship('HouseInfo', backref='alarm_records')

    def to_dict(self):
        """将模型实例转换为字典格式（用于API响应）"""
        return {
            'id': self.id,
            'communityId': self.community_id,
            'houseId': self.house_id,
            # 获取关联房屋的完整名称（如存在）
            'houseName': self.house.house_full_name if self.house else None,
            'alarmType': self.alarm_type,
            # 格式化时间为字符串（YYYY-MM-DD HH:MM:SS）
            'firstAlarmTime': self.first_alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
            # 处理可能为空的最近报警时间
            'latestAlarmTime': self.latest_alarm_time.strftime('%Y-%m-%d %H:%M:%S')
            if self.latest_alarm_time else None,
            'alarmDescription': self.alarm_description,
            'alarmStatus': self.alarm_status
        }