import logging
from os.path import dirname, abspath, exists
import sys
import socket
import datetime
import platform
import time
import traceback

# 今天的日期
dt = datetime.date.today().strftime('%Y-%m-%d')
# 本机的ip地址
ip = socket.gethostbyname((socket.gethostname()))

# window开发环境下
if platform.system() == 'Windows':
    # 文件和日志的主目录
    file_log_path = '/'.join(dirname(abspath(__file__)).split('\\')[:-1])+'/file_log'
    the_log_path = file_log_path + '/run_logs/windows_run_log.%s' % dt

# ip为生产环境
elif ip == '172.16.6.75':
    # 文件和日志的主目录
    file_log_path = '/'.join(dirname(abspath(__file__)).split('/')[:-1])+'/file_log'
    the_log_path = file_log_path + '/run_logs/shengchan_run_log.%s' % dt

# 其他ip或者ip为测试环境
else:
    # 文件和日志的主目录
    file_log_path = '/'.join(dirname(abspath(__file__)).split('/')[:-1]) + '/file_log'
    the_log_path = file_log_path + '/run_logs/ceshi_run_log.%s' % dt

# 临时文件夹
tem_file_path = dirname(dirname(abspath(__file__))) + '/file_log/tem_file/'
# 临时文件路径及名称，文件名为：时间戳.txt
tem_file_name = tem_file_path + str(time.time()) + '.txt'
# 非临时文件夹
un_tem_file_path = dirname(dirname(abspath(__file__))) + '/file_log/un_tem_file/'

# ##############################  以上为初始化的一些参数  #################################

"""
参数解释：
{'log_path':'日志写入文件路径', 'file_level':'日志写入文件的等级', 
'print_level':'日志打印到控制台的等级','log_name':'日志的名字'}
"""


def get_logger(log_path=the_log_path, file_level='INFO', print_level='INFO', log_name='new_log'):
    log_dir = dirname(log_path)
    print('日志路径：'+log_path)
    if not exists(log_dir):
        raise Exception("'%s' 文件夹路径不存在，请先创建路径" % log_dir)
    f_level = file_level.lower()
    p_level = print_level.lower()
    dic_level = {'debug': logging.DEBUG, 'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR,
                 'critical': logging.CRITICAL}
    for tem in [f_level, p_level]:
        if tem not in dic_level:
            raise Exception("日志等级或打印等级不符合条件")
    # 实例化一个名为new_log的logger
    logger = logging.getLogger(log_name)
    # 初始化默认所有级别日志都可以被写入和打印到控制台
    logger.setLevel(dic_level[f_level])
    # 创建日志写入文件工具fh，并把fh添加到logger
    fh = logging.FileHandler(log_path)
    fh.setLevel(dic_level[p_level])  # 设置写入文件的日志的级别
    formatter = logging.Formatter("%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s")
    fh.setFormatter(formatter)  # 设置日志写入文件格式为formatter
    # 添加日志打印到控制台工具sh，并把sh添加到logger
    sh = logging.StreamHandler()  # 实例化sh
    sh.setLevel(print_level)   # 设置打印到控制台的日志级别
    formatter = logging.Formatter("%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s")
    sh.setFormatter(formatter)  # 设置打印日志格式
    if not logger.handlers:
        logger.addHandler(fh)  # fh添加到logger
        logger.addHandler(sh)  # sh添加到logger
    return logger


if __name__ == '__main__':
    # 实例化日志对象
    logger = get_logger()
    # 几种类型的日志打印
    logger.info('abc')
    logger.error('def')
    logger.warning('ghi')

    # 捕获异常并打印到日志
    try:
        logger.info('计算除数为0的式子')
        a = 1/0
        logger.info('计算的结果为：%s' % a)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

