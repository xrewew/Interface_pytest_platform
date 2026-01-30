"""
    工具类,#这里负责实现对于yaml里面所需要的功能
"""
import random
import re

from api_key.readyaml import ReadWriteYamlData


class DbugTalk:
    def __init__(self):
        self.read = ReadWriteYamlData()


    def get_extract_order_data(self,data,randoms):
        """
        获取extract.yaml数据，不为0、-1、-2，则按顺序读取文件key的数据，如输入3就是获取3个值
        :param data: extract.yaml文件中的数据
        :param randoms:
        :return:
        """
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]


    def get_extract_data(self,key,randoms=None) ->str:  #->str表示返回值为字符串类型
        """
        获取extract.yaml数据，首先判断randoms是否为数字类型，如果不是就获取下一个node节点的数据
        :param node_name: extract.yaml文件中的key值
        :param randoms: int类型，0：随机读取；-1：读取全部，返回字符串形式；-2：读取全部，返回列表形式；其他根据列表索引取值，取第一个值为1，第二个为2，以此类推;
        :return:
        """
        data = self.read.get_extract_yaml(key)
        if randoms is not None and bool(re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$').match(randoms)): #判断是否是数字
            randoms = int(randoms)
            data_value = {
                randoms:self.get_extract_order_data(data,randoms),
                0:random.choice(data),
                -1: ','.join(data),
                -2: ','.join(data).split(','),
            }
            data = data_value[randoms]
        else:
            return data
        return data

if __name__ == '__main__':
    xxx = DbugTalk()
    data = xxx.get_extract_data('goodsId',)
    print(type(data))
    print(data)
