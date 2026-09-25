import csv
import math
from pathlib import Path

import pandas as pd

from app.core.config import settings
from app.utils.exceptions import BizException


def _resolve_csv_path(filename: str) -> Path:
    """校验并返回 data 目录下的 csv 文件路径"""
    file_path: Path = settings.data_dir / filename

    if not file_path.exists():
        raise BizException(f"文件不存在: {filename}", code=404)

    if file_path.suffix.lower() != ".csv":
        raise BizException("只支持 .csv 文件", code=400)

    return file_path


def read_csv(filename: str, limit: int | None = None) -> list[dict]:
    """
    读取 data 目录下的 csv 文件，返回字典列表。
    limit 为可选的最大条数，防止大文件一次性全量读入。
    """
    file_path = _resolve_csv_path(filename)

    rows: list[dict] = []
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit is not None and i >= limit:
                break
            rows.append(row)
    return rows


def read_csv_paginated(filename: str, page: int = 1, page_size: int = 50) -> dict:
    """
    分页读取 csv。流式遍历，只把目标页的数据留在内存里，
    适合 worldcities.csv 这种几万行的大文件。
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 1
    if page_size > 1000:
        page_size = 1000  # 单页上限，避免一次拉太多

    file_path = _resolve_csv_path(filename)

    start = (page - 1) * page_size
    end = start + page_size

    rows: list[dict] = []
    total = 0
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if start <= i < end:
                rows.append(row)
            total += 1

    total_pages = math.ceil(total / page_size) if total else 0
    return {
        "filename": filename,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "rows": rows,
    }


# 支持的聚合方式：列名 -> pandas 聚合函数名
_ALLOWED_AGGS = {"count", "sum", "mean", "min", "max", "median"}


def pie_csv_read(filename:str)->dict:
    file_path = _resolve_csv_path(filename)
    df = pd.read_csv(file_path)

    grouped_multiple = df.groupby('country').agg({'population': 'sum','id': 'first',}).reset_index() 
    # 2. 使用 nlargest 直接获取人口最多的前 10 条记录
    top_10_df = grouped_multiple.nlargest(10, 'population')

    # 3. 将人口转换为百万级别，并保留两位小数
    top_10_df['population'] = (top_10_df['population'] / 1_000_000).round(2)
    top_10_df['unit'] = '百万'
    print(top_10_df.info)
    # 4. 仅选取需要的三个字段，并转换为字典列表传给前端
    result_list = top_10_df[['id', 'country', 'population','unit']].to_dict(orient='records')

    return {
        'total':len(result_list),
        'page':result_list
        
    }



def stats_csv(
    filename: str,
    group_by: str,
    agg: str = "count",
    metric: str | None = None,
    top: int | None = None,
) -> dict:
    """
    对 csv 按 group_by 列分组统计后返回结果。
    - agg=count 时无需 metric，直接统计每组行数
    - 其他聚合（sum/mean/min/max/median）需指定数值列 metric
    - top 可选，只返回按结果值降序的前 N 组
    """
    if agg not in _ALLOWED_AGGS:
        raise BizException(f"不支持的聚合方式: {agg}，可选 {sorted(_ALLOWED_AGGS)}", code=400)

    file_path = _resolve_csv_path(filename)
    df = pd.read_csv(file_path)

    if group_by not in df.columns:
        raise BizException(f"分组列不存在: {group_by}", code=400)

    if agg == "count":
        series = df.groupby(group_by).size()
    else:
        if not metric:
            raise BizException(f"聚合 {agg} 需要指定数值列 metric", code=400)
        if metric not in df.columns:
            raise BizException(f"数值列不存在: {metric}", code=400)
        numeric = pd.to_numeric(df[metric], errors="coerce")
        series = numeric.groupby(df[group_by]).agg(agg)

    series = series.sort_values(ascending=False)
    if top is not None and top > 0:
        series = series.head(top)

    items = [{"key": str(k), "value": _to_native(v)} for k, v in series.items()]
    return {
        "filename": filename,
        "group_by": group_by,
        "agg": agg,
        "metric": metric,
        "count": len(items),
        "items": items,
    }


def _to_native(value):
    """把 numpy 数值转成原生 python 类型，方便 JSON 序列化"""
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def list_csv_files() -> list[str]:
    """列出 data 目录下所有可用的 csv 文件名"""
    if not settings.data_dir.exists():
        return []
    return [p.name for p in settings.data_dir.glob("*.csv")]
