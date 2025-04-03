from backend.db import db
from datetime import datetime


# 广告信息模型类（对应门禁设备内容管理表）
class Advertisement(db.Model):
    __tablename__ = 'door_machine_content_management'  # 门禁设备广告内容表

    # 主键ID（自增唯一标识）
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # 关联社区ID（外键指向community_info表）
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)

    # 广告标题（最大100字符，不可为空）
    title = db.Column(db.String(100), nullable=False)

    # 广告图片URL（存储图片路径，最大255字符）
    image_url = db.Column(db.String(255), nullable=False)

    # 广告方向（枚举horizontal/vertical，控制展示方式）
    orientation = db.Column(db.String(20), nullable=False)

    # 创建时间（自动记录数据创建时间）
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 更新时间（每次修改自动更新）
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now
    )

    def to_dict(self):
        """模型转字典方法（用于接口数据序列化）"""
        return {
            'id': self.id,
            'communityId': self.community_id,  # 社区ID驼峰式转换
            'title': self.title,
            'imageUrl': self.image_url,  # 图片地址字段格式转换
            'orientation': self.orientation,
            # 时间格式化为标准字符串（ISO 8601格式）
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }