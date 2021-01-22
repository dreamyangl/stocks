import datetime

import akshare as ak

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
    data.to_csv('./todaydata.csv')
    list.append(data)
    return list


def up(data):
    list = []
    data = data.sort_values('涨跌幅', ascending=False).head(10)
    data = data.sort_values('超大单净流入-净占比', ascending=False)
    data = data[['代码', '名称', '主力净流入-净额', '大单净流入-净占比', '超大单净流入-净占比', '涨跌幅', '主力净流入-净占比', ]]
    data.to_csv('./up.csv')
    list.append(data)
    return list


def executeTodayAk():
    # 上午11点半到1点不查询
    if isNotify() == False:
        return
    data = ak.stock_individual_fund_flow_rank(indicator="今日")
    data = data.drop(data[(data['主力净流入-净额'] == "-")].index)
    data = data[(data['涨跌幅'] < 9.5) & (~data['名称'].str.contains('ST'))]
    data['主力净流入-净额'] = data['主力净流入-净额'].astype('float64')
    data['主力净流入-净占比'] = data['主力净流入-净占比'].astype('float64')
    streage = {
        '今日主力净买入排序前30 字段:代码 名称 主力净流入-净额 超大单净流入-净占比 涨跌幅 大单净流入-净占比 主力净流入-净占比': mainNetInflow,
        '涨跌幅，超大单排序前30 字段:代码 名称 主力净流入-净额 超大单净流入-净占比 涨跌幅 大单净流入-净占比 主力净流入-净占比': up,
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
    isNotify()
    # pd.set_option('display.float_format', lambda x: '%.2f' % x)
    # executeTodayAk()
    # print(isNotify())
    # executeTodayAk()
    # index = pd.date_range('1/1/2000', periods=8)
    # data = pd.DataFrame(np.random.randn(8, 3), index=index,
    #                     columns=['A', 'B', 'C'])
    # print(data)
    # print(data.sum())
