"""
    日志模块配置
"""
import datetime
import logging.config
import os
import pathlib
import time
from logging.handlers import RotatingFileHandler

from conf import setting

#设置日志目录
LOG_PATH = setting.FILE_PATH['LOG']
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
    print(f"日志目录创建成功: {LOG_PATH}")
#设置日志文件名
LOG_FILE_NAME = os.path.join(LOG_PATH,f"test.{time.strftime('%Y%m%d')}.log")

def get_logger():
    #读取loggin.ini 配置文件
    logging_path_ini =pathlib.Path(__file__).parents[0].resolve() / 'logging.ini'
    #通过logging.config.fileConfig()方法读取logging.ini配置文件
    logging.config.fileConfig(logging_path_ini,encoding='utf-8')
    #获取logger对象,生成日志记录器
    logger = logging.getLogger(__name__) #__name__获取当前模块的名称

    #创建一个RotationFileHandler对象，用于日志文件的滚动
    flie_hander = RotatingFileHandler(filename=LOG_FILE_NAME, mode='a',maxBytes=5242880, backupCount=17,encoding='utf-8')
    #设置日志的等级
    flie_hander.setLevel(logging.DEBUG)
    #定义日志的格式
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s')
    flie_hander.setFormatter(formatter)
    #将文件处理器加入到logger日志记录器当中
    logger.addHandler(flie_hander)

    return logger

def clean_logger():
    """
    清理logger的过期文件
    """
    #获取当前的系统时间
    current_time = datetime.datetime.now()
    #创建一个表示30天前的时间增量
    offset_time = datetime.timedelta(days = -30)
    #计算出30天前的那个时间点的时间戳
    before_time = (current_time + offset_time).timestamp()
    #列出日志目录下的所有文件
    files = os.listdir(LOG_PATH)
    for file in files:
        #判断文件名是否有拓展名字，以此过滤掉文件夹
        if os.path.splitext(file)[1]:
            #拼接成完整的文件路径
            file_path = os.path.join(LOG_PATH, file)
            #获取文件创建时间的时间戳
            file_create_time = os.path.getctime(file_path)
            #判断文件创建时间是否早于30天前的时间点
            if file_create_time < before_time:
                #删除过期文件
                os.remove(file_path)
                print(f"删除过期文件: {file_path}")

#定义一个日志记录类
class MyLogger():
    def __init__(self):
        clean_logger() #在初始化时清理过期日志文件

    def log(self):
        logger = get_logger()
        return logger

logger = MyLogger()
logs = logger.log()
