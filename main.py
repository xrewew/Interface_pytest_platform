import os

import pytest

if __name__ == '__main__':
    pytest.main(['-s', '-v', '--alluredir=./report/allure-results', './test_cases', '--clean-alluredir'])
    os.system(f'allure serve ./report/allure-results')
