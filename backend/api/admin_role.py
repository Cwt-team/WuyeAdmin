from flask import Blueprint, jsonify, request
from models import AdminRole
from db import db

admin_role_bp = Blueprint('admin_role', __name__)

@admin_role_bp.route('/api/admin-roles', methods=['GET'])
def get_admin_roles():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        search = request.args.get('search', '')
        
        query = AdminRole.query
        if search:
            query = query.filter(AdminRole.role_name.like(f'%{search}%'))
            
        total = query.count()
        roles = query.order_by(AdminRole.sort_number)\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'code': 200,
            'data': {
                'list': [role.to_dict() for role in roles],
                'total': total
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取角色列表失败: {str(e)}'
        })

@admin_role_bp.route('/api/admin-roles', methods=['POST'])
def create_admin_role():
    try:
        data = request.get_json()
        role = AdminRole(
            role_name=data['name'],
            sort_number=data['sortNo'],
            description=data.get('description', '')
        )
        db.session.add(role)
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': '添加成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'添加角色失败: {str(e)}'
        })

@admin_role_bp.route('/api/admin-roles/<int:role_id>', methods=['PUT'])
def update_admin_role(role_id):
    try:
        role = AdminRole.query.get(role_id)
        if not role:
            return jsonify({
                'code': 404,
                'message': '角色不存在'
            })
            
        data = request.get_json()
        role.role_name = data['name']
        role.sort_number = data['sortNo']
        role.description = data.get('description', '')
        
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': '更新成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'更新角色失败: {str(e)}'
        })

@admin_role_bp.route('/api/admin-roles/<int:role_id>', methods=['DELETE'])
def delete_admin_role(role_id):
    try:
        role = AdminRole.query.get(role_id)
        if not role:
            return jsonify({
                'code': 404,
                'message': '角色不存在'
            })
            
        db.session.delete(role)
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': '删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'删除角色失败: {str(e)}'
        }) 