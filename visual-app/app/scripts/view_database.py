import os
import argparse
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def get_conn():
    """连接指定数据库"""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,  # 返回字典，方便看
    )


def show_tables():
    """查看所有表"""
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            rows = cursor.fetchall()
            if not rows:
                print("当前数据库没有表")
                return
            print(f"数据库 {DB_NAME} 共 {len(rows)} 张表：")
            for row in rows:
                # SHOW TABLES 返回的 key 是动态的，取第一个值
                print(" -", list(row.values())[0])
    finally:
        conn.close()


def show_columns(table: str):
    """查看某张表的字段结构"""
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"DESCRIBE `{table}`")
            rows = cursor.fetchall()
            if not rows:
                print(f"表 {table} 不存在或没有字段")
                return
            print(f"表 {table} 的字段结构：")
            for row in rows:
                print(
                    f"  {row['Field']:<15} {row['Type']:<15} "
                    f"NULL={row['Null']:<4} KEY={row['Key']:<4} DEFAULT={row['Default']}"
                )
    finally:
        conn.close()


def show_data(table: str, limit: int = 10):
    """查看某张表的数据，默认前 10 条"""
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{table}` LIMIT {limit}")
            rows = cursor.fetchall()
            if not rows:
                print(f"表 {table} 没有数据")
                return
            print(f"表 {table} 前 {len(rows)} 条数据：")
            for row in rows:
                print(" ", row)
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="数据库查看工具")
    parser.add_argument(
        "action",
        choices=["tables", "columns", "data"],
        help="tables=看所有表, columns=看表结构, data=看表数据",
    )
    parser.add_argument("--table", "-t", help="表名（columns/data 必填）")
    parser.add_argument("--limit", "-l", type=int, default=10, help="查看数据条数，默认 10")

    args = parser.parse_args()

    if args.action == "tables":
        show_tables()
    elif args.action == "columns":
        if not args.table:
            print("请用 --table 指定表名")
            return
        show_columns(args.table)
    elif args.action == "data":
        if not args.table:
            print("请用 --table 指定表名")
            return
        show_data(args.table, args.limit)


if __name__ == "__main__":
    show_data('ai_info')
