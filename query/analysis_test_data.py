import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('./data/20210126_limit_up.csv')
    data['涨停时间'] = pd.to_datetime(data['涨停时间'])
    print(data.dtypes)
    data = data[(data['所属概念'].str.contains('重仓|预增')) & (
        ~data['名称'].str.contains('ST'))]
    data = data.sort_values('换手率（%）',ascending=False)
    data.to_csv('./data/test.csv')
