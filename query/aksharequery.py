import datetime

import akshare as ak

# 603565
# df = ak.stock_zh_a_new().sort_values('amount',ascending=False).head(50)
# df = df[df['code']=='688819']
# 603565
import schedule

import settings
import testnotice
from query import util
import pandas as pd
import numpy as np


def queryJGTJ():
    list = []
    stock_em_jgdy_tj_df = ak.stock_em_jgdy_tj()
    days = util.days(3)
    data = stock_em_jgdy_tj_df[stock_em_jgdy_tj_df['接待日期'].isin(days)]
    data['接待机构数量'] = data['接待机构数量'].astype('int')
    data = data.sort_values('接待机构数量', ascending=False)
    data = data[['代码', '名称', '最新价', '涨跌幅', '接待日期', '公告日期', '接待机构数量']]
    # data.to_csv('./JGTJ.csv')
    list.append(data.to_csv())
    return list


def query():
    stock_sector_fund_flow_rank_df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
    print(stock_sector_fund_flow_rank_df)
    stock_sector_fund_flow_rank_df = stock_sector_fund_flow_rank_df.sort_values(by='今日主力净流入-净额', ascending=False).head(
        10)
    print(stock_sector_fund_flow_rank_df)


def mainNetDaysPurchase():
    list = []
    df1 = ak.stock_individual_fund_flow_rank(indicator="5日")
    df1 = df1.drop(df1[(df1['主力净流入-净额'] == "-")].index)
    df1 = df1[(df1['涨跌幅'] < 9) & (~df1['名称'].str.contains('ST'))]
    df1['主力净流入-净额'] = df1['主力净流入-净额'].astype('float64')
    df1 = df1.sort_values('主力净流入-净占比', ascending=False)
    df1 = df1[['代码', '名称', '主力净流入-净额', '大单净流入-净占比', '超大单净流入-净占比', '涨跌幅', '主力净流入-净占比', ]].head(30)
    # df1.to_csv('./data.csv')
    list.append(df1)
    return list


def executeAk():
    streage = {
        '5日内主力净买入 字段:代码 名称 主力净流入-净额 主力净流入-净占比 涨跌幅 大单净流入-净占比 超大单净流入-净占比': mainNetDaysPurchase,
        '机构三日内调研,按调研机构数排序 字段:代码 名称 最新价 涨跌幅 接待日期 公告日期 接待机构数量': queryJGTJ,
    }
    for item, fuc in streage.items():
        mec = fuc()
        for i in mec:
            testnotice.notify(
                '"{0}"\n{1}'.format(item, i))
def testJob():
    print('111')

if __name__ == '__main__':
    # queryJGTJ()
    executeAk()