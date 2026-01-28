"""

"""
import configparser

from conf.setting import FILE_PATH
from logging_conf.logging_config import logs


class operationConfig():
    def __init__(self, file_path = None):
        if file_path is None:
            self.__yaml_file = FILE_PATH['conf']
        else:
            self.__yaml_file = file_path

        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__yaml_file,encoding='utf-8')
        except Exception as e:
            logs.error(f"读取配置文件{self.__yaml_file}失败：错误信息为:{e}")



    def get_section_for_data(self,section,option):
        """
        获取配置文件中的section
        :param section:
        :param option:
        :return:
        """
        try:
            data = self.conf.get(section,option)
            return data
        except Exception as e:
            logs.error(e)

    def get_envi(self,option):
        """
        获取环境变量
        :param option:
        :return:
        """
        return self.get_section_for_data('api_envi',option)

    def get_mysql_conf(self,option):
        """
        获取mysql配置
        :param option:
        :return:
        """
        return self.get_section_for_data('MYSQL',option)



if __name__ == '__main__':
    config = operationConfig()
    host = config.get_envi('host') + "/login/user"
    print(host)

