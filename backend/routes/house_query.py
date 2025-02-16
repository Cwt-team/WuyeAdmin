from flask import Blueprint, jsonify
from models.house import HouseInfo
from db import db

house_query_bp = Blueprint('house_query', __name__)

@house_query_bp.route('/api/areas', methods=['GET'])
def get_areas():
    try:
        # 获取所有区域信息
        areas = db.session.query(HouseInfo.district_number)\
            .filter(HouseInfo.district_number.isnot(None))\
            .distinct()\
            .all()
        
        return jsonify([
            {'value': area[0], 'label': f'{area[0]}区'} 
            for area in areas if area[0]
        ])
    except Exception as e:
        print(f"获取区域信息失败: {str(e)}")
        return jsonify([])

@house_query_bp.route('/api/buildings', methods=['GET'])
def get_buildings():
    try:
        # 获取所有楼栋信息
        buildings = db.session.query(HouseInfo.building_number)\
            .filter(HouseInfo.building_number.isnot(None))\
            .distinct()\
            .all()
        
        return jsonify([
            {'value': building[0], 'label': f'{building[0]}栋'} 
            for building in buildings if building[0]
        ])
    except Exception as e:
        print(f"获取楼栋信息失败: {str(e)}")
        return jsonify([])

@house_query_bp.route('/api/units', methods=['GET'])
def get_units():
    try:
        # 获取所有单元信息
        units = db.session.query(HouseInfo.unit_number)\
            .filter(HouseInfo.unit_number.isnot(None))\
            .distinct()\
            .all()
        
        return jsonify([
            {'value': unit[0], 'label': f'{unit[0]}单元'} 
            for unit in units if unit[0]
        ])
    except Exception as e:
        print(f"获取单元信息失败: {str(e)}")
        return jsonify([]) 