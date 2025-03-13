import os
import pymysql
from dotenv import load_dotenv
import time

# 加载环境变量
load_dotenv()

# 数据库连接配置
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'wuye')

def add_building_unit_data():
    """查询现有社区和区域数据，并添加楼栋和单元数据"""
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
            
            print(f"找到 {len(communities)} 个社区")
            
            # 遍历每个社区
            for community_id, community_name in communities:
                print(f"\n处理社区: {community_name} (ID: {community_id})")
                
                # 查询该社区的区域数据
                cursor.execute("SELECT id, district_name, district_number FROM district_info WHERE community_id = %s AND status = 1", (community_id,))
                districts = cursor.fetchall()
                
                if not districts:
                    print(f"  社区 {community_name} 未找到区域数据，跳过")
                    continue
                
                print(f"  找到 {len(districts)} 个区域")
                
                # 遍历每个区域
                for district_id, district_name, district_number in districts:
                    print(f"  处理区域: {district_name} (ID: {district_id})")
                    
                    # 查询该区域是否已有楼栋数据
                    cursor.execute("SELECT COUNT(*) FROM building_info WHERE community_id = %s AND district_id = %s", (community_id, district_id))
                    building_count = cursor.fetchone()[0]
                    
                    if building_count > 0:
                        print(f"    区域 {district_name} 已有 {building_count} 个楼栋，跳过")
                        continue
                    
                    # 为该区域添加3个楼栋
                    for building_number in range(1, 4):
                        building_name = f"{district_name}{building_number}栋"
                        
                        # 插入楼栋数据
                        cursor.execute("""
                            INSERT INTO building_info 
                            (community_id, district_id, building_name, building_number, floor_count, unit_count, house_count, status, created_at, updated_at) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                        """, (
                            community_id, 
                            district_id, 
                            building_name, 
                            str(building_number), 
                            18,  # 楼层数
                            2,   # 单元数
                            36,  # 房屋数
                            1    # 状态
                        ))
                        
                        # 获取新插入的楼栋ID
                        building_id = cursor.lastrowid
                        
                        print(f"    添加楼栋: {building_name} (ID: {building_id})")
                        
                        # 为该楼栋添加2个单元
                        for unit_number in range(1, 3):
                            unit_name = f"{building_name}{unit_number}单元"
                            
                            # 插入单元数据
                            cursor.execute("""
                                INSERT INTO unit_info 
                                (community_id, district_id, building_id, unit_name, unit_number, house_count, status, created_at, updated_at) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                            """, (
                                community_id, 
                                district_id, 
                                building_id, 
                                unit_name, 
                                str(unit_number), 
                                18,  # 房屋数
                                1    # 状态
                            ))
                            
                            print(f"      添加单元: {unit_name} (ID: {cursor.lastrowid})")
                    
                    # 更新区域的楼栋数量
                    cursor.execute("UPDATE district_info SET building_count = building_count + 3 WHERE id = %s", (district_id,))
                    
                # 更新社区的楼栋数量
                cursor.execute("SELECT COUNT(*) FROM building_info WHERE community_id = %s", (community_id,))
                total_buildings = cursor.fetchone()[0]
                cursor.execute("UPDATE community_info SET building_count = %s WHERE id = %s", (total_buildings, community_id))
            
            # 提交事务
            connection.commit()
            
            # 验证数据
            cursor.execute("SELECT COUNT(*) FROM building_info")
            building_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM unit_info")
            unit_count = cursor.fetchone()[0]
            
            print(f"\n数据库中现有楼栋数量: {building_count}")
            print(f"数据库中现有单元数量: {unit_count}")
        
    except Exception as e:
        print(f"添加楼栋和单元数据失败: {str(e)}")
        if 'connection' in locals():
            connection.rollback()
    finally:
        # 关闭连接
        if 'connection' in locals():
            connection.close()
            print("数据库连接已关闭")

if __name__ == '__main__':
    add_building_unit_data() 