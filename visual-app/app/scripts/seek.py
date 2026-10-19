import random
from datetime import date, timedelta
import numpy as np
from faker import Faker
from sqlalchemy.orm import Session

from app.models.sales import DimDate, DimProduct, DimRegion, FactSales

fake = Faker("zh_CN")
rng = np.random.default_rng(42)  # 固定随机种子，结果可复现

# ---------- 维度数据 ----------

PROVINCES = {
    "华东": [("江苏", ["南京", "苏州", "无锡"]),
             ("浙江", ["杭州", "宁波", "温州"]),
             ("上海", ["上海"])],
    "华南": [("广东", ["广州", "深圳", "东莞"]),
             ("福建", ["福州", "厦门"])],
    "华北": [("北京", ["北京"]),
             ("河北", ["石家庄", "唐山"])],
    "西南": [("四川", ["成都", "绵阳"]),
             ("重庆", ["重庆"])],
}

# (品类, 名称模板, 基准价, 价格浮动)
PRODUCT_TEMPLATES = [
    ("数码", "智能手机", 3500, 0.3),
    ("数码", "无线耳机", 500, 0.25),
    ("数码", "平板电脑", 2800, 0.3),
    ("家电", "空气净化器", 1200, 0.2),
    ("家电", "扫地机器人", 2000, 0.25),
    ("家电", "电饭煲", 400, 0.2),
    ("服饰", "运动鞋", 600, 0.3),
    ("服饰", "羽绒服", 900, 0.3),
    ("服饰", "T恤", 120, 0.25),
    ("食品", "坚果礼盒", 180, 0.15),
    ("食品", "进口牛奶", 80, 0.15),
    ("食品", "咖啡豆", 150, 0.2),
]


def seed_dim_date(db: Session, start: date, end: date):
    rows = []
    cur = start
    while cur <= end:
        rows.append(
            DimDate(
                date_id=int(cur.strftime("%Y%m%d")),
                date=cur,
                year=cur.year,
                quarter=(cur.month - 1) // 3 + 1,
                month=cur.month,
                day=cur.day,
                weekday=cur.isoweekday(),
                is_weekend=1 if cur.isoweekday() >= 6 else 0,
            )
        )
        cur += timedelta(days=1)
    db.add_all(rows)
    db.commit()
    return len(rows)


def seed_dim_region(db: Session):
    rows = []
    for region, prov_list in PROVINCES.items():
        for province, cities in prov_list:
            for city in cities:
                rows.append(DimRegion(region=region, province=province, city=city))
    db.add_all(rows)
    db.commit()
    return len(rows)


def seed_dim_product(db: Session):
    rows = []
    for i, (cat, name, base_price, float_ratio) in enumerate(PRODUCT_TEMPLATES):
        price = round(base_price * (1 + rng.uniform(-float_ratio, float_ratio)), 2)
        rows.append(
            DimProduct(
                product_name=f"{fake.color_name()}{name}",
                category=cat,
                unit_price=price,
            )
        )
    db.add_all(rows)
    db.commit()
    return len(rows)


# ---------- 事实数据（核心：构造有意义的时间模式） ----------

def _daily_multiplier(d: date) -> float:
    """构造时间因素：趋势增长 × 季节性 × 周末波动"""
    # 1) 长期增长：一年内线性增长 ~30%
    base_date = date(d.year, 1, 1)
    day_of_year = (d - base_date).days
    growth = 1.0 + 0.3 * day_of_year / 365

    # 2) 季节性：Q4 旺季
    season_map = {1: 0.85, 2: 0.75, 3: 0.95, 4: 1.0,
                  5: 1.0, 6: 1.05, 7: 1.05, 8: 1.0,
                  9: 1.0, 10: 1.1, 11: 1.4, 12: 1.35}
    season = season_map[d.month]

    # 3) 周末效应
    weekend = 1.25 if d.isoweekday() >= 6 else 1.0

    # 4) 随机噪声（对数正态，右偏）
    noise = float(rng.lognormal(mean=0, sigma=0.15))

    return growth * season * weekend * noise


def seed_fact_sales(db: Session, start: date, end: date):
    # 一次性取出维度
    products = db.query(DimProduct).all()
    regions = db.query(DimRegion).all()

    # 区域权重：一线城市销量更高
    region_weights = np.array([
        1.5 if r.city in ("上海", "北京", "深圳", "广州") else 1.0
        for r in regions
    ])
    region_weights = region_weights / region_weights.sum()

    batch = []
    cur = start
    while cur <= end:
        date_id = int(cur.strftime("%Y%m%d"))
        multiplier = _daily_multiplier(cur)

        # 每天成交记录条数：基础 60 条 × 时间因子
        record_count = int(rng.poisson(60 * multiplier))

        for _ in range(record_count):
            prod = products[rng.integers(0, len(products))]
            reg = regions[rng.choice(len(regions), p=region_weights)]

            # 数量：对数正态，多数 1-3 件，偶尔批发
            qty = max(1, int(rng.lognormal(mean=0.5, sigma=0.5)))
            # 售价围绕 unit_price 上下浮动 10%
            unit_price = float(prod.unit_price) * rng.uniform(0.9, 1.1)
            amount = round(unit_price * qty, 2)
            # 成本约为售价 60%~75%
            cost = round(amount * rng.uniform(0.6, 0.75), 2)

            batch.append(
                FactSales(
                    date_id=date_id,
                    product_id=prod.product_id,
                    region_id=reg.region_id,
                    quantity=qty,
                    amount=amount,
                    cost=cost,
                )
            )

            if len(batch) >= 2000:
                db.bulk_save_objects(batch)
                db.commit()
                batch.clear()

        cur += timedelta(days=1)

    if batch:
        db.bulk_save_objects(batch)
        db.commit()


def run_seed(db: Session, start: date, end: date):
    seed_dim_date(db, start, end)
    n_region = seed_dim_region(db)
    n_product = seed_dim_product(db)
    seed_fact_sales(db, start, end)

    total = db.query(FactSales).count()
    print(f"✅ 维度: 区域={n_region}, 商品={n_product}")
    print(f"✅ 事实: {total} 条销售记录")
