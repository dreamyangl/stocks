import pandas as pd
last = pd.read_csv('./data/up_limit_up20210126.csv')
now = pd.read_csv('./data/up_limit_up20210127.csv')
data = last.merge(now,on='代码')
print(data)