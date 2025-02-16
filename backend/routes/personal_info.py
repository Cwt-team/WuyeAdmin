from flask import Blueprint, jsonify, request, session
from models.personal_info import PersonalInfo
from db import db

personal_info_bp = Blueprint('personal_info', __name__)

@personal_info_bp.route('/api/personal-info', methods=['GET'])
def get_personal_info():
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        user = PersonalInfo.query.filter_by(username=session['username']).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        return jsonify(user.to_dict())
    except Exception as e:
        print(f"获取个人信息失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@personal_info_bp.route('/api/personal-info', methods=['POST'])
def update_personal_info():
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        data = request.json
        user = PersonalInfo.query.filter_by(username=session['username']).first()
        
        if 'name' in data:
            user.name = data['name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'email' in data:
            user.email = data['email']
            
        db.session.commit()
        return jsonify({'message': '更新成功'})
    except Exception as e:
        db.session.rollback()
        print(f"更新个人信息失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@personal_info_bp.route('/api/change-password', methods=['POST'])
def change_password():
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        data = request.json
        user = PersonalInfo.query.filter_by(account_number=session['username']).first()
        
        user.password = data['newPassword']  # 直接设置新密码
        db.session.commit()
        
        return jsonify({'message': '密码修改成功'})
    except Exception as e:
        db.session.rollback()
        print(f"修改密码失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 