"""
    商品管理模块测试用例
"""
import allure
import pytest

from api_key.apiutil import BaseRequests
from api_key.readyaml import get_yaml_data


class TestProduct:
    @allure.epic('商品管理模块')
    @allure.feature('获取商品列表')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase', get_yaml_data('test_cases/productManger/getProductList.yaml'))
    def test_product_list(self,base_info,testcase):
        """
        获取商品列表
        :return:
        """
        allure.dynamic.title(testcase['case_name'])
        base = BaseRequests()
        base.send_specification_yaml(base_info,testcase)

    @allure.epic('商品管理模块')
    @allure.feature('获取商品详情')
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_yaml_data('test_cases/productManger/ProductDetail.yaml'))
    def test_product_detail(self,base_info,testcase):
        """
        获取商品详情
        :return:
        """
        base = BaseRequests()
        base.send_specification_yaml(base_info,testcase)

    @allure.epic("提交订单")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_yaml_data('test_cases/productManger/commitOrder.yaml'))
    def test_commit_order(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        base = BaseRequests()
        base.send_specification_yaml(base_info, testcase)