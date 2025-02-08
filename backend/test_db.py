import pymysql
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MYSQL_CONFIG

def test_db_connection():
    """测试数据库连接"""
    try:
        # 创建连接
        conn = pymysql.connect(**MYSQL_CONFIG)
        print("数据库连接成功！")
        
        # 测试查询
        with conn.cursor() as cursor:
            # 测试查询community_info表
            cursor.execute("SELECT COUNT(*) FROM community_info")
            count = cursor.fetchone()[0]
            print(f"community_info表中共有{count}条记录")
            
            # 测试查询admin_role表
            cursor.execute("SELECT COUNT(*) FROM admin_role")
            count = cursor.fetchone()[0]
            print(f"admin_role表中共有{count}条记录")
            
        conn.close()
        print("数据库连接测试完成！")
        return True
        
    except Exception as e:
        print(f"数据库连接失败：{str(e)}")
        return False

if __name__ == "__main__":
    test_db_connection() 