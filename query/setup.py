import datetime
import os
import sys
import time
import pandas as pd

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import schedule
from query.aksharequery import executeAk
from query.akTodaysharequery import executeTodayAk

from query.suspend import execute

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import settings
from query.mechanismInfo import custom_stocks_streage

if __name__ == '__main__':
    settings.init()
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    EXEC_TIME_MECHANISMINFO = "21:00"
    schedule.every().days.at(EXEC_TIME_MECHANISMINFO).do(custom_stocks_streage)
    schedule.every().days.at(EXEC_TIME_MECHANISMINFO).do(executeAk)
    EXEC_TIME_SUSPEND = "08:30"
    schedule.every().days.at(EXEC_TIME_SUSPEND).do(execute)
    schedule.every(2).minutes.do(executeTodayAk)
    while True:
        schedule.run_pending()
        time.sleep(30)
    # custom_stocks_streage()
    # execute()
    # executeAk()
    # executeTodayAk()
