import time

import pytest

from api_key.apiutil import BaseRequests
from api_key.readyaml import get_yaml_data
from logging_conf.logging_config import logs

# from common.operJenkins import OperJenkins

"""
-function：每一个函数或方法都会调用
-class：每一个类调用一次，一个类中可以有多个方法
-module：每一个.py文件调用一次，该文件内又有多个function和class
-session：是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module,整个会话只会运行一次
-autouse：默认为false，不会自动执行，需要手动调用，为true可以自动执行，不需要调用
- yield：前置、后置
"""


# @pytest.fixture(autouse=True)
# def start_test_end():
#     logs.info('-----------------接口测试开始---------------------')
#     yield
#     logs.info('-----------------接口测试结束---------------------')


# @pytest.fixture(scope='session', autouse=True)
def system_login():
    params = get_yaml_data('test_cases/login/login.yaml')
    BaseRequests().send_specification_yaml(params)

#
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     """
#     pytest内置的钩子函数，函数名为固定写法，不可变更
#     每次pytest测试完成后，会自动化收集测试结果的数据
#     :param terminalreporter: 内部终端报告对象，对象的stats属性
#     :param exitstatus: 将报告回操作系统的退出状态
#     :param config: pytest配置对象
#     :return:
#     """
#     print(terminalreporter.stats)
#     # 收集测试用例总数
#     case_total = terminalreporter._numcollected
#     # 收集测试用例通过数
#     passed = len(terminalreporter.stats.get('passed', []))
#     # 收集测试用例失败数
#     failed = len(terminalreporter.stats.get('failed', []))
#     # 收集测试用例错误数量
#     error = len(terminalreporter.stats.get('error', []))
#     # 收集测试用例跳过执行数
#     skipped = len(terminalreporter.stats.get('skipped', []))
#     # 收集测试用例执行时长
#     duration = time.time() - terminalreporter._sessionstarttime
#
#     # 需要部署到Jenkins持续集成当中去运行
#     # oper = OperJenkins()
#     # report = oper.report_success_or_fail()
#
#     content = f"""
#         各位好，本次XXX智慧物流项目的接口自动化测试结果如下，请注意失败及错误的接口：
#         测试用例总数：{case_total}个
#         通过数：{passed}个
#         失败数：{failed}个
#         跳过执行数：{skipped}个
#         错误异常：{error}个
#         测试用例执行时长：{duration}
#         点击查看测试报告：http://192.168.112.59:8088/job/ZHWLXM/138/allure/
#         """
#     # send_dingding_msg(content=content)
#
if __name__ == '__main__':
    system_login()