# -*- coding: utf-8 -*-

# 微信公众号：AlgoPlus
# 官网：http://algo.plus
# 项目地址：https://gitee.com/AlgoPlus/

import time
from multiprocessing import Queue
from AlgoPlus.CTP.TraderApiBase import TraderApiBase
from AlgoPlus.CTP.FutureAccount import get_simulate_account


class RollingTrade(TraderApiBase):
    def __init__(self, broker_id, td_server, investor_id, password, app_id, auth_code, md_queue=None, page_dir='', private_resume_type=2, public_resume_type=2):
        pass

    def init_extra(self):
        """
        初始化策略参数
        :return:
        """
        # {
        #     'ExchangeID': b'',  # 交易所
        #     'InstrumentID': b'',  # 合约代码
        #     'UpperLimitPrice': 0.0,  # 涨停板
        #     'LowerLimitPrice': 0.0,  # 跌停板
        #     'Volume': 1,  # 报单手数
        # }
        self.parameter_dict = self.md_queue.get(block=False)

    def OnRtnTrade(self, pTrade):
        pass

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        pass

    # 订单状态通知
    def OnRtnOrder(self, pOrder):

        if pOrder['OrderStatus'] == b"0":
            if self.order_ref < 100:
                self.buy_open(self.parameter_dict['ExchangeID'], self.parameter_dict['InstrumentID'], self.parameter_dict['UpperLimitPrice'], self.parameter_dict['Volume'])
            else:
                self.write_log("滚动交易（100笔）已经全部完成！")

    def Join(self):
        while True:
            if self.status >= 0 and self.order_ref == 0:
                self.buy_open(self.parameter_dict['ExchangeID'], self.parameter_dict['InstrumentID'], self.parameter_dict['UpperLimitPrice'], self.parameter_dict['Volume'])

            time.sleep(1)


if __name__ == "__main__":
    # 账户配置
    account = get_simulate_account(
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

    # 参数
    parameter_dict = {
        'ExchangeID': b'SHFE',  # 交易所
        'InstrumentID': b'rb2310',  # 合约代码
        'UpperLimitPrice': 4380,  # 涨停板
        'LowerLimitPrice': 3511,  # 跌停板
        'Volume': 1,  # 报单手数
    }

    # 共享队列
    share_queue = Queue(maxsize=100)
    share_queue.put(parameter_dict)

    #
    rolling_trade = RollingTrade(
        account.broker_id,
        account.server_dict['TDServer'],
        account.investor_id,
        account.password,
        account.app_id,
        account.auth_code,
        share_queue,
        account.td_flow_path
    )

    #
    rolling_trade.Join()
