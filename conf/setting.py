# 导入日志模块，用于记录程序运行时的信息
import logging
# 导入os模块，用于与操作系统交互，如此处用于处理文件路径
import os
# 导入sys模块，用于访问与Python解释器相关的变量和函数，如此处用于修改模块搜索路径
import sys

# 获取当前文件所在目录的上两级目录，即项目的根目录
DIR_PATH = os.path.dirname(os.path.dirname(__file__))
# 将项目根目录添加到Python的模块搜索路径中，这样就可以在任何地方直接导入项目中的模块
sys.path.append(DIR_PATH)

# 文件路径设置: 定义一个字典来集中管理项目中用到的各个文件和目录的路径
FILE_PATH = {
    # 日志文件存放目录
    'LOG': os.path.join(DIR_PATH, 'log'),
    'extract': os.path.join(DIR_PATH,'data', 'extract.yaml'),
    'yaml': os.path.join(DIR_PATH, 'testcase', 'login.yaml'),
    'conf': os.path.join(DIR_PATH, 'conf', 'config.ini')
}

