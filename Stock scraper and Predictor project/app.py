from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo
import datetime

app = Flask(__name__)

def scrape_stock_price(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    #history = f"https://finance.yahoo.com/quote/{symbol}/history/" - This link is currently undergoing maintenance. Its purpose is to retrieve historical stock price data, which will be used for our graph and AI model. Changes will be made and implemented once it is back online.
    
    response = requests.get(url)
    #response2 = requests.get(history)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        #soup2 = BeautifulSoup(response2.text, 'html.parser')
        
        try:
            price = float(soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text.replace(',', ''))
            change = soup.find('fin-streamer', {'data-field': 'regularMarketChange'}).text
            change_value = float(change[1:].replace(',', '')) if change.startswith('+') or change.startswith('-') else float(change.replace(',', ''))
            percent = (change_value / float(price)) * 100 if price > 0 else 0
            prev_close = float(soup.find('fin-streamer', {'data-field': 'regularMarketPreviousClose'}).text.replace(',', ''))
            market_val = soup.find('fin-streamer', {'data-field': 'marketCap'}).text
            news = soup.find('h3', class_="clamp").text
            news_time = soup.find('div', class_="publishing").text
            links = soup.find_all('a', class_='subtle-link')
            company_url = links[0]['href'] if links else "No valid company link found."
            news_link = links[4]['href'] if len(links) > 4 else "No valid news link found."
            
            # The previous data is hard-coded; however, once the link is operational again, we will insert this data into the lists to enable the AI to make accurate predictions for tomorrow's price
            # The more data the AI is trained on, the higher its accuracy will be. 
            Previous_data = {
                'Previous Close': [182.00, 189.00, 176.00, 220.50, 212.11],
                'Open Price': [180.50, 181.50, 188.50, 173.50, 221.50]
            }
            
            predicted_price = ai_price_prediction(prev_close, Previous_data)
            generate_price_graph(symbol, Previous_data, price, predicted_price)  # Pass predicted price to the graph generation

            return {
                'symbol': symbol,
                'price': price,
                'change': f"{change[0]}${change[1:]}",
                'percent': f"{change[0]}{percent:.2f}%",
                'prev_close': prev_close,
                'market_val': market_val,
                'news': news,
                'news_time': news_time,
                'company_url': company_url,
                'news_link': news_link,
                'predicted_price': f"{predicted_price:.2f}",
                'error': None
            }
        except AttributeError:
            return {'error': "Could not retrieve data. Please check the stock symbol."}
    else:
        return {'error': f"Failed to retrieve data for {symbol}. Status code: {response.status_code}"}

# Linear linear regression model.
def ai_price_prediction(prev_close, Previous_data):
    df = pd.DataFrame(Previous_data)
    X = df[['Previous Close']]
    y = df['Open Price']
    model = LinearRegression()
    model.fit(X, y)
    input_data = pd.DataFrame({'Previous Close': [prev_close]})
    predicted_price = model.predict(input_data)[0]
    return predicted_price 

# Price Graph
def generate_price_graph(symbol, Previous_data, current_price, predicted_price):
    x = datetime.datetime.now()
    dates = pd.date_range(start=f"{x.year}-{x.month}-{x.day - 4}", periods=5)
    
    # Prepare historical prices with the current price as the last element
    historical_prices = Previous_data['Previous Close'] + [current_price]  # Append the current price
   

    # Prepare predicted prices for the next day
    next_day_price = predicted_price  # Predicted price is already calculated for next day
    next_day_date = x + datetime.timedelta(days=1)  # Next day

    fig = go.Figure()
    
    # Historical prices
    fig.add_trace(go.Scatter(
        x=dates,
        y=historical_prices[:-1],  # Exclude current price from historical
        mode='lines+markers',
        name='Historical Price',
        line=dict(color='royalblue', width=2),
        marker=dict(size=8)
    ))

    # Current price line
    fig.add_trace(go.Scatter(
        x=[dates[-1], x],  # Line from last historical date to current date
        y=[historical_prices[-2], current_price],
        mode='lines',
        name='Current Price Line',
        line=dict(color='green', dash='dash')
    ))

    # Current price marker
    fig.add_trace(go.Scatter(
        x=[x],  # Current date
        y=[current_price],
        mode='markers+text',
        name='Current Price',
        marker=dict(color='green', size=12, symbol='cross'),
        text=['Current Price'],
        textposition='top center'
    ))

    # Next day's predicted price
    fig.add_trace(go.Scatter(
        x=[next_day_date],  # Next day date
        y=[next_day_price],
        mode='markers+text',
        name='Predicted Price for Next Day',
        marker=dict(color='orange', size=12, symbol='diamond'),
        text=[f'Predicted: {next_day_price:.2f}'],
        textposition='top center'
    ))


    fig.update_layout(
        title=f'Stock Price History for {symbol}',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        legend=dict(x=0, y=1),
        hovermode='x unified',
        template='plotly_white'
    )

    plot_file = f'static/{symbol}_price_graph.html'
    pyo.plot(fig, filename=plot_file, auto_open=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_info = {}
    if request.method == 'POST':
        symbol = request.form['symbol']
        stock_info = scrape_stock_price(symbol)
    return render_template('index.html', stock_info=stock_info)

if __name__ == '__main__':
    app.run(debug=True)
