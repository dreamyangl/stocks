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
    limitUpData = pd.read_csv('./data/limit_up.csv')
    if (pd.DataFrame(limitUpData).empty):
        return
    limitUpData = limitUpData[(~limitUpData['名称'].str.contains('ST'))]
    allStockData = pd.read_csv('./data/all_stocks.csv')
    data = limitUpData.merge(allStockData, on='代码')
    groupData = data.groupby('所属行业')
    data = groupData['成交额（元）'].agg(['count']).sort_values('count', ascending=False)
    # data = groupData.agg({'成交额（元）': ['count', 'sum'], '涨停时间': 'min'})
    # data.to_csv('./data/plate_limit_up.csv')
    list.append(data.to_csv())
    return list


def executeTodayLimitUp():
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
    executeTodayLimitUp()

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
