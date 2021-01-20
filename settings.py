# -*- encoding: UTF-8 -*-


def init():
    global DB_DIR, DATA_DIR, NOTIFY, CONFIG, STOCKS_FILE,MECHANISM_FILE,SALES_DEPARTMENT,\
        MECHANISM_DETAIL,MECHANISM_DETAIL_ORDER_BY_BUYCOUNT,TOKEN

    DATA_DIR = 'data'
    DB_DIR = 'storage'
    NOTIFY = True
    STOCKS_FILE = './storage/stocks.csv'
    MECHANISM_FILE = '../storage/mechanism.csv'
    SALES_DEPARTMENT = '../storage/sales_department.csv'
    MECHANISM_DETAIL = '../storage/mechanism_detail.csv'
    MECHANISM_DETAIL_ORDER_BY_BUYCOUNT = '../storage/mechanism_detail_order_by_buycount.csv'
    TOKEN = '6c0171c5179b008eedf3a32391be1ce08627e10684aa6215bc8edc28'
    # CONFIG = 'config/主板200亿-创业板100亿.xlsx'
    # CONFIG = 'config/沪深A股.xlsx'
