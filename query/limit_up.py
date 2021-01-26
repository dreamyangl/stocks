import pandas as pd

import settings
import testnotice


def limit_up():
    list = []
    data = pd.read_csv('./data/20210126_limit_up.csv')
    data['涨停时间'] = pd.to_timedelta(data['涨停时间'])
    print(data.dtypes)
    data = data[(data['所属概念'].str.contains('调研|预增|摘帽')) & (
        ~data['名称'].str.contains('ST'))]
    data = data.sort_values('换手率（%）', ascending=False)
    data = data[['代码', '名称', '涨停时间', '换手率（%）', '所属概念']]
    list.append(data)
    data.to_csv('./data/limit_up.csv')
    return list


def executeLimitUp():
    streage = {
        '涨停筛选 字段：代码 名称 涨停时间 换手率 所属概念': limit_up,
    }
    for item, fuc in streage.items():
        mec = fuc()
        for i in mec:
            testnotice.notify(
                '"{0}"\n{1}'.format(item, i))


if __name__ == '__main__':
    settings.init()
    executeLimitUp()
