import streamlit as st
import os
import json
from datetime import datetime
from google import genai
from google.genai import types
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from utils.database_setup import get_database_connection
from utils.auth import get_user_id

# Initialize Gemini client
# Note that the newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
# do not change this unless explicitly requested by the user
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-api-key-here")
client = genai.Client(api_key=GEMINI_API_KEY)

def get_financial_context(username):
    """Get user's financial context for AI responses"""
    try:
        from utils.user_preferences import get_user_preferences
        
        # Get user preferences from database
        preferences = get_user_preferences(username)
        
        # Get portfolio data (placeholder for now, would be from portfolio_holdings table)
        context = {
            'portfolio_value': 125430,
            'holdings': [
                {'symbol': 'AAPL', 'shares': 50, 'value': 7512.50},
                {'symbol': 'GOOGL', 'shares': 25, 'value': 68770.00},
                {'symbol': 'MSFT', 'shares': 75, 'value': 22886.25},
                {'symbol': 'TSLA', 'shares': 20, 'value': 17008.00},
                {'symbol': 'AMZN', 'shares': 15, 'value': 2711.25}
            ],
            'risk_tolerance': preferences.get('risk_tolerance', 'Moderate'),
            'investment_goals': preferences.get('investment_goals', ['Wealth Building']),
            'monthly_investment': preferences.get('monthly_investment', 1000),
            'age': preferences.get('age', 35),
            'investment_timeline': preferences.get('investment_timeline', '10+ years'),
            'annual_income': preferences.get('annual_income', 0),
            'debt_amount': preferences.get('debt_amount', 0),
            'financial_goals': preferences.get('financial_goals', '')
        }
        return context
    except Exception as e:
        st.error(f"Error getting financial context: {str(e)}")
        return {}

def save_chat_message(username, role, content, session_id=None):
    """Save chat message to database"""
    user_id = get_user_id(username)
    if not user_id:
        return False
    
    engine = get_database_connection()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO ai_chat_history (user_id, message_role, message_content, session_id)
                    VALUES (:user_id, :role, :content, :session_id)
                """),
                {
                    "user_id": user_id,
                    "role": role,
                    "content": content,
                    "session_id": session_id
                }
            )
            conn.commit()
            return True
    
    except SQLAlchemyError as e:
        st.error(f"Error saving chat message: {str(e)}")
        return False

def get_chat_history(username, limit=20):
    """Get chat history from database"""
    user_id = get_user_id(username)
    if not user_id:
        return []
    
    engine = get_database_connection()
    if not engine:
        return []
    
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT message_role, message_content, timestamp
                    FROM ai_chat_history 
                    WHERE user_id = :user_id
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """),
                {"user_id": user_id, "limit": limit}
            )
            messages = result.fetchall()
            
            # Reverse to get chronological order
            chat_history = []
            for msg in reversed(messages):
                chat_history.append({
                    'role': msg[0],
                    'content': msg[1],
                    'timestamp': msg[2].isoformat() if msg[2] else None
                })
            
            return chat_history
    
    except SQLAlchemyError as e:
        st.error(f"Error getting chat history: {str(e)}")
        return []

def get_ai_response(user_query, username, chat_history=None):
    """Get AI response to user query"""
    try:
        # Save user message to database
        save_chat_message(username, "user", user_query)
        
        # Get user's financial context
        context = get_financial_context(username)
        
        # Get recent chat history if not provided
        if chat_history is None:
            chat_history = get_chat_history(username, limit=10)
        
        # Prepare system message with context
        system_message = f"""
        You are a knowledgeable financial advisor assistant. You have access to the user's financial information:
        
        Portfolio Value: ${context.get('portfolio_value', 0):,}
        Risk Tolerance: {context.get('risk_tolerance', 'Not specified')}
        Investment Goals: {', '.join(context.get('investment_goals', []))}
        Monthly Investment: ${context.get('monthly_investment', 0):,}
        Age: {context.get('age', 'Not specified')}
        Investment Timeline: {context.get('investment_timeline', 'Not specified')}
        
        Current Holdings:
        """
        
        for holding in context.get('holdings', []):
            system_message += f"- {holding['symbol']}: {holding['shares']} shares, ${holding['value']:,.2f}\n"
        
        system_message += """
        
        Please provide helpful, personalized financial advice based on this information. 
        Keep responses conversational but informative. Always remind users that this is for 
        informational purposes only and they should consult with a qualified financial advisor 
        for important decisions.
        """
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_query}
        ]
        
        # Add recent chat history for context
        if chat_history:
            # Add last few messages for context (limit to avoid token limits)
            recent_history = chat_history[-6:]  # Last 6 messages
            for msg in recent_history[:-1]:  # Exclude the current message
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Get response from Gemini
        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            if msg["role"] == "user":
                gemini_messages.append(types.Content(role="user", parts=[types.Part(text=msg["content"])]))
            elif msg["role"] == "system":
                # System message becomes part of the user message or instruction
                continue
        
        # Combine system message with user query
        combined_prompt = f"{system_message}\n\nUser Question: {user_query}"
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=combined_prompt
        )
        
        ai_response = response.text or "I apologize, but I'm having trouble processing your request right now."
        
        # Save AI response to database
        save_chat_message(username, "assistant", ai_response)
        
        return ai_response
    
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return "I apologize, but I'm having trouble processing your request right now. Please try again later or contact support if the issue persists."

def get_ai_insights(username, user_preferences):
    """Generate AI-powered financial insights"""
    try:
        context = get_financial_context(username)
        
        insights_prompt = f"""
        Based on the user's financial profile, generate personalized insights:
        
        Portfolio Value: ${context.get('portfolio_value', 0):,}
        Risk Tolerance: {context.get('risk_tolerance', 'Moderate')}
        Investment Goals: {', '.join(context.get('investment_goals', []))}
        Age: {context.get('age', 35)}
        Monthly Investment: ${context.get('monthly_investment', 1000):,}
        
        Holdings:
        """
        
        for holding in context.get('holdings', []):
            insights_prompt += f"- {holding['symbol']}: ${holding['value']:,.2f}\n"
        
        insights_prompt += """
        
        Provide insights on:
        1. Portfolio health and performance
        2. Risk assessment
        3. Diversification recommendations
        4. Rebalancing suggestions
        5. Tax optimization opportunities
        
        Format as JSON with categories: portfolio_health, risk_assessment, recommendations, opportunities
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"You are a financial advisor providing portfolio insights. {insights_prompt}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        insights = json.loads(response.text)
        return insights
    
    except Exception as e:
        st.error(f"Error generating AI insights: {str(e)}")
        return {
            "portfolio_health": "Unable to generate insights at this time.",
            "risk_assessment": "Please try again later.",
            "recommendations": [],
            "opportunities": []
        }

def get_investment_recommendations(risk_tolerance, investment_goals, current_holdings):
    """Get AI-powered investment recommendations"""
    try:
        prompt = f"""
        Based on the following profile, recommend 3-5 specific investment opportunities:
        
        Risk Tolerance: {risk_tolerance}
        Investment Goals: {', '.join(investment_goals)}
        Current Holdings: {', '.join([h['symbol'] for h in current_holdings])}
        
        Provide specific stock/ETF recommendations with reasons why they fit the profile.
        Format as JSON with: symbol, name, reason, expected_return, risk_level
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"You are a financial advisor providing investment recommendations. {prompt}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        recommendations = json.loads(response.text)
        return recommendations.get('recommendations', [])
    
    except Exception as e:
        st.error(f"Error getting investment recommendations: {str(e)}")
        return []

def analyze_portfolio_risk(holdings, user_preferences):
    """Analyze portfolio risk using AI"""
    try:
        holdings_summary = []
        for holding in holdings:
            holdings_summary.append(f"{holding['symbol']}: ${holding['value']:,.2f}")
        
        prompt = f"""
        Analyze the risk profile of this portfolio:
        
        Holdings: {', '.join(holdings_summary)}
        User Risk Tolerance: {user_preferences.get('risk_tolerance', 'Moderate')}
        Investment Timeline: {user_preferences.get('investment_timeline', '5-10 years')}
        
        Provide risk analysis including:
        1. Overall risk level (1-10 scale)
        2. Concentration risk assessment
        3. Sector/geographic diversification
        4. Volatility assessment
        5. Specific risk mitigation recommendations
        
        Format as JSON.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"You are a risk analysis expert. {prompt}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        risk_analysis = json.loads(response.text)
        return risk_analysis
    
    except Exception as e:
        st.error(f"Error analyzing portfolio risk: {str(e)}")
        return {
            "overall_risk_level": 5,
            "concentration_risk": "Unable to assess",
            "diversification_score": "Unable to calculate",
            "recommendations": []
        }
