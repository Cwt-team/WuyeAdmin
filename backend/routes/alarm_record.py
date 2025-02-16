from flask import Blueprint, jsonify, request
from models.alarm_record import AlarmRecord
from models.house import HouseInfo
from db import db
from datetime import datetime

alarm_record_bp = Blueprint('alarm_record', __name__)

@alarm_record_bp.route('/api/alarm-records', methods=['GET'])
def get_alarm_records():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        community_id = request.args.get('communityId')
        district = request.args.get('district')
        building = request.args.get('building')
        unit = request.args.get('unit')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        query = AlarmRecord.query.join(AlarmRecord.house)
        
        if community_id:
            query = query.filter(AlarmRecord.community_id == community_id)
        if district:
            query = query.filter(HouseInfo.district == district)
        if building:
            query = query.filter(HouseInfo.building == building)
        if unit:
            query = query.filter(HouseInfo.unit == unit)
        if start_date:
            query = query.filter(AlarmRecord.first_alarm_time >= start_date)
        if end_date:
            query = query.filter(AlarmRecord.first_alarm_time <= end_date)
            
        total = query.count()
        records = query.order_by(AlarmRecord.first_alarm_time.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'records': [record.to_dict() for record in records],
            'total': total
        })
        
    except Exception as e:
        print(f"获取报警记录列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500