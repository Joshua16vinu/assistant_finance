import streamlit as st

def add_enhanced_sidebar():
    """Add enhanced sidebar navigation to all pages"""
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
        nav_buttons = [
            ("🏠", "Dashboard", "app.py"),
            ("📊", "Portfolio", "pages/1_Dashboard.py"),
            ("🤖", "AI Assistant", "pages/2_AI_Assistant.py"),
            ("⚙️", "Preferences", "pages/3_User_Preferences.py"),
            ("⏰", "Reminders", "pages/4_Reminders.py"),
            ("💡", "Insights", "pages/5_Insights.py")
        ]
        
        for icon, label, page in nav_buttons:
            if st.button(f"{icon} {label}", use_container_width=True, key=f"nav_{label}_{page}"):
                st.switch_page(page)
        
        # User info section
        if 'username' in st.session_state and st.session_state.username:
            st.markdown(f"""
            <div style="background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 10px; 
                        margin: 20px 0; text-align: center;">
                <p style="margin: 0; font-size: 0.9em; color: #666;">Logged in as</p>
                <p style="margin: 5px 0 0 0; font-weight: bold; color: #667eea;">{st.session_state.username}</p>
            </div>
            """, unsafe_allow_html=True)

def add_page_css():
    """Add consistent CSS styling across all pages"""
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

    /* Enhanced buttons */
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

    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e4e7;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }

    /* Priority indicators */
    .priority-high {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        display: inline-block;
    }

    .priority-medium {
        background: linear-gradient(45deg, #ffa726, #ff9800);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        display: inline-block;
    }

    .priority-low {
        background: linear-gradient(45deg, #66bb6a, #4caf50);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        display: inline-block;
    }

    /* Notification styling */
    .notification-success {
        background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }

    .notification-warning {
        background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }

    .notification-error {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }

    /* Animation for loading */
    .loading-pulse {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }

    .insight-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)