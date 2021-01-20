# -*- encoding: UTF-8 -*-
from DingDingBot.DDBOT import DingDing

import settings


def notify(msg=None, type='TEXT'):
    if settings.NOTIFY:
        if msg is None or not msg:
            return
    dd = DingDing(
        webhook='https://oapi.dingtalk.com/robot/send?access_token=4f7745a212c76d23f3b65150e19669fa3335a1640f7a1226f2c1f061ed03db22')
    strategies = {
        'TEXT': lambda msg: print(dd.Send_Text_Msg(Content=msg+'stocks', isAtAll=True)),
        'LINK': lambda msg: print(
            type + ":" + dd.Send_Link_Msg(Content='stocks', Title=msg, MsgUrl='https://www.baidu.com',
                                          PicUrl='https://cn.bing.com/images/search?q=outgoing%e6%9c%ba%e5%99%a8%e4%ba%ba&id=FEE700371845D9386738AAAA51DCC43DC54911AA&FORM=IQFRBA')),
        'MARK_DOWN': lambda msg: (print(msg),
                                  print(dd.Send_MardDown_Msg(Content=msg+'stocks', Title='stocks')))
    }
    return strategies[type](msg)


if __name__ == '__main__':
    settings.init()
    notify(msg="stocks", type="TEXT")
