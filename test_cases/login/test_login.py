# import os
#
# import allure
# import pytest
#
# from api_key.readyaml import get_yaml_data
# from api_key.apiutil import BaseRequests
#
# class TestLogin:
#     #测试用例01
#     @allure.epic("登录测试")
#     @allure.feature('登录')
#     @allure.story('登录业务流程')
#     @allure.title('实现测试用例的登录操作')
#     @allure.description('前置登录')
#     @pytest.mark.parametrize('params',get_yaml_data('test_cases/login/login.yaml')) #test_cases/login/logins.yaml
#     def test_login01(self,params):
#         base = BaseRequests()
#         base.send_specification_yaml(params)
