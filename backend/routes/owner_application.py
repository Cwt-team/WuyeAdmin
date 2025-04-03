from flask import Blueprint, jsonify, request
from models.owner_application import OwnerApplication
from backend.models import HouseInfo
from db import db
from datetime import datetime

owner_application_bp = Blueprint('owner_application', __name__)

@owner_application_bp.route('/api/owner-applications', methods=['GET'])
def get_applications():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        area = request.args.get('area', '')
        building = request.args.get('building', '')
        unit = request.args.get('unit', '')
        name = request.args.get('name', '')
        
        query = OwnerApplication.query
        
        if area:
            query = query.join(HouseInfo).filter(HouseInfo.district_number == area)
        if building:
            query = query.join(HouseInfo).filter(HouseInfo.building_number == building)
        if unit:
            query = query.join(HouseInfo).filter(HouseInfo.unit_number == unit)
        if name:
            query = query.filter(
                db.or_(
                    OwnerApplication.name.like(f'%{name}%'),
                    OwnerApplication.phone_number.like(f'%{name}%')
                )
            )
            
        total = query.count()
        applications = query.order_by(OwnerApplication.application_time.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'applications': [app.to_dict() for app in applications],
            'total': total
        })
    except Exception as e:
        print(f"获取业主申请列表失败: {str(e)}")
        return jsonify({
            'applications': [],
            'total': 0
        })

@owner_application_bp.route('/api/owner-applications/<int:id>/approve', methods=['POST'])
def approve_application(id):
    try:
        application = OwnerApplication.query.get_or_404(id)
        application.application_status = 'Approved'
        application.updated_at = datetime.now()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'审批失败: {str(e)}'
        }), 500

@owner_application_bp.route('/api/owner-applications/<int:id>/return', methods=['POST'])
def return_application(id):
    try:
        data = request.get_json()
        application = OwnerApplication.query.get_or_404(id)
        application.application_status = 'Returned'
        application.callback_message = data.get('reason')
        application.updated_at = datetime.now()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'打回失败: {str(e)}'
        }), 500

@owner_application_bp.route('/api/owner-applications/<int:id>', methods=['DELETE'])
def delete_application(id):
    try:
        application = OwnerApplication.query.get_or_404(id)
        db.session.delete(application)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 500 