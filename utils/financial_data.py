import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

def get_stock_data(symbol):
    """Get stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period="5d")
        
        if hist.empty:
            raise ValueError(f"No data found for symbol {symbol}")
        
        current_price = hist['Close'].iloc[-1]
        previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        day_change = ((current_price - previous_close) / previous_close) * 100
        
        return {
            'symbol': symbol,
            'current_price': round(current_price, 2),
            'day_change': round(day_change, 2),
            'volume': hist['Volume'].iloc[-1],
            'high_52w': round(hist['High'].max(), 2),
            'low_52w': round(hist['Low'].min(), 2),
            'company_name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A')
        }
    
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def get_market_overview():
    """Get market overview data"""
    try:
        # Major indices
        indices = {
            '^GSPC': 'S&P 500',
            '^IXIC': 'NASDAQ',
            '^DJI': 'Dow Jones',
            '^RUT': 'Russell 2000'
        }
        
        market_data = {}
        
        for symbol, name in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    day_change = ((current_price - previous_close) / previous_close) * 100
                    
                    market_data[name] = {
                        'price': round(current_price, 2),
                        'change': round(day_change, 2)
                    }
            except Exception as e:
                st.warning(f"Could not fetch data for {name}: {str(e)}")
                continue
        
        return market_data
    
    except Exception as e:
        st.error(f"Error fetching market data: {str(e)}")
        return {}

def get_portfolio_data(username, time_period="1M"):
    """Get portfolio performance data"""
    try:
        # Sample portfolio data - in a real app, this would come from database
        end_date = datetime.now()
        
        # Determine start date based on time period
        if time_period == "1D":
            start_date = end_date - timedelta(days=1)
        elif time_period == "5D":
            start_date = end_date - timedelta(days=5)
        elif time_period == "1M":
            start_date = end_date - timedelta(days=30)
        elif time_period == "3M":
            start_date = end_date - timedelta(days=90)
        elif time_period == "6M":
            start_date = end_date - timedelta(days=180)
        elif time_period == "1Y":
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Generate sample portfolio data
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Simulate portfolio performance
        np.random.seed(42)  # For consistent results
        returns = np.random.normal(0.001, 0.02, len(dates))  # Daily returns
        
        # Starting portfolio value
        initial_value = 120000
        portfolio_values = [initial_value]
        
        for return_rate in returns[1:]:
            new_value = portfolio_values[-1] * (1 + return_rate)
            portfolio_values.append(new_value)
        
        portfolio_df = pd.DataFrame({
            'Date': dates,
            'Portfolio_Value': portfolio_values
        })
        
        return portfolio_df
    
    except Exception as e:
        st.error(f"Error generating portfolio data: {str(e)}")
        return pd.DataFrame()

def get_sector_performance():
    """Get sector performance data"""
    try:
        # Sample sector ETFs
        sectors = {
            'XLK': 'Technology',
            'XLV': 'Healthcare',
            'XLF': 'Financial',
            'XLE': 'Energy',
            'XLY': 'Consumer Discretionary'
        }
        
        sector_data = {}
        
        for symbol, name in sectors.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1mo")
                
                if not hist.empty:
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    performance = ((end_price - start_price) / start_price) * 100
                    
                    sector_data[name] = round(performance, 2)
            except Exception as e:
                st.warning(f"Could not fetch data for {name}: {str(e)}")
                continue
        
        return sector_data
    
    except Exception as e:
        st.error(f"Error fetching sector data: {str(e)}")
        return {}

def calculate_portfolio_metrics(portfolio_data):
    """Calculate portfolio risk metrics"""
    try:
        if portfolio_data.empty:
            return {}
        
        # Calculate returns
        returns = portfolio_data['Portfolio_Value'].pct_change().dropna()
        
        # Calculate metrics
        metrics = {
            'total_return': ((portfolio_data['Portfolio_Value'].iloc[-1] / portfolio_data['Portfolio_Value'].iloc[0]) - 1) * 100,
            'volatility': returns.std() * np.sqrt(252) * 100,  # Annualized
            'sharpe_ratio': (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0,
            'max_drawdown': ((portfolio_data['Portfolio_Value'] / portfolio_data['Portfolio_Value'].cummax()) - 1).min() * 100
        }
        
        return {k: round(v, 2) for k, v in metrics.items()}
    
    except Exception as e:
        st.error(f"Error calculating portfolio metrics: {str(e)}")
        return {}

def get_dividend_stocks():
    """Get dividend-paying stocks data"""
    try:
        # Sample dividend stocks
        dividend_stocks = ['AAPL', 'MSFT', 'JNJ', 'PG', 'KO', 'PFE', 'VZ', 'T']
        
        dividend_data = []
        
        for symbol in dividend_stocks[:5]:  # Limit to 5 for MVP
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                dividend_yield = info.get('dividendYield', 0)
                if dividend_yield and dividend_yield > 0:
                    dividend_data.append({
                        'symbol': symbol,
                        'company': info.get('longName', symbol),
                        'dividend_yield': round(dividend_yield * 100, 2),
                        'price': round(info.get('currentPrice', 0), 2)
                    })
            except Exception as e:
                continue
        
        return dividend_data
    
    except Exception as e:
        st.error(f"Error fetching dividend data: {str(e)}")
        return []
