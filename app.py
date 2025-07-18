import streamlit as st
import pandas as pd
from utils.auth import authenticate_user, register_user, logout_user
from utils.financial_data import get_market_overview
from utils.database_setup import initialize_database
import plotly.graph_objects as go
import plotly.express as px

# Load custom CSS
def load_css():
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def add_dynamic_css():
    st.markdown("""
    <style>
    /* Dynamic background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Enhanced sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Navigation buttons with icons */
    .nav-btn {
        display: flex;
        align-items: center;
        padding: 12px 20px;
        margin: 8px 0;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        text-decoration: none;
        width: 100%;
        justify-content: flex-start;
    }
    
    .nav-btn:hover {
        background: linear-gradient(45deg, #5a67d8, #6b46c1);
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(90, 103, 216, 0.4);
    }
    
    .nav-btn-icon {
        margin-right: 10px;
        font-size: 1.2em;
    }
    
    /* Main content cards */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Animated metrics */
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e4e7;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        border: none;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 12px 24px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #5a67d8, #6b46c1);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(90, 103, 216, 0.4);
    }
    
    /* Welcome section */
    .welcome-section {
        text-align: center;
        padding: 40px 0;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
    }
    
    .welcome-title {
        font-size: 3em;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    .feature-icon {
        font-size: 2em;
        margin-bottom: 10px;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    </style>
    """, unsafe_allow_html=True)

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
    # Apply custom CSS
    add_dynamic_css()
    
    st.markdown("""
    <div class="welcome-section">
        <div class="welcome-title">💰 Smart Financial Assistant</div>
        <p style="color: white; font-size: 1.2em; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
            Your intelligent financial companion powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights with animated icons
    st.markdown("""
    <div class="main-card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0;">
            <div style="text-align: center;">
                <div class="feature-icon">📊</div>
                <h4>Portfolio Tracking</h4>
                <p>Track your investments with real-time data and beautiful visualizations</p>
            </div>
            <div style="text-align: center;">
                <div class="feature-icon">🤖</div>
                <h4>AI-Powered Insights</h4>
                <p>Get personalized recommendations from our advanced AI assistant</p>
            </div>
            <div style="text-align: center;">
                <div class="feature-icon">⏰</div>
                <h4>Smart Reminders</h4>
                <p>Never miss important financial deadlines and investment opportunities</p>
            </div>
            <div style="text-align: center;">
                <div class="feature-icon">🎯</div>
                <h4>Goal Setting</h4>
                <p>Set and track your financial goals with intelligent guidance</p>
            </div>
            <div style="text-align: center;">
                <div class="feature-icon">📈</div>
                <h4>Market Analysis</h4>
                <p>Stay ahead with comprehensive market trends and analysis</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="main-card">
            <h3 style="text-align: center; margin-bottom: 20px;">🔐 Login</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            login_username = st.text_input("Username", placeholder="Enter your username")
            login_password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if login_submit:
                if authenticate_user(login_username, login_password):
                    st.session_state.authenticated = True
                    st.session_state.username = login_username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
    
    with col2:
        st.markdown("""
        <div class="main-card">
            <h3 style="text-align: center; margin-bottom: 20px;">📝 Sign Up</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form"):
            signup_username = st.text_input("Choose Username", placeholder="Create a unique username")
            signup_email = st.text_input("Email", placeholder="your.email@example.com")
            signup_password = st.text_input("Choose Password", type="password", placeholder="Create a strong password")
            signup_submit = st.form_submit_button("🎯 Sign Up", use_container_width=True)
            
            if signup_submit:
                if register_user(signup_username, signup_email, signup_password):
                    st.success("✅ Registration successful! Please login.")
                else:
                    st.error("❌ Username already exists")

def show_main_dashboard():
    """Display the main dashboard for authenticated users"""
    # Apply custom CSS
    add_dynamic_css()
    
    # Enhanced welcome header
    st.markdown(f"""
    <div class="main-card">
        <h1 style="text-align: center; margin-bottom: 10px;">
            <span class="gradient-text">Welcome back, {st.session_state.username}!</span> 
            <span style="font-size: 0.8em;">👋</span>
        </h1>
        <p style="text-align: center; color: #666; font-size: 1.1em;">
            Your financial dashboard is ready to help you succeed
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar navigation
    with st.sidebar:
        # Logo section
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(45deg, #667eea, #764ba2); 
                    border-radius: 15px; margin-bottom: 25px; color: white;">
            <h2 style="margin: 0; font-weight: bold;">💰 FinAssist</h2>
            <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.9;">Smart Financial AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons with enhanced styling
        st.markdown("""
        <div style="margin: 15px 0;">
        """, unsafe_allow_html=True)
        
        nav_buttons = [
            ("🏠", "Dashboard", "app.py"),
            ("📊", "Portfolio", "pages/1_Dashboard.py"),
            ("🤖", "AI Assistant", "pages/2_AI_Assistant.py"),
            ("⚙️", "Preferences", "pages/3_User_Preferences.py"),
            ("⏰", "Reminders", "pages/4_Reminders.py"),
            ("💡", "Insights", "pages/5_Insights.py")
        ]
        
        for icon, label, page in nav_buttons:
            if st.button(f"{icon} {label}", use_container_width=True, key=f"nav_{label}"):
                st.switch_page(page)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # User info section
        st.markdown(f"""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 10px; 
                    margin: 20px 0; text-align: center;">
            <p style="margin: 0; font-size: 0.9em; color: #666;">Logged in as</p>
            <p style="margin: 5px 0 0 0; font-weight: bold; color: #667eea;">{st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()
    
    # Enhanced metrics with animations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="main-card" style="text-align: center;">
            <div style="font-size: 1.1em; color: #666; margin-bottom: 10px;">Portfolio Value</div>
            <div class="metric-value">$125,430</div>
            <div style="color: #4caf50; font-weight: bold; font-size: 1.1em;">
                ↗️ $2,450 (2.0%)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="main-card" style="text-align: center;">
            <div style="font-size: 1.1em; color: #666; margin-bottom: 10px;">Today's Change</div>
            <div class="metric-value">$1,250</div>
            <div style="color: #4caf50; font-weight: bold; font-size: 1.1em;">
                📈 +1.2%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="main-card" style="text-align: center;">
            <div style="font-size: 1.1em; color: #666; margin-bottom: 10px;">Total Return</div>
            <div class="metric-value">$15,430</div>
            <div style="color: #4caf50; font-weight: bold; font-size: 1.1em;">
                🚀 +14.1%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Overview with enhanced styling
    st.markdown("""
    <div class="main-card">
        <h2 style="text-align: center; margin-bottom: 30px;">
            <span class="gradient-text">📈 Market Overview</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        market_data = get_market_overview()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Create a sample chart for market indices
            indices = ['S&P 500', 'NASDAQ', 'DOW', 'Russell 2000']
            changes = [0.8, 1.2, 0.6, -0.3]
            
            fig = px.bar(
                x=indices,
                y=changes,
                title="Major Indices Performance (%)",
                color=changes,
                color_continuous_scale=['#ff6b6b', '#4ecdc4']
            )
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#333'),
                title_font=dict(size=16, color='#667eea')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Portfolio allocation pie chart
            labels = ['Stocks', 'Bonds', 'ETFs', 'Cash']
            values = [60, 25, 12, 3]
            colors = ['#667eea', '#764ba2', '#4ecdc4', '#45b7d1']
            
            fig = px.pie(
                values=values,
                names=labels,
                title="Portfolio Allocation",
                color_discrete_sequence=colors
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#333'),
                title_font=dict(size=16, color='#667eea')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.markdown(f"""
        <div class="notification-error">
            <strong>⚠️ Error loading market data:</strong> {str(e)}
        </div>
        <div class="notification-warning">
            <strong>💡 Tip:</strong> Please check your internet connection and try again.
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Quick Actions
    st.markdown("""
    <div class="main-card">
        <h2 style="text-align: center; margin-bottom: 30px;">
            <span class="gradient-text">🚀 Quick Actions</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    action_buttons = [
        ("📊", "View Portfolio", "Detailed portfolio analysis", "pages/1_Dashboard.py"),
        ("🤖", "Ask AI", "Get personalized advice", "pages/2_AI_Assistant.py"),
        ("⏰", "Set Reminder", "Manage financial tasks", "pages/4_Reminders.py"),
        ("💡", "Get Insights", "AI-powered recommendations", "pages/5_Insights.py")
    ]
    
    for i, (icon, title, desc, page) in enumerate(action_buttons):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="main-card" style="text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 3em; margin-bottom: 10px;">{icon}</div>
                <h4 style="margin: 10px 0; color: #667eea;">{title}</h4>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Go to {title}", use_container_width=True, key=f"action_{i}"):
                st.switch_page(page)

# Initialize database on app startup
@st.cache_resource
def init_db():
    """Initialize database with caching to avoid repeated initialization"""
    return initialize_database()

# Initialize database
init_db()

# Main application logic
if not st.session_state.authenticated:
    show_landing_page()
else:
    show_main_dashboard()
