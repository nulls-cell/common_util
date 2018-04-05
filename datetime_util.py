import datetime
import calendar


# n天之后，n可以是负数，返回datetime格式
def add_date(n):
    assert(isinstance(n, int))
    return datetime.datetime.now() + datetime.timedelta(days=n)


# 本月1日，返回datetime格式
def this_month_first():
    return datetime.datetime.now().replace(day=1)


# 本月最后一天，返回datetime格式
def this_month_last():
    _dt = datetime.datetime.now()
    _year = _dt.year
    _month = _dt.month
    last_day = calendar.monthrange(_year, _month)[1]
    return _dt.replace(day=last_day)


# 某个月的第一天
def month_first(dt):
    assert(isinstance(dt, datetime.datetime))
    return dt.replace(day=1)


# 某个月的最后一天
def month_last(dt):
    assert (isinstance(dt, datetime.datetime))
    _year = dt.year
    _month = dt.month
    last_day = calendar.monthrange(_year, _month)[1]
    return dt.replace(day=last_day)


# n个月之后的月初（n可以是负数），返回datetime格式
def next_n_month_first(n):
    assert(isinstance(n, int))
    dt = datetime.datetime.now()
    this_year = dt.year
    this_month = dt.month
    target_year = this_year + (n + this_month)//12
    target_month = (n + this_month) % 12
    return dt.replace(year=target_year, month=target_month, day=1)


# n个月之后的月末（n可以是负数），返回datetime格式
def next_n_month_last(n):
    dt = next_n_month_first(n)
    return month_last(dt)


# 字符串日期转时间戳，返回13位整形时间戳
def dtstr_to_timestamp(dt_str, dt_format):
    dt = datetime.datetime.strptime(dt_str, dt_format)
    return int(dt.timestamp()*1000)


# datetime格式日期转时间戳，返回13位整形时间戳
def dt_to_timestamp(dt):
    return int(dt.timestamp()*1000)


# 13位整形时间戳转日期，返回datetime格式
def timestamp_to_dt(_timestamp):
    assert(isinstance(_timestamp, int) and len(str(_timestamp)) == 13)
    return datetime.datetime.utcfromtimestamp(_timestamp/1000)


if __name__ == '__main__':
    print('5天之前：', add_date(-5).strftime('%Y-%m-%d'))
    print('本月第一天：', this_month_first().strftime('%Y-%m-%d'))
    print('本月最后一天：', this_month_last().strftime('%Y-%m-%d'))
    print('2019-5-18 的当月的第一天：', month_first(datetime.datetime(2019, 5, 18, 20, 18, 12)).strftime('%Y-%m-%d'))
    print('2019-5-18 的当月的最后一天：', month_last(datetime.datetime(2019, 5, 18, 20, 18, 12)).strftime('%Y-%m-%d'))
    print('11个月之后的当月第一天：', next_n_month_first(11).strftime('%Y-%m-%d'))
    print('15个月之前的当月最后一天：', next_n_month_last(-15).strftime('%Y-%m-%d'))
    print('2019-02-03 字符串转时间戳：', dtstr_to_timestamp('2019-02-03', '%Y-%m-%d'))
    print('2019-05-18 日期格式转时间戳：', dt_to_timestamp(datetime.datetime(2019, 5, 18)))
    print('时间戳转日期格式：', timestamp_to_dt(dtstr_to_timestamp('2019-02-03', '%Y-%m-%d')).strftime('%Y-%m-%d'))


