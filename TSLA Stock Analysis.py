#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Libraries needed
import os
import numpy as np
import pandas as pd

#All necessary plotly libraries
import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# In[3]:


df = pd.read_csv("Desktop/TSLA-2.csv")
df.head()


# In[5]:


df['Date'] = pd.to_datetime(df['Date'])
df.index = range(len(df))
df.head()


# In[6]:


#Creating time series plot
fig = go.Figure([go.Scatter(x=df['Date'], y=df['Close'])])
fig.show()


# In[8]:


fig = go.Figure()
fig.add_trace(go.Bar(x=df['Date'], y=df['Volume']))


# In[9]:


#candlestick plot
fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.show()


# In[10]:


#OHLC plots
fig = make_subplots(rows=2, cols=1)

fig.add_trace(go.Ohlc(x=df.Date, open=df.Open, high=df.High, low=df.Low, close=df.Close, name='Price'), row=1, col=1)
#Volume PLot
fig.add_trace(go.Scatter(x=df.Date, y=df.Volume, name='Volume'), row=2, col=1)

fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()


# In[11]:


fig = go.Figure(data=go.Ohlc(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']))

fig.update_layout(
    title='The BOOM',
    yaxis_title='TSLA Stock',
    shapes = [dict(x0='2019-10-10', x1='2019-10-10', y0=0, y1=1, xref='x', yref='paper',line_width=3)],
    annotations=[dict(x='2019-10-10', y=0.05, xref='x', yref='paper', xanchor='left', text='The Boom in TSLA Stock')]
)

fig.show()


# In[12]:


#EMA
df['EMA_9'] = df['Close'].ewm(9).mean().shift()
df['EMA_22'] = df['Close'].ewm(22).mean().shift()
#SMA
df['SMA_5'] = df['Close'].rolling(5).mean().shift()
df['SMA_10'] = df['Close'].rolling(10).mean().shift()
df['SMA_15'] = df['Close'].rolling(15).mean().shift()
df['SMA_30'] = df['Close'].rolling(30).mean().shift()
#RSI14
def RSI(df, n=14):
    close = df['Close']
    delta = close.diff()
    delta = delta[1:]
    pricesUp = delta.copy()
    pricesDown = delta.copy()
    pricesUp[pricesUp < 0] = 0
    pricesDown[pricesDown > 0] = 0
    rollUp = pricesUp.rolling(n).mean()
    rollDown = pricesDown.abs().rolling(n).mean()
    rs = rollUp / rollDown
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi

df['RSI'] = RSI(df).fillna(0)

EMA_12 = pd.Series(df['Close'].ewm(span=12, min_periods=12).mean())
EMA_26 = pd.Series(df['Close'].ewm(span=26, min_periods=26).mean())
df['MACD'] = pd.Series(EMA_12 - EMA_26)
df['MACD_signal'] = pd.Series(df.MACD.ewm(span=9, min_periods=9).mean())


# In[13]:


fig = go.Figure()
fig.add_trace(go.Scatter(x=df.Date, y=df.EMA_9, name='EMA 9'))
fig.add_trace(go.Scatter(x=df.Date, y=df.EMA_22, name='EMA 22'))
fig.add_trace(go.Scatter(x=df.Date, y=df.SMA_5, name='SMA 5'))
fig.add_trace(go.Scatter(x=df.Date, y=df.SMA_10, name='SMA 10'))
fig.add_trace(go.Scatter(x=df.Date, y=df.SMA_15, name='SMA 15'))
fig.add_trace(go.Scatter(x=df.Date, y=df.SMA_30, name='SMA 30'))
fig.add_trace(go.Scatter(x=df.Date, y=df.Close, name='Close', opacity=0.3))
fig.show()


# In[14]:


fig = go.Figure(go.Scatter(x=df.Date, y=df.RSI, name='RSI'))
fig.show()


# In[16]:


fig = make_subplots(rows=2, cols=1)
fig.add_trace(go.Scatter(x=df.Date, y=df.Close, name='Close'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.Date, y=EMA_12, name='EMA 12'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.Date, y=EMA_26, name='EMA 26'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.Date, y=df['MACD'], name='MACD'), row=2, col=1)
fig.add_trace(go.Scatter(x=df.Date, y=df['MACD_signal'], name='Signal line'), row=2, col=1)
fig.show()


# In[17]:


fig = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = ["relative", "relative", "total", "relative", "relative", "total"],
    x = ["Sales", "Royalties", "Net revenue", "Purchases", "Other expenses", "Profit before tax"],
    textposition = "outside",
    text = ["+1000", "+800", "", "-400", "-200", "Total"],
    y = [1000, 800, 0, -400, -200, 0],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))


fig.update_layout(
        title = "Profit and Loss",
        showlegend = True
)

fig.show()


# In[18]:


#Example of this very notebook ;)
data = dict(
    number=[880, 34, 22, 17],
    stage=["Notebook views", "Upvotes", "Comments", "Forks"])
fig = px.funnel(data, x='number', y='stage')
fig.show()


# In[19]:


labels = ['Asia','Australia','North America','Europe']
values = [3500, 4500, 1050, 500]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                             insidetextorientation='radial'
                            )])
fig.show()


# In[20]:


labels = ['Asia','Australia','North America','Europe']
values = [3500, 4500, 1050, 500]

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.show()


# In[ ]:




