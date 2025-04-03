from flask import Blueprint, jsonify, request
from backend.models.call_record import CallRecord
from backend.db import db
from datetime import datetime

call_record_bp = Blueprint('call_record', __name__)

@call_record_bp.route('/api/call-records', methods=['GET'])
def get_call_records():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        community_id = request.args.get('communityId')
        district = request.args.get('district')
        building = request.args.get('building')
        unit = request.args.get('unit')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        query = CallRecord.query
        
        if community_id:
            query = query.filter(CallRecord.community_id == community_id)
            
        # 根据房屋信息筛选
        if any([district, building, unit]):
            query = query.join(CallRecord.house)
            if district:
                query = query.filter(CallRecord.house.has(district=district))
            if building:
                query = query.filter(CallRecord.house.has(building=building))
            if unit:
                query = query.filter(CallRecord.house.has(unit=unit))
                
        if start_date:
            query = query.filter(CallRecord.call_start_time >= start_date)
        if end_date:
            query = query.filter(CallRecord.call_start_time <= end_date)
            
        total = query.count()
        records = query.order_by(CallRecord.call_start_time.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'records': [record.to_dict() for record in records],
            'total': total
        })
        
    except Exception as e:
        print(f"获取呼叫记录列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 