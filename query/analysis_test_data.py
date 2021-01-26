import pandas as pd
if __name__ == '__main__':
    data = pd.read_csv('./data/20210126_limit_up.csv')
    data = data[data['所属概念'].str.contains('重仓',case=True,na=False)]
    print(data)
