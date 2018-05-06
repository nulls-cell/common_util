import socket
import json


# 获取本地ip
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    except Exception:
        print("未联网或ip获取失败，ip将被置为空字符串")
        return ''
    finally:
        s.close()


# 尝试转成json，如果出错，则给一个自定义的默认值
def try_transto_json(json_str, default_value):
    try:
        result = json.loads(json_str)
    except Exception as e:
        print(e)
        result = default_value
    return result