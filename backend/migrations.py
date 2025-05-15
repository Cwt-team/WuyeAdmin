#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库迁移管理脚本
使用方法:
1. 初始化迁移仓库：flask --app backend.migrations db init
2. 创建迁移脚本：flask --app backend.migrations db migrate -m "迁移说明"
3. 应用迁移：flask --app backend.migrations db upgrade
4. 查看迁移历史：flask --app backend.migrations db history
5. 回滚迁移：flask --app backend.migrations db downgrade
"""

import os
import sys
from flask import Flask

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# 导入应用和数据库
from backend import create_app
from backend.db import db, migrate

# 创建应用实例
app = create_app()

# 确保所有模型都被导入，这样Flask-Migrate才能检测到它们
from backend.models.community_info import CommunityInfo
from backend.models.house import HouseInfo
from backend.models.owner import OwnerInfo
from backend.models.alarm_record import AlarmRecord
from backend.models.housing_application import HousingApplication
from backend.models.maintenance_request import MaintenanceRequest
from backend.models.community_notification import CommunityNotification

if __name__ == '__main__':
    print("""
请使用以下命令来管理数据库迁移：
初始化迁移仓库：flask --app backend.migrations db init
创建迁移脚本：flask --app backend.migrations db migrate -m "迁移说明"
应用迁移：flask --app backend.migrations db upgrade
查看迁移历史：flask --app backend.migrations db history
回滚迁移：flask --app backend.migrations db downgrade
    """) 