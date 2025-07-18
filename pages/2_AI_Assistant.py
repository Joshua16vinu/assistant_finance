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

# Add enhanced CSS styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}

.chat-message {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #667eea;
    animation: slideIn 0.3s ease;
}

.ai-message {
    border-left: 4px solid #4ecdc4;
    background: linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(102, 126, 234, 0.1) 100%);
}

.user-message {
    border-left: 4px solid #667eea;
    background: rgba(255, 255, 255, 0.95);
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.example-prompt {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 15px;
    margin: 5px 0;
    font-weight: 500;
    transition: all 0.3s ease;
    width: 100%;
    text-align: left;
}

.example-prompt:hover {
    background: linear-gradient(45deg, #5a67d8, #6b46c1);
    transform: translateX(5px);
    box-shadow: 0 4px 15px rgba(90, 103, 216, 0.4);
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

.gradient-text {
    background: linear-gradient(45deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-card">
    <h1 style="text-align: center; margin-bottom: 20px;">
        <span class="gradient-text">🤖 AI Financial Assistant</span>
    </h1>
    <p style="text-align: center; color: #666; font-size: 1.1em;">
        Ask me anything about your finances, investments, and market trends
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Import UI components
from utils.ui_components import add_enhanced_sidebar, add_page_css

# Add consistent styling and sidebar
add_page_css()
add_enhanced_sidebar()

# Sidebar with example prompts
with st.sidebar:
    st.markdown("---")
    st.markdown("""
    <h3 style="color: #667eea; margin-bottom: 15px;">💡 Example Questions</h3>
    """, unsafe_allow_html=True)
    
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
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong style="color: #667eea;">👤 You:</strong><br>
                <div style="margin-top: 10px;">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong style="color: #4ecdc4;">🤖 AI Assistant:</strong><br>
                <div style="margin-top: 10px;">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)

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
