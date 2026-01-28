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
    @pytest.mark.parametrize('params', get_yaml_data('test_cases/productManger/getProductList.yaml'))
    def test_product_list(self,params):
        """
        获取商品列表
        :return:
        """
        base = BaseRequests()
        base.send_specification_yaml(params)

    @allure.epic('商品管理模块')
    @allure.feature('获取商品详情')
    @pytest.mark.parametrize('params', get_yaml_data('test_cases/productManger/ProductDetail.yaml'))
    def test_product_detail(self,params):
        """
        获取商品详情
        :return:
        """
        base = BaseRequests()
        base.send_specification_yaml(params)
