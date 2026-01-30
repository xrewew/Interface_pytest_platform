import os
import json
import yaml

from conf.setting import FILE_PATH
from logging_conf.logging_config import logs


class ReadWriteYamlData:
    def __init__(self, yaml_file = None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = 'test_cases/login/login.yaml'



    def write_yaml(self, value):
        """
        写入固定值到yaml当中
        :param value:
        :return:
        """
        file = None
        file_path = FILE_PATH['extract']
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path),exist_ok=True)
            logs.info(f'yaml文件{file_path}创建成功')
        try:
            file = open(file_path, 'a',encoding='utf-8')
            if isinstance(value, dict): #判断value是否是字典类型
                write_data = yaml.dump(value, allow_unicode=True,sort_keys=False) #yaml.dump写入数据，allow_unicode=True允许使用中文
                file.write(write_data)
            else:
                logs.info(f"写入数据到{file_path}失败，数据类型不是字典")
        except Exception as e:
            logs.info(f"写入数据到{file_path}失败：{e}")
        finally:
            if file:
                file.close()

    def get_extract_yaml(self,key,sec_key = None):
        """
        读取extract.yaml文件中的数据
        :return:
        """
        file_path = FILE_PATH['extract']
        if not os.path.exists(file_path):
            logs.info(f'extract.yaml文件不存在，无法读取{file_path}')
            os.makedirs(os.path.dirname(file_path),exist_ok=True)
            with open(file_path,'r',encoding='utf-8') as f:
                f.write('') #写入点东西以创建文件
            logs.info(f'extract.yaml创建成功{file_path}')
            return None

        try:
            with open(file_path,'r',encoding='utf-8') as f:
                extract_data = yaml.safe_load(f)
                if extract_data is None:
                    logs.info(f'警告：{file_path}文件为空')
                    return None
                if sec_key is None:
                    return extract_data[key]
                else:
                    if key in extract_data:
                        return extract_data[key][sec_key] #get()方法获取sec_key对应的值，如果不存在则返回None
                    return None

        except Exception as e:
            logs.info(f"读取文件{file_path}失败：错误信息为:{e}")
            return None

    def clean_yaml_data(self):
        with open(FILE_PATH['extract'],'w') as f:
            f.truncate() #清空文件内容




def get_yaml_data(file):

    #判断文件路径是否是相对路径，是的话就转换为绝对路径
    if not os.path.isabs(file): # os.path.isabs()判断是否是绝对路径
        #获取当前路径的目录
        current_path = os.path.dirname(os.path.abspath(__file__)) #os.path.abspath(__file__)获取当前文件的绝对路径，os.path.dirname()获取当前文件的目录
        #回到项目根目录
        project_root = os.path.dirname(current_path) #os.path.dirname()获取上一级目录
        #拼接文件路径
        file = os.path.join(project_root, file.lstrip('./')) #os.path.join()拼接路径

    logs.info(f"读取文件路径：{file}")

    if not os.path.exists(file):
        logs.info(f"警告：当前文件{file}不存在")
        return []

    testcase_list = []

    try:
        with open(file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            if len(yaml_data) <= 1:
                data = yaml_data[0]
                base_info = data.get('baseInfo')
                for tc in data.get('testCase'):
                    params = [base_info,tc]
                    testcase_list.append(params)
                return testcase_list
            else:
                #确保返回的yaml_data是列表类型
                return yaml_data


    except UnicodeDecodeError:
        logs.error(f"[{file}]文件编码格式错误，--尝试使用utf-8编码解码YAML文件时发生了错误，请确保你的yaml文件是UTF-8格式！")
    except FileNotFoundError:
        logs.error(f'[{file}]文件未找到，请检查路径是否正确')
    except Exception as e:
        logs.error(f'获取【{file}】文件数据时出现未知错误: {str(e)}')

    # with open(file, 'r',encoding='utf-8') as f:
    #     yaml_data = yaml.safe_load(f)
    #     if yaml_data is None:
    #         raise ValueError(f'文件{file}为空')
    #         return []
    #     return yaml_data if isinstance(yaml_data,list) else [yaml_data]


if __name__ == '__main__':
    data = get_yaml_data('test_cases/login/login.yaml')
    logs.info(f"读取到的yaml数据为：{data}")
    print("例表数据一：",data[0][0])
    print("例表数据二",data[0][1])
    # base = ReadWriteYamlData()
    # base.write_yaml({'name':'谢锡新','sex':'男'})
    # data = base.get_extract_yaml('Cookie')
    # logs.info(f"读取到的yaml数据为：{data}")
