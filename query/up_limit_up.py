import datetime, re, time, os, sys, sqlite3, random
import requests
import pandas as pd
import tushare as ts

import settings
import testnotice
from query.util import createDays


class LimitUp:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), 'data')
        self.header = {
            "Host": "homeflashdata2.jrj.com.cn",
            "Referer": "http://stock.jrj.com.cn/tzzs/zdtwdj/zdforce.shtml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        self.columns = [u'代码', u'名称', u'当前价格', u'涨幅', u'封单金额/日成交额', u'封单手数/流通股本', u'封单金额', u'第一次涨停时间',
                        u'最后一次涨停时间', u'打开次数', u'振幅', u'强度']

    # 要爬取的js地址
    def getUrl(self, date):
        return 'http://homeflashdata2.jrj.com.cn/limitStatistic/ztForce/' + date + ".js?_=" + str(
            int(round(time.time() * 1000)))

    # 请求原始内容
    def getData(self, date, retry=5):
        req = requests.get(self.getUrl(date), headers=self.header)
        for i in range(retry):
            try:
                content = req.text
                md_check = re.findall(r'"Data":\[\[', content)
                if content and len(md_check) > 0:
                    return content
                else:
                    time.sleep(60)
                    print('failed to get content, retry: {}'.format(i))
                    continue
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
        return None

    # 将原始内容转化为json
    def convertToJson(self, content):
        p = re.compile(r'"Data":(.*)};', re.S)
        if len(content) <= 0:
            print('Content\'s length is 0')
            exit(0)
        result = p.findall(content)
        if result:
            try:
                t1 = result[0]
                t2 = list(eval(t1))
                return t2
            except Exception as e:
                print(e)
                return None
        else:
            return None

    # 保存数据至csv文件和sqlite数据库
    def saveData(self, data, date):
        if not data:
            exit()
        df = pd.DataFrame(data, columns=self.columns)
        # 过滤st股
        df['封单金额/日成交额'] = df['封单金额/日成交额']*100
        df = df[(~df['名称'].str.contains('ST|N')) & (df['封单金额/日成交额'] > 50)]
        df = df.sort_values('封单金额/日成交额',ascending=False)
        filename = os.path.join(self.path, "up_limit_up" + ".csv")
        df.to_csv(filename)
        return df.to_csv()
        # try:
        #     df.to_sql(date, sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db_limit_up.db')),
        #               if_exists='fail')
        # except Exception as e:
        #     print(e)

    # 爬取、保存数据
    def crawlData(self, day):
        days = createDays(day,'%Y%m%d')
        list = []
        for date in days:
            # if not ts.is_holiday(datetime.datetime.strptime(date,'%Y%m%d').strftime('%Y-%m-%d')):
            print(date)
            content = self.getData(date)
            json = self.convertToJson(content)
            data = self.saveData(json, date)
            list.append(data)
            time.sleep(5)
        return list

        # else:
        #     print('Holiday')

def executeUplimitUp():
    lu = LimitUp()
    streage = {
        '可打板:': lu.crawlData,
    }
    for item, fuc in streage.items():
        mec = fuc(1)
        for i in mec:
            testnotice.notify(
                '"{0}"\n{1}'.format(item, i))


if __name__ == '__main__':
    settings.init()
    # executeUplimitUp()
    limitUp = pd.read_csv('./data/up_limit_up.csv')
    optionalStock = pd.read_csv('./data/optional_stock.csv')
    data = pd.concat([limitUp['代码'],optionalStock['代码']],axis=0)
    data.to_csv('./data/optional_stock.csv')
