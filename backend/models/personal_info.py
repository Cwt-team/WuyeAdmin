from db import db
from datetime import datetime

class PersonalInfo(db.Model):
    """用户个人信息模型（对应个人基础信息表）"""
    __tablename__ = 'personal_info' # 数据库表名
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)                                 #主键ID
    account_number = db.Column(db.String(50), unique=True, nullable=False)                              #登录账号（唯一标识）
    nickname = db.Column(db.String(50))                                                                 #用户昵称（可空）
    phone_number = db.Column(db.String(20), unique=True)                                                #手机号码（带国际区号格式）
    email = db.Column(db.String(100), unique=True)                                                      #电子邮箱（需符合邮箱格式）
    profile_picture_path = db.Column(db.String(200))                                                    #头像路径（支持云存储URL）
    password = db.Column(db.String(50), nullable=False)                                                 #登录密码（建议使用BCrypt加密）
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)                           #账户创建时间
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)   #最后更新时间

    def to_dict(self):
        """模型序列化方法（用于接口响应）

                安全注意事项：
                - 排除敏感字段：密码及时间戳字段
                - 字段命名转换：蛇形命名转驼峰式
                """
        return {
            'id': self.id,
            'accountNumber': self.account_number,
            'nickname': self.nickname,
            'phoneNumber': self.phone_number,
            'email': self.email,
            'profilePicturePath': self.profile_picture_path
        } 