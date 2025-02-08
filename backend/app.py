from flask import Flask, jsonify, request, session
from flask_cors import CORS
from db import db, init_db
from routes.community import community_bp

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # 允许跨域请求并支持 Cookie
    app.secret_key = 'your_secret_key'  # 用于 session 加密

    # 初始化数据库
    init_db(app)

    # 注册蓝图
    app.register_blueprint(community_bp)

    # 获取用户信息的API
    @app.route('/api/user-info', methods=['GET'])
    def get_user_info():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        return jsonify({'username': session['username']})

    # 退出登录的API
    @app.route('/api/logout', methods=['POST'])
    def logout():
        session.pop('username', None)
        return jsonify({'message': '已成功退出登录'})

    # 修改后的登录的API
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # 仅当用户名为 'admin' 且密码为 'password' 时登录成功
        if username == 'admin' and password == 'password':
            session['username'] = username
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'})

    @app.route('/api/owners/export-template', methods=['GET'])
    def export_owner_template():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        
        # Create CSV template
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        # Write header
        writer.writerow(['房间号', '姓名', '性别', '身份证号', '手机号', '备注', '业主类型'])
        
        # Create response
        response = app.response_class(
            response=output.getvalue(),
            status=200,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=owner_template.csv'}
        )
        return response

    @app.route('/api/owners/export', methods=['GET'])
    def export_owners():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        
        # Get filter parameters from request
        room = request.args.get('room')
        name = request.args.get('name')
        
        # Query owners
        from db import Owner
        query = Owner.query
        if room:
            query = query.filter(Owner.room.contains(room))
        if name:
            query = query.filter(Owner.name.contains(name))
        
        owners = query.all()
        
        # Create CSV
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        # Write header
        writer.writerow(['房间号', '姓名', '性别', '身份证号', '手机号', '备注', '业主类型', '更新时间'])
        # Write data
        for owner in owners:
            writer.writerow([
                owner.room,
                owner.name,
                owner.gender,
                owner.id_card,
                owner.phone,
                owner.remark,
                owner.owner_type,
                owner.update_time.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Create response
        response = app.response_class(
            response=output.getvalue(),
            status=200,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=owners_export.csv'}
        )
        return response

    @app.route('/api/owners/import', methods=['POST'])
    def import_owners():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        
        if 'file' not in request.files:
            return jsonify({'error': '未上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '未选择文件'}), 400
        
        try:
            import io
            import csv
            from db import db, Owner
            
            # Read and parse CSV
            stream = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
            reader = csv.reader(stream)
            
            # Skip header
            next(reader)
            
            # Process rows
            for row in reader:
                if len(row) != 7:
                    continue
                
                owner = Owner(
                    community_id=1,  # TODO: Get community ID from session
                    room=row[0],
                    name=row[1],
                    gender=row[2],
                    id_card=row[3],
                    phone=row[4],
                    remark=row[5],
                    owner_type=row[6]
                )
                db.session.add(owner)
            
            db.session.commit()
            return jsonify({'success': True, 'message': '导入成功'})
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'导入失败: {str(e)}'}), 500

    @app.route('/api/owner-applications', methods=['GET'])
    def get_owner_applications():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        
        # Get filter parameters
        area = request.args.get('area')
        building = request.args.get('building')
        name = request.args.get('name')
        phone = request.args.get('phone')
        
        # TODO: Implement actual filtering logic
        # For now return mock data
        return jsonify({
            'applications': [
                {
                    'id': 1,
                    'name': '王五',
                    'phone': '13800138000',
                    'area': 'A区',
                    'building': '1栋',
                    'status': 'pending',
                    'applyTime': '2024-08-01 10:00:00'
                }
            ],
            'total': 1
        })

    @app.route('/api/owner-applications/qrcode', methods=['GET'])
    def generate_qrcode():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        
        application_id = request.args.get('id')
        if not application_id:
            return jsonify({'error': '缺少申请ID'}), 400
        
        # TODO: Generate actual QR code
        # For now return mock data
        import base64
        from io import BytesIO
        from PIL import Image
        
        # Create a simple QR code image
        img = Image.new('RGB', (200, 200), color = (73, 109, 137))
        
        # Convert to bytes
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'qrcode': f'data:image/png;base64,{img_str}'
        })

    @app.errorhandler(500)
    def handle_500_error(error):
        print('Server Error:', error)  # 在控制台打印详细错误信息
        return jsonify({'error': 'Internal Server Error'}), 500

    return app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
