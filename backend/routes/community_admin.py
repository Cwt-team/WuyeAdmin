from flask import Blueprint, jsonify, request
from models.community_admin import CommunityAdmin
from db import db

community_admin_bp = Blueprint('community_admin', __name__)

@community_admin_bp.route('/api/admins', methods=['GET'])
def get_admins():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        name = request.args.get('name', '')
        username = request.args.get('username', '')
        community_id = request.args.get('communityId', '')
        
        query = CommunityAdmin.query
        if name:
            query = query.filter(CommunityAdmin.other_name.like(f'%{name}%'))
        if username:
            query = query.filter(CommunityAdmin.account_number.like(f'%{username}%'))
        if community_id:
            query = query.filter(CommunityAdmin.community_id == community_id)
            
        total = query.count()
        admins = query.order_by(CommunityAdmin.created_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'success': True,
            'data': {
                'admins': [admin.to_dict() for admin in admins],
                'total': total
            }
        })
    except Exception as e:
        print(f"获取管理员列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取管理员列表失败'
        }), 500

@community_admin_bp.route('/api/admins', methods=['POST'])
def create_admin():
    try:
        data = request.get_json()
        admin = CommunityAdmin(
            community_id=data['communityId'],
            other_name=data['nickname'],
            account_number=data['username'],
            character_type=data['role'],
            phone_number=data['phone']
        )
        db.session.add(admin)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '添加成功'
        })
    except Exception as e:
        db.session.rollback()
        print(f"添加管理员失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '添加管理员失败'
        }), 500

@community_admin_bp.route('/api/admins/<int:admin_id>', methods=['PUT'])
def update_admin(admin_id):
    try:
        admin = CommunityAdmin.query.get(admin_id)
        if not admin:
            return jsonify({
                'success': False,
                'message': '管理员不存在'
            }), 404
            
        data = request.get_json()
        admin.community_id = data['communityId']
        admin.other_name = data['nickname']
        admin.account_number = data['username']
        admin.character_type = data['role']
        admin.phone_number = data['phone']
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '更新成功'
        })
    except Exception as e:
        db.session.rollback()
        print(f"更新管理员失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '更新管理员失败'
        }), 500

@community_admin_bp.route('/api/admins/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    try:
        admin = CommunityAdmin.query.get(admin_id)
        if not admin:
            return jsonify({
                'success': False,
                'message': '管理员不存在'
            }), 404
            
        db.session.delete(admin)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        db.session.rollback()
        print(f"删除管理员失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '删除管理员失败'
        }), 500 