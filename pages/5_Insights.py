import streamlit as st
from utils.auth import check_authentication
from utils.ai_assistant import get_ai_insights
from utils.database import get_user_preferences
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# Check authentication
check_authentication()

st.set_page_config(
    page_title="Financial Insights",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Financial Insights")

# Load user preferences for personalized insights
try:
    user_prefs = get_user_preferences(st.session_state.username)
except Exception as e:
    st.error(f"Error loading user preferences: {str(e)}")
    user_prefs = {}

# Generate AI insights
with st.spinner("🧠 Generating personalized insights..."):
    try:
        insights = get_ai_insights(st.session_state.username, user_prefs)
    except Exception as e:
        st.error(f"Error generating insights: {str(e)}")
        insights = {}

# Key Insights Section
st.subheader("🎯 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Portfolio Health Score",
        "8.2/10",
        "+0.5 from last month",
        help="Overall assessment of your portfolio's performance and risk balance"
    )

with col2:
    st.metric(
        "Risk Level",
        "Moderate",
        "Optimal for your profile",
        help="Current risk level compared to your stated risk tolerance"
    )

with col3:
    st.metric(
        "Diversification Score",
        "7.8/10",
        "+0.3 from last month",
        help="How well diversified your portfolio is across different asset classes"
    )

# AI-Generated Insights
st.markdown("---")
st.subheader("🤖 AI-Generated Recommendations")

# Recommendation cards
recommendations = [
    {
        "title": "Portfolio Rebalancing",
        "priority": "High",
        "description": "Your technology allocation has grown to 35% of your portfolio, exceeding your target of 30%. Consider rebalancing to maintain optimal risk levels.",
        "action": "Sell $2,500 worth of tech stocks and invest in bonds or international funds",
        "impact": "Reduce portfolio volatility by 2-3%"
    },
    {
        "title": "Tax-Loss Harvesting",
        "priority": "Medium",
        "description": "You have unrealized losses in your energy sector holdings that could be used to offset capital gains.",
        "action": "Realize $1,200 in losses before year-end",
        "impact": "Potential tax savings of $300-400"
    },
    {
        "title": "Emergency Fund",
        "priority": "High",
        "description": "Your emergency fund covers only 3 months of expenses. Consider increasing it to 6 months for better financial security.",
        "action": "Increase monthly emergency fund contribution to $500",
        "impact": "Achieve 6-month emergency fund in 12 months"
    }
]

for rec in recommendations:
    priority_color = "🔴" if rec["priority"] == "High" else "🟡" if rec["priority"] == "Medium" else "🟢"
    
    with st.expander(f"{priority_color} {rec['title']} - {rec['priority']} Priority"):
        st.markdown(f"""
        **Issue:** {rec['description']}
        
        **Recommended Action:** {rec['action']}
        
        **Expected Impact:** {rec['impact']}
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"✅ Implement", key=f"implement_{rec['title']}"):
                st.success("Added to your action items!")
        
        with col2:
            if st.button(f"💬 Ask AI More", key=f"ask_{rec['title']}"):
                st.info("Navigate to AI Assistant to discuss this recommendation in detail.")

# Market Analysis Section
st.markdown("---")
st.subheader("📊 Market Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Sector Performance (Last 30 Days)")
    
    # Sample sector performance data
    sectors = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer Goods']
    performance = [2.5, 1.8, -0.5, 3.2, 1.1]
    
    fig = px.bar(
        x=sectors,
        y=performance,
        title="Sector Performance (%)",
        color=performance,
        color_continuous_scale=['red', 'green']
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 📊 Your vs. Market Performance")
    
    # Sample performance comparison
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    your_portfolio = [100]
    market_benchmark = [100]
    
    for i in range(1, len(dates)):
        your_portfolio.append(your_portfolio[-1] * (1 + 0.0005 + 0.001 * (i % 7 - 3) / 10))
        market_benchmark.append(market_benchmark[-1] * (1 + 0.0003 + 0.001 * (i % 5 - 2) / 10))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=your_portfolio, mode='lines', name='Your Portfolio'))
    fig.add_trace(go.Scatter(x=dates, y=market_benchmark, mode='lines', name='S&P 500'))
    
    fig.update_layout(title="Portfolio vs Market Performance", xaxis_title="Date", yaxis_title="Value")
    st.plotly_chart(fig, use_container_width=True)

# Risk Analysis
st.markdown("---")
st.subheader("⚠️ Risk Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 Risk Metrics")
    
    risk_metrics = {
        'Beta': 1.15,
        'Standard Deviation': 18.5,
        'Sharpe Ratio': 1.45,
        'Maximum Drawdown': -12.3,
        'Value at Risk (95%)': -8.2
    }
    
    for metric, value in risk_metrics.items():
        if 'Drawdown' in metric or 'Risk' in metric:
            st.metric(metric, f"{value}%", delta=None)
        elif 'Standard Deviation' in metric:
            st.metric(metric, f"{value}%", delta=None)
        else:
            st.metric(metric, f"{value}", delta=None)

with col2:
    st.markdown("#### 📊 Risk Distribution")
    
    # Risk distribution by asset class
    risk_data = {
        'Asset Class': ['Stocks', 'Bonds', 'ETFs', 'Cash'],
        'Risk Contribution': [65, 15, 18, 2]
    }
    
    fig = px.pie(
        values=risk_data['Risk Contribution'],
        names=risk_data['Asset Class'],
        title="Risk Contribution by Asset Class"
    )
    st.plotly_chart(fig, use_container_width=True)

# Opportunities Section
st.markdown("---")
st.subheader("🎯 Investment Opportunities")

opportunities = [
    {
        "title": "Undervalued Tech Stocks",
        "description": "Several quality tech companies are trading below their intrinsic value",
        "potential_return": "15-25%",
        "risk_level": "Medium",
        "time_horizon": "6-12 months"
    },
    {
        "title": "Dividend Growth Stocks",
        "description": "Companies with strong dividend growth history and sustainable payouts",
        "potential_return": "8-12%",
        "risk_level": "Low",
        "time_horizon": "3-5 years"
    },
    {
        "title": "International Diversification",
        "description": "Emerging markets showing strong recovery potential",
        "potential_return": "10-20%",
        "risk_level": "High",
        "time_horizon": "1-3 years"
    }
]

for opp in opportunities:
    with st.expander(f"🎯 {opp['title']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Description:** {opp['description']}
            
            **Potential Return:** {opp['potential_return']}
            """)
        
        with col2:
            st.markdown(f"""
            **Risk Level:** {opp['risk_level']}
            
            **Time Horizon:** {opp['time_horizon']}
            """)
        
        if st.button(f"📚 Learn More", key=f"learn_{opp['title']}"):
            st.info("More detailed analysis available in the AI Assistant.")

# Action Items
st.markdown("---")
st.subheader("✅ Recommended Action Items")

action_items = [
    "Review and rebalance portfolio allocation",
    "Increase emergency fund contributions",
    "Consider tax-loss harvesting opportunities",
    "Research undervalued dividend stocks",
    "Schedule quarterly portfolio review"
]

for i, item in enumerate(action_items):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"{i+1}. {item}")
    
    with col2:
        if st.button("✅ Done", key=f"action_{i}"):
            st.success("Action item completed!")

# Insights Summary
st.markdown("---")
st.info("""
💡 **Summary:** Your portfolio is performing well with good diversification. Focus on rebalancing tech allocation 
and building your emergency fund. The market shows opportunities in undervalued stocks and international diversification.
""")
