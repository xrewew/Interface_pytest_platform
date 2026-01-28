import os

import pytest

if __name__ == '__main__':
    pytest.main(['-s', '-v', '--alluredir=./report/temp', './test_cases', '--clean-alluredir'])
    os.system(f'allure serve ./report/temp')
