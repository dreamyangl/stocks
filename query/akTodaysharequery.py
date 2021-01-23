import datetime

import akshare as ak
import tushare as ts

# 603565
# df = ak.stock_zh_a_new().sort_values('amount',ascending=False).head(50)
# df = df[df['code']=='688819']
# 603565
import settings
import testnotice
from query import util
import pandas as pd
import numpy as np


def mainNetInflow(data):
    list = []
    data = data.sort_values('主力净流入-净额', ascending=False)
    data = data[['代码', '名称', '主力净流入-净额', '大单净流入-净占比', '超大单净流入-净占比', '涨跌幅', '主力净流入-净占比', ]].head(30)
    data.to_csv('../data/todaydata.csv')
    list.append(data)
    return list


def up(data):
    list = []
    data = data.sort_values('涨跌幅', ascending=False).head(20)
    data = data.sort_values('超大单净流入-净占比', ascending=False)
    data = data[['代码', '名称', '主力净流入-净额', '大单净流入-净占比', '超大单净流入-净占比', '涨跌幅', '主力净流入-净占比', ]]
    data.to_csv('../data/up.csv')
    list.append(data)
    return list


def optionalStock(data):
    list = []
    optionalStock = pd.read_csv('../data/optional_stock.csv')
    todayOptionalStock = pd.merge(optionalStock, data, on=['代码'])
    todayOptionalStock = todayOptionalStock[['代码', '名称', '主力净流入-净额', '大单净流入-净占比', '超大单净流入-净占比', '涨跌幅', '主力净流入-净占比', ]]
    list.append(todayOptionalStock)
    return list


def executeTodayAk():
    # 上午11点半到1点不查询
    if isNotify() == False:
        return
    data = ak.stock_individual_fund_flow_rank(indicator="今日")
    data = data.drop(data[(data['主力净流入-净额'] == "-")].index)
    data = data[(data['涨跌幅'] < 9.5) & (~data['名称'].str.contains('ST'))]
    data['代码'] = data['代码'].astype('int64')
    data['主力净流入-净额'] = data['主力净流入-净额'].astype('float64')
    data['主力净流入-净占比'] = data['主力净流入-净占比'].astype('float64')
    streage = {
        '今日主力净买入排序前30 字段:代码 名称 主力净流入-净额 超大单净流入-净占比 涨跌幅 大单净流入-净占比 主力净流入-净占比': mainNetInflow,
        '涨跌幅，超大单排序前30 字段:代码 名称 主力净流入-净额 超大单净流入-净占比 涨跌幅 大单净流入-净占比 主力净流入-净占比': up,
        '自选股 字段:代码 名称 主力净流入-净额 超大单净流入-净占比 涨跌幅 大单净流入-净占比 主力净流入-净占比': optionalStock,
    }
    for item, fuc in streage.items():
        mec = fuc(data)
        for i in mec:
            testnotice.notify(
                '"{0}"\n{1}'.format(item, i))


def isNotify():
    now = datetime.datetime.now()
    amStartTime = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')
    amEndTime = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:00', '%Y-%m-%d%H:%M')
    pmStartTime = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    pmEndTime = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:15', '%Y-%m-%d%H:%M')
    if now > amStartTime and now < amEndTime:
        return False
    if now > pmStartTime or now < pmEndTime:
        return False
    return True


if __name__ == '__main__':
    settings.init()
    # executeTodayAk()
    pro = ts.pro_api(token=settings.TOKEN)
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    data.colum = ['序列','代码','名称','所在地域','所属行业','上市日期']
    todayData = pd.read_csv('../data/todaydata.csv')
    pd.merge(data,todayData,on = '代码')
    data.to_csv('../data/all_stocks.csv')
