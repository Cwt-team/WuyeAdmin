from db import db  # 从自定义的 db 模块中导入 SQLAlchemy 实例，用于数据库操作
from datetime import datetime  # 导入 datetime 模块，用于获取当前时间


# 定义一个名为 HouseInfo 的数据模型类，继承自 SQLAlchemy 的 db.Model
class HouseInfo(db.Model):
    __tablename__ = 'house_info'  # 指定数据库中对应的表名为 "house_info"

    # 定义字段 id：整型，主键
    id = db.Column(db.Integer, primary_key=True)

    # 定义字段 community_id：整型，外键，关联到 community_info 表的 id 字段，不能为空
    community_id = db.Column(db.Integer, db.ForeignKey('community_info.id'), nullable=False)

    # 定义区域编号字段，类型为字符串，最大长度 10
    district_number = db.Column(db.String(10))

    # 定义楼栋编号字段，类型为字符串，最大长度 10
    building_number = db.Column(db.String(10))

    # 定义单元编号字段，类型为字符串，最大长度 10
    unit_number = db.Column(db.String(10))

    # 定义房间号字段，类型为字符串，最大长度 10
    room_number = db.Column(db.String(10))

    # 定义完整房屋名称字段，类型为字符串，最大长度 100，不能为空
    house_full_name = db.Column(db.String(100), nullable=False)

    # 定义房屋层级字段，类型为整型，不能为空
    house_level = db.Column(db.Integer, nullable=False)

    # 定义父房屋 ID 字段，类型为整型，外键，关联到本表的 id 字段，用于自引用关系（表示上级房屋）
    parent_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))

    # 定义创建时间字段，类型为 DateTime，默认值为当前时间
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关联关系：关联 CommunityInfo 模型，表示当前房屋所属的社区
    # backref='houses' 意味着在 CommunityInfo 对象上可以通过 houses 属性访问该社区下的所有房屋信息
    community = db.relationship('CommunityInfo', backref='houses')

    # 自引用关联关系：关联同一模型 HouseInfo，用于表示父子房屋关系
    # remote_side=[id] 指定外键关联的目标字段为当前表的 id
    # backref='children' 意味着在父房屋对象上可以通过 children 属性访问其所有子房屋信息
    parent = db.relationship('HouseInfo', remote_side=[id], backref='children')

    # 定义一个实例方法，将对象转换成字典格式，便于序列化（如返回 JSON 数据）
    def to_dict(self):
        return {
            'id': self.id,  # 房屋的主键 ID
            'communityId': self.community_id,  # 所属社区的 ID
            'districtNumber': self.district_number,  # 区号
            'buildingNumber': self.building_number,  # 楼栋号
            'unitNumber': self.unit_number,  # 单元号
            'roomNumber': self.room_number,  # 房间号
            'fullName': self.house_full_name,  # 房屋的完整名称
            'level': self.house_level,  # 房屋层级（例如区、栋、单元）
            'parentId': self.parent_id,  # 父级房屋的 ID
            'createTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化后的创建时间
            # 如果当前房屋有子房屋，则返回子房屋数量，否则返回 0
            'count': len(self.children) if self.children else 0
        }
