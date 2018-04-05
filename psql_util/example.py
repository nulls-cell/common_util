from common_util.psql_util.psql_conn import PsqlUtil

if __name__ == '__main__':
    # 获取key为formal_rc_prd的数据库连接
    db1 = PsqlUtil.get_conn('test_db')
    # 获取key为formal_application_db的数据库连接
    db2 = PsqlUtil.get_conn('formal_db')
    # 获取key为formal_application_db的数据库连接
    db3 = PsqlUtil.get_conn('formal_db')

    # 打印3个连接对象的十进制的内存地址
    print(id(db1))
    print(id(db2))
    print(id(db3))
    # 通过打印，发现db2和db3的内存地址相同，说明相同连接名指向同一个内存地址

    # 断开数据库名为formal_rc_prd的数据库连接
    PsqlUtil.close_by_name('test_db')
    # 断开所有数据库连接
    PsqlUtil.close_all()
