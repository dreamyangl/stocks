import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体：解决plot不能显示中文问题
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

index = [i for i in range(2, 12)]
print(index)
col1 = pd.date_range('2021-01-10', '2021-01-19')
col2 = np.random.randint(11, 20, 10)
data = pd.DataFrame({'col1': col1, 'col2': col2}, index=index)
print(data)
data.plot('col1', 'col2')
plt.show()
print(data.sample(n=2, axis=1))
