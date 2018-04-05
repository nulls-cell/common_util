from redis_util.publish_and_subscribe import RedisHelper
import time

# 获取redis连接
r = RedisHelper().get_conn()

# 每间隔3秒，向频道lr_chann发送消息
for i in range(100):
    r.publish('lr_chann', '第%s条消息被发布' % i)
    print('第%s条消息被发布' % i)
    time.sleep(3)