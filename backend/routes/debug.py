from flask import Blueprint, jsonify
from backend.models.community_info import CommunityInfo
from backend.models.district_info import DistrictInfo
from backend.models.building_info import BuildingInfo
from backend.models.unit_info import UnitInfo
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/api/debug/database-status', methods=['GET'])
def check_database_status():
    try:
        result = {
            'status': 'ok',
            'tables': {}
        }
        
        # 检查社区表
        communities = CommunityInfo.query.all()
        result['tables']['community_info'] = {
            'count': len(communities),
            'sample': [c.to_dict() for c in communities[:3]] if communities else []
        }
        
        # 检查区域表
        districts = DistrictInfo.query.all()
        result['tables']['district_info'] = {
            'count': len(districts),
            'sample': [d.to_dict() for d in districts[:3]] if districts else []
        }
        
        # 检查楼栋表
        buildings = BuildingInfo.query.all()
        result['tables']['building_info'] = {
            'count': len(buildings),
            'sample': [b.to_dict() for b in buildings[:3]] if buildings else []
        }
        
        # 检查单元表
        units = UnitInfo.query.all()
        result['tables']['unit_info'] = {
            'count': len(units),
            'sample': [u.to_dict() for u in units[:3]] if units else []
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"数据库状态检查失败: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 