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

# Enhanced CSS styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}

.main-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 10px 40px rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.metric-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    border: 1px solid rgba(255, 255, 255, 0.18);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-align: center;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 48px rgba(31, 38, 135, 0.5);
}

.gradient-text {
    background: linear-gradient(45deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: bold;
}

.chart-container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-card">
    <h1 style="text-align: center; margin-bottom: 20px;">
        <span class="gradient-text">📊 Portfolio Dashboard</span>
    </h1>
    <p style="text-align: center; color: #666; font-size: 1.1em;">
        Track your investments and monitor performance in real-time
    </p>
</div>
""", unsafe_allow_html=True)

# Import UI components
from utils.ui_components import add_enhanced_sidebar, add_page_css

# Add consistent styling and sidebar
add_page_css()
add_enhanced_sidebar()

# Portfolio filters in sidebar
with st.sidebar:
    st.markdown("---")
    st.subheader("📊 Portfolio Filters")
    time_period = st.selectbox("Time Period", ["1D", "5D", "1M", "3M", "6M", "1Y", "5Y"])
    view_type = st.selectbox("View Type", ["Holdings", "Performance", "Allocation"])

# Enhanced metrics with animations
col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("Total Portfolio Value", "$125,430.50", "+$2,450.30 (2.0%)", "#4caf50"),
    ("Today's P&L", "$1,250.75", "+1.2%", "#4caf50"),
    ("Total Return", "$15,430.50", "+14.1%", "#4caf50"),
    ("Cash Available", "$5,680.25", "", "#2196f3")
]

for i, (label, value, delta, color) in enumerate(metrics):
    with [col1, col2, col3, col4][i]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9em; color: #666; margin-bottom: 8px;">{label}</div>
            <div style="font-size: 1.8em; font-weight: bold; color: #333; margin-bottom: 5px;">{value}</div>
            <div style="color: {color}; font-weight: bold; font-size: 0.9em;">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

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
    
    styled_df = holdings_df.style.map(color_pnl, subset=['P&L', '% Change'])
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
