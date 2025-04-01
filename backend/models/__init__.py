from models.community_info import CommunityInfo
from models.house import HouseInfo
from models.owner import OwnerInfo
# 其他模型导入...

# 这样其他文件只需要从models导入即可
# from models import CommunityInfo, HouseInfo 

__all__ = ['HouseInfo', 'CommunityInfo', 'OwnerInfo'] 