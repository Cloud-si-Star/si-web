import itertools
from datetime import date, timedelta

# 中国省份、自治区、直辖市、特别行政区列表
province_list = [
    {"id": 0, "label": "贵州省"},
    {"id": 1, "label": "北京市"},
    {"id": 2, "label": "天津市"},
    {"id": 3, "label": "上海市"},
    {"id": 4, "label": "重庆市"},
    {"id": 5, "label": "河北省"},
    {"id": 6, "label": "山西省"},
    {"id": 7, "label": "辽宁省"},
    {"id": 8, "label": "吉林省"},
    {"id": 9, "label": "黑龙江省"},
    {"id": 10, "label": "江苏省"},
    {"id": 11, "label": "浙江省"},
    {"id": 12, "label": "安徽省"},
    {"id": 13, "label": "福建省"},
    {"id": 14, "label": "江西省"},
    {"id": 15, "label": "山东省"},
    {"id": 16, "label": "河南省"},
    {"id": 17, "label": "湖北省"},
    {"id": 18, "label": "湖南省"},
    {"id": 19, "label": "广东省"},
    {"id": 20, "label": "海南省"},
    {"id": 21, "label": "四川省"},
    {"id": 22, "label": "云南省"},
    {"id": 23, "label": "陕西省"},
    {"id": 24, "label": "甘肃省"},
    {"id": 25, "label": "青海省"},
    {"id": 26, "label": "台湾省"},
    {"id": 27, "label": "内蒙古自治区"},
    {"id": 28, "label": "广西壮族自治区"},
    {"id": 29, "label": "西藏自治区"},
    {"id": 30, "label": "宁夏回族自治区"},
    {"id": 31, "label": "新疆维吾尔自治区"},
    {"id": 32, "label": "香港特别行政区"},
    {"id": 33, "label": "澳门特别行政区"},
]

ai_ids = [key for key in range(1, 11)]

current_date = date(2025, 10, 12)

current_date += timedelta(days=1)

print(current_date.isoformat())
