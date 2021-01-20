import matplotlib.pyplot as mplt
import tushare as ts

# 支持中文
data = ts.inst_detail()
print(data)