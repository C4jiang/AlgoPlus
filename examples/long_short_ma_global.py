import time
from AlgoPlus.CTP.MdApiBase import MdApiBase
from AlgoPlus.CTP.TraderApiBase import TraderApiBase
from AlgoPlus.CTP.FutureAccount import FutureAccount, get_simulate_account
from AlgoPlus.ta.time_bar import tick_to_bar


class MyTrader(TraderApiBase):
    def __init__(self, broker_id, td_server, investor_id, password, app_id, auth_code, md_queue=None, page_dir='', private_resume_type=2, public_resume_type=2):
        pass

    def OnRtnTrade(self, pTrade):
        print("||OnRtnTrade||", pTrade)

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        print("||OnRspOrderInsert||", pInputOrder, pRspInfo, nRequestID, bIsLast)

    # 订单状态通知
    def OnRtnOrder(self, pOrder):
        print("||OnRtnOrder||", pOrder)


class MyMd(MdApiBase):
    global g_trader

    def __init__(self, broker_id, md_server, subscribe_list, md_queue_list=None, investor_id=b'', password=b'', flow_path='', using_udp=False, multicast=False):
        self.bar = {
            "InstrumentID": b"",
            "UpdateTime": b"99:99:99",
            "LastPrice": 0.0,
            "HighPrice": 0.0,
            "LowPrice": 0.0,
            "OpenPrice": 0.0,
            "BarVolume": 0,
            "BarTurnover": 0.0,
            "BarSettlement": 0.0,
            "BVolume": 0,
            "SVolume": 0,
            "FVolume": 0,
            "DayVolume": 0,
            "DayTurnover": 0.0,
            "DaySettlement": 0.0,
            "OpenInterest": 0.0,
            "TradingDay": b"99999999",
        }
        self.bar_close_list = []
        self.long_n = 20
        self.short_n = 10
        self.long_ma = 0.0
        self.short_ma = 0.0
        self.bar_count = 0

    def OnRtnDepthMarketData(self, snapshot):
        is_new_10s = (snapshot['UpdateTime'][:-1] != self.bar["UpdateTime"][:-1])

        # 新K线开始
        if is_new_10s:
            self.bar_count += 1
            if self.bar_count > 1:
                self.bar_close_list.append(self.bar["LastPrice"])
                print(snapshot['UpdateTime'], snapshot['InstrumentID'], snapshot['LastPrice'], self.bar_close_list[-self.long_n:])

                if self.bar_count > self.long_n:
                    long_ma = sum(self.bar_close_list[-self.long_n:]) / self.long_n
                    short_ma = sum(self.bar_close_list[-self.short_n:]) / self.short_n
                    if short_ma < long_ma and self.short_ma >= self.long_ma:
                        g_trader.sell_close("SHFE", "rb2310", snapshot['BidPrice1'], 1, True)
                    elif short_ma > long_ma and self.short_ma <= self.long_ma:
                        g_trader.buy_open("SHFE", "rb2310", snapshot['AskPrice1'], 1)

                    print(short_ma, long_ma, self.short_ma, self.long_ma)

                    self.long_ma = long_ma
                    self.short_ma = short_ma

        # # 将Tick池化为Bar
        tick_to_bar(self.bar, snapshot, is_new_10s)


if __name__ == '__main__':
    future_account = get_simulate_account(
        investor_id='',  # 账户
        password='',  # 密码
        server_name='TEST',  # 电信1、电信2、移动、TEST、N视界
        subscribe_list=[b'rb2310'],  # 合约列表
    )

    # future_account = FutureAccount(
    #     broker_id='',  # 期货公司BrokerID
    #     server_dict={'TDServer': "ip:port", 'MDServer': 'tcp://101.226.253.244:21213'},  # TDServer为交易服务器，MDServer为行情服务器。服务器地址格式为"ip:port。"
    #     reserve_server_dict={},  # 备用服务器地址
    #     investor_id='',  # 账户
    #     password='',  # 密码
    #     app_id='simnow_client_test',  # 认证使用AppID
    #     auth_code='0000000000000000',  # 认证使用授权码
    #     subscribe_list=[b'SP si2308&si2309'],  # 订阅合约列表
    #     md_flow_path='./log',  # MdApi流文件存储地址，默认MD_LOCATION
    #     td_flow_path='./log',  # TraderApi流文件存储地址，默认TD_LOCATION
    # )

    g_trader = MyTrader(
        future_account.broker_id,
        future_account.server_dict['TDServer'],
        future_account.investor_id,
        future_account.password,
        future_account.app_id,
        future_account.auth_code,
        None,
        future_account.td_flow_path
    )

    tick_engine = MyMd(
        future_account.broker_id,
        future_account.server_dict['MDServer'],
        future_account.subscribe_list,
        None,
        future_account.investor_id,
        future_account.password,
        future_account.md_flow_path
    )
    
    while True:
        time.sleep(1)
