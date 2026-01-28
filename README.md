框架结构
- base 基础类封装，测试用例工具
- common  公共方法封装
- conf  存放全局配置文件目录
- data  存放测试数据路径
- logs  存放测试日志目录
- report    测试报告生成目录，目前支持生成两种形式的报告
- testcase  存放测试用例文件目录
- venv  本框架使用的虚拟环境
- conftest.py 全局操作，名称是固定写法不可更改
- environment.xml allure测试报告总览-环境显示内容
- extract.yaml 接口依赖参数存放文件
- pytest.ini pytest框架规范约束，名称是固定写法不可更改
- requirements.txt 本框架所使用的到的第三方库
- run.py 主程序入口

**1、用例模板(baseInfo、testcase的关键字不能缺少）**
------------------------------------------------------------------------------------------------
- baseInfo:
    api_name: 轨迹查询
    url: /monitor/vehicle/getMileageFrom
    method: post
    header:
      Content-Type: application/x-www-form-urlencoded;charset=UTF-8
      token: ${get_extract_data(token)}
      userid: ${get_extract_data(userid)}
    cookies: //可有可无，根据项目实际情况，如果项目需要cookie则要写
      SESSION: ${get_extract_data(Cookie,SESSION)}
  testCase:
    -
      case_name: 有效车牌号轨迹查询
      data:
        vno: 鲁E00098
        color: 2
        startDate: ${start_time()}
        ruleIds: ["${get_extract_data_lst(forbiddenRule,-2)}"]  #参数是列表形式的，列表内必须为字符串形式，否则读取不到
        endDate: ${end_time()}
        vehicleNo: ${get_extract_data(fatig_vahicle,randoms)}  # 参数1 是extract.yaml里面的key；参数2 randoms默认为空，若提取的值是个列表，该参数填列表取值的索引值,0随机，其他根据列表，1第一个，以此类推
      files:
        file: ./data/heimingdan.xlsx   # 注意有些导入文件接口不需要设置请求头，设置了反而会报错
      validation: # 断言验证，根据实际需求选择使用以下哪种断言方式
        - contains: {status_code: 200}     # 字符串包含断言模式，有多种断言时，contains必须在前面
        - contains: {'message':'success'}  # 字符串包含断言模式
        - contains: {'message':None}  # 字符串为空断言
        - eq: {'state': '已入网'}           # 相等断言模式，这个要在contains的下面
        - ne: {'state': '已入网'}           # 不相等断言模式
        - rv: {"data":2}                   # 断言接口返回值的任意值模式
        - db: select * from sys_user su where login_name ='test999'    #数据库断言，这里直接写SQL即可
        - contains: {'csrfToken': '${get_extract_data(Cookie,csrfToken)}' }  #因格式问题，这里面的提取表达式必须要用引号
      extract:  # 提取一个参数，支持json提取和正则表达式提取
        id: $.data
        status: '"status":"(.*?)"'
        data: '"data":(\d*)'        #提取数字  
      extract_list:  #提取多个参数，以列表形式返回，支持json提取和正则表达式提取
        id: $.result.id
          
**关于参数提取，json提取器表达式***
-----------------
可以使用这个在线jsonpath解析器：http://www.atoolbox.net/Tool.php?Id=792

-------------------------------------------------------------------------------------------------
**2、参数说明**
-----------------------------
    `url`：只写接口地址，ip和端口去conf目录下的config.ini配置[api_envi]
    `参数传递: ${get_extract_data(token)}` ：参数传递格式为：${函数名(*args)}，args参数可有可无，函数实现可以去common目录下的debugtalk.py去实现具体方法

**3、接口参数类型**
-----------------------------
参数类型主要有：params、data、json（只能填这三个其中一个，根据接口接口的请求方式、参数类型选择）
post请求：1）表单提交-->data
         2)json提交--->json
get请求：1）url传参--->params

注：参数类型一定要写对，根据你的实际接口传参类型类型，对应的header也要变更

如： data   对应的header为：  Content-Type:application/x-www-form-urlencoded;charset=UTF-8
    json   对应的header为：  Content-Type:application/json;charset=UTF-8
    files  文件提交          Content-type:multipart/form-data; charset=utf-8
