from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy import desc
from backend.models.area_maintenance import CommunityReview
from backend.models.community_info import CommunityInfo
from backend.models.personal_info import PersonalInfo
from backend.db import db
from sqlalchemy.sql import text
import logging

community_review_bp = Blueprint('community_review', __name__)

@community_review_bp.route('/api/community-reviews', methods=['GET'])
def get_community_reviews():
    """获取社区评价列表"""
    # 获取查询参数
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    community_id = request.args.get('community')
    rating = request.args.get('rating')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    
    # 构建查询
    query = CommunityReview.query
    
    # 应用过滤条件
    if community_id:
        query = query.filter(CommunityReview.community_id == community_id)
    if rating:
        query = query.filter(CommunityReview.rating == rating)
    if start_date:
        query = query.filter(CommunityReview.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        # 添加一天以包含结束日期的所有记录
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        query = query.filter(CommunityReview.created_at <= end_datetime)
    
    # 按创建时间降序排序
    query = query.order_by(desc(CommunityReview.created_at))
    
    # 分页
    total = query.count()
    reviews = query.paginate(page=page, per_page=page_size, error_out=False)
    
    # 格式化结果
    result = {
        'items': [review.to_dict() for review in reviews.items],
        'total': total,
        'page': page,
        'pageSize': page_size
    }
    
    return jsonify(result)

@community_review_bp.route('/api/community-reviews/<int:review_id>/reply', methods=['POST'])
def reply_to_review(review_id):
    """回复社区评价"""
    data = request.json
    reply_content = data.get('reply')
    
    if not reply_content:
        return jsonify({'message': '回复内容不能为空'}), 400
    
    review = CommunityReview.query.get_or_404(review_id)
    review.reply = reply_content
    review.reply_time = datetime.now()
    review.status = 1  # 已回复
    
    try:
        db.session.commit()
        return jsonify({'message': '回复成功', 'review': review.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'回复失败: {str(e)}'}), 500

@community_review_bp.route('/api/community-reviews/<int:review_id>', methods=['GET'])
def get_review_detail(review_id):
    """获取评价详情"""
    review = CommunityReview.query.get_or_404(review_id)
    return jsonify(review.to_dict())

@community_review_bp.route('/api/reviews/communities', methods=['GET'])
def get_review_communities():
    """获取社区列表供筛选使用"""
    try:
        # 查询社区信息
        sql = text("""
            SELECT 
                id,
                community_name
            FROM community_info 
            ORDER BY id
        """)
        
        result = db.session.execute(sql)
        communities = result.fetchall()
        
        if not communities:
            logging.warning("未查询到社区数据")
            return jsonify([])
            
        logging.info(f"查询到 {len(communities)} 个社区")
        
        return jsonify([{
            'id': row.id,
            'community_name': row.community_name  # 确保返回社区名称
        } for row in communities])
        
    except Exception as e:
        logging.error(f"获取社区列表失败: {str(e)}")
        return jsonify({
            'error': '获取社区列表失败',
            'message': str(e)
        }), 500 