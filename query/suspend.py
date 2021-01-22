import tushare as ts
import settings
from datetime import datetime

import testnotice


def suspendInfo():
    pro = ts.pro_api(settings.TOKEN)
    df = pro.suspend(resume_date=datetime.today().strftime("%Y%m%d"), fields='')
    return df.to_csv()
def execute():
    streage = {
        '今日复牌信息 字段: 股票代码 停牌日期 复牌日期 公告日期 停牌原因 停牌原因类别': suspendInfo
    }
    for des,value in streage.items():
        data = value()
        testnotice.notify(
            '"{0}"\n{1}'.format(des, data))

if __name__ == '__main__':
    settings.init()
    # execute()
    # settings.init()
    # pro = ts.pro_api(settings.TOKEN)
    # df = pro.suspend_d(suspend_type='R', trade_date='20210118')
    # print(df)
    df = ts.get_today_ticks('600460')
    print(df.tail(10))