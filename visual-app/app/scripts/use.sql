use visual;

# 新建用户表 简单版
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`
(
    `id`       INT        NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(8) NOT NULL COMMENT '用户名',
    PRIMARY KEY (`id`)
);

# 新建AI会话表
-- ========== 会话表 ==========
CREATE TABLE `chat_conversation`
(
    `id`            BIGINT       NOT NULL AUTO_INCREMENT COMMENT '会话ID',
    `user_id`       BIGINT       NULL COMMENT '用户ID(单用户可空)',
    `title`         VARCHAR(64)  NOT NULL DEFAULT '新对话' COMMENT '会话标题',
    `last_message`  VARCHAR(255) NULL COMMENT '最后一条消息摘要(左边栏预览)',
    `message_count` INT          NOT NULL DEFAULT 0 COMMENT '消息数量',
    `created_at`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_updated` (`user_id`, `updated_at` DESC)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='会话表';


-- ========== 消息表 ==========
CREATE TABLE `chat_message`
(
    `id`              BIGINT      NOT NULL AUTO_INCREMENT COMMENT '消息ID',
    `conversation_id` BIGINT      NOT NULL COMMENT '所属会话ID',
    `role`            VARCHAR(20) NOT NULL COMMENT '角色: user/assistant/system',
    `content`         TEXT        NOT NULL COMMENT '消息内容',
    `created_at`      DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_conversation` (`conversation_id`, `id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='消息表';