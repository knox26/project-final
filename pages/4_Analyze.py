import streamlit as st
from streamlit_option_menu import option_menu
from tradingview_ta import TA_Handler, Interval
import pandas as pd
from alpha_vantage.fundamentaldata import FundamentalData
from finvizfinance.quote import finvizfinance

st.set_page_config(
        page_title="Stock X",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
)


with open('pages\styles5.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

st.markdown("<h1 class='Title' >Analyze</h1>", unsafe_allow_html=True)

Stock = st.session_state['Stock']
flag=False   

df = pd.read_csv('companiesTicker.csv')

if Stock in df['Ticker'].astype(str).str.strip().values:
    print(f"The stock ticker {Stock} is present in the CSV file.")
    flag=True
else:
    print(f"The stock ticker {Stock} is not present in the CSV file.")
    flag=False

if flag==True:
    Tticker =Stock[:-3] 
    print(Tticker)
else:
    Tticker = Stock
    print(Tticker)


st.subheader(Tticker)

selected = option_menu(
              menu_title="",  # required
              options=['Fundamental Data', 'News','Indicator Analysis'],  # required
              default_index=0,  # optional
              orientation = "horizontal", 
               styles={
                 
                "container": {"padding": "0!important",
                              },
                
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "0px",
                    
                },
                
                
            }, # optional
          )
    


if selected == 'Fundamental Data':
    st.write("<br>", unsafe_allow_html=True)

    if flag==False:
        try:
            key = ' 4BLVRHXAUWVRIZTR'
            fd = FundamentalData(key, output_format='pandas')

            st.subheader('Balance Sheet')
            balance_sheet = fd.get_balance_sheet_annual(Stock)[0]
            bs = balance_sheet.T[2:]
            bs.columns = list(balance_sheet.T.iloc[0])
            st.write(bs)

            st.subheader('Income Statement')
            income_statement = fd.get_income_statement_annual(Stock)[0]
            is1 = income_statement.T[2:]
            is1.columns = list(income_statement.T.iloc[0])
            st.write(is1)

            st.subheader('Cash Flow Statement')
            cash_flow = fd.get_cash_flow_annual(Stock)[0]
            cf = cash_flow.T[2:]
            cf.columns = list(cash_flow.T.iloc[0])
            st.write(cf)

        except Exception as e:
            st.error('API call limit reached. Please try again later.')
    elif flag == True:
        st.write("buy premium version of alpha vantage to get fundamental data")
        st.write("Basic version only supports US stock market data")
    # import finnhub
    # key = 'coa3m71r01qg9u90tsn0coa3m71r01qg9u90tsng'
    # finnhub_client = finnhub.Client(api_key=key)

    # # Get company fundamentals for a specific Indian stock ticker symbol
    # print(finnhub_client.financials_reported(symbol='TATAMOTORS.NS', freq='annual'))
        



elif selected == 'Indicator Analysis':

  st.write("<br>", unsafe_allow_html=True)
       
  if flag==True:
    handler = TA_Handler(
        symbol=Tticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_1_DAY
    )
    
    T1=handler.get_analysis().summary
    
    
    T2=handler.get_analysis().oscillators
    
    T3=handler.get_analysis().moving_averages
    Summery, Oscillators_analysis, MovingAverage_analysis = st.tabs(["Overall Analysis", "  Oscillators Analysis  ", "  Moving Average Analysis"])
    with Summery:
        st.write("<br>", unsafe_allow_html=True)
        for key, value in T1.items():
            st.write(f"{key}: {value}")
    
    with Oscillators_analysis:
        st.write("<br>", unsafe_allow_html=True)
        for key, value in list(T2.items())[:4]:
            st.write(f"{key}: {value}")
        st.header("individual oscillators:")
        for key, value in T2['COMPUTE'].items():
            st.write(f"{key}: {value}")
        
    
    with MovingAverage_analysis: 
        st.write("<br>", unsafe_allow_html=True)    
        for key, value in list(T3.items())[:4]:
            st.write(f"{key}: {value}")
        st.header("individual moving averages:")
        for key, value in T3['COMPUTE'].items():
            st.write(f"{key}: {value}")   

  else:
    
    handler = TA_Handler(
        symbol=Stock,
        screener="america",
        exchange="NASDAQ",
        interval=Interval.INTERVAL_1_DAY
    )
    
    T1=handler.get_analysis().summary
    
    
    T2=handler.get_analysis().oscillators
    
    T3=handler.get_analysis().moving_averages
    Summery, Oscillators_analysis, MovingAverage_analysis = st.tabs(["Overall Analysis", "Oscillators Analysis", "Moving Average Analysis"])
    with Summery:
        st.write("<br>", unsafe_allow_html=True)
        for key, value in T1.items():
            st.write(f"{key}: {value}")
    
    with Oscillators_analysis:
        st.write("<br>", unsafe_allow_html=True)
        for key, value in list(T2.items())[:4]:
            st.write(f"{key}: {value}")
        st.header("individual oscillators:")
        for key, value in T2['COMPUTE'].items():
            st.write(f"{key}: {value}")
        
    
    with MovingAverage_analysis: 
        st.write("<br>", unsafe_allow_html=True)    
        for key, value in list(T3.items())[:4]:
            st.write(f"{key}: {value}")
        st.header("individual moving averages:")
        for key, value in T3['COMPUTE'].items():
            st.write(f"{key}: {value}")   

elif selected == 'News':
    if flag == True:
        st.write("buy premium version of Finviz Finance to get news data")
        st.write("Basic version only supports US stock news")
    elif flag == False:
        stocknews = finvizfinance(Tticker)
        st.header('News of '+ str(Tticker))
        news_df = stocknews.ticker_news()
        for i in range(10):
            st.subheader(f'News {i+1}')
            st.write(news_df['Date'][i])
            st.write(news_df['Title'][i])
            st.write(news_df['Link'][i])

