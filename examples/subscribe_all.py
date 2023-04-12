# -*- coding: utf-8 -*-

# 微信公众号：AlgoPlus
# 官网：http://algo.plus
# 项目地址：https://gitee.com/AlgoPlus/

from multiprocessing import Process, Queue
from AlgoPlus.CTP.QueryInstrumentHelper import run_query_instrument
from AlgoPlus.CTP.MdApi import run_mdrecorder
from AlgoPlus.CTP.FutureAccount import FutureAccount, get_simulate_account

if __name__ == '__main__':
    # 账户配置
    future_account = get_simulate_account(
        investor_id='',  # 账户
        password='',  # 密码
        server_name='',  # 电信1、电信2、移动、TEST、N视界
    )

    # future_account = FutureAccount(
    #     broker_id='',  # 期货公司BrokerID
    #     server_dict={'TDServer': "ip:port", 'MDServer': 'ip:port'},  # TDServer为交易服务器，MDServer为行情服务器。服务器地址格式为"ip:port。"
    #     reserve_server_dict={},  # 备用服务器地址
    #     investor_id='',  # 账户
    #     password='',  # 密码
    #     app_id='simnow_client_test',  # 认证使用AppID
    #     auth_code='0000000000000000',  # 认证使用授权码
    #     subscribe_list=[],  # 订阅合约列表
    #     md_flow_path='./log',  # MdApi流文件存储地址，默认MD_LOCATION
    #     td_flow_path='./log',  # TraderApi流文件存储地址，默认TD_LOCATION
    # )

    # 查询所有期货合约
    future_account.subscribe_list = run_query_instrument(future_account)

    # 订阅并保存行情为csv文件
    run_mdrecorder(future_account)
