from db import db

class DistrictInfo(db.Model):
    __tablename__ = 'district_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    community_id = db.Column(db.Integer, nullable=False, comment='所属社区ID')
    district_name = db.Column(db.String(100), nullable=False, comment='区域名称')
    district_number = db.Column(db.String(50), nullable=False, comment='区域编号')
    status = db.Column(db.Integer, nullable=False, default=1, comment='状态（1：启用，0：禁用）')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now(), comment='更新时间') 