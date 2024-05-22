from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import os
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import numpy as np
import pandas as pd
import math
from sklearn.metrics import mean_squared_error

st.set_page_config(
    page_title="Stock X",
    page_icon="🧊",
    layout="wide",
    
)

Stock = st.session_state['Stock']
PredData = st.session_state['PredData']

st.write("prediction is available only for rellience with accurecy of 50%")
backdata= 7

load_existing_model = True  
save_model = True  
if load_existing_model and os.path.exists(str (Stock) + "lstm_model.h5"):
    regressor = load_model( str (Stock) + "lstm_model.h5")
    
    dfSet=PredData.copy()
    dfSet1=dfSet.copy()
    dfSet1['Difference'] = dfSet1['Close'].shift(-1) - dfSet1['Close']

    dfSet1 = dfSet1.drop(dfSet1.index[-1])
    dfSet1 = dfSet1[['Difference']]

    dfset_train = dfSet1.iloc[0:int(0.8 * len(dfSet1)), :]
    dfset_test = dfSet1.iloc[int(0.8 * len(dfSet1)):, :]

    # Feature Scaling


    training_set = dfSet1.iloc[:, 0:1].values  # Extracting the "Difference" column as numpy array

    # Scaling the data
    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # Creating the data structure with 7 timesteps and 1 output
    X_train = []  # Memory with 7 days from day i
    y_train = []  # Day i
    for i in range(backdata, len(training_set_scaled)):
        X_train.append(training_set_scaled[i - backdata:i, 0])
        y_train.append(training_set_scaled[i, 0])

    # Convert lists to numpy arrays
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Reshaping: Adding 3rd dimension
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Now, to integrate the forecasting part
    X_forecast = np.array(X_train[-1, 1:])  # Selecting the last 6 values from X_train
    X_forecast = np.append(X_forecast, y_train[-1])  # Appending the last actual y_train value
    X_forecast = np.reshape(X_forecast, (1, X_forecast.shape[0], 1))  # Reshaping for LSTM input

# Now, X_train and y_train are prepared for training, and X_forecast is prepared for forecasting.
        
    real_stock_price = dfset_test.iloc[:, 0:1].values

    # To predict, we need stock prices of 7 days before the test set
    # So combine train and test set to get the entire df set
    dfset_total = pd.concat((dfset_train, dfset_test), axis=0)
    testing_set = dfset_total[len(dfset_total) - len(dfset_test) - backdata:].values
    testing_set = testing_set.reshape(-1, 1)
    # -1=till last row, (-1,1)=>(80,1). otherwise only (80,0)

    # Feature scaling
    testing_set = sc.transform(testing_set)

    # Create df structure
    X_test = []
    for i in range(backdata, len(testing_set)):
        X_test.append(testing_set[i - backdata:i, 0])
    # Convert list to numpy arrays
    X_test = np.array(X_test)

    # Reshaping: Adding 3rd dimension
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Testing Prediction
    predicted_stock_price = regressor.predict(X_test)

    # Getting original prices back from scaled values
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    # Forecasting Prediction
    forecasted_stock_price = regressor.predict(X_forecast)

    # Getting original prices back from scaled values
    forecasted_stock_price = sc.inverse_transform(forecasted_stock_price)

    lstm_pred = forecasted_stock_price[0, 0]

    latest_closed_price = dfSet.iloc[-1]['Close']
    print("Latest closed price:", latest_closed_price)

    final_forecast= latest_closed_price + lstm_pred


    error_lstm = math.sqrt(mean_squared_error(real_stock_price, predicted_stock_price))
    final_forecast= round(final_forecast, 3)
    error_lstm = round(error_lstm, 2)
    if final_forecast > latest_closed_price:
      forecasted_stock_price = final_forecast - error_lstm
    elif final_forecast < latest_closed_price:
      forecasted_stock_price = final_forecast + error_lstm
    else:
        st.write("Error: latest closed price is equal to forecasted price")
    print("##############################################################################")


    st.text("Next Month's prediction is: ")
    if final_forecast > latest_closed_price:
      st.header(str(final_forecast)+" or greater" )
    elif final_forecast < latest_closed_price:
      st.header(str(final_forecast)+" or lesser" )
    st.text("RSME : " + str(error_lstm))





else:
    st.write("model not available")

