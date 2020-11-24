import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import cbpro
import plotly.figure_factory as ff
import plotly.graph_objects as go

public_client = cbpro.PublicClient()

st.write("""
# Simple App to Show Crypto Trading Info

Here is what the application shows:

- 24 hour stats for the selected coins(s)
- the order book for the selected coin(s)
- the ticker for the selected coin(s)
""")

expander = st.beta_expander("Guide")
expander.write("""
to use the application open the sidebar to the left (if not already open)

then do the following:

- select coin(s) you would like data for
- select the currency you wish to use

That's it!
""")

coins = st.sidebar.multiselect('Check the cryptos you want to watch', ['BTC', 'ETH', 'ETC', 'XRP'])
currency = st.sidebar.selectbox('Choose a currency', ['USD', 'EUR', 'GBP'])

# format_string = coin_symbol + '-' + currency

# append the currency to each coin in the list
for i in range(len(coins)):
    coins[i] = coins[i] + '-' + currency

# create a list to store all the stats from multi coins
daily_stats_list = []
product_order_book_list = []
product_ticker_list = []

# populate the list
for coin in coins:
    daily_stats = public_client.get_product_24hr_stats(coin)
    daily_stats_list.append(daily_stats)

    order_book = public_client.get_product_order_book(coin, level=1)
    product_order_book_list.append(order_book)

    product_ticker = public_client.get_product_ticker(product_id=coin)
    product_ticker_list.append(product_ticker)

# now combine the dictionary values into one dict
collective_24hr_dict = {}
if len(daily_stats_list) != 0:
    for k in daily_stats_list[0]:
        collective_24hr_dict[k] = [d[k] for d in daily_stats_list]

# create dataframe fo 24hr stats on coin(s)
df_for_daily_stats = pd.DataFrame(collective_24hr_dict)

# combine the dictionary values for order book into one dict
collective_order_book_dict = {}
if len(product_order_book_list) != 0:
    for k in product_order_book_list[0]:
        collective_order_book_dict[k] = [d[k] for d in product_order_book_list]

# create dataframe for order book on coin(s)
df_for_order_book = pd.DataFrame(collective_order_book_dict)

# combine the dictionary values for ticker info into one dict
collective_ticker_dict = {}
if len(product_ticker_list) != 0:
    for k in product_ticker_list[0]:
        collective_ticker_dict[k] = [d[k] for d in product_ticker_list]

# create dataframe for order book on coin(s)
df_for_product_ticker = pd.DataFrame(collective_ticker_dict)

st.write("""
## 24hr Stats:

the rows are ordered as follows:

""", coins, df_for_daily_stats)

st.write("""
## Order Book:

the rows are ordered as follows:

""", coins, df_for_order_book)

st.write("""
## Coin Ticker:

the rows are ordered as follows:

""", coins, df_for_product_ticker)

st.date_input('enter a date')

default_date = dt.date.today()
default_beg_date = default_date - dt.timedelta(days=30)

date_list = []
date_list.append(default_date)

increment_date = default_date
while increment_date != default_beg_date:
    increment_date -= dt.timedelta(days=1)
    date_list.append(increment_date)

print(date_list)

historic_data = public_client.get_product_historic_rates('ETH-USD', default_beg_date, default_date, 86400)
df_for_historic_data = pd.DataFrame(historic_data)

fig = go.FigureWidget(data=[go.Candlestick(x=date_list,
                low=df_for_historic_data[1],
                high=df_for_historic_data[2],
                open=df_for_historic_data[3],
                close=df_for_historic_data[4])])

fig.update_layout(
    title='ETH-USD stock price',
    yaxis_title='ETH-USD price'
)

st.write(historic_data)
st.plotly_chart(fig)
# st.write(df_for_historic_data)