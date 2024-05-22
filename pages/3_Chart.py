
import pandas as pd
from lightweight_charts.widgets import StreamlitChart
from streamlit_option_menu import option_menu
import streamlit as st
import os

st.set_page_config(
        page_title="Stock X",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
)


with open(os.path.join('pages', 'styles5.css')) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

Viz = st.session_state['Viz']
Stock = st.session_state['Stock']
Tticker =Stock[:-3]  
#calculating technical indicators

def calculate_bollinger_bands(Viz, period: int = 20):
    sma = Viz['Close'].rolling(window=period).mean()
    std_dev = Viz['Close'].rolling(window=period).std()
    
    return pd.DataFrame({
        'time': Viz['Date'],
        f'Bollinger Band Upper {period}': sma + (std_dev * 2),
        f'Bollinger Band Lower {period}': sma - (std_dev * 2)
    }).dropna()

bb_data = calculate_bollinger_bands(Viz, period=20)

def calculate_sma(Viz, period: int = 20):
    return pd.DataFrame({
        'time': Viz['Date'],
        f'SMA {period}': Viz['Close'].rolling(window=period).mean()
    }).dropna()

sma_data = calculate_sma(Viz, period=20)

def calculate_ema(Viz, period: int = 20):
    return pd.DataFrame({
        'time': Viz['Date'],
        f'EMA {period}': Viz['Close'].ewm(span=period, adjust=False).mean()
    })

ema_data = calculate_ema(Viz, period=20)

    # Add this to the visualization section
    
#visualizing technical indicators



st.markdown(f"<h2 class='Heading' >Visualize -- {Tticker}</h2>", unsafe_allow_html=True)

selected = option_menu(
            menu_title="",  # required
            options=['Chart', 'B Bands', 'SMA', 'EMA'],  # required
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

# Bollinger bands


if selected == 'Chart':
    
    chart = StreamlitChart(width=930, height=470)
    chart.set(Viz)
    chart.load()
    
        # Adjust padding as needed
elif selected == 'B Bands':
    
    chart = StreamlitChart(width=930, height=470)
    chart.set(Viz)
    
    bb_upper_line = chart.create_line('Bollinger Band Upper 20', color='#6e3fe7', price_label=False, width=1.4, price_line=False)
    bb_upper_line.set(bb_data)
    bb_lower_line = chart.create_line('Bollinger Band Lower 20',color='#6e3fe7',price_label=False, width=1.4 ,price_line=False)
    bb_lower_line.set(bb_data)
    chart.load()
    
    


elif selected == 'SMA':
    
    chart = StreamlitChart(width=930, height=470)
    chart.set(Viz)
    line = chart.create_line('SMA 20', color='#62D6E4', price_label=False, width=1.2 , price_line=False)
    
    line.set(sma_data)
    chart.load()
    

else:
    
    chart = StreamlitChart(width=930, height=470)
    chart.set(Viz)
    
    ema_line = chart.create_line('EMA 20',color='red',price_label=False, width=1.2, price_line=False, )
    ema_line.set(ema_data)
    chart.load()