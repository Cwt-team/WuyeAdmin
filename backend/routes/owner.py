from flask import Blueprint, jsonify, request
from models.owner import OwnerInfo, OwnerPermission
from db import db
from datetime import datetime

owner_bp = Blueprint('owner', __name__)

@owner_bp.route('/api/owners', methods=['GET'])
def get_owners():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        name = request.args.get('name', '')
        phone = request.args.get('phone', '')
        house = request.args.get('house', '')
        
        query = OwnerInfo.query
        if name:
            query = query.filter(OwnerInfo.name.like(f'%{name}%'))
        if phone:
            query = query.filter(OwnerInfo.phone_number.like(f'%{phone}%'))
        if house:
            query = query.join(OwnerInfo.house).filter(
                db.or_(
                    HouseInfo.district_number.like(f'%{house}%'),
                    HouseInfo.building_number.like(f'%{house}%'),
                    HouseInfo.unit_number.like(f'%{house}%')
                )
            )
            
        total = query.count()
        owners = query.order_by(OwnerInfo.updated_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'owners': [owner.to_dict() for owner in owners],
            'total': total
        })
    except Exception as e:
        print(f"获取业主列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取业主列表失败'
        }), 500

@owner_bp.route('/api/owners/<int:owner_id>/permission', methods=['GET'])
def get_owner_permission(owner_id):
    try:
        permission = OwnerPermission.query.filter_by(owner_id=owner_id).first()
        if not permission:
            return jsonify({
                'success': False,
                'message': '未找到业主权限信息'
            }), 404
            
        return jsonify({
            'success': True,
            'data': permission.to_dict()
        })
    except Exception as e:
        print(f"获取业主权限失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取业主权限失败'
        }), 500

# 其他必要的路由方法(POST/PUT/DELETE)省略... 