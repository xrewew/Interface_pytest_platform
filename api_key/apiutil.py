import json
import re
import allure
import jsonpath

from api_key.api_keys import ApiKeys
from api_key.readyaml import ReadWriteYamlData
from common.DbugTalk import DbugTalk
from conf.operationConfig import operationConfig
from logging_conf.logging_config import logs
from common.assertions import Assertions

class BaseRequests:

    def __init__(self):
        self.read = ReadWriteYamlData()
        self.conf = operationConfig()
        self.apikey = ApiKeys()
        self.asserts = Assertions()

    def replace_load(self,data):
        """
        替换data yaml文件中的中的${key}
        :param data:
        :return:
        """
        str_data = data
        #判断传入的data数据是否为str格式，json类型数据也算是str格式
        if not isinstance(data,str):
            str_data = json.dumps(data,ensure_ascii=False)

        ##通过字符串索引将${}的值取出来替换
        for i in range(str_data.count('${')): #遍历这个数据含有中所有的${开头的
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$') ##找到该含有${}再字符串的索引位置,这里是开头的位置
                end_index = str_data.index('}',start_index) #找到该含有${}再字符串的索引位置,这里是结尾的位置
                #通过开始位置以及结束位置将${}中的值取出来
                ref_all_params = str_data[start_index:end_index+1]
                # print(ref_all_params)
                #将读到${}中的内容进行提取函数名,如：ref_all_params = "${get_extract_data(product_id,1)}"
                func_name = ref_all_params[2:ref_all_params.index('(')] ##从第二个索引开始提取到‘（’结束
                # print(func_name)
                #取出函数里面的参数值
                func_params = ref_all_params[ref_all_params.index('(')+1:ref_all_params.index(')')]
                # print(func_params)
                #通过反射调用到测试用例中的函数获取数据, #加个*表示传参数量未知，得加这个
                extract_data = getattr(DbugTalk(),func_name)(*func_params.split(',') if func_params else '')
                #将提取到的结果替换原来的信息
                str_data = str_data.replace(ref_all_params,str(extract_data))

        #还原数据
        if data and isinstance(data,dict):
            data = json.loads(str_data)
        else:
            data = str_data #如果data不是dict类型，就说明是str类型，直接返回

        return data


    def send_specification_yaml(self,case_info):
        """
        规范yaml接口测试数据的写法
        :param self:
        :param case_info: 通过get_yaml_data()方法获取的yaml测试用例的数据
        :return:
        """
        cookie = None
        params_type = ['params','json','data'] #请求参数的类型列表，实现发送接口请求时只支持这三种
        try:
            base_url = self.conf.get_envi('host')
            url = base_url + case_info['baseInfo']['url']
            allure.attach(url,f'请求url为：{url}')
            api_name = case_info['baseInfo']['api_name']
            allure.attach(api_name,f'请求接口名称为：{api_name}')
            method = case_info['baseInfo']['method']
            allure.attach(method,f'请求方法为：{method}')
            headers = case_info['baseInfo']['header']
            allure.attach(str(headers),f'请求头为：{headers}',allure.attachment_type.TEXT)
            try:
                cookie = self.replace_load(case_info['baseInfo']['cookie'])
            except Exception as e:
                pass

            for testcase in case_info['testCase']: #循环testcase中的每一个测试用例
                case_name = testcase.pop('case_name') #。pop函数为先返回case_name给case_name后返回从tc例表中删除case_name的新的列表数据
                allure.attach(case_name,f'测试用例名称为：{case_name}')
                #处理断言数据
                val = self.replace_load(testcase.get('validation'))
                testcase['validation'] = val
                validation = eval(testcase.pop('validation')) #eval函数将字符串转换为字典类型
                #处理需要从返回值中提取的数据
                extract = testcase.pop('extract',None)
                extract_list = testcase.pop('extract_list',None) #获取到extract_list字段的值
                for key,value in testcase.items(): #循环testcase中的每一个key,value
                    if key in params_type: #如果key在params_type中，就说明是请求参数
                        testcase[key] = self.replace_load(value)
                #根据处理后的yaml数据进行发送请求
                resp = self.apikey.run_main(name=api_name,url=url,case_name=case_name,method=method,header=headers,cookies=cookie,**testcase)
                resp_text = resp.text #接口实际返回的值
                status_code = resp.status_code #接口的状态码
                allure.attach(resp_text,f'接口实际返回值信息',allure.attachment_type.TEXT)
                allure.attach(str(resp.status_code),f'接口的状态码：{resp.status_code}',allure.attachment_type.TEXT)
                #将返回的数据转化为json格式
                resp_json = resp.json()
                #下面开始提取返回数据中的值，接口关联的内容
                if extract is not None:
                    self.extract_data(extract,resp_text)
                if extract_list is not None:
                    self.extract_data_list(extract_list,resp_text)

                # 处理断言
                self.asserts.assert_result(validation, resp_json, status_code)

        except Exception as e:
            logs.error(f"接口发生异常：{e}")
            raise #这里必须加这个。不然allure生成的报告即使测试用例不通过，也会给显示痛过

    # 提取返回数据中的值，接口关联的内容
    def extract_data(self, testcase_extract, response):
        """
        提取返回数据中的值，接口关联的内容,并支持两种提取
        方式：正则表达式提取和JSON 提取器。提取的数据会被保存到 extract.yaml 文件中，供后续测试用例使用
        :param self:
        :param testcase_extract: 从yaml中提取到的需要提取的字段信息
        :param resp_text: 接口实际返回的值
        :return:
        """
        prttenr_list = ['(.+?)','(.*?)',r'(\d+)',r'(\d*)']
        try:
            for key,value in testcase_extract.items():
                #处理正则表达式的提取
                for prt in prttenr_list:
                    if prt in value:
                        ext_list = re.search(value,response)
                        if prt in [r'(\d+)',r'(\d*)']:
                            extract_data = {key:int(ext_list.group(1))}
                        else:
                            extract_data = {key:ext_list.group(1)}
                        logs.debug(f"正则表达式提取到的token参数：{extract_data}")
                        self.read.write_yaml(extract_data)
                #处理json表达式的提取
                if '$' in value:
                    ext_json = jsonpath.jsonpath(json.loads(response),value)[0]
                    if ext_json:
                        extract_data = {key:ext_json}
                    else:
                        extract_data = {key:'未提取到数据，该接口返回值为空或者json提取表达式有误'}
                    logs.info(f'json提取到的参数为：{extract_data}')
                    self.read.write_yaml(extract_data)
        except Exception as e:
            logs.error(f"接口返回值提取异常，请检查yaml文件的extract表达式是否正确，异常信息为：{e}")

    def extract_data_list(self,testcase_extract_list,response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param resp_text: 接口实际返回的值
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    #模拟case_info数据
    #模拟response数据
    #模拟response数据
    case_info = {
        "baseInfo": {
            "url": "/dar/user/login",
            "api_name": "登录接口",
            "method": "POST",
            "header": {
                "Content-Type": "application/json"
            },
            "cookie": "${get_extract_data(Cookie,access_token_cookie)}"
        },
        "testCase": [
            {
                "case_name": "登录成功",
                "params": {
                    "username": "admin",
                    "password": "123456"
                },
                "extract": {
                    "token": "access_token_cookie"
                },
                "validation": {
                    "code": 200
                }
            }
        ]
    }
    # data = {"token": "${get_extract_data(product_id,1)}"}
    base = BaseRequests()
    base.send_specification_yaml(case_info)

    # resp_text = '{"code":200,"msg":"登录成功","token":"123456"}'
    # # 模拟多个商品返回的数据
    # product_list = {"goodsId": "213123213","goodsName": "商品1"}
    # # test_cases = {"token": "$.token","user_id": '"token":"(.*?)"'}
    # test_cases = {"token": "$.token"}
    # base.extract_data(test_cases,resp_text)

