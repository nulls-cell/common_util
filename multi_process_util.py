#  !!!!!!!注意此方法在windows下无效，请在linux系统下执行！！！！！！！！
from multiprocessing import Pool, Manager
import time
import os
from common_util.log_util import get_logger

# 初始化进程锁（注意在使用进程池的时候要用Manager的Lock）
lock = Manager().Lock()
path = os.path.dirname(os.path.abspath(__file__))
logger = get_logger(log_path=path+'/tem.log')

# 此函数用于多进程的“无”返回值的函数执行，func为传入的函数，argvs为传入函数的元祖构成的列表，callback为函数的回调函数，process_num为进程数量
# argvs按照列表套元祖的形式传入，如[(argv11,argv12),(argv21,argv22)]，每个元祖元素的个数代表func接收的参数的个数，传多了或少了都会报错；
# callback为回调函数，接收的参数为func的return的结果
def multi_exec_func(func, argvs, callback=None, process_num=8):
    pool = Pool(processes=process_num)
    for argv_tuple in argvs:
        # 将func的多个参数按照元祖的形式传入，如：
        pool.apply_async(func,args=argv_tuple, callback=callback)
    pool.close()
    pool.join()


# 此函数用于多进程的“有”返回值的函数执行，func为传入的函数，argvs为传入函数的元祖构成的列表，callback为函数的回调函数，process_num为进程数量
# 最终returnt的结果为每个func返回值组成的列表，callback函数的返回值无法通过此函数拿到，需要通过其他交互方式，比如队列，此处不再多赘述
def multi_exec_func_result(func, argvs, callback=None, process_num=8):
    pool = Pool(processes=process_num)
    res_list = []
    for argv_tuple in argvs:
        res = pool.apply_async(func, argv_tuple, callback=callback)
        res_list.append(res)
    pool.close()
    pool.join()
    return [x.get() for x in res_list]


# 专门用于多进程的类装饰器，用于打印此进程的pid，使用方法如下：
# func_decorate = OutputPid(func)
# func_decorate()
class OutputPidAndName:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("当前进程的pid为：%s，函数名为：%s" % (os.getpid(), self.func.__name__))
        # 注意这里要return结果，callback函数才能正常收到参数
        return self.func(*args, **kwargs)


# 测试用的函数，用于测试上面定义的多进程函数
if __name__ == '__main__':

    # 初始化参数
    argvs = [('http://maoyan.com/board/' + str(x), lock) for x in range(1, 11)]
    # 初始化文件，用于加锁测试
    f = open('temfile.txt', 'a', encoding='utf-8')

    # 测试多进程的函数，内部包含进程锁（注意，在多进程下，暂时不是使用装饰器，此问题待解决）
    def get_page(url, lock=lock):
        global f
        print('(进程 %s) 正在下载页面 %s' % (os.getpid(), url))
        lock.acquire()
        f.write('(进程 %s) 正在下载页面 %s' % (os.getpid(), url) + '\n')
        f.flush()
        logger.info('(进程 %s) 正在下载页面 %s' % (os.getpid(), url))
        lock.release()
        time.sleep(1)
        # 返回参数用于回调函数的参数
        return url + 'result'

    # get_page的回调函数，接收get_page返回的数据作为参数，继续执行
    def parse_page(page_content):
        print('<进程 %s> 正在解析页面: %s' % (os.getpid(), page_content))

    # get_page函数用OutputPidAndName装饰器包裹，注意此处一定要用类装饰器，且不能使用@装饰器的语法糖
    get_page_decorate = OutputPidAndName(get_page)

    # 无返回值的多进程执行
    multi_exec_func(get_page_decorate, argvs=argvs, callback=parse_page, process_num=10)

    # 带返回值的多进程执行，注意res_list接收到的是get_page主函数的返回结果，而非callback函数的返回结果
    res_list = multi_exec_func_result(get_page_decorate, argvs=argvs, callback=parse_page,process_num=10)
    for res in res_list:
        print(res)
