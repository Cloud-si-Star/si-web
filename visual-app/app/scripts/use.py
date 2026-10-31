import os
import sys

# 让 Spark 的 driver 和 worker 都使用当前 venv 的 Python
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable


def splitChar(charset: str, type: int):
    char = charset.split(',')
    for value in char:
        if (type == 1):
            text = 'route_run_' + value
        if (type == 2):
            text = 'route_query_' + value
        print(text)


def xhxchangehg(char: str):
    char = char.split(',')
    for value in char:
        print(value.replace('_', '-'))


from pyspark.sql import SparkSession


def test_spark():
    spark = SparkSession.builder.appName("test").getOrCreate()
    data = [("Alice", 25), ("Bob", 30)]
    df = spark.createDataFrame(data, ["name", "age"])
    df.show()
    spark.stop()


if __name__ == '__main__':
    nst = 'ods_sales,dwd_sales_detail,dws_sales_daily,dws_sales_daily_category,dws_sales_monthly_region'
    # xhxchangehg(nst)
    test_spark()
