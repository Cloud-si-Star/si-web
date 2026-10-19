from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String, DECIMAL, ForeignKey, Index, Date


class DimDate(Base):
    __tablename__ = 'dim_date'
    __table_args__ = {
        "comment": "日期维度表：主键=YYYYMMDD整数，供所有事实表按日关联"
    }
    date_id = Column(Integer, primary_key=True, comment="日期主键")
    date = Column(Date, nullable=False, index=True, comment="标准日期")
    year = Column(Integer, nullable=False, comment="年，如 2024")
    quarter = Column(Integer, nullable=False, comment="季度 1-4")
    month = Column(Integer, nullable=False, comment="月 1-12")
    day = Column(Integer, nullable=False, comment="日 1-31")
    weekday = Column(Integer, nullable=False, comment="星期，1=周一 ... 7=周日（ISO 标准）")
    is_weekend = Column(Integer, nullable=False, comment="是否周末：1=是，0=否")


class DimProduct(Base):
    __tablename__ = "dim_product"
    __table_args__ = {
        "comment": "商品维度表：记录商品基础信息与基准价，售价在事实表里浮动",
    }
    product_id = Column(Integer, primary_key=True, autoincrement=True, comment="商品ID")
    product_name = Column(String(100), nullable=False, comment="商品全名，如 深蓝色智能手机")
    category = Column(String(50), nullable=False, index=True, comment="品类：数码/家电/服饰/食品")
    unit_price = Column(DECIMAL(10, 2), nullable=False, comment="基准单价(元)，实际售价在事实表中浮动 ±10%")


class DimRegion(Base):
    __tablename__ = "dim_region"
    __table_args__ = {
        "comment": "区域维度表：三层地理层级 区域>省>市",
    }
    region_id = Column(Integer, primary_key=True, autoincrement=True, comment="区域ID")
    province = Column(String(50), nullable=False, comment="省份，如 江苏")
    city = Column(String(50), nullable=False, index=True, comment="城市，如 南京")
    region = Column(String(20), nullable=False, index=True, comment="大区：华东/华南/华北/西南")


class FactSales(Base):
    __tablename__ = "fact_sales"
    __table_args__ = (
        Index("idx_date_product", "date_id", "product_id"),
        {"comment": "销售事实表：每行=一条成交明细；amount 为实收金额(已含单价浮动)，cost 为成本"},
    )
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键")
    date_id = Column(Integer, ForeignKey("dim_date.date_id"), nullable=False, index=True,
                     comment="外键→dim_date，按日分析用")
    product_id = Column(Integer, ForeignKey("dim_product.product_id"), nullable=False, index=True,
                        comment="外键→dim_product")
    region_id = Column(Integer, ForeignKey("dim_region.region_id"), nullable=False, index=True,
                       comment="外键→dim_region")
    quantity = Column(Integer, nullable=False, comment="购买数量(件)")
    amount = Column(DECIMAL(12, 2), nullable=False, comment="实收金额(元)=实际单价×数量")
    cost = Column(DECIMAL(12, 2), nullable=False, comment="成本金额(元)，毛利率=(amount-cost)/amount")
