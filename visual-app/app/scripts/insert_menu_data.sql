USE visual;

-- 本文件仅插入菜单数据，不创建或删除表；请审阅后由你手动执行。
-- 页面来源：visual-web/src/router/index.ts 中已注册的 views 路由。
-- component 保存当前路由的动态 import 路径，按前端约定不带 @/ 前缀。
-- menu_type：d 开头工作台=1，v 开头可视化=2；visible 默认启用。
-- 以下统一 parent_id=0：现有路由并未定义 sys_menu 的数据库父子菜单层级，请确认是否需要改成两级菜单。
-- icon 使用 Element Plus 图标组件名作为暂定值，请确认项目菜单渲染器是否接受这些名称。
-- label 对工作台菜单沿用 digital-menu.vue 文案；可视化菜单沿用 visual-menu.vue 文案。
-- 注意：重复执行会插入重复数据；本表没有唯一约束，执行前请检查当前 sys_menu 内容。
-- d-chat/demo.vue 是被 d-chat 页面复用的演示文件，没有独立路由，因此不单独插入菜单。

INSERT INTO `sys_menu`
    (`parent_id`, `label`, `icon`, `path`, `component`, `sort_order`, `visible`, `menu_type`)
VALUES
    (0, '数据仓库', 'DataAnalysis', '/v-digital/d-table', 'views/d-table/index.vue', 10, 1, 1),
    (0, 'AI对话', 'ChatDotRound', '/v-digital/d-chat', 'views/d-chat/index.vue', 20, 1, 1),
    (0, '动态组件', 'Connection', '/v-digital/d-drag', 'views/d-drag/index.vue', 30, 1, 1),
    (0, '数据管理', 'Document', '/v-digital/d-demo', 'views/d-demo/index.vue', 40, 1, 1),
    (0, '菜单管理', 'Menu', '/v-digital/d-menu', 'views/d-menu/index.vue', 50, 1, 1),
    (0, '数据可视化', 'DataLine', '/v-visual/v1-view', 'views/v-echarts/view-visual.vue', 10, 1, 2),
    (0, '数据并发化', 'Histogram', '/v-visual/v2-view', 'views/v-scorll/view-scroll.vue', 20, 1, 2);

-- 待确认：当前侧边栏另有“数据大屏”入口，目标路径为 /v-visual（会重定向到 /v-visual/v1-view），
-- 它对应 visual layout 而非 views 下的页面，不作为 views 菜单记录单独插入。
