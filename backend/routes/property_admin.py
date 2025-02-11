from flask import Blueprint, jsonify, request
from models.property_admin import PropertyAdmin
from db import db

property_admin_bp = Blueprint('property_admin', __name__)

@property_admin_bp.route('/api/property-admins', methods=['GET'])
def get_property_admins():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        name = request.args.get('name', '')
        phone = request.args.get('phone', '')
        
        query = PropertyAdmin.query
        if name:
            query = query.filter(PropertyAdmin.name.like(f'%{name}%'))
        if phone:
            query = query.filter(PropertyAdmin.phone_number.like(f'%{phone}%'))
            
        total = query.count()
        admins = query.order_by(PropertyAdmin.updated_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'admins': [admin.to_dict() for admin in admins],
            'total': total
        })
    except Exception as e:
        print(f"获取物业管理员列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取物业管理员列表失败'
        }), 500

@property_admin_bp.route('/api/property-admins', methods=['POST'])
def create_property_admin():
    try:
        data = request.get_json()
        admin = PropertyAdmin(
            community_id=data['communityId'],
            name=data['name'],
            phone_number=data['phone'],
            remark=data.get('remark', ''),
            face_image=data.get('faceImage', ''),
            face_status=data.get('faceStatus', 0)
        )
        db.session.add(admin)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '添加成功'
        })
    except Exception as e:
        db.session.rollback()
        print(f"添加物业管理员失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '添加物业管理员失败'
        }), 500

@property_admin_bp.route('/api/property-admins/<int:admin_id>', methods=['PUT'])
def update_property_admin(admin_id):
    try:
        admin = PropertyAdmin.query.get(admin_id)
        if not admin:
            return jsonify({
                'success': False,
                'message': '物业管理员不存在'
            }), 404
            
        data = request.get_json()
        admin.community_id = data['communityId']
        admin.name = data['name']
        admin.phone_number = data['phone']
        admin.remark = data.get('remark', admin.remark)
        admin.face_image = data.get('faceImage', admin.face_image)
        admin.face_status = data.get('faceStatus', admin.face_status)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '更新成功'
        })
    except Exception as e:
        db.session.rollback()
        print(f"更新物业管理员失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '更新物业管理员失败'
        }), 500

@property_admin_bp.route('/api/property-admins/<int:admin_id>', methods=['DELETE'])
def delete_property_admin(admin_id):
    try:
        admin = PropertyAdmin.query.get(admin_id)
        if not admin:
            return jsonify({
                'success': False,
                'message': '物业管理员不存在'
            }), 404
            
        db.session.delete(admin)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        db.session.rollback()
        print(f"删除物业管理员失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '删除物业管理员失败'
        }), 500 