from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String, DECIMAL, BigInteger, Index
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="订单主键")

    # 业务字段
    order_no = Column(String(32), unique=True, nullable=False, comment="订单号")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    product_name = Column(String(64), nullable=False, comment="商品名称")
    category = Column(String(32), nullable=False, comment="商品品类")
    amount = Column(DECIMAL(10, 2), nullable=False, comment="订单金额")
    region = Column(String(16), nullable=False, comment="地区")
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment="下单时间")

    # 索引：单列 + 联合，后面 Pandas 分析按这些字段 groupby 会快很多
    __table_args__ = (
        Index("idx_category", "category"),
        Index("idx_region", "region"),
        Index("idx_created_at", "created_at"),
        Index("idx_user_created", "user_id", "created_at"),
        {"comment": "订单表"},
    )

    def __repr__(self):
        return f"<Order {self.order_no} ¥{self.amount}>"

