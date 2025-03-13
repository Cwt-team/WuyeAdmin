from flask import Blueprint, jsonify, request
from models.area_maintenance import MaintenanceRequest, CommunityReview, ComplaintSuggestion
from db import db
from datetime import datetime

area_maintenance_bp = Blueprint('area_maintenance', __name__)

@area_maintenance_bp.route('/api/maintenance-requests', methods=['GET'])
def get_maintenance_requests():
    try:
        community_id = request.args.get('communityId')
        district_id = request.args.get('districtId')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))

        query = MaintenanceRequest.query
        if community_id:
            query = query.filter(MaintenanceRequest.community_id == community_id)
        if district_id:
            query = query.filter(MaintenanceRequest.district_id == district_id)
        if status:
            query = query.filter(MaintenanceRequest.status == status)

        total = query.count()
        requests = query.offset((page - 1) * size).limit(size).all()

        return jsonify({
            'total': total,
            'items': [req.to_dict() for req in requests]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@area_maintenance_bp.route('/api/community-reviews', methods=['GET'])
def get_community_reviews():
    try:
        community_id = request.args.get('communityId')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))

        query = CommunityReview.query
        if community_id:
            query = query.filter(CommunityReview.community_id == community_id)

        total = query.count()
        reviews = query.offset((page - 1) * size).limit(size).all()

        return jsonify({
            'total': total,
            'items': [review.to_dict() for review in reviews]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@area_maintenance_bp.route('/api/complaint-suggestions', methods=['GET'])
def get_complaint_suggestions():
    try:
        community_id = request.args.get('communityId')
        type = request.args.get('type')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))

        query = ComplaintSuggestion.query
        if community_id:
            query = query.filter(ComplaintSuggestion.community_id == community_id)
        if type:
            query = query.filter(ComplaintSuggestion.type == type)
        if status:
            query = query.filter(ComplaintSuggestion.status == status)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return jsonify({
            'total': total,
            'items': [item.to_dict() for item in items]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 