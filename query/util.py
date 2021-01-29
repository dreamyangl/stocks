import datetime
def is_today(target_date):
    """
    Detects if the date is current date
    :param target_date:
    :return: Boolean
    """
    # Get the year, month and day
    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month
    c_day = datetime.datetime.now().day

    # Disassemble the date
    date_list = target_date.split(" ")[0].split("-")
    t_year = int(date_list[0])
    t_month = int(date_list[1])
    t_day = int(date_list[2])

    final = False
    if c_year == t_year and c_month == t_month and c_day - t_day <= 5:
        final = True
    return final

# 生成几天内的日期
def createDays(day, format=None):
    if not format:
        format = '%Y-%m-%d'
    list = []
    for i in range(day):
       time = datetime.date.today()-datetime.timedelta(i)
       list.append(time.strftime(format))
    return list

if __name__ == '__main__':
    for i in createDays(1, '%Y%m%d'):
        print(i)
