from common_util.log_util import tem_file_path, tem_file_name, un_tem_file_path
import os

# 临时文件夹
TEM_PATH = tem_file_path
# 临时文件
TEM_FILE = tem_file_name
# 非临时文件
UN_TEM_PATH = un_tem_file_path

if not os.path.exists(UN_TEM_PATH):
    os.makedirs(UN_TEM_PATH)

if not os.path.exists(TEM_PATH):
    os.makedirs(TEM_PATH)
