import streamlit as st
import pandas as pd
from utils.auth import authenticate_user, register_user, logout_user
from utils.financial_data import get_market_overview
import plotly.graph_objects as go
import plotly.express as px

# Configure the page
st.set_page_config(
    page_title="Smart Financial Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

def show_landing_page():
    """Display the landing page with authentication"""
    st.markdown("""
    # 💰 Smart Financial Assistant
    
    Welcome to your intelligent financial companion! Our AI-powered assistant helps you:
    
    - 📊 **Track your portfolio** with real-time data
    - 🤖 **Get AI-powered insights** and recommendations
    - ⏰ **Manage financial reminders** and deadlines
    - 🎯 **Set and track financial goals**
    - 📈 **Analyze market trends** and opportunities
    
    ---
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 Login")
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Login")
            
            if login_submit:
                if authenticate_user(login_username, login_password):
                    st.session_state.authenticated = True
                    st.session_state.username = login_username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with col2:
        st.subheader("📝 Sign Up")
        with st.form("signup_form"):
            signup_username = st.text_input("Choose Username")
            signup_email = st.text_input("Email")
            signup_password = st.text_input("Choose Password", type="password")
            signup_submit = st.form_submit_button("Sign Up")
            
            if signup_submit:
                if register_user(signup_username, signup_email, signup_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")

def show_main_dashboard():
    """Display the main dashboard for authenticated users"""
    st.title(f"Welcome back, {st.session_state.username}! 👋")
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=FinAssist", width=150)
        st.markdown("---")
        
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("app.py")
        if st.button("📊 Portfolio Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.switch_page("pages/2_AI_Assistant.py")
        if st.button("⚙️ Preferences", use_container_width=True):
            st.switch_page("pages/3_User_Preferences.py")
        if st.button("⏰ Reminders", use_container_width=True):
            st.switch_page("pages/4_Reminders.py")
        if st.button("💡 Insights", use_container_width=True):
            st.switch_page("pages/5_Insights.py")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
    
    # Main content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Portfolio Value",
            value="$125,430",
            delta="$2,450 (2.0%)"
        )
    
    with col2:
        st.metric(
            label="Today's Change",
            value="$1,250",
            delta="1.2%"
        )
    
    with col3:
        st.metric(
            label="Total Return",
            value="$15,430",
            delta="14.1%"
        )
    
    st.markdown("---")
    
    # Market Overview
    st.subheader("📈 Market Overview")
    
    try:
        market_data = get_market_overview()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create a sample chart for market indices
            indices = ['S&P 500', 'NASDAQ', 'DOW', 'Russell 2000']
            changes = [0.8, 1.2, 0.6, -0.3]
            
            fig = px.bar(
                x=indices,
                y=changes,
                title="Major Indices Performance (%)",
                color=changes,
                color_continuous_scale=['red', 'green']
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Portfolio allocation pie chart
            labels = ['Stocks', 'Bonds', 'ETFs', 'Cash']
            values = [60, 25, 12, 3]
            
            fig = px.pie(
                values=values,
                names=labels,
                title="Portfolio Allocation"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")
        st.info("Please check your internet connection and try again.")
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 View Portfolio", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
    
    with col2:
        if st.button("🤖 Ask AI", use_container_width=True):
            st.switch_page("pages/2_AI_Assistant.py")
    
    with col3:
        if st.button("⏰ Set Reminder", use_container_width=True):
            st.switch_page("pages/4_Reminders.py")
    
    with col4:
        if st.button("💡 Get Insights", use_container_width=True):
            st.switch_page("pages/5_Insights.py")

# Main application logic
if not st.session_state.authenticated:
    show_landing_page()
else:
    show_main_dashboard()
