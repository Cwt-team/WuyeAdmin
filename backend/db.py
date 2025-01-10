# db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# 创建一个示例模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    total_units = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    owners = db.relationship('Owner', backref='community', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'location': self.location,
            'totalUnits': self.total_units,
            'status': self.status,
            'createTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    id_card = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    remark = db.Column(db.String(200))
    owner_type = db.Column(db.String(20), nullable=False)
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'communityId': self.community_id,
            'room': self.room,
            'name': self.name,
            'gender': self.gender,
            'idCard': self.id_card,
            'phone': self.phone,
            'remark': self.remark,
            'ownerType': self.owner_type,
            'updateTime': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }
