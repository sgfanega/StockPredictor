# This program will take stock data from Yahoo! Finance and use Machine Learning to Predict future stock prices
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

# Dependencies
import yfinance as yf
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None


class StockPredictor:
    # Constructor
    def __init__(self, ticker_symbol, forecast_days=10, machine_learning_type="LR"):
        self.ticker_symbol = ticker_symbol
        self.forecast_days = forecast_days
        self.machine_learning_type = machine_learning_type
        self.confidence = ""
        self.predictions = ""
        self.start_process()

    # Get Method
    # Return String
    def __get_ticker_symbol(self):
        return self.ticker_symbol

    # Get Method
    # Return int
    def __get_forecast_days(self):
        return self.forecast_days

    # Get Method
    # Return String
    def __get_machine_learning_type(self):
        return self.machine_learning_type

    # Get Method
    # Return float
    def get_confidence(self):
        return self.confidence

    # Get Method
    # Return List
    def get_prediction(self):
        return self.predictions

    # Start Method
    def start_process(self):
        print(self.__get_machine_learning_type())
        # Throws Error if the Machine Learning Type is not LR or SVM
        if self.__get_machine_learning_type() is not 'LR' and self.__get_machine_learning_type() is not 'SVM':
            raise ValueError("Machine Learning Type must be either LR or SVM")
        # Throws Error if Forecast Days is not an int
        if type(self.__get_forecast_days()) is not int:
            raise ValueError("Forecast Days is not a valid amount")

        data = self.__get_data()  # Original Data
        x = self.__get_independent_set(data)  # Independent Data set
        y = self.__get_dependent_set(data)  # Dependent Data set

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)  # Create the training and testing

        x_forecast = self.__get_independent_forecast(data)

        if self.__get_machine_learning_type() is 'LR':
            self.__linear_regression_process( x_train, x_test, y_train, y_test, x_forecast)
        else:
            self.__support_vector_machine_process( x_train, x_test, y_train, y_test, x_forecast)

    # Get Method
    # Return 2D List
    def __get_data(self):
        data = yf.download(self.__get_ticker_symbol())
        data = data[['Adj Close']]  # Discard everything but the Adj Close Column
        data['Prediction'] = data[['Adj Close']].shift(-self.__get_forecast_days())  # Shift the data N up

        return data

    # Get Method
    # Return 2D List
    def __get_independent_set(self, data):
        x = np.array(data.drop(['Prediction'], 1))  # Creates a numpy array without 'Prediction'
        x = preprocessing.scale(x)  # Standardizes the data set, not sure if needed
        x = x[:-self.__get_forecast_days()]  # Removes the last N rows

        return x

    # Get Method
    # Return List
    def __get_dependent_set(self, data):
        y = np.array(data['Prediction'])  # Creates a numpy array just of 'Prediction'
        y = y[:-self.__get_forecast_days()]  # Removes the last N rows

        return y

    # Get Method
    # Return List
    def __get_independent_forecast(self, data):
        x_forecast = np.array(data.drop(['Prediction'], 1))[-self.__get_forecast_days():]

        return x_forecast

    def __linear_regression_process(self, x_train, x_test, y_train, y_test, x_forecast):
        lr = LinearRegression()
        lr.fit(x_train, y_train)

        self.confidence = lr.score(x_test, y_test)
        self.predictions = lr.predict(x_forecast)

    def __support_vector_machine_process(self, x_train, x_test, y_train, y_test, x_forecast):
        svr = SVR(kernel='rbf', C=1e3, gamma=0.1)
        svr.fit(x_train, y_train)

        self.confidence = svr.score(x_test, y_test)
        self.predictions = svr.predict(x_forecast)


# ts = input("What stock do you want predicted?: ")
# fd = input("How many days in the future do you want to predict?: ")
mlt = input("What type of Machine Learning do you want to use? LR or SVM?: ")
if mlt != "LR":
    print("It's not LR")
# sp = StockPredictor(ts, int(fd), mlt)
# print(sp.get_confidence())
# print(sp.get_prediction())
