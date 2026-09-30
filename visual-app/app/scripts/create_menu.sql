USE visual;

DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`(
    `id`            INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
    `parent_id`     INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '父菜单ID',
    `label`         VARCHAR(50) NOT NULL COMMENT '菜单名称',
    `icon`          VARCHAR(50) NOT NULL COMMENT '菜单图标',
    `path`          VARCHAR(100) NOT NULL COMMENT '菜单路径',
    `component`     VARCHAR(100) NOT NULL COMMENT '菜单组件',
    `sort_order`    INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '排序',
    `visible`       TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否可见（0否，1是）',
    `menu_type`     TINYINT(1) NOT NULL DEFAULT 0 COMMENT '菜单类型（1工作台，2可视化）',
    `created_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    INDEX `idx_parent_id` (`parent_id`)
)