from backend.db import db  # 使用绝对导入
from datetime import datetime  # 导入 datetime 模块，用于获取当前时间
from backend.models.community_info import CommunityInfo  # 显式导入CommunityInfo


# 定义一个名为 HouseInfo 的数据模型类，继承自 SQLAlchemy 的 db.Model
class HouseInfo(db.Model):
    __tablename__ = 'house_info'  # 指定数据库中对应的表名为 "house_info"

    # 添加extend_existing=True以解决元数据冲突
    __table_args__ = {'extend_existing': True}

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
    community = db.relationship('CommunityInfo', backref=db.backref('houses', lazy='dynamic'))

    # 自引用关联关系：关联同一模型 HouseInfo，用于表示父子房屋关系
    # remote_side=[id] 指定外键关联的目标字段为当前表的 id
    # backref='children' 意味着在父房屋对象上可以通过 children 属性访问其所有子房屋信息
    parent = db.relationship('HouseInfo', remote_side=[id], backref='children')

    # 定义一个实例方法，将对象转换成字典格式，便于序列化（如返回 JSON 数据）
    def to_dict(self):
        # 根据不同层级计算实际的子节点数量
        children_count = 0
        if self.house_level == 1:  # 区级，统计下属楼栋数
            children_count = HouseInfo.query.filter_by(
                parent_id=self.id,
                house_level=2  # 楼栋级
            ).count()
        elif self.house_level == 2:  # 楼栋级，统计下属单元数
            children_count = HouseInfo.query.filter_by(
                parent_id=self.id,
                house_level=3  # 单元级
            ).count()
        elif self.house_level == 3:  # 单元级，统计下属房间数
            children_count = HouseInfo.query.filter_by(
                parent_id=self.id,
                house_level=4  # 房间级
            ).count()

        return {
            'id': self.id,
            'communityId': self.community_id,
            'districtNumber': self.district_number,
            'buildingNumber': self.building_number,
            'unitNumber': self.unit_number,
            'roomNumber': self.room_number,
            'fullName': self.house_full_name,
            'level': self.house_level,
            'parentId': self.parent_id,
            'createTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'count': children_count  # 使用实际计算的子节点数量
        }
