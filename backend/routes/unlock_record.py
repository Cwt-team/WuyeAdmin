from flask import Blueprint, jsonify, request
from models.unlock_record import UnlockRecord
from db import db
from datetime import datetime

unlock_record_bp = Blueprint('unlock_record', __name__)

@unlock_record_bp.route('/api/unlock-records', methods=['GET'])
def get_unlock_records():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        community_id = request.args.get('communityId')
        district = request.args.get('district')
        building = request.args.get('building')
        unit = request.args.get('unit')
        device_type = request.args.get('deviceType')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        query = UnlockRecord.query
        
        if community_id:
            query = query.filter(UnlockRecord.community_id == community_id)
        if device_type:
            query = query.filter(UnlockRecord.device_type == device_type)
            
        # 根据房屋信息筛选
        if any([district, building, unit]):
            query = query.join(UnlockRecord.house)
            if district:
                query = query.filter(UnlockRecord.house.has(district=district))
            if building:
                query = query.filter(UnlockRecord.house.has(building=building))
            if unit:
                query = query.filter(UnlockRecord.house.has(unit=unit))
                
        if start_date:
            query = query.filter(UnlockRecord.unlocking_time >= start_date)
        if end_date:
            query = query.filter(UnlockRecord.unlocking_time <= end_date)
            
        total = query.count()
        records = query.order_by(UnlockRecord.unlocking_time.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'records': [record.to_dict() for record in records],
            'total': total
        })
        
    except Exception as e:
        print(f"获取开锁记录列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500