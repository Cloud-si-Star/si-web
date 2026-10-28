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


if __name__ == '__main__':
    nst = 'ods_sales,dwd_sales_detail,dws_sales_daily,dws_sales_daily_category,dws_sales_monthly_region'
    xhxchangehg(nst)
