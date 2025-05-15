# 从house.py导入HouseInfo模型，提供向后兼容性
from backend.models.house import HouseInfo

# 重新导出类，使其可以被导入
__all__ = ['HouseInfo'] 