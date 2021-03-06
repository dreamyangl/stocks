from datetime import datetime

import pandas as pd

import settings
import testnotice
from query.testScrapy import LimitUp


def todayLimitUp():
    list = []
    lu = LimitUp()
    today = datetime.now().strftime('%Y%m%d')
    start = today
    end = today
    lu.crawlData(start, end)
    try:
        limitUpData = pd.read_csv('./data/limit_up.csv')
    except Exception as e:
        return list
    if (pd.DataFrame(limitUpData).empty):
        return list
    limitUpData = limitUpData[(~limitUpData['名称'].str.contains('ST'))]
    allStockData = pd.read_csv('./data/all_stocks.csv')
    data = limitUpData.merge(allStockData, on='代码')
    data.to_csv('./data/limit_up_merge_data')
    groupData = data.groupby('所属行业')
    data = groupData['成交额（元）'].agg(['count']).sort_values('count', ascending=False)
    # data = groupData.agg({'成交额（元）': ['count', 'sum'], '涨停时间': 'min'})
    list.append(data.to_csv())
    return list


def isNotify():
    now = datetime.now()
    if (now.isoweekday() == 6 or now.isoweekday() == 7):
        return False
    amStartTime = datetime.strptime(str(datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')
    amEndTime = datetime.strptime(str(datetime.now().date()) + '13:00', '%Y-%m-%d%H:%M')
    pmStartTime = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    pmEndTime = datetime.strptime(str(datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
    if now > amStartTime and now < amEndTime:
        return False
    if now > pmStartTime or now < pmEndTime:
        return False
    return True


def executeTodayLimitUp():
    if isNotify() == False:
        return
    streage = {
        '今日涨停股分类,除去st股': todayLimitUp,
    }
    for item, fuc in streage.items():
        mec = fuc()
        for i in mec:
            testnotice.notify(
                '"{0}"\n{1}'.format(item, i))


if __name__ == '__main__':
    settings.init()
    # executeTodayLimitUp()
    allStockData = pd.read_csv('./data/all_stocks.csv')
    print(allStockData[['代码','volume']])


    # df = pd.DataFrame(
    #     {
    #         "A": [1, 1, 2, 2],
    #         "B": [1, 2, 3, 4],
    #         "C": [0.362838, 0.227877, 1.267767, -0.562860],
    #     }
    # )
    # print(df)
    # # data = df.groupby('A').B.agg(['min', 'max'])
    # data = df.groupby('A').agg({'B': ['min', 'max'], 'C': 'sum'})
    # print(data)
