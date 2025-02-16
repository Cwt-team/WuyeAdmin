from db import db
from datetime import datetime

class PersonalInfo(db.Model):
    __tablename__ = 'personal_info'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    account_number = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    phone_number = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True)
    profile_picture_path = db.Column(db.String(200))
    password = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'accountNumber': self.account_number,
            'nickname': self.nickname,
            'phoneNumber': self.phone_number,
            'email': self.email,
            'profilePicturePath': self.profile_picture_path
        } 