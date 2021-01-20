# -*- encoding: UTF-8 -*-
from datetime import datetime

import sys
import os

from query.util import is_today

import tushare as ts
import settings
import testnotice
import schedule


# 机构席位追踪
def institutional_seat_tracking(mechanism1):
    list = []
    list.append(mechanism1.to_csv())
    return list



def institutional_seat_tracking_detail(mechanism1):
    list = []
    mechanism2 = ts.inst_detail()
    mechanism1.apply(lambda row: list.append(mechanism2[mechanism2['code'] == row['code']].to_csv()),
                     axis=1)
    return list


def profit(mechanism1):
    list = []
    df = ts.profit_data(top=10, year=datetime.now().year - 1).sort_values('shares', ascending=False)
    df.apply(lambda row: list.append(row.to_csv()) if
    is_today(row['report_date']) == True else None, axis=1)
    return list

def today_institutional_seat_tracking_detail(mechanism1):
    list = []
    data = ts.inst_detail()
    data = data[data['date'] == datetime.today().strftime('%Y-%m-%d')]
    print(data)
    # data['net'] = data.apply((lambda row: row['bamount'] - row['samount']), axis=1)
    data['net'] = data['bamount'] - data['samount']
    data = data.sort_values('net', ascending=False).head(10)
    list.append(data.to_csv())
    return list


def custom_stocks_streage():
    streage = {
        '机构五日内买卖数据按买入 - 卖出倒序\n字段：代码 名称 累积买入额(万) 买入次数 累积卖出额(万) 卖出次数 净额(万)': institutional_seat_tracking,
        '成交明细': institutional_seat_tracking_detail,
        '5天之内公布的分配预案\n字段：股票代码 股票名称 分配年份 公布日期 分红金额（每10股）:转增和送股数（每10股)': profit,
        '今日机构买卖数据按买入 - 卖出倒序\n字段：代码 股票名称 交易日期 机构席位买入额(万) 机构席位卖出额(万) type 差额': today_institutional_seat_tracking_detail
    }
    data = ts.inst_tops().sort_values(by='net', ascending=False).head(5)
    for item, fuc in streage.items():
        mec = fuc(data)
        for i in mec:
            testnotice.notify(
                '"{0}"\n{1}'.format(item, i))


if __name__ == '__main__':
    data = ts.get_today_all().sort_values('amount',ascending=False).head(10).to_csv()
    print(data)
    # settings.init()
    # EXEC_TIME = "14:41"
    # schedule.every().days.at(EXEC_TIME).do(custom_stocks_streage)
    # while True:
    #     schedule.run_pending()
    # settings.init()
    # custom_stocks_streage()
