# 数据库配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3326,
    'user': 'root',
    'password': '123456',
    'database': 'wuye',
    'charset': 'utf8mb4'
}

# Flask-SQLAlchemy配置
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True  # 在开发环境下打印SQL语句 