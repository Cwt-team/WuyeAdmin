import os
import pymysql
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 加载环境变量
load_dotenv()

# 数据库连接配置
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'wuye')

def add_notification_examples():
    """添加房间通知示例数据"""
    try:
        # 连接数据库
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        print(f"成功连接到数据库 {DB_NAME}")
        
        with connection.cursor() as cursor:
            # 查询现有社区数据
            cursor.execute("SELECT id, community_name FROM community_info WHERE status = 1")
            communities = cursor.fetchall()
            
            if not communities:
                print("未找到社区数据，请先添加社区数据")
                return
            
            # 当前日期
            now = datetime.now()
            
            # 通知示例数据
            notifications = []
            
            # 为每个社区添加通知
            for community_id, community_name in communities:
                # 社区级通知
                notifications.append({
                    'community_id': community_id,
                    'district_number': None,
                    'building_number': None,
                    'unit_number': None,
                    'title': f'{community_name}物业费缴纳通知',
                    'content': f'请各位业主于{now.year}年12月31日前完成{now.year + 1}年第一季度物业费缴纳，感谢配合。',
                    'display_start_time': (now - timedelta(days=5)).strftime('%Y-%m-%d 00:00:00'),
                    'display_end_time': (now + timedelta(days=30)).strftime('%Y-%m-%d 23:59:59'),
                    'status': 1,
                    'created_by': 'admin'
                })
                
                # 查询该社区的区域数据
                cursor.execute("SELECT district_number FROM district_info WHERE community_id = %s AND status = 1", (community_id,))
                districts = cursor.fetchall()
                
                if districts:
                    # 区域级通知
                    district_number = districts[0][0]
                    notifications.append({
                        'community_id': community_id,
                        'district_number': district_number,
                        'building_number': None,
                        'unit_number': None,
                        'title': f'{community_name}{district_number}区绿化养护通知',
                        'content': f'{district_number}区绿化将于{now.year}年{now.month}月15日至{now.month}月20日进行春季养护，请业主避免在草坪休息。',
                        'display_start_time': (now - timedelta(days=2)).strftime('%Y-%m-%d 00:00:00'),
                        'display_end_time': (now + timedelta(days=15)).strftime('%Y-%m-%d 23:59:59'),
                        'status': 1,
                        'created_by': 'admin'
                    })
                    
                    # 查询该区域的楼栋数据
                    cursor.execute("""
                        SELECT building_number 
                        FROM building_info 
                        WHERE community_id = %s AND district_id = (
                            SELECT id FROM district_info WHERE community_id = %s AND district_number = %s
                        ) AND status = 1
                    """, (community_id, community_id, district_number))
                    buildings = cursor.fetchall()
                    
                    if buildings:
                        # 楼栋级通知
                        building_number = buildings[0][0]
                        notifications.append({
                            'community_id': community_id,
                            'district_number': district_number,
                            'building_number': building_number,
                            'unit_number': None,
                            'title': f'{community_name}{district_number}区{building_number}栋电梯维修通知',
                            'content': f'{district_number}区{building_number}栋电梯将于{now.year}年{now.month}月5日进行维修，预计维修时间为上午9:00至下午17:00，请业主做好准备。',
                            'display_start_time': (now - timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'),
                            'display_end_time': (now + timedelta(days=10)).strftime('%Y-%m-%d 23:59:59'),
                            'status': 1,
                            'created_by': 'admin'
                        })
                        
                        # 查询该楼栋的单元数据
                        cursor.execute("""
                            SELECT unit_number 
                            FROM unit_info 
                            WHERE community_id = %s AND district_id = (
                                SELECT id FROM district_info WHERE community_id = %s AND district_number = %s
                            ) AND building_id = (
                                SELECT id FROM building_info 
                                WHERE community_id = %s AND district_id = (
                                    SELECT id FROM district_info WHERE community_id = %s AND district_number = %s
                                ) AND building_number = %s
                            ) AND status = 1
                        """, (community_id, community_id, district_number, community_id, community_id, district_number, building_number))
                        units = cursor.fetchall()
                        
                        if units:
                            # 单元级通知
                            unit_number = units[0][0]
                            notifications.append({
                                'community_id': community_id,
                                'district_number': district_number,
                                'building_number': building_number,
                                'unit_number': unit_number,
                                'title': f'{community_name}{district_number}区{building_number}栋{unit_number}单元楼道清洁通知',
                                'content': f'{district_number}区{building_number}栋{unit_number}单元楼道将于{now.year}年{now.month}月10日进行深度清洁，请业主避免在此期间使用楼道。',
                                'display_start_time': now.strftime('%Y-%m-%d 00:00:00'),
                                'display_end_time': (now + timedelta(days=5)).strftime('%Y-%m-%d 23:59:59'),
                                'status': 1,
                                'created_by': 'admin'
                            })
            
            # 插入通知数据
            for notification in notifications:
                cursor.execute("""
                    INSERT INTO room_notification 
                    (community_id, district_number, building_number, unit_number, title, content, 
                     display_start_time, display_end_time, status, created_at, updated_at, created_by) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)
                """, (
                    notification['community_id'],
                    notification['district_number'],
                    notification['building_number'],
                    notification['unit_number'],
                    notification['title'],
                    notification['content'],
                    notification['display_start_time'],
                    notification['display_end_time'],
                    notification['status'],
                    notification['created_by']
                ))
                
                print(f"添加通知: {notification['title']}")
            
            # 提交事务
            connection.commit()
            
            # 验证数据
            cursor.execute("SELECT COUNT(*) FROM room_notification")
            notification_count = cursor.fetchone()[0]
            
            print(f"\n数据库中现有房间通知数量: {notification_count}")
        
    except Exception as e:
        print(f"添加房间通知示例数据失败: {str(e)}")
        if 'connection' in locals():
            connection.rollback()
    finally:
        # 关闭连接
        if 'connection' in locals():
            connection.close()
            print("数据库连接已关闭")

if __name__ == '__main__':
    add_notification_examples() 