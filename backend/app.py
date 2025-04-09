from backend import app
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 设置 SQLAlchemy 的日志级别为 WARNING 或更高
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

if __name__ == '__main__':
    logger.info("Flask应用启动")
    app.run(host='0.0.0.0', port=5000, debug=True)
