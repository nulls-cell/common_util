from redis_util.publish_and_subscribe import RedisHelper

# 获取连接
r = RedisHelper().get_conn()
# 开发频道选择器
chan = r.pubsub()
# 连接到频道
chan.subscribe("lr_chann")
# 初始化接收队列，默认会返回来 (message, lr_chann, 1) 这个元祖
msgs = chan.parse_response()

# 写死循环，默认阻塞状态，有消息发布过来就会进行接收处理
while True:
    msgs = chan.parse_response()
    if isinstance(msgs[2], bytes):
        print(msgs[2].decode('utf-8'))
    else:
        print(str(msgs[2]))
