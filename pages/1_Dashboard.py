import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.financial_data import get_portfolio_data, get_stock_data
from utils.auth import check_authentication
import yfinance as yf
from datetime import datetime, timedelta

# Check authentication
check_authentication()

st.set_page_config(
    page_title="Portfolio Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Portfolio Dashboard")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=FinAssist", width=150)
    st.markdown("---")
    
    # Portfolio filters
    st.subheader("Portfolio Filters")
    time_period = st.selectbox("Time Period", ["1D", "5D", "1M", "3M", "6M", "1Y", "5Y"])
    view_type = st.selectbox("View Type", ["Holdings", "Performance", "Allocation"])

# Main content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Portfolio Value", "$125,430.50", "+$2,450.30 (2.0%)")

with col2:
    st.metric("Today's P&L", "$1,250.75", "+1.2%")

with col3:
    st.metric("Total Return", "$15,430.50", "+14.1%")

with col4:
    st.metric("Cash Available", "$5,680.25", "")

st.markdown("---")

# Portfolio Performance Chart
st.subheader("📈 Portfolio Performance")

try:
    # Get portfolio performance data
    portfolio_data = get_portfolio_data(st.session_state.username, time_period)
    
    if not portfolio_data.empty:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=portfolio_data['Date'],
            y=portfolio_data['Portfolio_Value'],
            mode='lines',
            name='Portfolio Value',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig.update_layout(
            title="Portfolio Value Over Time",
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No portfolio data available. Add some holdings to see performance.")

except Exception as e:
    st.error(f"Error loading portfolio data: {str(e)}")
    
    # Fallback: Show sample data structure
    st.info("Unable to load real portfolio data. Please check your API connections.")

# Holdings Table
st.subheader("📋 Current Holdings")

try:
    # Sample holdings data - in a real app, this would come from the database
    holdings_data = [
        {"Symbol": "AAPL", "Company": "Apple Inc.", "Shares": 50, "Current Price": "$150.25", "Market Value": "$7,512.50", "P&L": "+$512.50", "% Change": "+7.3%"},
        {"Symbol": "GOOGL", "Company": "Alphabet Inc.", "Shares": 25, "Current Price": "$2,750.80", "Market Value": "$68,770.00", "P&L": "+$2,770.00", "% Change": "+4.2%"},
        {"Symbol": "MSFT", "Company": "Microsoft Corp.", "Shares": 75, "Current Price": "$305.15", "Market Value": "$22,886.25", "P&L": "+$1,386.25", "% Change": "+6.4%"},
        {"Symbol": "TSLA", "Company": "Tesla Inc.", "Shares": 20, "Current Price": "$850.40", "Market Value": "$17,008.00", "P&L": "-$508.00", "% Change": "-2.9%"},
        {"Symbol": "AMZN", "Company": "Amazon.com Inc.", "Shares": 15, "Current Price": "$180.75", "Market Value": "$2,711.25", "P&L": "+$211.25", "% Change": "+8.4%"}
    ]
    
    holdings_df = pd.DataFrame(holdings_data)
    
    # Style the dataframe
    def color_pnl(val):
        if '+' in val:
            return 'color: green'
        elif '-' in val:
            return 'color: red'
        return ''
    
    styled_df = holdings_df.style.applymap(color_pnl, subset=['P&L', '% Change'])
    st.dataframe(styled_df, use_container_width=True)
    
except Exception as e:
    st.error(f"Error loading holdings data: {str(e)}")

# Portfolio Analytics
col1, col2 = st.columns(2)

with col1:
    st.subheader("🥧 Asset Allocation")
    
    # Asset allocation pie chart
    allocation_data = {
        'Asset Class': ['Technology', 'Healthcare', 'Finance', 'Consumer Goods', 'Energy'],
        'Allocation': [35, 20, 15, 20, 10]
    }
    
    fig = px.pie(
        values=allocation_data['Allocation'],
        names=allocation_data['Asset Class'],
        title="Portfolio Allocation by Sector"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Risk Analysis")
    
    # Risk metrics
    risk_metrics = {
        'Beta': 1.15,
        'Volatility': 18.5,
        'Sharpe Ratio': 1.45,
        'Max Drawdown': -12.3
    }
    
    for metric, value in risk_metrics.items():
        if metric == 'Max Drawdown':
            st.metric(metric, f"{value}%", delta=None)
        elif metric == 'Volatility':
            st.metric(metric, f"{value}%", delta=None)
        else:
            st.metric(metric, f"{value}", delta=None)

# Stock Research Tool
st.markdown("---")
st.subheader("🔍 Stock Research Tool")

col1, col2 = st.columns([1, 3])

with col1:
    stock_symbol = st.text_input("Enter Stock Symbol", placeholder="e.g., AAPL")
    
    if st.button("Get Stock Data"):
        if stock_symbol:
            try:
                stock_data = get_stock_data(stock_symbol.upper())
                st.session_state.current_stock = stock_data
            except Exception as e:
                st.error(f"Error fetching stock data: {str(e)}")

with col2:
    if 'current_stock' in st.session_state and st.session_state.current_stock:
        stock_info = st.session_state.current_stock
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Current Price", f"${stock_info.get('current_price', 'N/A')}")
        
        with col_b:
            st.metric("Day Change", f"{stock_info.get('day_change', 'N/A')}%")
        
        with col_c:
            st.metric("Volume", f"{stock_info.get('volume', 'N/A')}")
