-- 文件上传记录表
-- 用于记录文件上传信息：文件类型、文件名称、上传时间、上传用户

CREATE TABLE IF NOT EXISTS `file_record` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `file_name` VARCHAR(255) NOT NULL COMMENT '原始文件名',
    `file_type` VARCHAR(50) NOT NULL COMMENT '文件类型/扩展名',
    `file_path` VARCHAR(500) NOT NULL COMMENT '文件存储路径',
    `file_size` INT NOT NULL COMMENT '文件大小（字节）',
    `upload_user` VARCHAR(100) DEFAULT NULL COMMENT '上传用户',
    `upload_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    `remark` TEXT DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`id`),
    INDEX `idx_file_name` (`file_name`),
    INDEX `idx_file_type` (`file_type`),
    INDEX `idx_upload_user` (`upload_user`),
    INDEX `idx_upload_time` (`upload_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文件上传记录表';
