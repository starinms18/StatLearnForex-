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

class RSS2:
    def __init__(self, granularity, count, currency_pair, oanda_account_id, oanda_access_token, domain, oanda, period, sensitivity_range, srzone_range):
        self.granularity = granularity
        self.count = count
        self.currency_pair = currency_pair
        self.oanda_account_id = oanda_account_id
        self.oanda_access_token = oanda_access_token
        self.price_type1 = 'closeAsk'
        self.price_type2 = 'openAsk'
        self.oanda = oanda
        self.array = None
        self.now = None
        self.now_min = None
        self.domain = domain
        self.minutes = 5
        self.seconds = 60
        self.period = period
        self.sensitivity_range = sensitivity_range
        self.srzone_range = srzone_range
        global close_ask_array
        global open_ask_array

    def main_fx(self):

        self.now = datetime.utcnow()
        self.now_rounded = self.now - timedelta(minutes=self.now.minute % self.minutes,
                                                seconds=self.now.second % self.seconds,
                                                microseconds=self.now.microsecond)

        print 'Currency Pair is ', self.currency_pair  # fetch historical candlestick data
        instance2 = RestfulAPI(self.granularity, self.count, self.currency_pair, self.oanda_account_id,
                               self.oanda_access_token, self.domain, self.now)
        self.array = instance2.get_restful_price()
        global close_ask_array
        global open_ask_array

        close_ask_array = np.array(self.array[self.price_type1][0:len(self.array)])
        open_ask_array = np.array(self.array[self.price_type2][0:len(self.array)])

        # instance3 = Reversal(close_ask_array, self.sensitivity_range)
        # locations = instance3.reversal_m_m()
        #
        # instance4 = SRZones(locations, self.currency_pair, self.srzone_range)
        # #sr1_ar = instance4.sup_rest()


        # Create indicator feature vectors
        EMA_vals = talib.EMA(close_ask_array)
        SMA_vals = talib.SMA(close_ask_array)
        RSI_vals = talib.RSI(close_ask_array,timeperiod=self.period)
        ADX_vals = talib.ADX(close_ask_array)



        # Range of closing values to grab
        n = (self.count-40)/2

        y_train_close = np.array(close_ask_array[40:-n])
        y_train_open = np.array(open_ask_array[40:-n])

        y_test_close = np.array(close_ask_array[n+40:])
        y_test_open = np.array(open_ask_array[n+40:])

        # Training feature vectors
        X_train1 =np.array(RSI_vals[40:-n]).reshape(-1,1)
        X_train2 = np.array(EMA_vals[40:-n]).reshape(-1,1)
        X_train3 = np.array(ADX_vals[40:-n]).reshape(-1,1)

        # Testing feature vectors
        X_test1 =np.array(RSI_vals[n+40:]).reshape(-1,1)
        X_test2 = np.array(EMA_vals[n+40:]).reshape(-1,1)
        X_test3 = np.array(ADX_vals[n+40:]).reshape(-1,1)

        X_train = np.concatenate((X_train1.T,X_train2.T), axis=0)
        X_train = X_train.T

        X_test = np.concatenate((X_test1.T,X_test2.T), axis=0)
        X_test = X_test.T



        # Create output for training data of for SVM machine based on classification
        for i in range(0,len(y_train_close)):

            if y_train_close[i] - y_train_open[i] > 0:
                y_train_close[i] = 1

            else:
                y_train_close[i] = 0

        # Create output for testing data of for SVM machine based on classification
        for i in range(0,len(y_test_close)):

            if y_test_close[i] - y_test_open[i] > 0:
                y_test_close[i] = 1

            else:
                y_test_close[i] = 0




        clf = SVC(kernel='rbf', C=1,gamma=0.5)
        clf.fit(X_train, y_train_close)
        predicted= clf.predict(X_test)

        hit_rate = 0
        # compare predicted with actual market movement to determine prediction accuracy.
        for i in range(0,len(predicted)):
            if predicted[i] == y_test_close[i]:
                hit_rate+=1

        print 'accuracy: ', hit_rate/float(len(predicted))

        print 'predicted ', predicted
        print ' '
        print ' actual y_train ', y_test_close

        # Plot outputs
        fig, ax = plt.subplots()
        plt.plot(y_test_close, "o", color='black')
        plt.ylim([-1,2])
        plt.plot(clf.predict(X_test), "o",color='blue')
        ax.set_xlabel('RSI')
        ax.set_ylabel('Closing Prices')
        plt.show()



        ################################################################

        # Train the model using the training sets
        # regr = linear_model.LogisticRegression()
        # regr.fit(X_train, y_train)
        #
        # predicted= regr.predict(X_train)
        # print 'predicted ', predicted
        #
        # print ' '
        # print ' actual y_train ', y_train
        # # The coefficients
        # print('Coefficients: \n', regr.coef_)
        # # The mean square error
        # print("Residual sum of squares: %.2f"
        #       % np.mean((regr.predict(X_train) - y_train) ** 2))
        # # Explained variance score: 1 is perfect prediction
        # print('Variance score: %.2f' % regr.score(X_train, y_train))
        #
        # # Plot outputs
        # fig, ax = plt.subplots()
        # plt.plot(X_train, y_train,  color='black')
        #
        # plt.plot(X_train, regr.predict(X_train), color='blue',linewidth=3)
        # ax.set_xlabel('EMA')
        # ax.set_ylabel('Closing Prices')
        #plt.show()
















