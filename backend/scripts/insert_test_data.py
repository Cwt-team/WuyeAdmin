from app import app
from db import db
from models.community_info import CommunityInfo
from models.district_info import DistrictInfo
from models.building_info import BuildingInfo
from models.unit_info import UnitInfo
from datetime import datetime

def insert_test_data():
    with app.app_context():
        # 清空现有数据
        UnitInfo.query.delete()
        BuildingInfo.query.delete()
        DistrictInfo.query.delete()
        CommunityInfo.query.delete()
        db.session.commit()
        
        # 插入社区数据
        communities = [
            CommunityInfo(
                community_name='阳光花园',
                community_code='YG001',
                address='北京市朝阳区阳光大道1号',
                area=50000.00,
                building_count=10,
                house_count=500,
                developer='阳光地产',
                property_company='阳光物业',
                property_fee=2.50,
                contact_person='张经理',
                contact_phone='13800138001',
                status=1
            ),
            CommunityInfo(
                community_name='翡翠湾',
                community_code='FC001',
                address='北京市海淀区翡翠路88号',
                area=80000.00,
                building_count=15,
                house_count=800,
                developer='翡翠地产',
                property_company='翡翠物业',
                property_fee=3.00,
                contact_person='李经理',
                contact_phone='13800138002',
                status=1
            ),
            CommunityInfo(
                community_name='金色家园',
                community_code='JS001',
                address='北京市丰台区金色大道66号',
                area=60000.00,
                building_count=12,
                house_count=600,
                developer='金色地产',
                property_company='金色物业',
                property_fee=2.80,
                contact_person='王经理',
                contact_phone='13800138003',
                status=1
            )
        ]
        
        db.session.add_all(communities)
        db.session.commit()
        
        # 插入区域数据
        districts = []
        
        # 阳光花园的区域
        for i in range(1, 4):
            districts.append(
                DistrictInfo(
                    community_id=1,
                    district_name=f'阳光花园{i}区',
                    district_number=str(i),
                    building_count=3,
                    house_count=150,
                    status=1
                )
            )
        
        # 翡翠湾的区域
        for i in range(1, 4):
            districts.append(
                DistrictInfo(
                    community_id=2,
                    district_name=f'翡翠湾{i}区',
                    district_number=str(i),
                    building_count=5,
                    house_count=250,
                    status=1
                )
            )
        
        # 金色家园的区域
        for i in range(1, 4):
            districts.append(
                DistrictInfo(
                    community_id=3,
                    district_name=f'金色家园{i}区',
                    district_number=str(i),
                    building_count=4,
                    house_count=200,
                    status=1
                )
            )
        
        db.session.add_all(districts)
        db.session.commit()
        
        # 插入楼栋数据
        buildings = []
        
        # 为每个区域添加楼栋
        for district in districts:
            for i in range(1, 4):  # 每个区域3栋楼
                buildings.append(
                    BuildingInfo(
                        community_id=district.community_id,
                        district_id=district.id,
                        building_name=f'{district.district_name}{i}栋',
                        building_number=str(i),
                        floor_count=18,
                        unit_count=2,
                        house_count=36,
                        status=1
                    )
                )
        
        db.session.add_all(buildings)
        db.session.commit()
        
        # 插入单元数据
        units = []
        
        # 为每个楼栋添加单元
        for building in buildings:
            for i in range(1, 3):  # 每栋楼2个单元
                units.append(
                    UnitInfo(
                        community_id=building.community_id,
                        district_id=building.district_id,
                        building_id=building.id,
                        unit_name=f'{building.building_name}{i}单元',
                        unit_number=str(i),
                        house_count=18,
                        status=1
                    )
                )
        
        db.session.add_all(units)
        db.session.commit()
        
        print("测试数据插入成功！")

if __name__ == '__main__':
    insert_test_data() 