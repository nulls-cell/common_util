"""
需要注意的是，redis的订阅功能并不适合做消息队列，因为订阅者只能接收到自己订阅时间点之后，发布者发布的消息
就是说订阅者一旦宕机，宕机期间，发布者发布的消息将全部丢失，且无任何交互，并不是一种稳定的方式
"""

from redis_util.redis_conn import RedisUtil

class RedisHelper(object):

    def __init__(self):
        self.__conn = RedisUtil.get_conn('lr_db')
        self.chan_sub = 'lr_chann'
        self.chan_pub = 'lr_chann'

    # 获取连接
    def get_conn(self):
        return self.__conn

    # 发布消息
    def public(self, msg):
        self.__conn.publish(self.chan_pub, msg)
        return True

    # 订阅并接收消息
    def subscribe(self):
        pub = self.__conn.pubsub()   # 打开收音机
        pub.subscribe(self.chan_sub)  # 订阅频道
        pub.parse_response()  # 等待消息
        return pub   # 开始接收并返回消息


if __name__ == '__main__':
    t = RedisHelper()
    t.public('test') #发布了test这个消息

