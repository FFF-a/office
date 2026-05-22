-- ============================================================
-- 人工专高复赛考题 - MySQL 8.0 建表脚本
-- 数据库名与 .env 中 DB_NAME 保持一致
-- ============================================================

CREATE DATABASE IF NOT EXISTS office_manage
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE office_manage;

-- ------------------------------------------------------------
-- 1. 员工（用户）表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(20)  NOT NULL COMMENT '姓名 1-20字符',
    age         INT          NOT NULL COMMENT '年龄 18-60',
    email       VARCHAR(120) NOT NULL COMMENT '邮箱',
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工表';

-- ------------------------------------------------------------
-- 2. 管理员表（密码 bcrypt 哈希存储）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admins (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL COMMENT '用户名',
    password_hash VARCHAR(128) NOT NULL COMMENT 'bcrypt密码哈希',
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_admins_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员表';

-- ------------------------------------------------------------
-- 3. 设备分类表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS device_categories (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(50)  NOT NULL COMMENT '分类名称',
    description VARCHAR(255) NULL     COMMENT '分类描述',
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_device_categories_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备分类表';

-- ------------------------------------------------------------
-- 4. 设备表（多对一关联分类，外键 RESTRICT 禁止误删分类）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS devices (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL COMMENT '设备名称',
    model         VARCHAR(100) NULL     COMMENT '设备型号',
    serial_number VARCHAR(100) NULL     COMMENT '序列号',
    status        VARCHAR(20)  NOT NULL DEFAULT 'available' COMMENT '状态',
    category_id   INT          NOT NULL COMMENT '分类ID',
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_devices_serial (serial_number),
    KEY idx_devices_category_id (category_id),
    CONSTRAINT fk_devices_category
        FOREIGN KEY (category_id) REFERENCES device_categories(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备表';

-- ------------------------------------------------------------
-- 示例数据（可选）
-- ------------------------------------------------------------
INSERT INTO device_categories (name, description) VALUES
('办公电脑', '台式机与笔记本'),
('网络设备', '路由器、交换机'),
('外设', '打印机、扫描仪')
ON DUPLICATE KEY UPDATE name = VALUES(name);
