import datetime

import akshare as ak
import tushare as ts

import settings
import testnotice
from query import util
import pandas as pd
import numpy as np


def queryAll():
    list = []
    pro = ts.pro_api(token=settings.TOKEN)
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,area,industry,list_date')
    data.columns = ['序列', '代码', '所在地域', '所属行业', '上市日期']
    data.to_csv('./data/all_stocks.csv')
    list.append('查询成功')
    return list


def executeBasic():
    streage = {
        '查询所有股票信息': queryAll,
    }
    for item, fuc in streage.items():
        mec = fuc()
        for i in mec:
            testnotice.notify(
                '"{0}"\n{1}'.format(item, i))


if __name__ == '__main__':
    # queryJGTJ()
    settings.init()
    executeBasic()
