import streamlit as st
from utils.ai_assistant import get_ai_response, get_financial_context
from utils.auth import check_authentication
import json
from datetime import datetime

# Check authentication
check_authentication()

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Financial Assistant")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar with example prompts
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=FinAssist", width=150)
    st.markdown("---")
    
    st.subheader("💡 Example Questions")
    
    example_prompts = [
        "How is my portfolio performing?",
        "What are the best SIPs this month?",
        "Should I rebalance my portfolio?",
        "What are the risks in my current holdings?",
        "Suggest some dividend stocks",
        "What's the market outlook for tech stocks?",
        "How can I reduce my portfolio risk?",
        "What are tax-efficient investment strategies?"
    ]
    
    for prompt in example_prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state.current_prompt = prompt

# Main chat interface
st.subheader("💬 Chat with your Financial Assistant")

# Display chat history
chat_container = st.container()

with chat_container:
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**🤖 Assistant:** {message['content']}")
        
        if i < len(st.session_state.chat_history) - 1:
            st.markdown("---")

# Chat input
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Ask me anything about your finances...",
        placeholder="e.g., How is my portfolio performing?",
        key="chat_input",
        value=st.session_state.get('current_prompt', '')
    )

with col2:
    send_button = st.button("Send", type="primary")

# Handle user input
if send_button and user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # Show loading spinner
    with st.spinner("🤖 Thinking..."):
        try:
            # Get AI response
            ai_response = get_ai_response(
                user_input, 
                st.session_state.username,
                st.session_state.chat_history
            )
            
            # Add AI response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            st.error(f"Error getting AI response: {str(e)}")
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "I'm sorry, I encountered an error processing your request. Please try again or contact support if the issue persists.",
                "timestamp": datetime.now().isoformat()
            })
    
    # Clear the current prompt and rerun
    if 'current_prompt' in st.session_state:
        del st.session_state.current_prompt
    st.rerun()

# Clear chat history button
if st.session_state.chat_history:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col2:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# AI Assistant Features
st.markdown("---")
st.subheader("🎯 What I Can Help You With")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Portfolio Analysis**
    - Performance review
    - Risk assessment
    - Asset allocation advice
    - Rebalancing suggestions
    """)

with col2:
    st.markdown("""
    **Investment Research**
    - Stock analysis
    - Market trends
    - Sector insights
    - Investment recommendations
    """)

with col3:
    st.markdown("""
    **Financial Planning**
    - Goal setting
    - Retirement planning
    - Tax optimization
    - Risk management
    """)

# Context Information
with st.expander("🔍 How I Generate Responses"):
    st.markdown("""
    I analyze your financial data including:
    - Current portfolio holdings
    - Transaction history
    - Risk preferences
    - Investment goals
    - Market conditions
    
    I use advanced AI to provide personalized financial advice based on your specific situation.
    
    **Please note:** My responses are for informational purposes only and should not be considered as professional financial advice. Always consult with a qualified financial advisor for important financial decisions.
    """)
