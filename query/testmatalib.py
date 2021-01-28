import matplotlib.pyplot as plt
#mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']    # 指定默认字体：解决plot不能显示中文问题
plt.rcParams['axes.unicode_minus'] = False           # 解决保存图像是负号'-'显示为方块的问题
import pandas as pd
data = pd.read_csv('./data/plate_limit_up.csv')
data.plot('所属行业','count')
plt.show()
