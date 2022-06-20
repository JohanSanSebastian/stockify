import streamlit as st
import backtrader as bt
import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import hydralit_components as hc
import matplotlib
import numpy as np
import warnings
from matplotlib import warnings
from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN)
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from rsi import RSIStrategy
from datetime import date
st.set_page_config(page_title='Tradelyne', layout="wide",initial_sidebar_state='collapsed')#initial_sidebar_state='collapsed', 
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
def fxn():
    warnings.warn("deprecated", DeprecationWarning)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
st.set_option('deprecation.showPyplotGlobalUse', False)
today=date.today()
def backtestrsi():
    global strategy
    ticker=st.sidebar.text_input("Stock ticker", value="AAPL")
    start=st.sidebar.text_input("Start date", value="2018-01-31")
    end=st.sidebar.text_input("End date", value=today)
    cash=st.sidebar.text_input("Starting cash", value=10000)
    cash=int(cash)
    cerebro=bt.Cerebro()
    cerebro.broker.set_cash(cash)
    start_value=cash
    data = bt.feeds.PandasData(dataname=yf.download(ticker, start, end))
    start=start.split("-")
    end=end.split("-")
    for i in range(len(start)):
        start[i]=int(start[i])
    for j in range(len(end)):
        end[j]=int(end[j])
    year=end[0]-start[0]
    month=end[1]-start[1]
    day=end[2]-start[2]
    totalyear=year+(month/12)+(day/365)
    matplotlib.use('Agg')
    cerebro.adddata(data)

    cerebro.addstrategy(RSIStrategy)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    final_value=cerebro.broker.getvalue()
    returns=(final_value-start_value)*100/start_value
    annual_return=returns/totalyear
    returns=round(returns, 2)
    annual_return=round(annual_return,2)
    returns=str(returns)
    annual_return=str(annual_return)
    figure = cerebro.plot()[0][0]
    st.pyplot(figure)
    st.write('')
    st.subheader(f"{ticker}'s total returns are {returns}% with a {annual_return}% APY")
    strategy=''

def volatility():
    global strategy
    import backtrader as bt
    import os
    from VIXStrategy import VIXStrategy
    import yfinance as yf
    import pandas as pd
    global ticker
    ticker=st.sidebar.text_input("Stock ticker", value="AAPL")
    start=st.sidebar.text_input("Start date", value="2018-01-31")
    end=st.sidebar.text_input("End date", value=today)
    cash=st.sidebar.text_input("Starting cash", value=10000)
    cash=int(cash)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    start_value=cash
    class SPYVIXData(bt.feeds.GenericCSVData):
        lines = ('vixopen', 'vixhigh', 'vixlow', 'vixclose',)

        params = (
            ('dtformat', '%Y-%m-%d'),#'dtformat', '%Y-%m-%d'),
            ('date', 0),
            ('spyopen', 1),
            ('spyhigh', 2),
            ('spylow', 3),
            ('spyclose', 4),
            ('spyadjclose', 5),
            ('spyvolume', 6),
            ('vixopen', 7),
            ('vixhigh', 8),
            ('vixlow', 9),
            ('vixclose', 10)
        )

    class VIXData(bt.feeds.GenericCSVData):
            params = (
            ('dtformat', '%Y-%m-%d'),
            ('date', 0),
            ('vixopen', 1),
            ('vixhigh', 2),
            ('vixlow', 3),
            ('vixclose', 4),
            ('volume', -1),
            ('openinterest', -1)
        )
    #
    ticker=ticker
    df = yf.download(tickers=ticker, start=start, end=end, rounding= False)
    df=df.reset_index() 
    df2 = yf.download(tickers='^VIX', start=start, end=end, rounding= False)
    df2.rename(columns = {'Open':'Vix Open', 'High':'Vix High', 'Low':'Vix Low', 'Close':'Vix Close'}, inplace = True)
    df2=df2.drop("Volume", axis=1)
    df2=df2.drop("Adj Close", axis=1)
    df2=df2.reset_index()
    df3=df2
    df2=df2.drop("Date", axis=1)
    result=pd.concat([df, df2], axis=1, join='inner')
    results=result
    df3.to_csv(r'https://github.com/Utkarshhh20/trial/blob/main/trial.csv')
    results.to_csv(r'https://github.com/Utkarshhh20/trial/blob/main/trial2.csv')
    first_column1 = results.columns[0]
    results.to_csv('trial2.csv', index=False)
    #results = pd.read_csv('trial2.csv')
    # If you know the name of the column skip this
    # Delete first
    #result = result.drop([first_column], axis=1)
    # If you know the name of the column skip this
    first_column2 = df3.columns[0]
    # Delete first
    df3.to_csv('trial.csv', index=False)
    st.dataframe(result)
    st.dataframe(df3)
    csv_file = os.path.dirname(os.path.realpath(__file__)) + "/trial2.csv"
    vix_csv_file = os.path.dirname(os.path.realpath(__file__)) + "/trial.csv"

    spyVixDataFeed = SPYVIXData(dataname=csv_file)
    vixDataFeed = VIXData(dataname=vix_csv_file)
    start=start.split("-")
    end=end.split("-")
    for i in range(len(start)):
        start[i]=int(start[i])
    for j in range(len(end)):
        end[j]=int(end[j])
    year=end[0]-start[0]
    month=end[1]-start[1]
    day=end[2]-start[2]
    totalyear=year+(month/12)+(day/365)
    matplotlib.use('Agg')
    cerebro.adddata(spyVixDataFeed)
    cerebro.adddata(vixDataFeed)

    cerebro.addstrategy(VIXStrategy)

    cerebro.run()
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    final_value=cerebro.broker.getvalue()
    returns=(final_value-start_value)*100/start_value
    annual_return=returns/totalyear
    returns=round(returns, 2)
    annual_return=round(annual_return,2)
    returns=str(returns)
    annual_return=str(annual_return)
    figure = cerebro.plot(volume=False)[0][0]
    st.pyplot(figure)
    st.subheader(f"{ticker}'s total returns are {returns}% with a {annual_return}% APY")
    strategy=''

def backtestgolden():
    global strategy
    from goldencrossover import goldencrossover
    ticker=st.sidebar.text_input("Stock ticker", value="AAPL")
    start=st.sidebar.text_input("Start date", value="2018-01-31")
    end=st.sidebar.text_input("End date", value=today)
    cash=st.sidebar.text_input("Starting cash", value=10000)
    cash=int(cash)
    cerebro=bt.Cerebro()
    cerebro.broker.set_cash(cash)
    start_value=cash
    data = bt.feeds.PandasData(dataname=yf.download(ticker, start, end))
    start=start.split("-")
    end=end.split("-")
    for i in range(len(start)):
        start[i]=int(start[i])
    for j in range(len(end)):
        end[j]=int(end[j])
    year=end[0]-start[0]
    month=end[1]-start[1]
    day=end[2]-start[2]
    totalyear=year+(month/12)+(day/365)
    matplotlib.use('Agg')
    cerebro.adddata(data)

    cerebro.addstrategy(goldencrossover)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    final_value=cerebro.broker.getvalue()
    returns=(final_value-start_value)*100/start_value
    annual_return=returns/totalyear
    returns=round(returns, 2)
    annual_return=round(annual_return,2)
    returns=str(returns)
    annual_return=str(annual_return)
    figure = cerebro.plot()[0][0]
    st.pyplot(figure)
    st.subheader(f"{ticker}'s total returns are {returns}% with a {annual_return}% APY")
    strategy=''
def backtestbollinger():
    global strategy
    import numpy as np
    import pandas as pd
    import pandas_datareader as pdr
    import matplotlib.pyplot as plt
    symbol=st.sidebar.text_input("Stock ticker", value="AAPL")
    start=st.sidebar.text_input("Start date", value="2018-01-31")
    end=st.sidebar.text_input("End date", value=today)
    cash=st.sidebar.text_input("Starting cash", value=10000)
    cash=int(cash)
    def get_bollinger_bands(prices, rate=20):
        sma=prices.rolling(rate).mean()
        std = prices.rolling(rate).std()
        bollinger_up = sma + std * 2 # Calculate top band
        bollinger_down = sma - std * 2 # Calculate bottom band
        return bollinger_up, bollinger_down, sma
    df = pdr.DataReader(symbol, 'yahoo', start=start, end=end)
    start=start.split("-")
    end=end.split("-")
    for i in range(3):
        start[i]=int(start[i])
        end[i]=int(end[i])
    totalyear=(end[0]-start[0])+((end[1]-start[1])/12)+((end[2]-start[2])/365)
    df.index = np.arange(df.shape[0])
    closing_prices = df['Close']
    money=cash
    investpercent=0.9
    bollinger_up, bollinger_down, sma = get_bollinger_bands(closing_prices)
    matplotlib.use('Agg')
    fig=plt.title(symbol + ' Bollinger Bands')
    fig=plt.xlabel('Days')
    fig=plt.ylabel('Closing Prices')
    fig=plt.plot(sma, label='SMA', c='y', linewidth=1)
    fig=plt.plot(closing_prices, label='Closing Prices')
    fig=plt.plot(bollinger_up, label='Bollinger Up', c='g', linewidth=1)
    fig=plt.plot(bollinger_down, label='Bollinger Down', c='r', linewidth=1)
    sell=[]
    sellday=[]
    buy=[]
    buyday=[]
    close=df['Close']
    position=1
    for i in range(len(close)):
        if position==-1 and i==(len(close)-1):
            print('selling', df['Close'][i], bollinger_up[i])
            sell.append(df['Close'][i])
            sellday.append(i)
            position=1
        elif df['Close'][i]<=bollinger_down[i] and position==1:
            print('buying', df['Close'][i], bollinger_down[i])
            buy.append(df['Close'][i])
            buyday.append(i)
            position=-1
        elif df['Close'][i]>=bollinger_up[i] and position==-1:
            print('selling', df['Close'][i], bollinger_up[i])
            sell.append(df['Close'][i])
            sellday.append(i)
            position=1
    print(sell, buy)
    trades=len(buy)
    for i in range(trades):
        if cash==money:
            profit=((sell[i]-buy[i])/buy[i])*investpercent*cash
            cash=cash+profit
        else:
            profit=((sell[i]-buy[i])/buy[i])*investpercent*cash
            cash=cash+profit
    returns=(cash-money)*100/money
    annual_return=returns/totalyear
    returns=round(returns, 2)
    annual_return=round(annual_return,2)
    returns=str(returns)
    annual_return=str(annual_return)
    for i in range(len(sellday)):
        fig=plt.plot(sellday[i], sell[i], marker="v", markersize=7, markeredgecolor="red", markerfacecolor="red")
        fig=plt.plot(buyday[i], buy[i], marker="^", markersize=7, markeredgecolor="green", markerfacecolor="green")
    fig=plt.savefig(fname='hi')
    plt.legend()
    plt.show()
    st.pyplot(fig)
    st.subheader(f"{symbol}'s total returns are {returns}% with a {annual_return}% APY")
    strategy=''
def get_fundamentals():
    try:
        # Find fundamentals table
        fundamentals = pd.read_html(str(html), attrs = {'class': 'snapshot-table2'})[0]
        
        # Clean up fundamentals dataframe
        fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        colOne = []
        colLength = len(fundamentals)
        for k in np.arange(0, colLength, 2):
            colOne.append(fundamentals[f'{k}'])
        attrs = pd.concat(colOne, ignore_index=True)
    
        colTwo = []
        colLength = len(fundamentals)
        for k in np.arange(1, colLength, 2):
            colTwo.append(fundamentals[f'{k}'])
        vals = pd.concat(colTwo, ignore_index=True)
        
        fundamentals = pd.DataFrame()
        fundamentals['Attributes'] = attrs
        fundamentals['Values'] = vals
        fundamentals = fundamentals.set_index('Attributes')
        return fundamentals

    except Exception as e:
        return e
    
def get_news():
    try:
        # Find news table
        news = pd.read_html(str(html), attrs = {'class': 'fullview-news-outer'})[0]
        links = []
        for a in html.find_all('a', class_="tab-link-news"):
            links.append(a['href'])
        
        # Clean up news dataframe
        news.columns = ['Date', 'News Headline']
        news['Article Link'] = links
        news = news.set_index('Date')
        return news

    except Exception as e:
        return e

def get_insider():
    try:
        # Find insider table
        insider = pd.read_html(str(html), attrs = {'class': 'body-table'})[0]
        
        # Clean up insider dataframe
        insider = insider.iloc[1:]
        insider.columns = ['Trader', 'Relationship', 'Date', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']
        insider = insider[['Date', 'Trader', 'Relationship', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']]
        insider = insider.set_index('Date')
        return insider

    except Exception as e:
        return e
title="""
    <style>
    .Tradelyne {
    text-align: center;
    margin-top: -100px;
    margin-left: 67px;
    font-size: 40px;
    font-family: Arial, Helvetica, sans-serif;
    letter-spacing: 2px;
    }
    </style>
    <body>
    <p1 class='Tradelyne'>Tradelyne</p1>
    </body>
    """
st.sidebar.markdown(title, unsafe_allow_html=True)
st.sidebar.write('_______________________')
trade_lyne="""
    <style>
    .trial2 {
    text-align: center;
    margin-top: -30px;
    margin-left: -13px;
    font-size: 300px;
    }
    </style>
    <body>
    <h1 class='trial2'>Select your dashboard</h1>
    </body>
    """
st.sidebar.markdown(trade_lyne, unsafe_allow_html=True)
navbar='''
    <style>
    .padding{
    font-size: 100px;
    padding: 10px, 20px, 30px;  
    background-color: green;
    margin-top: 0px;  
    margin-left: 200px;
    }
    </style>
    <body>
    <p1 class='padding'>hidddd</p1>
    </body>
'''
#st.markdown(navbar, unsafe_allow_html=True)

trial=st.columns([1])
menu_data = [
    {'icon': "far fa-copy", 'label':"Fundamental analysis"},
    #{'icon': "fa-solid fa-radar",'label':"Dropdown1   ", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
    {'icon': "far fa-chart-bar", 'label':"Technical Indicators"},#no tooltip message
    #{'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar   "},
    #{'icon': "fas fa-tachometer-alt", 'label':"Dashboard   ",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
    {'icon': "fas fa-tachometer-alt", 'label':"Backtesting"},
    #{'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
    {'icon': "bi bi-telephone", 'label':"Contact us"},
]

over_theme = {'txc_inactive': '#FFFFFF'}
over_theme = {'txc_inactive': "#D3D3D3",'menu_background':'#3948A5','txc_active':'white','option_active':'#3948A5'}
with trial[0]:
    dashboard = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Tradelyne',
    #login_name='Logout',
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
    use_animation=True,
    key='NavBar'
    )
dashboard = st.sidebar.selectbox('', ('Home', 'Fundamental Analysis', 'Technical Indicators', 'Backtesting', 'Pattern Stocks'), 0)
st.title(dashboard)
st.write('___')
if dashboard!='Tradelyne':
    st.title(dashboard)
if dashboard=='Tradelyne':
    logo='''
    <style>
    .logo{
        width: 100%;
        margin-top:-100px;
        margin-left:-30px;
    }
    </style>
    <body>
    <img src='https://cdn.myportfolio.com/fd40c2a8-1f6f-47d7-8997-48ba5415a69c/6c46ac13-6a18-427a-9baa-01ad3b53ac45_rw_600.png?h=21b14417887f0576feb32fcbfd191788' alt='logo' class='logo'></img> 
    </body>
    '''
    homeimage='''
    <style>
    .homeimg {
    width: 100%;
    float: right;
    margin-top: 0px;
    z-index: 1;
    position: relative;
    border-radius: 10%;
    }
    </style>
    <body>
    <img src="https://cdn.myportfolio.com/fd40c2a8-1f6f-47d7-8997-48ba5415a69c/3da6f1b3-6f54-41c3-8643-01aae0b48ef3_rw_1200.png?h=39a23c885e98a256c9f1f14906ee2e68" alt="House" class='homeimg'></img>
    </body>'''
    fundament='''
    <style>
    .faimg {
    width: 350px;
    float: center;
    margin-top: 18px;
    z-index: 1;
    position: relative;
    }
    </style>
    <body>
    <img src="https://cdn.myportfolio.com/fd40c2a8-1f6f-47d7-8997-48ba5415a69c/3a56fae1-6ca5-40c6-b6c6-ff39fc47e486_rw_600.png?h=f3306082b779851a92589d8b668951d7" alt="House" class='faimg'></img>
    </body>'''
    fundtxt='''
    <style>
    .fundtxt {
        font-size: 25px;
        margin-top:0px;
        font-weight: 700;
        margin-bottom: 0px;
    }
    </style>
    <body>
    <center> <p1 class='fundtxt'> FUNDAMENTAL ANALYSIS </p1> </center>
    </body>
    '''
    fundsubtxt='''
    <style>
    .fundsubtxt {
        font-size: 15px;
        margin-top:20px;
        font-weight: 100;
        margin-bottom: 0px;
    }
    </style>
    <body>
    <center> <p1 class='fundsubtxt'> Check the latest fundamentals of a stock just by entering a stock ticker using our fundamental analysis feature. Utilize the information on the recent insider trades and news of the company of your choice to make profits. </p1> </center>
    </body>
    '''
    tech='''
    <style>
    .taimg {
    width: 435px;
    float: center;
    z-index: 1;
    position: relative;
    border-radius: 5%;
    }
    </style>
    <body>
    <img src="https://cdn.myportfolio.com/fd40c2a8-1f6f-47d7-8997-48ba5415a69c/5627fdb1-f10a-4d6c-b026-7abb76b92aa8_rw_600.png?h=ea32c83843aee2609aa26561a36bb4ea" alt="House" class='taimg'></img>
    </body>'''
    techtxt='''
    <style>
    .techtxt {
        font-size: 25px;
        margin-top:0px;
        font-weight: 700;
        margin-bottom: 0px;
    }
    </style>
    <body>
    <center> <p1 class='techtxt'> TECHNICAL INDICATORS </p1> </center>
    </body>
    '''
    techsubtxt='''
    <style>
    .techsubtxt {
        font-size: 15px;
        margin-top:20px;
        font-weight: 100;
        margin-bottom: 0px;
    }
    </style>
    <body>
    <center> <p1 class='techsubtxt'> Find the latest patterns emerging within stocks or locate stocks that showcase a recent pattern using our technical indicators feature. </p1> </center>
    </body>
    '''
    backt='''
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    .btimg {
    float: center;
    z-index: 1;
    width: 400px;
    position: relative;
    border-radius: 5%;
    }
    </style>
    <body>
    <center><img src="https://cdn.myportfolio.com/fd40c2a8-1f6f-47d7-8997-48ba5415a69c/3c7a6502-fcd7-43ed-bf9b-444bd71825e7_rw_600.png?h=a77fdb06036cb1e327227058b42f4baa" alt="House" class='btimg'></img></center>
    <p1 class>
    </body>'''
    bttxt='''
    <style>
    .techtxt {
        font-size: 25px;
        margin-top:0px;
        font-weight: 700;
        margin-bottom: 0px;
    }
    </style>
    <body>
    <center> <p1 class='techtxt'> BACKTESTING </p1> </center>
    </body>
    '''
    btsubtxt='''
    <style>
    .btsubtxt {
        font-size: 15px;
        margin-top:20px;
        font-weight: 100;
        margin-bottom: 0px;
    }
    </style>
    <body>
    <center> <p1 class='btsubtxt'> What if you had invested your money in a stock using a certain startegy? How much profit would you have made? Find out using our backtesting feature which has certain predefined strategies to backtest. </p1> </center>
    </body>
    '''
    #st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">', unsafe_allow_html=True,)
    #st.markdown(trade_lyne, unsafe_allow_html=True)
    #st.markdown(slogan, unsafe_allow_html=True)
    tradelyne,eth=st.columns(2)
    with tradelyne:
        st.markdown(logo, unsafe_allow_html=True)
    with eth: 
        st.markdown(homeimage, unsafe_allow_html=True)
    st.write('_______________________________________')
    #st.text('Get Started')
    #with st.container():
    #    st.write('Hi')
    #    st.write('')
    fundamental,technical,backtesting=st.columns(3)
    with fundamental:
        st.markdown(fundament, unsafe_allow_html=True)
        st.markdown(fundtxt, unsafe_allow_html=True)
        st.markdown(fundsubtxt, unsafe_allow_html=True)
        #st.write('Fundamental Analysis can be done using ')
        #st.image('https://cdn.myportfolio.com/fd40c2a8-1f6f-47d7-8997-48ba5415a69c/4649c3af-7f27-4709-9780-fda372566b4a_rw_1200.png?h=3454dba140a41751142c60641be53ed2', width=450)
        st.write('______________')
        
    with technical:
        st.markdown(tech, unsafe_allow_html=True)
        st.markdown(techtxt, unsafe_allow_html=True)
        st.markdown(techsubtxt, unsafe_allow_html=True)
        #st.write('Fundamental Analysis can be done using ')
        #st.image('https://cdn.myportfolio.com/fd40c2a8-1f6f-47d7-8997-48ba5415a69c/e62d6401-816c-4134-9879-e02429780e38_rw_1200.png?h=ffdf8eaa2424f3c2ef3249b4e6ad581a', width=450)
        st.write('______________')
        #st.write('')
        #st.header('Technical Analysis')
        #st.write('Blah')
    with backtesting:    
        st.markdown(backt, unsafe_allow_html=True)
        st.markdown(bttxt, unsafe_allow_html=True)
        st.markdown(btsubtxt, unsafe_allow_html=True)
        #st.write('Fundamental Analysis can be done using uUHUghuruuuuuuuuuuuuuuuuuuuuuuuuuuu ')
        st.write('______________')
        #st.image('https://cdn.myportfolio.com/fd40c2a8-1f6f-47d7-8997-48ba5415a69c/c24aca21-c03b-4c87-a7d8-25c550fd612c_rw_1200.png?h=1aa84baacad2b04ae4203946bf5ebe78', width=450)
        #st.write('')
        #st.header('Backtesting')
        #st.write('Back')
    first,second,third=st.columns(3)
    with first:
        st.header('Fundamental Analysis')
        st.write('Blah')
    with second:
        pass
    with third:
        pass
    #st.markdown(fundament, unsafe_allow_html=True)
    #st.markdown(tech, unsafe_allow_html=True)
    #st.markdown(backt, unsafe_allow_html=True)
    st.subheader('What is Tradelyne?')
    st.write('Tradelyne is a web application developed on python using the streamlit library which aims to provide you with the tools necessary to make trading and investing much simpler. Using this web app you can enhance and optimize your investing skills and take advantage of every opportunity presented to you by the market\n ')
    st.subheader('What can I do on Tradelyne?')
    st.write('''You can use this web app to do:\n
1. Fundamental Analysis - Learn and check the fundamentals of various companies and make inferences based on the data provided.\n
2. Technical Analysis - Read price chart movements and see important indicators to predict the price and make entry and exit positions accordingly.\n
3. Backtesting - Backtesting answer's your " What if ? " question as to what if you had used xyz strategy on a stock over a period of time. Would you make profits or would it be a loss? Find out using our pre defined strategies in backtesting module.\n''')
st.write('''**Utilize these features by using the sidebar by opening the menu on mobile.**\n''')
if dashboard=='Fundamental Analysis':
    s_fundament = st.sidebar.selectbox('What would you like to do?', ('Learn', 'Check fundamentals'), 0)
    if s_fundament=='Learn':
        st.subheader('What Is Fundamental Analysis?')
        st.write('''• Fundamental analysis is a method of determining a stock's real or "fair market" value.\n
• Fundamental analysts search for stocks that are currently trading at prices that are higher or lower than their real value.\n
• If the fair market value is higher than the market price, the stock is deemed to be undervalued and a buy recommendation is given.\n
• In contrast, technical analysts ignore the fundamentals in favor of studying the historical price trends of the stock.\n''')
        st.subheader('Understanding Fundamental Analysis')
        st.write('''All stock analysis tries to determine whether a security is correctly valued within the broader market. Fundamental analysis is usually done from a macro to micro perspective in order to identify securities that are not correctly priced by the market.\n
For stocks, fundamental analysis uses revenues, earnings, future growth, return on equity, profit margins, and other data to determine a company's underlying value and potential for future growth. All of this data is available in a company's financial statements.\n''')
        st.subheader('Financial Statements: Quantitative Fundamentals to Consider')
        st.write('Financial statements are the medium by which a company discloses information concerning its financial performance. Followers of fundamental analysis use quantitative information gleaned from financial statements to make investment decisions. The three most important financial statements are income statements, balance sheets, and cash flow statements.')
        st.write('')
        st.write('''**Check the fundamentals of any stock by entering the ticker in the sidebar on the next page.**\n''')
    elif s_fundament=='Check fundamentals':
        symbol=st.sidebar.text_input("Ticker", value='AAPL', max_chars=10)
        pd.set_option('display.max_colwidth', 25)
        st.subheader(f"{symbol}'s Fundamentals ")
        # Set up scraper
        url = ("https://finviz.com/quote.ashx?t=" + symbol.lower())
        req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
        webpage = urlopen(req)
        html = bs(webpage, "html.parser")
        fundament=get_fundamentals()
        inside=get_insider()
        news=get_news()
        st.write(fundament)
        st.write('Several important indicators which could be used like marketcap, P/E, PEG, Debt/Eq, ROI etc have been indicated within the dataframe above. These can be used to find entry and exit positions and see if the company is fundamentally sound.')
        st.write('_______________________________________________________________________________________________')
        st.subheader("\n\nRecent trades made by company's officials")
        st.write(inside)
        st.write('**When Insiders Buy, Should Investors Join Them?**\n \n')
        st.write('''This question doesn't have any right answers but one could sure speculate based on this information.\n
Tips for beating the market tend to come and go quickly, but one has held up extremely well: if executives, directors, or others with inside knowledge of a public company are buying or selling shares, investors should consider doing the same thing. Research shows that insider trading activity is a valuable barometer of broad shifts in market and sector sentiment.
However, before chasing each insider move, outsiders need to consider the factors that dictate the timing of trades and the factors that conceal the motivations and also that information is made public after a delay of the transaction made.''')
        st.write('_______________________________________________________________________________________________')
        st.subheader(f'Recent news on {symbol} stock')
        st.write(news)
        st.write('')
        st.write("\nStocks correlate the performance with the current market conditions and business news. They also predict the performance of the stock market and advise on buying and selling of stocks, mutual funds, and other securities.")
if dashboard=='Backtesting':
    strategy = st.sidebar.selectbox("Which Strategy?", ('Intro', 'RSI', 'Volatility', 'Golden Crossover', 'Bollinger Bands'), 0, key='strategy')
    st.header(strategy)
    if strategy=='Intro':
        st.subheader('What is backtesting?')
        st.write('''• Backtesting assesses the viability of a trading strategy or pricing model by discovering how it would have played out retrospectively using historical data.\n
• The underlying theory is that any strategy that worked well in the past is likely to work well in the future, and conversely, any strategy that performed poorly in the past is likely to perform poorly in the future.\n
• When testing an idea on historical data, it is beneficial to reserve a time period of historical data for testing purposes. If it is successful, testing it on alternate time periods or out-of-sample data can help confirm its potential viability.''')
        st.subheader('What is the need for backtesting?')
        st.write('Backtesting is one of the most important aspects of developing a trading system. If created and interpreted properly, it can help traders optimize and improve their strategies, find any technical or theoretical flaws, as well as gain confidence in their strategy before applying it to the real world markets.')
        st.subheader('Please choose one of our strategies on the sidebar to backtest')
    while strategy=='RSI':
            backtestrsi()
    while strategy=='Volatility':
        volatility()
    while strategy=='Golden Crossover':
            backtestgolden()
    while strategy=='Bollinger Bands':
            backtestbollinger()
