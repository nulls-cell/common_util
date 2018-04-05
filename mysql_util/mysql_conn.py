import pymysql
from common_util.mysql_util.mysql_conf import mysql_dic
import traceback


class MysqlUtil:
    # 键值对的形式存储数据库名称和数据库连接对象
    connecting_db_dic = {}

    @classmethod
    # 获取数据库连接，传入数据库配置key名，在mysql_conf.py中
    def get_conn(cls, db_name):
        assert (isinstance(db_name, str))
        # 如果是已经存在的数据库连接，则直接返回该连接，如果是不存在的连接，先创建再返回
        try:
            if db_name in cls.connecting_db_dic:
                _db = cls.connecting_db_dic[db_name]
            else:
                _db = pymysql.connect(**(mysql_dic[db_name]))
                cls.connecting_db_dic[db_name] = _db
            print('数据库连接成功，参数为：', mysql_dic[db_name])
            return _db
        except Exception as e:
            print('数据库连接失败，原因：' + str(e))
            print(traceback.format_exc())

    @classmethod
    # 关闭单个数据库连接，传入数据库名字，进行关闭
    def close_by_name(cls, db_name):
        assert (isinstance(db_name, str))
        try:
            cls.connecting_db_dic[db_name].close()
            del cls.connecting_db_dic[db_name]
        except Exception as e:
            print(db_name + ' 数据库不存在或数据库未连接或数据库关闭失败，具体原因：' + str(e))
            print(traceback.format_exc())

    @classmethod
    # 关闭当前所有连接的数据库
    def close_all(cls):
        for _db_name in list(cls.connecting_db_dic.keys()):
            cls.close_by_name(_db_name)


if __name__ == '__main__':
    # 获取key为formal_rc_prd的数据库连接
    db1 = MysqlUtil.get_conn('test_db')
    # 获取key为formal_application_db的数据库连接
    db2 = MysqlUtil.get_conn('formal_db')
    # 获取key为formal_application_db的数据库连接
    db3 = MysqlUtil.get_conn('formal_db')

    # 打印3个连接对象的十进制的内存地址
    print(id(db1))
    print(id(db2))
    print(id(db3))
    # 通过打印，发现db2和db3的内存地址相同，说明相同连接名指向同一个内存地址

    # 断开数据库名为formal_rc_prd的数据库连接
    MysqlUtil.close_by_name('test_db')
    # 断开所有数据库连接
    MysqlUtil.close_all()
