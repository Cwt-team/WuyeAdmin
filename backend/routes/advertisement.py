from flask import Blueprint, jsonify, request
from models.advertisement import Advertisement
from db import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime

advertisement_bp = Blueprint('advertisement', __name__)

UPLOAD_FOLDER = 'uploads/advertisements'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@advertisement_bp.route('/api/advertisements', methods=['GET'])
def get_advertisements():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        title = request.args.get('title')
        orientation = request.args.get('orientation')
        
        query = Advertisement.query
        
        if title:
            query = query.filter(Advertisement.title.like(f'%{title}%'))
        if orientation:
            query = query.filter(Advertisement.orientation == orientation)
            
        total = query.count()
        advertisements = query.order_by(Advertisement.created_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'records': [ad.to_dict() for ad in advertisements],
            'total': total
        })
        
    except Exception as e:
        print(f"获取广告列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@advertisement_bp.route('/api/advertisements', methods=['POST'])
def create_advertisement():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有文件上传'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            advertisement = Advertisement(
                community_id=request.form.get('communityId'),
                title=request.form.get('title'),
                image_url=f'/uploads/advertisements/{filename}',
                orientation=request.form.get('orientation', 'horizontal')
            )
            
            db.session.add(advertisement)
            db.session.commit()
            
            return jsonify({'message': '创建成功', 'data': advertisement.to_dict()})
            
    except Exception as e:
        db.session.rollback()
        print(f"创建广告失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@advertisement_bp.route('/api/advertisements/<int:ad_id>', methods=['DELETE'])
def delete_advertisement(ad_id):
    try:
        advertisement = Advertisement.query.get(ad_id)
        if not advertisement:
            return jsonify({'error': '广告不存在'}), 404
            
        # 删除图片文件
        if advertisement.image_url:
            file_path = os.path.join(os.getcwd(), advertisement.image_url.lstrip('/'))
            if os.path.exists(file_path):
                os.remove(file_path)
                
        db.session.delete(advertisement)
        db.session.commit()
        
        return jsonify({'message': '删除成功'})
        
    except Exception as e:
        db.session.rollback()
        print(f"删除广告失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 