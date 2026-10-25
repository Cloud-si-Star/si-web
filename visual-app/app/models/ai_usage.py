from sqlalchemy import BigInteger, Column, Date, String

from app.core.database import Base


class AiType(Base):
    __tablename__ = "ai_type"

    id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True, comment="AI类型ID")
    label = Column(String(64), nullable=False, comment="用户类型")


class AIUseDistribution(Base):
    __tablename__ = "ai_use_distribution"

    id = Column(BigInteger, autoincrement=True, primary_key=True, comment="分布情况数据ID")
    ai_use_province_id = Column(BigInteger, nullable=False, comment="省份的ID")
    ai_use_number = Column(BigInteger, nullable=False, default=0, comment="使用数量")
    ai_type_id = Column(BigInteger, nullable=False, comment="AI类型")
    ai_use_time = Column(Date, nullable=False, comment="使用时间")


class Province(Base):
    __tablename__ = "ai_province"

    adcode = Column(BigInteger, nullable=False, primary_key=True, comment="地区ID")
    name = Column(String(32), nullable=False, comment="省份名称")
