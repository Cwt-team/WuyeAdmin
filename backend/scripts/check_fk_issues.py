#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
检查外键约束问题的脚本
"""

import os
import sys
import pymysql
from backend.config import MYSQL_CONFIG

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

def check_fk_issues():
    """检查数据库中的外键约束问题"""
    print("正在检查外键约束问题...")
    
    # 连接到数据库
    conn = pymysql.connect(
        host=MYSQL_CONFIG['host'],
        port=MYSQL_CONFIG['port'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database'],
        charset=MYSQL_CONFIG['charset']
    )
    
    try:
        with conn.cursor() as cursor:
            # 检查community_notification表中的外键问题
            print("\n检查community_notification表中的外键问题:")
            cursor.execute("""
                SELECT cn.id, cn.community_id 
                FROM community_notification cn 
                LEFT JOIN community_info ci ON cn.community_id = ci.id 
                WHERE cn.community_id IS NOT NULL AND ci.id IS NULL
            """)
            invalid_records = cursor.fetchall()
            if invalid_records:
                print(f"发现{len(invalid_records)}条违反外键约束的记录:")
                for record in invalid_records:
                    print(f"  记录ID: {record[0]}, 无效的community_id: {record[1]}")
                # 提供修复建议
                print("\n修复建议: ")
                print("1. 删除这些记录:")
                print("   DELETE FROM community_notification WHERE id IN ({})".format(
                    ",".join(str(r[0]) for r in invalid_records)
                ))
                print("2. 或者设置这些记录的community_id为有效值:")
                cursor.execute("SELECT id FROM community_info LIMIT 1")
                valid_id = cursor.fetchone()
                if valid_id:
                    print(f"   UPDATE community_notification SET community_id = {valid_id[0]} WHERE id IN ({','.join(str(r[0]) for r in invalid_records)})")
            else:
                print("未发现违反外键约束的记录")
            
            # 检查其他表的外键问题
            # ... 类似的检查代码可以添加到这里

    finally:
        conn.close()

if __name__ == "__main__":
    check_fk_issues() 