__author__ = 'michaelstarin'


import numpy as np

from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
import talib

from Restful import RestfulAPI
from technical_analysis import Indicators
from ReversalMinMax import Reversal
from Support_Resistance import SRZones
from sklearn import datasets, linear_model
from sklearn.svm import SVC
from decimal import *

class RSS2:
    def __init__(self, granularity, count, currency_pair, oanda_account_id, oanda_access_token, domain, oanda, period, sensitivity_range, srzone_range,minutes):
        self.granularity = granularity
        self.count = count
        self.currency_pair = currency_pair
        self.oanda_account_id = oanda_account_id
        self.oanda_access_token = oanda_access_token
        self.price_type1 = 'closeAsk'
        self.price_type2 = 'openAsk'
        self.price_type3 = 'closeBid'
        self.price_type4 = 'openBid'

        self.oanda = oanda
        self.array = None
        self.now = None
        self.now_min = None
        self.domain = domain
        self.minutes = minutes
        self.seconds = 60
        self.period = period
        self.sensitivity_range = sensitivity_range
        self.srzone_range = srzone_range
        self.close_ask = []
        self.open_ask = []
        self.close_bid = []
        self.open_bid =[]
        global close_ask_array
        global open_ask_array

    def main_fx(self):

        self.now = datetime.utcnow()
        self.now_rounded = self.now - timedelta(minutes=self.now.minute % self.minutes,
                                                seconds=self.now.second % self.seconds,
                                                microseconds=self.now.microsecond)

        instanceSmall = RestfulAPI(self.granularity, 90, self.currency_pair, self.oanda_account_id,
                                       self.oanda_access_token, self.domain, self.now,self.minutes)
        self.arraySmall = instanceSmall.get_restful_price()
        self.close = self.arraySmall[self.price_type1][0:len(self.arraySmall)]

        print self.close
        print 'len close ', len(self.close)


        print 'Currency Pair is ', self.currency_pair  # fetch historical candlestick data
        number_loops = 3
        open_ask_array = []
        close_bid_array = []
        close_ask_array = []
        open_bid_array = []
        # Oanda API is limited to fetching 5000 data points in an instance - here we fetch in loops to collect more data
        self.now = self.now - timedelta(hours = (number_loops-1)*self.count)

        for index in range(0,number_loops):
            instanceBig = RestfulAPI(self.granularity, self.count, self.currency_pair, self.oanda_account_id,
                                       self.oanda_access_token, self.domain, self.now,self.minutes)
            self.arrayBig = instanceBig.get_restful_price()

            # instanceSmall = RestfulAPI(self.granularity, self.count, self.currency_pair, self.oanda_account_id,
            #                            self.oanda_access_token, self.domain, self.now,1)
            # self.arraySmall = instanceSmall.get_restful_price()


            self.close_ask = self.arrayBig[self.price_type1][0:len(self.arrayBig)]
            self.open_ask = self.arrayBig[self.price_type2][0:len(self.arrayBig)]
            self.close_bid = self.arrayBig[self.price_type3][0:len(self.arrayBig)]
            self.open_bid = self.arrayBig[self.price_type4][0:len(self.arrayBig)]


            open_ask_array = np.concatenate((open_ask_array,self.close_ask))
            close_bid_array = np.concatenate((close_bid_array,self.close_ask))
            close_ask_array = np.concatenate((close_ask_array,self.close_ask))
            open_bid_array = np.concatenate((open_bid_array,self.close_ask))
            print 'self.now ', self.now
            self.now = self.now + timedelta(hours = self.count)

        print close_ask_array
        print 'len close_ask_array ',len(close_ask_array)
        self.close_ask = np.array(self.close_ask)


        times = 0
        for t in range(0,len(self.close)):

            if close_ask_array[t] == self.close[t]:
                times+=1
        print times
# instance3 = Reversal(close_ask_array, self.sensitivity_range)
# locations = instance3.reversal_m_m()
        #
        # instance4 = SRZones(locations, self.currency_pair, self.srzone_range)
        # #sr1_ar = instance4.sup_rest()


        # # Create indicator feature vectors
        # EMA_vals = talib.EMA(close_ask_array)
        # SMA_vals = talib.SMA(close_ask_array)
        # RSI_vals = talib.RSI(close_ask_array,timeperiod=self.period)
        # #ADX_vals = talib.ADX(close_ask_array)
        # MOM_vals = talib.MOM(close_ask_array)
        # #WILLR_vals = talib.WILLR(close_ask_array)
        #
        # # Range of closing values to grab
        # n = (self.count-40)/2
        #
        # y_train_close = np.array(close_ask_array[40:-n])
        # y_train_open = np.array(open_ask_array[40:-n])
        #
        # y_test_close = np.array(close_ask_array[n+40:])
        # y_test_open = np.array(open_ask_array[n+40:])
        #
        # # Bid prices
        # y_test_close_bid = np.array(close_bid_array[n+40:])
        # y_test_open_bid = np.array(open_bid_array[n+40:])
        #
        #
        # # Training feature vectors
        # X_train1 =np.array(RSI_vals[40:-n]).reshape(-1,1)
        # X_train2 = np.array(EMA_vals[40:-n]).reshape(-1,1)
        # #X_train3 = np.array(MOM_vals[40:-n]).reshape(-1,1)
        #
        # # Testing feature vectors
        # X_test1 =np.array(RSI_vals[n+40:]).reshape(-1,1)
        # X_test2 = np.array(EMA_vals[n+40:]).reshape(-1,1)
        # #X_test3 = np.array(MOM_vals[n+40:]).reshape(-1,1)
        #
        # #X_train = np.concatenate((X_train1.T,X_train2.T,X_train3.T), axis=0)
        # X_train = np.concatenate((X_train1.T,X_train2.T), axis=0)
        #
        # X_train = X_train.T
        #
        # #X_test = np.concatenate((X_test1.T,X_test2.T,X_test3.T), axis=0)
        # X_test = np.concatenate((X_test1.T,X_test2.T), axis=0)
        #
        # X_test = X_test.T
        #
        #
        #
        #
        # y_train_close_bin = []
        # y_test_close_bin = []
        # # Create output for training data of SVM machine based on classification
        # for i in range(0,len(y_train_close)-1):
        #
        #     if y_train_close[i+1] - y_train_close[i] > self.sensitivity_range:
        #         y_train_close_bin.append(1)
        #
        #
        #     elif y_train_close[i] - y_train_close[i+1] > self.sensitivity_range:
        #         y_train_close_bin.append(0)
        #
        #     else:
        #         # Take no action
        #         y_train_close_bin.append(2)
        #
        # # Create output for testing data of for SVM machine based on classification
        # for i in range(0,len(y_test_close)-1):
        #
        #     if y_test_close[i+1] - y_test_close[i] > self.sensitivity_range:
        #         y_test_close_bin.append(1)
        #
        #     elif y_test_close[i] - y_test_close[i+1] > self.sensitivity_range:
        #         y_test_close_bin.append(0)
        #
        #     else:
        #         # Take no action
        #         y_test_close_bin.append(2)
        #
        #
        # clf = SVC(kernel='rbf', C=1,gamma=0.5)
        # clf.fit(X_train[0:-1], y_train_close_bin)
        # predicted1 = clf.predict(X_test)
        # print len(y_test_close)
        # print len(y_test_close_bin)
        # print len(X_train)
        # print len(predicted1)
        # hit_rate = 0
        # # compare predicted with actual market movement to determine prediction accuracy.
        # for i in range(0,len(predicted1)-1):
        #     if predicted1[i] == y_test_close_bin[i]:
        #
        #         hit_rate+=1
        # print 'accuracy: ', hit_rate/float(len(predicted1)-1)
        #
        # Balance = 5000
        # profit_loss_pips = 0
        # accur = 0
        #
        # for i in range(0,len(y_test_close)-1):
        #
        #     if predicted1[i] == 1:
        #         # Buy
        #         profit_loss_pips = profit_loss_pips + (y_test_close[i+1] - y_test_close[i]) #- abs(y_test_close_bid[i+1] - y_test_close[i])
        #
        #     if predicted1[i] == 0:
        #         # Buy
        #         profit_loss_pips = profit_loss_pips + (y_test_close[i] - y_test_close[i+1]) #- abs(y_test_close_bid[i] - y_test_close[i+1])
        #
        #
        # print abs(y_test_close_bid[-1] - y_test_close[-1])
        # print hit_rate
        # print accur
        # print profit_loss_pips
        #
        #
        #
        #












        #print ' '
        #print ' actual y_train ', y_test_close

#################################################











