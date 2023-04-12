# -*- coding: utf-8 -*-

# 微信公众号：AlgoPlus
# 官网：http://algo.plus
# 项目地址：https://gitee.com/AlgoPlus/

from multiprocessing import Process, Queue
from AlgoPlus.CTP.MdApi import run_tick_engine
from AlgoPlus.CTP.RiskManager import run_risk_manager
from AlgoPlus.CTP.FutureAccount import get_simulate_account

if __name__ == '__main__':

    # 参数
    pl_parameter = {
        'StrategyID': 0,
        'ProfitLossParameter': {
            b'rb2310': {'0': [2], '1': [2]},  # '0'代表止盈, '1'代表止损
        },
    }

    # 订阅列表
    subscribe_list = []
    for instrument_id in pl_parameter['ProfitLossParameter']:
        subscribe_list.append(instrument_id)

    # 账户
    future_account = get_simulate_account(
        investor_id='',  # 账户
        password='',  # 密码
        server_name='',  # 电信1、电信2、移动、TEST、N视界
        subscribe_list=subscribe_list,  # 合约列表
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

    # 共享队列
    share_queue = Queue(maxsize=100)
    share_queue.put(pl_parameter)

    # 行情进程
    md_process = Process(target=run_tick_engine, args=(future_account, [share_queue]))
    # 交易进程
    trader_process = Process(target=run_risk_manager, args=(future_account, share_queue))

    #
    md_process.start()
    trader_process.start()

    #
    md_process.join()
    trader_process.join()
