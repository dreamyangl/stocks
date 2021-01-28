import datetime
import os
import sys
import time
import pandas as pd


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import schedule
from query.today_limit_up import executeTodayLimitUp
from query.basicdata import executeBasic
from query.aksharequery import executeAk
from query.akTodaysharequery import executeTodayAk
from query.limit_up import executeLimitUp

from query.suspend import execute

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import settings

from query.mechanismInfo import custom_stocks_streage
if __name__ == '__main__':
    # pd.set_option('display.unicode.ambiguous_as_wide', True)
    # pd.set_option('display.unicode.east_asian_width', True)
    # # 显示所有列
    # pd.set_option('display.max_columns', None)
    # # 显示所有行
    # pd.set_option('display.max_rows', None)
    settings.init()
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    EXEC_TIME_MECHANISMINFO = "21:00"
    schedule.every().days.at(EXEC_TIME_MECHANISMINFO).do(custom_stocks_streage)
    schedule.every().days.at(EXEC_TIME_MECHANISMINFO).do(executeAk)
    schedule.every().days.at(EXEC_TIME_MECHANISMINFO).do(executeBasic)
    schedule.every().days.at(EXEC_TIME_MECHANISMINFO).do(executeLimitUp)
    EXEC_TIME_SUSPEND = "08:30"
    schedule.every().days.at(EXEC_TIME_SUSPEND).do(execute)
    schedule.every(2).minutes.do(executeTodayLimitUp)
    schedule.every(1).minutes.do(executeTodayAk)
    while True:
        schedule.run_pending()
        time.sleep(30)
    # custom_stocks_streage()
    # execute()
    # executeAk()
    # executeTodayAk()
