import redis
from common_util.redis_util.redis_conf import redis_dic
import traceback


# pool = redis.ConnectionPool(host='10.0.20.66', port=6379, db=10, password='')
# r = redis.Redis(connection_pool=pool)


class RedisUtil:

    # 键值对的形式存储数据库名称和数据库连接对象
    connecting_db_dic = {}

    @classmethod
    # 获取数据库连接，传入数据库配置key名，在psql_conf.py中
    def get_pool(cls, redis_name):
        assert (isinstance(redis_name, str))
        # 如果是已经存在的数据库连接，则直接返回该连接，如果是不存在的连接，先创建再返回
        try:
            if len(cls.connecting_db_dic) > 0:
                db = cls.connecting_db_dic[0]
            else:
                pool = redis.ConnectionPool(**redis_dic[redis_name])

                cls.connecting_db_dic[redis_name] = pool
                print('数据库连接成功，参数为：', redis_dic[redis_name])
            return pool
        except Exception as e:
            print('数据库连接失败，原因：' + str(e))
            print(traceback.format_exc())

    @classmethod
    # 先检查connecting_db_dic有没有已经存在的连接池，如果有，则在此基础上直接生成db，若没有，则先生成连接池再生成db
    def get_conn(cls, redis_name):
        if redis not in cls.connecting_db_dic:
            pool = cls.get_pool(redis_name)
        else:
            pool = cls.connecting_db_dic[redis_name]
        db = redis.Redis(connection_pool=pool)
        return db

    @classmethod
    # 关闭单个数据库，传入数据库名字，进行关闭
    def close_by_name(cls, redis_name):
        assert (isinstance(redis_name, str))
        try:
            del cls.connecting_db_dic[redis_name]
        except Exception as e:
            print(redis_name+' 数据库不存在或数据库未连接或数据库关闭失败，具体原因：' + str(e))
            print(traceback.format_exc())

    @classmethod
    # 关闭当前所有连接的数据库
    def close_all(cls):
        for _db_name in list(cls.connecting_db_dic.keys()):
            cls.close_by_name(_db_name)


if __name__ == '__main__':
    # 获取key为formal_rc_prd的数据库连接
    db1 = RedisUtil.get_conn('test_db')
    # 获取key为formal_application_db的数据库连接
    db2 = RedisUtil.get_conn('formal_db')
    # 获取key为formal_application_db的数据库连接
    db3 = RedisUtil.get_conn('formal_db')

    # 打印3个连接对象的十进制的内存地址
    print(id(db1))
    print(id(db2))
    print(id(db3))
    # 通过打印，发现db2和db3的内存地址相同，说明相同连接名指向同一个内存地址

    # 断开数据库名为formal_rc_prd的数据库连接
    RedisUtil.close_by_name('test_db')
    # 断开所有数据库连接
    RedisUtil.close_all()
