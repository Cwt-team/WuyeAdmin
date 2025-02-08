-- 创建数据库
CREATE DATABASE IF NOT EXISTS Wuye DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- 使用数据库
USE Wuye;


-- Create the community_info table    表1 - 小区信息列表
CREATE TABLE community_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    community_number VARCHAR(20) NOT NULL,
    community_name VARCHAR(100) NOT NULL,
    community_city VARCHAR(50) NOT NULL,
    creation_time DATETIME NOT NULL,
    is_enabled TINYINT NOT NULL COMMENT '0: disabled, 1: enabled',
    management_machine_quantity INT NOT NULL,
    indoor_machine_quantity INT NOT NULL,
    access_card_type VARCHAR(20) NOT NULL,
    app_record_face TINYINT NOT NULL COMMENT '0: disabled, 1: enabled',
    is_same_step TINYINT NOT NULL COMMENT '0: different, 1: same',
    is_record_upload TINYINT NOT NULL COMMENT '0: disabled, 1: enabled',
    community_password VARCHAR(32) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO community_info
(community_number, community_name, community_city, creation_time, is_enabled,
management_machine_quantity, indoor_machine_quantity, access_card_type,
app_record_face, is_same_step, is_record_upload, community_password)
VALUES
('CN001', '阳光花园', '上海市', '2024-01-01 08:00:00', 1, 5, 200, 'NFC', 1, 1, 1, 'pwd123'),
('CN002', '翡翠湾', '北京市', '2024-01-15 09:30:00', 1, 3, 150, 'IC卡', 1, 0, 1, 'pwd456'),
('CN003', '康庄小区', '广州市', '2024-02-01 10:00:00', 1, 4, 180, 'NFC', 0, 1, 0, 'pwd789'),
('CN004', '龙湖苑', '深圳市', '2024-02-15 14:30:00', 0, 2, 100, 'IC卡', 1, 1, 1, 'pwd321'),
('CN005', '海风小区', '厦门市', '2024-03-01 11:15:00', 1, 6, 250, 'NFC', 1, 0, 1, 'pwd654');



-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


-- 表2 - 房屋信息列表  （层级关系表）
CREATE TABLE house_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    community_id INT NOT NULL COMMENT '关联community_info表的id',
    district_number VARCHAR(10) COMMENT '区号',
    building_number VARCHAR(10) COMMENT '栋号',
    unit_number VARCHAR(10) COMMENT '单元号',
    house_full_name VARCHAR(100) NOT NULL COMMENT '完整房屋地址',
    house_level INT NOT NULL COMMENT '层级：1区、2栋、3单元',
    parent_id INT COMMENT '父级ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (community_id) REFERENCES community_info(id),
    FOREIGN KEY (parent_id) REFERENCES house_info(id)
);

-- 插入示例数据（基于前面小区的示例数据）

-- 先插入区
INSERT INTO house_info
(community_id, district_number, house_full_name, house_level, parent_id)
VALUES
(1, '1', '阳光花园1区', 1, NULL),
(1, '2', '阳光花园2区', 1, NULL),
(1, '5', '阳光花园5区', 1, NULL);

-- 插入栋
INSERT INTO house_info
(community_id, district_number, building_number, house_full_name, house_level, parent_id)
VALUES
-- 1区的楼栋
(1, '1', '1', '阳光花园1区1栋', 2, 1),
-- 2区的楼栋
(1, '2', '1', '阳光花园2区1栋', 2, 2),
-- 5区的楼栋
(1, '5', '42', '阳光花园5区42栋', 2, 3);

-- 插入单元
INSERT INTO house_info
(community_id, district_number, building_number, unit_number, house_full_name, house_level, parent_id)
VALUES
-- 1区1栋的单元
(1, '1', '1', '1', '阳光花园1区1栋1单元', 3, 4),
-- 2区1栋的单元
(1, '2', '1', '1', '阳光花园2区1栋1单元', 3, 5),
-- 5区42栋的单元
(1, '5', '42', '12', '阳光花园5区42栋12单元', 3, 6);

-- 创建视图便于查看层级关系
CREATE VIEW v_house_hierarchy AS
WITH RECURSIVE house_tree AS (
    -- 基础查询：获取顶层节点
    SELECT
        h.id,
        h.house_full_name,
        h.house_level,
        h.parent_id,
        1 AS depth,
        CAST(h.house_full_name AS CHAR(200)) AS path
    FROM house_info h
    WHERE h.parent_id IS NULL

    UNION ALL

    -- 递归查询：获取子节点
    SELECT
        h.id,
        h.house_full_name,
        h.house_level,
        h.parent_id,
        ht.depth + 1,
        CONCAT(ht.path, ' > ', h.house_full_name)
    FROM house_info h
    INNER JOIN house_tree ht ON h.parent_id = ht.id
)
SELECT path, house_level, depth
FROM house_tree
ORDER BY path;



-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --



-- 3. 网页后台管理员角色表
CREATE TABLE admin_role (
    id BIGINT PRIMARY KEY NOT NULL COMMENT '角色标识ID',
    role_name VARCHAR(50) NOT NULL COMMENT '角色名称',
    sort_number INT NOT NULL COMMENT '排序编号',
    description VARCHAR(200) COMMENT '角色描述',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY `uk_role_name` (`role_name`)
) COMMENT '管理员角色表';

-- 插入示例数据
INSERT INTO admin_role
(id, role_name, sort_number, description, created_at)
VALUES
(129295687549465048, '超级管理员', 10001, '系统最高权限管理员', '2024-01-15 10:15:30'),
(133272455163688408, '测试用户', 10001, '用于测试的临时角色', '2024-01-15 14:20:45'),
(133272455163688409, '物业管理员', 10002, '负责日常物业管理操作', '2024-01-15 16:30:00'),
(133272455163688410, '安保主管', 10003, '负责小区安防管理', '2024-01-16 09:45:15'),
(133272455163688411, '客服专员', 10004, '处理业主问题和反馈', '2024-01-16 11:20:30');




-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --





--   4.小区管理员表
CREATE TABLE community_manager (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '管理员ID',
    community_id INT NOT NULL COMMENT '关联的小区ID',
    other_name VARCHAR(50) NOT NULL COMMENT '别名',
    account_number VARCHAR(50) NOT NULL COMMENT '账号',
    character_type VARCHAR(50) NOT NULL COMMENT '角色',
    phone_number VARCHAR(20) NOT NULL COMMENT '手机号码',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY `uk_account_number` (`account_number`),
    FOREIGN KEY (community_id) REFERENCES community_info(id),
    FOREIGN KEY (character_type) REFERENCES admin_role(role_name)
) COMMENT '小区管理员表';

-- 插入示例数据
INSERT INTO community_manager
(community_id, other_name, account_number, character_type, phone_number)
VALUES
-- 阳光花园的管理员
(1, '张经理', 'manager001', '物业管理员', '13800138001'),
(1, '王队长', 'security001', '安保主管', '13800138002'),
(1, '李客服', 'service001', '客服专员', '13800138003'),

-- 翡翠湾的管理员
(2, '刘经理', 'manager002', '物业管理员', '13800138004'),
(2, '赵安保', 'security002', '安保主管', '13800138005'),

-- 康庄小区的管理员
(3, '孙经理', 'manager003', '物业管理员', '13800138006'),
(3, '钱客服', 'service002', '客服专员', '13800138007'),

-- 龙湖苑的管理员
(4, '周经理', 'manager004', '物业管理员', '13800138008'),

-- 海风小区的管理员
(5, '吴经理', 'manager005', '物业管理员', '13800138009'),
(5, '郑客服', 'service003', '客服专员', '13800138010');




-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --





-- 5.物业管理员表
CREATE TABLE property_manager (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '管理员ID',
    community_id INT NOT NULL COMMENT '关联的小区ID',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    phone_number VARCHAR(20) NOT NULL COMMENT '手机号码',
    remark VARCHAR(200) COMMENT '备注',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    face_image VARCHAR(200) COMMENT '人脸图片路径',
    face_status TINYINT DEFAULT 0 COMMENT '人脸状态：0-暂无数据 1-已录入',
    FOREIGN KEY (community_id) REFERENCES community_info(id),
    UNIQUE KEY `uk_phone_number` (`phone_number`)
) COMMENT '物业管理员表';

-- 插入示例数据
INSERT INTO property_manager
(community_id, name, phone_number, updated_at, remark)
VALUES
-- 崔庆科技小区的物业管理员
(1, '谢', '13711487267', '2024-06-08 11:40:49.266', NULL),
(1, '测试用', '13542406093', '2025-01-25 14:56:28.741', NULL),

-- 其他小区的物业管理员
(2, '王', '13800138001', '2024-01-15 09:30:00.000', '保洁主管'),
(2, '李', '13800138002', '2024-01-15 10:20:00.000', '维修组长'),
(3, '张', '13800138003', '2024-01-16 08:45:00.000', '园艺主管'),
(4, '刘', '13800138004', '2024-01-16 14:30:00.000', '设备维护'),
(5, '赵', '13800138005', '2024-01-17 11:20:00.000', '保安队长');




-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --




-- 6.业主信息表
CREATE TABLE owner_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '业主ID',
    community_id INT NOT NULL COMMENT '关联的小区ID',
    house_id INT NOT NULL COMMENT '关联的房屋ID',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender CHAR(1) NOT NULL COMMENT '性别：M-男 F-女',
    phone_number VARCHAR(20) NOT NULL COMMENT '手机号码',
    id_card VARCHAR(18) COMMENT '身份证号',
    email VARCHAR(100) COMMENT '邮箱',
    city VARCHAR(50) COMMENT '户籍城市',
    address VARCHAR(200) COMMENT '详细地址',
    owner_type VARCHAR(20) NOT NULL DEFAULT '业主' COMMENT '业主类型',
    face_image VARCHAR(200) COMMENT '人脸图片路径',
    face_status TINYINT DEFAULT 0 COMMENT '人脸状态：0-未录入 1-已录入',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (community_id) REFERENCES community_info(id),
    FOREIGN KEY (house_id) REFERENCES house_info(id),
    UNIQUE KEY `uk_phone_number` (`phone_number`),
    UNIQUE KEY `uk_id_card` (`id_card`)
) COMMENT '业主信息表';


-- 创建业主权限表
CREATE TABLE owner_permission (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '权限ID',
    owner_id BIGINT NOT NULL COMMENT '业主ID',
    house_id INT NOT NULL COMMENT '房屋ID',
    permission_status VARCHAR(20) NOT NULL DEFAULT '正常' COMMENT '权限状态',
    valid_period VARCHAR(20) NOT NULL DEFAULT '永久有效' COMMENT '有效期',
    calling_enabled TINYINT(1) DEFAULT 1 COMMENT '呼叫功能启用状态',
    pstn_enabled TINYINT(1) DEFAULT 0 COMMENT '手机转接(PSTN)启用状态',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (owner_id) REFERENCES owner_info(id),
    FOREIGN KEY (house_id) REFERENCES house_info(id)
) COMMENT '业主权限表';

-- 插入示例数据
INSERT INTO owner_info
(community_id, house_id, name, gender, phone_number, id_card, owner_type, updated_at)
VALUES
-- 崔氏科技小区的业主
(1, 1, '谢', 'M', '17362955521', NULL, '业主', '2024-07-30 10:10:24.586'),
(1, 2, '谢', 'M', '17362955522', NULL, '业主', '2024-07-30 09:50:30.203'),
(1, 3, '程', 'M', '13542406093', NULL, '业主', '2024-07-30 11:12:42.835'),
(1, 4, '业主', 'M', '13711487267', NULL, '业主', '2024-07-30 12:04:05.300'),
(1, 5, 'cui', 'M', '13542406094', NULL, '业主', '2024-08-03 15:27:25.602'),
(1, 6, 'xxx', 'M', '13509993912', '123456789000000', '业主', '2024-08-03 16:33:11.262');

-- 插入业主权限数据
INSERT INTO owner_permission
(owner_id, house_id, permission_status, valid_period, calling_enabled, pstn_enabled, updated_at)
VALUES
(1, 1, '正常', '永久有效', 1, 0, '2024-07-30 11:51:27.540'),
(2, 2, '正常', '永久有效', 1, 0, '2024-07-30 09:50:30.203'),
(3, 3, '正常', '永久有效', 1, 0, '2024-07-30 11:12:42.835'),
(4, 4, '正常', '永久有效', 1, 0, '2024-07-30 12:04:05.300'),
(5, 5, '正常', '永久有效', 1, 0, '2024-08-03 15:27:25.602'),
(6, 6, '正常', '永久有效', 1, 0, '2024-08-03 16:33:11.262');




-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --




-- 7.业主申请表

-- 8.门禁信息表

-- 9.设备信息表