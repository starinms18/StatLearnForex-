__author__ = 'michaelstarin'

import oandapy
import threading
from ML_Backtest import RSS2
from test import RSS3



oanda_account_id = 6980117
oanda_access_token = "74b91ee3fda0251126b3d4a319067b88-7a70489e0dd38f5e6994ddda09b0e1ca"

currency_pair = 'AUD_USD'

oanda = oandapy.API(environment="practice", access_token=oanda_access_token)
close_ask_array = None
open_ask_array = None
granularity = 'M15'
domain = "practice"
count = 5000
period = 14
sensitivity_range = .00065
srzone_range = .0002



def call_method1(granularity, count, currency_pair, oanda_account_id, oanda_access_token, domain, oanda, period, sensitivity_range, srzone_range):
    instance1 = RSS2(granularity, count, currency_pair, oanda_account_id, oanda_access_token, domain, oanda,period, sensitivity_range, srzone_range)
    instance1.main_fx()


def call_method2(granularity, count, currency_pair, oanda_account_id, oanda_access_token, domain, oanda, period, sensitivity_range, srzone_range):
    instance2 = RSS3(granularity, count, currency_pair, oanda_account_id, oanda_access_token, domain, oanda,period, sensitivity_range, srzone_range)
    instance2.main_fx()

call_method1(granularity, count, currency_pair, oanda_account_id, oanda_access_token, domain, oanda,period, sensitivity_range, srzone_range)
#
# #rss = threading.Thread(target=call_method, args=(granularity, count, currency_pair, oanda_account_id, oanda_access_token, domain, oanda,period))
# #rss.start()


















