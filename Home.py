
import streamlit as st
import os
import yfinance as yf
import datetime
from datetime import date





st.set_page_config(
    page_title="Stock X",
    page_icon="🧊",
    layout="wide",
    
)


with open(os.path.join('styles.css')) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.markdown("<h1 class='Title' >Stock X</h1>", unsafe_allow_html=True, )

st.sidebar.info('Welcome to the Stock Price Prediction App. Choose your Stocks below')

st.markdown("<div class='hero'><div class='mainpage'><p class='para'><h3>Why Stock X ?</h3><ol><b><i>Visualize with Clarity:</i></b> Gain a clear understanding of market movements with our intuitive visualization tools. Dive deep into interactive charts </ol> <ol><b><i>Stay Informed:</i></b> Stay ahead of the curve with real-time access to the latest news and updates from the world of finance.</ol>  <ol><b><i>Explore Fundamentals: </i></b>Dig deeper into the fundamentals of stocks with access to comprehensive financial data. From earnings reports to balance sheets</ol>  <ol><b><i>Predict price of stock</i></b></ol> </p></div><img src='https://img.freepik.com/free-vector/hand-drawn-stock-market-concept-with-analysts_23-2149163670.jpg' class='img' ></div>", unsafe_allow_html=True, )



#downloading data function

@st.cache_resource
def download_df(op, start_date, end_date):
    df = yf.download(op, start=start_date, end=end_date, progress=False)
    
    return df


#taking input from user

Stock = st.sidebar.text_input('Enter a Stock Symbol', placeholder ='STOCKTICKER.NS', value='RELIANCE.NS')
Stock = Stock.upper()
today = datetime.date.today()
duration = 1500
before = today - datetime.timedelta(days=duration)
start_date = before
end_date =  today
if st.sidebar.button('Send'):
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date: `%s`' %(start_date, end_date))
        download_df(Stock, start_date, end_date)
    else:
        st.sidebar.error('Error: End date must fall after start date')

st.session_state['Stock'] = Stock
#downloading data

df = download_df(Stock, start_date, end_date)
PredData =yf.download(Stock, start="2017-01-01", end=today, interval="1mo", progress=False)
Viz = df.copy()
Viz['Date'] = Viz.index.strftime('%Y-%m-%d')
st.session_state['Viz']= Viz
st.session_state['PredData']= PredData


        


    
    




