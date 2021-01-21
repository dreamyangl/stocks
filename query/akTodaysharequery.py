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


def mainNetTodayPurchase():
    list = []
    df1 = ak.stock_individual_fund_flow_rank(indicator="今日")
    df1 = df1.drop(df1[(df1['主力净流入-净额'] == "-")].index)
    df1 = df1[(df1['涨跌幅'] < 9) & (~df1['名称'].str.contains('ST'))]
    df1['主力净流入-净额'] = df1['主力净流入-净额'].astype('float64')
    df1 = df1.sort_values('主力净流入-净额', ascending=False)
    df1 = df1[['代码', '名称', '主力净流入-净额', '大单净流入-净占比', '超大单净流入-净占比', '涨跌幅', '主力净流入-净占比', ]].head(30)
    df1.to_csv('./todaydata.csv')
    list.append(df1)
    return list


def executeTodayAk():
    # 上午11点半到1点不查询
    if isNotify() == False:
        return
    streage = {
        '今日主力净买入 字段:代码 名称 主力净流入-净额 主力净流入-净占比 涨跌幅 大单净流入-净占比 超大单净流入-净占比': mainNetTodayPurchase,
    }
    for item, fuc in streage.items():
        mec = fuc()
        for i in mec:
            testnotice.notify(
                '"{0}"\n{1}'.format(item, i))


def isNotify():
    time = datetime.datetime.now()
    # 二进制与 必须全部满足
    if time.hour >= 11 & time.minute > 30 & time.hour <= 13:
        return False
    # 下午三点到9点不查询    逻辑or 一个满足直接返回
    if time.hour >=15 or time.hour < 9:
        return False
    return True


if __name__ == '__main__':
    # settings.init()
    # pd.set_option('display.float_format', lambda x: '%.2f' % x)
    # executeTodayAk()
    print(isNotify())
    # index = pd.date_range('1/1/2000', periods=8)
    # data = pd.DataFrame(np.random.randn(8, 3), index=index,
    #                     columns=['A', 'B', 'C'])
    # print(data)
    # print(data.sum())

    stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000002", start_date="20210120", end_date="20210121",
                                                  adjust="qfq")
    print(stock_zh_a_daily_qfq_df)
