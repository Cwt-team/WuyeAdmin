#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
修复外键约束问题的脚本
"""

import os
import sys
import pymysql
from backend.config import MYSQL_CONFIG

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

def fix_fk_issues():
    """修复数据库中的外键约束问题"""
    print("正在修复外键约束问题...")
    
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
            # 1. 修复community_notification表的外键问题
            print("\n修复community_notification表的外键问题:")
            # 先找出一个有效的community_id
            cursor.execute("SELECT id FROM community_info LIMIT 1")
            valid_community = cursor.fetchone()
            
            if valid_community:
                valid_community_id = valid_community[0]
                
                # 找出所有无效的community_id记录
                cursor.execute("""
                    SELECT cn.id
                    FROM community_notification cn 
                    LEFT JOIN community_info ci ON cn.community_id = ci.id 
                    WHERE cn.community_id IS NOT NULL AND ci.id IS NULL
                """)
                invalid_records = [str(r[0]) for r in cursor.fetchall()]
                
                if invalid_records:
                    # 更新无效记录为有效的community_id
                    update_sql = f"UPDATE community_notification SET community_id = {valid_community_id} WHERE id IN ({','.join(invalid_records)})"
                    print(f"执行: {update_sql}")
                    cursor.execute(update_sql)
                    conn.commit()
                    print(f"已更新{cursor.rowcount}条记录")
                else:
                    print("未发现无效记录")
            else:
                print("未找到有效的community_id，无法修复")
            
            # 如果有其他表需要修复，可以在这里添加类似代码
            
    finally:
        conn.close()
    
    print("修复完成！")

if __name__ == "__main__":
    fix_fk_issues() 