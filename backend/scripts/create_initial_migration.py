#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
为现有数据库创建初始迁移文件，标记所有表都已存在
这个脚本会创建一个新的迁移版本，将所有现有表标记为已创建
"""

import os
import sys
from pathlib import Path
import importlib
import uuid
from datetime import datetime
import re

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

def create_initial_migration():
    """创建初始迁移文件，将所有表标记为已存在"""
    print("正在创建初始迁移文件...")
    
    # 计算迁移文件路径
    migrations_dir = Path('../../migrations/versions')
    
    # 创建版本ID和时间戳
    revision_id = uuid.uuid4().hex[:12]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # 创建迁移文件名
    migration_filename = f"{timestamp}_{revision_id}_initial_database_structure.py"
    migration_path = migrations_dir / migration_filename
    
    # 迁移文件内容
    migration_content = f'''"""初始数据库结构

将所有已存在的表标记为已创建

Revision ID: {revision_id}
Revises: 
Create Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '{revision_id}'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### 所有表已存在，此处不需要创建 ###
    pass


def downgrade():
    # ### 因为没有实际创建表，所以也不需要删除 ###
    pass
'''
    
    # 写入文件
    with open(migration_path, 'w', encoding='utf-8') as f:
        f.write(migration_content)
        
    print(f"初始迁移文件已创建: {migration_path}")
    print("请运行: flask --app backend.migrations db stamp head")
    print("标记数据库为最新版本，后续变更将基于此迁移记录")

if __name__ == "__main__":
    create_initial_migration() 