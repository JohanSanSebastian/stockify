import matplotlib
import datetime
import warnings
import copy
import re

import streamlit as st
import backtrader as bt
import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
import plotly.graph_objs as go
import hydralit_components as hc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pandas_datareader import data as pdr

import matplotlib.pyplot as plt
from matplotlib import warnings
from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN)

from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
from pypfopt import objective_functions

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from rsi import RSIStrategy
from datetime import date
from datetime import datetime
from yahooquery import Screener
#import cufflinks as cf
from io import BytesIO

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
    '''global strategy
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
    '''

    global strategy
    s1,s2,s3,s4=st.columns(4)

    with s1:
        ticker=st.text_input("Stock ticker", value="AAPL")
    with s2:
        start=st.text_input("Start date", value="2018-01-31")
    with s3:
        end=st.text_input("End date", value=today)
    with s4:
        cash=st.text_input("Starting cash", value=10000)

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
    cerebro.addanalyzer(bt.analyzers.PyFolio ,_name='pf')
    cerebro.addanalyzer(bt.analyzers.PeriodStats, _name='cm')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='dd')
    cerebro.addanalyzer(bt.analyzers.VWR, _name='vwr')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer ,_name='ta')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio ,_name='sr')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    stratdd=cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    #back=Backtest(data, RSIStrategy, cash=10000)
    #stats=back.run()
    strat0 = stratdd[0]
    pyfolio = strat0.analyzers.getbyname('pf')
    returnss, positions, transactions, gross_lev,  = pyfolio.get_pf_items()
    final_value=cerebro.broker.getvalue()
    final_value=round(final_value, 2)
    returns=(final_value-start_value)*100/start_value
    annual_return=returns/totalyear
    returns=str(round(returns, 2))
    annual_return=str(round(annual_return,2))
    figure = cerebro.plot(style='line')[0][0]
    graph, info=st.columns([2,1])

    # print(stratdd[0].analyzers.dd.get_analysis())
    with graph:
        st.pyplot(figure)
    with info:
        trade=stratdd[0].analyzers.ta.get_analysis()
        tra=''
        trade=stratdd[0].analyzers.ta.get_analysis()
                #x=trade[i]
                #for i in x:
                #    tra=tra+(i.upper(), ':', x[i])
                #    st.write(tra)
        print("Trade info \n\n\n")
        print(trade)
        #st.write(trade)

        if int(start_value)<=int(final_value):
            fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = final_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Strategy returns"},
            delta = {'reference': start_value, 'increasing': {'color': "royalblue"}},
            gauge={'axis': {'range': [None, final_value*6/5], 'tickwidth': 1, 'tickcolor': "green"},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, start_value], 'color': '#D3D3D3'},
                    {'range': [start_value, final_value], 'color': 'royalblue'}],}
            ))
            fig.update_layout(paper_bgcolor = "white", font = {'color': "black", 'family': "Arial"}, width=500, height=500,)
            st.plotly_chart(fig, width=5)
        else:
            fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = final_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Strategy returns"},
            delta = {'reference': start_value, 'decreasing': {'color': "black"}},
            gauge={'axis': {'range': [None, start_value*6/5], 'tickwidth': 1, 'tickcolor': "red"},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, start_value], 'color': 'white'},
                    {'range': [final_value, start_value], 'color': '#D3D3D3'}],}
            ))

            fig.update_layout(paper_bgcolor = "white", font = {'color': "black", 'family': "Arial"}, width=500, height=500)
            st.image(fig)
            st.plotly_chart(fig)

        #st.subheader('Total returns: ', f"{returns}")
        #st.subheader('Annual returns: ', f"{annual_return}")
        st.subheader(f"{ticker}'s total returns are {returns}% with a {annual_return}% APY")
        st.subheader(f'Initial investment: {cash}')
        st.subheader(f'Final investment value: {final_value}')
        sr=stratdd[0].analyzers.sr.get_analysis()
        print(sr)

        for i in sr:
            ratio=sr[i]

        ratio=str(round(ratio, 3))
        print(ratio)
        st.subheader(f'Sharpe Ratio: {ratio}')

        dd=stratdd[0].analyzers.dd.get_analysis()
        max=dd['max']
        print(max)
        #max=max[1]+

        drawdown='Drawdown Stats: \n'

        for i in max:
            max[i]=str(round(max[i], 3))
            drawdown=f"{drawdown} {i} : {max[i]} \n"

        print(drawdown)
        st.subheader(drawdown)

        st.subheader('Trade Details')

        # trade_total = f"Total: {trade['AutoOrderedDict']['total']['AutoOrderedDict']['total']}"
        # trade_open = f"Open: {trade['AutoOrderedDict']['total']['AutoOrderedDict']['open']}"
        # trade_closed = f"Closed: {trade['AutoOrderedDict']['total']['AutoOrderedDict']['closed']}"
        # streak_won_current = f"Current: {['AutoOrderedDict']['streak']['AutoOrderedDict']['won']['AutoOrderedDict']['current']}"
        # streak_won_longest = f"Longest: {['AutoOrderedDict']['streak']['AutoOrderedDict']['won']['AutoOrderedDict']['longest']}"
        # streak_lost_current = f"Current: {['AutoOrderedDict']['streak']['AutoOrderedDict']['lost']['AutoOrderedDict']['current']}"
        # streak_lost_longest = f"Longest: {['AutoOrderedDict']['streak']['AutoOrderedDict']['lost']['AutoOrderedDict']['longest']}"
        # trade_details = "" f"{trade_total}\n{trade_open}\n{trade_closed}\n{streak_won_current}\n{streak_won_longest}\n{streak_lost_current}\n{streak_lost_longest}"

        # st.write(trade_details)
        for i in trade:
            if i=='total' or i=='streak' or i=='lost' or i=='won':
                if i=='pnl':
                    pass
                    for j in i:
                        pass

                x=str(trade[i])

                for k in str(trade[i]):
                    if k in "[(''":
                        x=x.replace(k, '')
                    if k in ")]":
                        x=x.replace(k, ' \n')
                    if k == ",":
                        x=x.replace(k, '')
                
                x, sep, end = x.partition('average')

                x=x.replace('AutoOrderedDict', '\n')

                def findWord(w):
                    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
                
                print(findWord("won")(x))

                x=x.replace('open', '\nOpen')
                x=x.replace('total', 'Total')
                x=x.replace('closed', '\nClosed')
                x=x.replace('longest', '\nLongest')
                x=x.replace('current', 'Current')
                x=x.replace('won', 'Won:\n')
                x=x.replace('lost', 'Lost:\n')
                x=x.replace('pnl', '\n\nPNL')

                title_trade = f"{str(i).upper()}\n"
                st.write(title_trade ,x)

    st.write('')
    st.subheader(f"{ticker}'s total returns are {returns}% with a {annual_return}% APY")
    #final_value=round(returns, 2)

    st.write(f'Initial investment: {cash}')
    st.write(f'Final money: {final_value}')
    st.write(stratdd[0].analyzers.sr.get_analysis())

    #st.write(stats)
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
    {'icon': "bi bi-laptop", 'label':"Screener"},
    {'icon': "far fa-copy", 'label':"Fundamental analysis"},
    #{'icon': "fa-solid fa-radar",'label':"Dropdown1   ", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
    {'icon': "far fa-chart-bar", 'label':"Technical Indicators"},#no tooltip message
    #{'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar   "},
    #{'icon': "fas fa-tachometer-alt", 'label':"Dashboard   ",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
    {'icon': "fas fa-tachometer-alt", 'label':"Backtesting"},
    #{'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
    {'icon': "bi bi-pie-chart", 'label':"Portfolio Optimizer"},
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
        pass
        #st.header('Fundamental Analysis')
        #st.write('Blah')
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
#st.write('''**Utilize these features by using the sidebar by opening the menu on mobile.**\n''')
if dashboard=='Screener':
    start_date = st.sidebar.date_input("Start date", date(2019, 1, 1))
    end_date = st.sidebar.date_input("End date", date(2021, 1, 31))

    # Retrieving tickers data
    ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
    tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
    tickerData = yf.Ticker(tickerSymbol) # Get ticker data
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

    # Ticker information
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)

    string_summary = tickerData.info['longBusinessSummary']
    st.info(string_summary)

    sector=tickerData.info['sector']
    st.subheader(f"Sector: {sector}")
    # Ticker data
    st.header('**Ticker data**')
    st.write(tickerDf)

    # Bollinger bands
    st.header('**Bollinger Bands**')
    qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
    qf.add_bollinger_bands()
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)
if dashboard=='Portfolio Optimizer':
    s = Screener()
    tickers_strings = ''
    count=0
    sectordict={}
    sectornames=['Individual Stocks', 'Technology', 'Utilities', 'Real Estate', 'Healthcare', 'Energy', 'Industrials', 'Materials', 'Communication Services', 'Financial Services', 'Consumer Defensive', 'Cryptocurrency']
    sectors=['ms_technology', 'ms_utilities', 'ms_real_estate', 'ms_healthcare', 'ms_energy', 'ms_industrials', 'ms_basic_materials', 'ms_communication_services','ms_financial_services','ms_consumer_defensive', 'all_cryptocurrencies_us',]
    portfolioinp=['Individual Stocks','ms_technology', 'ms_utilities', 'ms_real_estate', 'ms_healthcare', 'ms_energy', 'ms_industrials', 'ms_basic_materials', 'ms_communication_services','ms_financial_services','ms_consumer_defensive', 'all_cryptocurrencies_us']
    for i in range(len(sectornames)):
        sectordict[sectornames[i]]=portfolioinp[i]

    yf.pdr_override()
    def plot_cum_returns(data, title):    
        daily_cum_returns = 1 + data.dropna().pct_change()
        daily_cum_returns = daily_cum_returns.cumprod()*100
        fig = px.line(daily_cum_returns, title=title)
        return fig
        
    def plot_efficient_frontier_and_max_sharpe(mu, S): 
        # Optimize portfolio for max Sharpe ratio and plot it out with efficient frontier curve
        ef = EfficientFrontier(mu, S)
        fig, ax = plt.subplots(figsize=(6,4))
        ef_max_sharpe = copy.deepcopy(ef)
        plotting.plot_efficient_frontier(ef, ax=ax, show_assets=False)
        # Find the max sharpe portfolio
        ef_max_sharpe.max_sharpe(risk_free_rate=0.02)
        ret_tangent, std_tangent, _ = ef_max_sharpe.portfolio_performance()
        ax.scatter(std_tangent, ret_tangent, marker="*", s=100, c="r", label="Max Sharpe")
        # Generate random portfolios
        n_samples = 1000
        w = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
        rets = w.dot(ef.expected_returns)
        stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
        sharpes = rets / stds
        ax.scatter(stds, rets, marker=".", c=sharpes, cmap="viridis_r")
        # Output
        ax.legend()
        return fig


    st.header("Mean-variance Stock Portfolio Optimizer")

    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("Start Date",datetime(2015, 1, 1))
        
    with col2:
        end_date = st.date_input("End Date") # it defaults to current date
    with col3:
        sectorinp=st.selectbox(label='Select a sector', options=sectornames, index=0)
    data = s.get_screeners(sectors,  count=15)
    for i in sectors:
        if i==sectordict[sectorinp]:
            df=pd.DataFrame(data[i]['quotes'])
            tickers=df['symbol']
            for j in tickers:
                if count!=0:
                    tickers_strings = tickers_strings+','+j
                else:
                    tickers_strings = tickers_strings+j
                count=count+1
        else:
            pass
    if sectorinp=='Individual Stocks':
        tickers_string = st.text_input('Enter all stock tickers to be included in portfolio separated by commas \
                                    WITHOUT spaces, e.g. "MA,FB,V,AMZN,JPM,BA"', '').upper()
    else:
        tickers_string = st.text_input('Enter all stock tickers to be included in portfolio separated by commas \
                                    WITHOUT spaces, e.g. "MA,FB,V,AMZN,JPM,BA"', value=tickers_strings).upper()
    tickers = tickers_string.split(',')
    try:
        # Get Stock Prices using pandas_datareader Library	
        stocks_df = pdr.get_data_yahoo(tickers, start = start_date, end = end_date)['Adj Close']
        sp500=pdr.get_data_yahoo('SPY', start = start_date, end = end_date)['Adj Close']
            # Plot Individual Stock Prices
        fig_price = px.line(stocks_df, title='')
            # Plot Individual Cumulative Returns
        fig_cum_returns = plot_cum_returns(stocks_df, '')
            # Calculatge and Plot Correlation Matrix between Stocks
        corr_df = stocks_df.corr().round(2)
        fig_corr = px.imshow(corr_df, text_auto=True)
            # Calculate expected returns and sample covariance matrix for portfolio optimization later
        mu = expected_returns.mean_historical_return(stocks_df)
        S = risk_models.sample_cov(stocks_df)
            # Plot efficient frontier curve
        fig = plot_efficient_frontier_and_max_sharpe(mu, S)
        fig_efficient_frontier = BytesIO()
        fig.savefig(fig_efficient_frontier, format="png")
            # Get optimized weights
        ef = EfficientFrontier(mu, S)
        ef.add_objective(objective_functions.L2_reg, gamma=0.1)
        ef.max_sharpe(risk_free_rate=0.02)
        weights = ef.clean_weights()
        expected_annual_return, annual_volatility, sharpe_ratio = ef.portfolio_performance()
        weights_df = pd.DataFrame.from_dict(weights, orient = 'index')
        weights_df.columns = ['weights']  
            # Calculate returns of portfolio with optimized weights
        stocks_df['Optimized Portfolio'] = 0
        for ticker, weight in weights.items():
                stocks_df['Optimized Portfolio'] += stocks_df[ticker]*weight
            
            # Plot Cumulative Returns of Optimized Portfolio
        fig_cum_returns_optimized = plot_cum_returns(stocks_df['Optimized Portfolio'], 'Cumulative Returns of Optimized Portfolio Starting with $100')
        latest_prices = get_latest_prices(stocks_df)
        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=100000)
        allocation, leftover = da.greedy_portfolio()
        print(allocation, leftover)
                # Display everything on Streamlit
        st.subheader("Your Portfolio Consists of: {} Stocks".format(tickers_string))
        col1,col2=st.columns([1.3,1])
        with col1:
            st.plotly_chart(fig_cum_returns_optimized, use_container_width=True)
        with col2:
            st.write('')	
            st.write('')	
            st.subheader('\tStock Prices')
            st.write(stocks_df)
        st.write('___________________________')
        col1,col2, stats=st.columns([0.5,1.3, 0.7])   
        with col1: 
            st.write('')
            st.write('')
            st.write('')
            st.subheader("Max Sharpe Portfolio Weights")
            st.dataframe(weights_df)
        with col2:
            st.write('')
            st.write('')
            stock_tickers=[]
            weightage=[]
            for i in weights:
                if weights[i]!=0:
                    stock_tickers.append(i)
                    weightage.append(weights[i])
            fig_pie = go.Figure(
                go.Pie(
                labels =stock_tickers,
                values = weightage,
                hoverinfo = "label+percent",
                textinfo = "value"
                ))
            holdings='''
            <style>
            .holding{
                float: center;
                font-weight: 600;
                font-size: 35px;
                font-family: arial;
            }
            </style>
            <body>
            <center><p1 class='holding'> Optimized Portfolio Holdings </p1></center>
            </body>
            '''
            st.markdown(holdings, unsafe_allow_html=True)
            st.plotly_chart(fig_pie)
        with stats:
            st.subheader('Expected annual return: {}%'.format((expected_annual_return*100).round(2)))
            st.write('___________')
            st.subheader('Annual volatility: {}%'.format((annual_volatility*100).round(2)))
            st.write('___________')
            st.subheader('Sharpe Ratio: {}'.format(sharpe_ratio.round(2)))
            st.write('___________')
            st.subheader('''Discrete allocation: 
            {}'''.format(allocation))
            st.write('___________')
            st.subheader("Funds remaining: ${:.2f}".format(leftover))
        st.write('___________________________')
        col1, col2=st.columns(2)
        with col1:
            st.subheader("Optimized Max Sharpe Portfolio Performance")
            st.image(fig_efficient_frontier)
        with col2:
            st.subheader("Correlation between stocks")
            st.plotly_chart(fig_corr) # fig_corr is not a plotly chart
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Price of Individual Stocks')
            st.plotly_chart(fig_price)
        with col2:
            st.subheader('Cumulative Returns of Stocks Starting with $100')
            st.plotly_chart(fig_cum_returns)	
    except:
        st.write('Enter correct stock tickers to be included in portfolio separated\
        by commas WITHOUT spaces, e.g. "MA,FB,V,AMZN,JPM,BA"and hit Enter.')
        
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
if dashboard=='Fundamental analysis':
    s_fundament=st.sidebar.selectbox('What would you like to do?', ('Learn', 'Check fundamentals'), 0, key='fundamentals')
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
