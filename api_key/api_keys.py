import json
import allure
import pytest
import requests
from api_key.readyaml import ReadWriteYamlData
from logging_conf.logging_config import logs

class ApiKeys(object):
    """
    封装接口的请求
    """
    def __init__(self):
        self.read = ReadWriteYamlData()

    def send_request(self,**kwargs):
        """
        发送请求
        :param kwargs:
        :return:
        """
        cookie = {} # 定义一个空字典，用于存储请求cookies
        session = requests.session() #创建一个会话对象，用于保持会话状态
        result = {}  # 定义一个空字典，用于存储响应结果
        try:
            result = session.request(**kwargs) # 发送请求，将响应结果赋值给result变量
            set_cookie = requests.utils.dict_from_cookiejar(session.cookies) # 将会话对象中的cookies转换为字典格式
            if set_cookie:
                cookie['Cookie'] = set_cookie
                self.read.write_yaml(cookie)
                logs.info(f'写入Cookie成功：{cookie}')
            logs.info(f'接口的实际返回信息:{result.text}')
        except requests.exceptions.ConnectionError as e:
            logs.error('接口链接服务器异常！')
            pytest.fail('接口请求异常，可能是request的链接数过多或者请求速度过快导致程序报错！')
        except requests.exceptions.HTTPError as e:
            logs.error('Http异常')
            pytest.fail('Http请求异常')
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail('请求异常，请检查系统或者数据是否正常！')

        return result


    def run_main(self,name,url,case_name,header,method,cookies=None,file=None,**kwargs):
        """
        接口请求主函数
        :param name: 接口名称
        :param url: 接口url
        :param case_name: 用例名称
        :param header: 请求头
        :param method: 请求方法
        :param cookies: 请求cookies
        :param file: 请求文件
        :param kwargs: 其他参数
        :return:
        """
        try:
            #搜集报告日志信息
            logs.info(f"接口名称：{name}")
            logs.info(f"接口url：{url}")
            logs.info(f"用例名称：{case_name}")
            logs.info(f"请求头：{header}")
            logs.info(f"请求方法：{method}")
            logs.info(f"请求cookies：{cookies}")
            #处理请求数据
            request_data = json.dumps(kwargs,ensure_ascii= False) #将请求参数转换为json字符串

            if 'data' in kwargs.keys():
                logs.info(f"请求参数：{kwargs}")
                allure.attach(request_data,f'请求参数：{request_data}',allure.attachment_type.TEXT)
            elif 'json' in kwargs.keys():
                logs.info(f"请求参数：{kwargs}")
                allure.attach(request_data,f'请求参数：{request_data}',allure.attachment_type.TEXT)
            elif 'params' in kwargs.keys():
                logs.info(f"请求参数：{kwargs}")
                allure.attach(request_data,f'请求参数：{request_data}',allure.attachment_type.TEXT)
        except Exception as e:
                logs.error(f"请求参数处理异常：{e}")

        res = self.send_request(url=url,method=method,headers=header,cookies=None,files=file,verify=False,**kwargs)
        return res


if __name__ == '__main__':
    send = ApiKeys()
    url = 'http://127.0.0.1:8787/dar/user/login'
    data = {"user_name": "test01", "passwd": "admin123"}
    header = None
    method = "POST"

    res = send.run_main(name='登录接口',url=url,case_name='登录接口',header=header,method=method,data=data)
    print(res)