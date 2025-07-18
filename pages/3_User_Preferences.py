import streamlit as st
from utils.auth import check_authentication
from utils.user_preferences import save_user_preferences, get_user_preferences
import json

# Check authentication
check_authentication()

st.set_page_config(
    page_title="User Preferences",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ User Preferences")

# Load existing preferences
try:
    user_prefs = get_user_preferences(st.session_state.username)
except Exception as e:
    st.error(f"Error loading preferences: {str(e)}")
    user_prefs = {}

# Initialize session state with existing preferences
if 'preferences_updated' not in st.session_state:
    st.session_state.preferences_updated = False

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Investment Profile")
    
    # Risk Tolerance
    risk_tolerance = st.select_slider(
        "Risk Tolerance",
        options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"],
        value=user_prefs.get('risk_tolerance', 'Moderate'),
        help="How comfortable are you with potential losses in exchange for higher returns?"
    )
    
    # Investment Timeline
    investment_timeline = st.selectbox(
        "Investment Timeline",
        ["Less than 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
        index=["Less than 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"].index(
            user_prefs.get('investment_timeline', '5-10 years')
        )
    )
    
    # Investment Goals
    st.subheader("🏆 Investment Goals")
    
    investment_goals = st.multiselect(
        "Select your investment goals",
        ["Wealth Building", "Retirement Planning", "Emergency Fund", "Education Fund", 
         "Home Purchase", "Debt Reduction", "Passive Income", "Short-term Savings"],
        default=user_prefs.get('investment_goals', ['Wealth Building', 'Retirement Planning'])
    )
    
    # Monthly Investment Amount
    monthly_investment = st.number_input(
        "Monthly Investment Amount ($)",
        min_value=0,
        value=int(user_prefs.get('monthly_investment', 1000)),
        step=100
    )

with col2:
    st.subheader("📊 Asset Preferences")
    
    # Preferred Asset Classes
    preferred_assets = st.multiselect(
        "Preferred Asset Classes",
        ["Stocks", "Bonds", "ETFs", "Mutual Funds", "REITs", "Commodities", "Cryptocurrencies"],
        default=user_prefs.get('preferred_assets', ['Stocks', 'ETFs'])
    )
    
    # Sector Preferences
    sector_preferences = st.multiselect(
        "Sector Preferences",
        ["Technology", "Healthcare", "Finance", "Consumer Goods", "Energy", 
         "Real Estate", "Utilities", "Materials", "Telecommunications"],
        default=user_prefs.get('sector_preferences', ['Technology', 'Healthcare'])
    )
    
    # Geographic Preferences
    geographic_preferences = st.multiselect(
        "Geographic Preferences",
        ["US Domestic", "International Developed", "Emerging Markets", "Global"],
        default=user_prefs.get('geographic_preferences', ['US Domestic'])
    )
    
    # ESG Preferences
    esg_important = st.checkbox(
        "ESG (Environmental, Social, Governance) investing is important to me",
        value=user_prefs.get('esg_important', False)
    )

# Additional Preferences
st.markdown("---")
st.subheader("🔔 Notification Preferences")

col1, col2 = st.columns(2)

with col1:
    notifications = user_prefs.get('notifications', {})
    email_notifications = st.checkbox(
        "Email Notifications",
        value=notifications.get('email_notifications', True)
    )
    
    portfolio_alerts = st.checkbox(
        "Portfolio Performance Alerts",
        value=notifications.get('portfolio_alerts', True)
    )
    
    market_news = st.checkbox(
        "Market News & Updates",
        value=notifications.get('market_news', True)
    )

with col2:
    reminder_notifications = st.checkbox(
        "Reminder Notifications",
        value=notifications.get('reminder_notifications', True)
    )
    
    ai_insights = st.checkbox(
        "AI-Generated Insights",
        value=notifications.get('ai_insights', True)
    )
    
    weekly_reports = st.checkbox(
        "Weekly Performance Reports",
        value=notifications.get('weekly_reports', False)
    )

# Financial Goals Section
st.markdown("---")
st.subheader("💰 Financial Goals")

financial_goals = st.text_area(
    "Describe your financial goals in detail",
    value=user_prefs.get('financial_goals', ''),
    height=100,
    placeholder="e.g., Save $100,000 for retirement by age 40, build an emergency fund of 6 months expenses..."
)

# Risk Capacity
st.subheader("📈 Risk Capacity")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=int(user_prefs.get('age', 30)) if user_prefs.get('age') else 30
    )
    
    annual_income = st.number_input(
        "Annual Income ($)",
        min_value=0,
        value=int(user_prefs.get('annual_income', 75000)),
        step=5000
    )

with col2:
    dependents = st.number_input(
        "Number of Dependents",
        min_value=0,
        value=int(user_prefs.get('dependents', 0))
    )
    
    debt_amount = st.number_input(
        "Total Debt Amount ($)",
        min_value=0,
        value=int(user_prefs.get('debt_amount', 0)),
        step=1000
    )

# Save preferences
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col2:
    if st.button("💾 Save Preferences", type="primary", use_container_width=True):
        preferences = {
            'risk_tolerance': risk_tolerance,
            'investment_timeline': investment_timeline,
            'investment_goals': investment_goals,
            'monthly_investment': monthly_investment,
            'preferred_assets': preferred_assets,
            'sector_preferences': sector_preferences,
            'geographic_preferences': geographic_preferences,
            'esg_important': esg_important,
            'email_notifications': email_notifications,
            'portfolio_alerts': portfolio_alerts,
            'market_news': market_news,
            'reminder_notifications': reminder_notifications,
            'ai_insights': ai_insights,
            'weekly_reports': weekly_reports,
            'financial_goals': financial_goals,
            'age': age,
            'annual_income': annual_income,
            'dependents': dependents,
            'debt_amount': debt_amount
        }
        
        try:
            save_user_preferences(st.session_state.username, preferences)
            st.success("✅ Preferences saved successfully!")
            st.session_state.preferences_updated = True
        except Exception as e:
            st.error(f"Error saving preferences: {str(e)}")

# Display current profile summary
if st.session_state.preferences_updated or user_prefs:
    st.markdown("---")
    st.subheader("📋 Your Investment Profile Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Risk Profile:** {risk_tolerance}
        **Timeline:** {investment_timeline}
        **Monthly Investment:** ${monthly_investment:,}
        **Primary Goals:** {', '.join(investment_goals[:3])}
        """)
    
    with col2:
        st.info(f"""
        **Preferred Assets:** {', '.join(preferred_assets[:3])}
        **Top Sectors:** {', '.join(sector_preferences[:3])}
        **Geographic Focus:** {', '.join(geographic_preferences)}
        **ESG Focus:** {'Yes' if esg_important else 'No'}
        """)
