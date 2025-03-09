from db import db
from datetime import datetime

class CommunityInfo(db.Model):
    """小区基础信息模型（对应社区信息表）"""
    __tablename__ = 'community_info'        #数据库表名
    
    id = db.Column(db.Integer, primary_key=True)                            #主键ID
    community_number = db.Column(db.String(20), nullable=False)             #小区唯一编号 CN001
    community_name = db.Column(db.String(100), nullable=False)              #小区全称   阳光花园
    community_city = db.Column(db.String(50), nullable=False)               #所在城市   上海市
    creation_time = db.Column(db.DateTime, nullable=False)                  #小区建档时间 2024-01-01 08:00:00
    is_enabled = db.Column(db.Integer, nullable=False)                      #启用状态   1
    management_machine_quantity = db.Column(db.Integer, nullable=False)     #管理机数量  5
    indoor_machine_quantity = db.Column(db.Integer, nullable=False)         #室内机数量  200
    access_card_type = db.Column(db.String(20), nullable=False)             #门禁卡类型  NFC
    app_record_face = db.Column(db.Integer, nullable=False)                 #APP人脸录入 1
    is_same_step = db.Column(db.Integer, nullable=False)                    #配置同步状态 1
    is_record_upload = db.Column(db.Integer, nullable=False)                #记录上传开关 1
    community_password = db.Column(db.String(32), nullable=False)           #密码 pwd123
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        """模型序列化方法（适配前端接口）

                字段命名规则：
                - 数据库蛇形命名 → 接口驼峰命名
                - 状态字段保持原始数值类型
                - 时间字段格式化为字符串
                """
        return {
            'id': self.id,
            'code': self.community_number,      # 编号字段重命名为code
            'name': self.community_name,
            'location': self.community_city,
            'createTime': self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),     # 时间格式化
            'isEnabled': self.is_enabled,
            'managerMachineCount': self.management_machine_quantity,
            'indoorMachineCount': self.indoor_machine_quantity,
            'accessCardType': self.access_card_type,
            'appRecordFace': self.app_record_face,
            'isSameStep': self.is_same_step,
            'isRecordUpload': self.is_record_upload
            # 注意：created_at和community_password未包含在输出中
        } 