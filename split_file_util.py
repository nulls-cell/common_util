import sys
import os
import datetime

if len(sys.argv) != 4:
    raise Exception("传输参数的数量不正确，应传入3个参数，参数的格式为：需要拆分的文件路径 将文件拆分到的文件夹路径 需要拆分的文件份数")

split_file_name, result_path, file_nums = sys.argv[1:]

# 处理成末尾带/的路径
result_path = (result_path.replace('\\', '/') + '/').replace('//', '/')
# 处理成整数
file_nums = int(file_nums)

if not os.path.exists(split_file_name):
    raise Exception("%s文件不存在" % split_file_name)

if not os.path.exists(result_path):
    raise Exception("%s文件夹路径不存在" % result_path)

print("切割的文件为：%s" % split_file_name)
print("切割后存入的文件夹为：%s" % result_path)
print("切分的文件份数为：%s" % file_nums)

print("开始时间：%s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
os.system('awk \'{number=NR%%%s;outputfilename="%s/output."number;print $0 > outputfilename}\' %s ' % (file_nums, result_path, split_file_name))
print("切分完毕")
result_list = ['%soutput.%s' %(result_path, i) for i in range(file_nums)]
print("切分后的文件列表为[%s ... %s]" % (result_list[0], result_list[-1]))
print("结束时间：%s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
