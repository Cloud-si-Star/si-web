from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.menu import MenuCreate, MenuResponse, MenuTreeResponse, MenuVisibilityUpdate
from app.schemas.response import ResponseModel, success
from app.services import menu as menu_service

router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("", response_model=ResponseModel[list[MenuTreeResponse]])
def get_menu_list(db: Session = Depends(get_db)):
    """获取递归树形菜单列表，children 包含下级菜单。"""
    return success(data=menu_service.get_menu_tree(db))


@router.get("/tree", response_model=ResponseModel[list[MenuTreeResponse]])
def get_menu_list(db: Session = Depends(get_db)):
    """获取递归树形菜单列表，children 包含下级菜单。"""
    return success(data=menu_service.get_menu_tree_extra_parent_zero(db))


@router.post("", response_model=ResponseModel[MenuResponse], status_code=status.HTTP_201_CREATED)
def create_menu(payload: MenuCreate, db: Session = Depends(get_db)):
    """新增菜单。"""
    try:
        menu = menu_service.create_menu(db, payload)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    return success(data=menu, message="菜单创建成功")


@router.patch("/{menu_id}/visibility", response_model=ResponseModel[MenuResponse])
def update_menu_visibility(
        menu_id: int,
        payload: MenuVisibilityUpdate,
        db: Session = Depends(get_db),
):
    """启用或关闭菜单；关闭只更新 visible，不删除记录。"""
    menu = menu_service.update_menu_visibility(db, menu_id, payload.visible)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="菜单不存在")
    return success(data=menu, message="菜单状态更新成功")


@router.delete("/{menu_id}", response_model=ResponseModel[None])
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """物理删除菜单；含子菜单时返回 409，需先删除子菜单。"""
    deleted, reason = menu_service.delete_menu(db, menu_id)
    if reason == "not_found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="菜单不存在")
    if reason == "has_children":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="该菜单仍包含子菜单，请先删除子菜单")
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="菜单删除失败")
    return success(message="菜单删除成功")
