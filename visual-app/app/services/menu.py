from typing import Optional

from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuTreeResponse


def get_menu_tree(db: Session) -> list[MenuTreeResponse]:
    """查询全部菜单并按 parent_id 组装树，根菜单和孤儿菜单都作为根节点返回。"""
    rows = db.query(Menu).order_by(Menu.sort_order.asc(), Menu.id.asc()).all()
    nodes = {
        row.id: MenuTreeResponse.model_validate(row)
        for row in rows
    }
    roots: list[MenuTreeResponse] = []

    for row in rows:
        node = nodes[row.id]
        parent = nodes.get(row.parent_id) if row.parent_id != 0 else None
        if parent is None:
            roots.append(node)
        else:
            parent.children.append(node)

    return roots


def get_menu_tree_extra_parent_zero(db: Session) -> list[MenuTreeResponse]:
    """
    查询全部菜单并按parent_id组装树结构
    修改点：不再返回partent_id=0的一级菜单
    """
    rows = db.query(Menu).order_by(Menu.sort_order.asc(), Menu.id.asc()).all()
    nodes = {
        row.id: MenuTreeResponse.model_validate(row) for row in rows
    }

    roots: list[MenuTreeResponse] = []

    for row in rows:
        node = nodes[row.id]
        parent = nodes.get(row.parent_id)

        # 父级id
        if row.parent_id == 0:
            continue
        elif parent is not None:
            roots.append(node)
        else:
            parent.children.append(node)

    return roots


def get_menu_by_id(db: Session, menu_id: int) -> Optional[Menu]:
    """按主键查找菜单。"""
    return db.query(Menu).filter(Menu.id == menu_id).first()


def create_menu(db: Session, payload: MenuCreate) -> Menu:
    """创建菜单；非根菜单必须关联已存在的父菜单。"""
    if payload.parent_id != 0 and not get_menu_by_id(db, payload.parent_id):
        raise ValueError(f"父菜单不存在: parent_id={payload.parent_id}")

    menu = Menu(**payload.model_dump())
    db.add(menu)
    try:
        db.commit()
        db.refresh(menu)
    except Exception:
        db.rollback()
        raise
    return menu


def update_menu_visibility(db: Session, menu_id: int, visible: int) -> Optional[Menu]:
    """更新菜单 visible 状态；关闭菜单不删除记录。"""
    menu = get_menu_by_id(db, menu_id)
    if not menu:
        return None

    menu.visible = visible
    try:
        db.commit()
        db.refresh(menu)
    except Exception:
        db.rollback()
        raise
    return menu


def delete_menu(db: Session, menu_id: int) -> tuple[bool, str | None]:
    """物理删除菜单；存在子菜单时拒绝删除以避免孤儿记录。"""
    menu = get_menu_by_id(db, menu_id)
    if not menu:
        return False, "not_found"

    has_children = db.query(Menu.id).filter(Menu.parent_id == menu_id).first() is not None
    if has_children:
        return False, "has_children"

    try:
        db.delete(menu)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return True, None
