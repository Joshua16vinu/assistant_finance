import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from utils.database_setup import get_database_connection
from utils.auth import get_user_id

def get_user_preferences(username):
    """Get user preferences from database"""
    user_id = get_user_id(username)
    if not user_id:
        return {}
    
    engine = get_database_connection()
    if not engine:
        return {}
    
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT risk_tolerance, investment_timeline, investment_goals, 
                           monthly_investment, preferred_assets, sector_preferences,
                           geographic_preferences, esg_important, email_notifications,
                           portfolio_alerts, market_news, reminder_notifications,
                           ai_insights, weekly_reports, financial_goals, age,
                           annual_income, dependents, debt_amount
                    FROM user_preferences 
                    WHERE user_id = :user_id
                """),
                {"user_id": user_id}
            )
            pref = result.fetchone()
            
            if pref:
                return {
                    'risk_tolerance': pref[0],
                    'investment_timeline': pref[1],
                    'investment_goals': pref[2] or [],
                    'monthly_investment': float(pref[3]) if pref[3] else 0.0,
                    'preferred_assets': pref[4] or [],
                    'sector_preferences': pref[5] or [],
                    'geographic_preferences': pref[6] or [],
                    'esg_important': pref[7] or False,
                    'notifications': {
                        'email_notifications': pref[8] or True,
                        'portfolio_alerts': pref[9] or True,
                        'market_news': pref[10] or True,
                        'reminder_notifications': pref[11] or True,
                        'ai_insights': pref[12] or True,
                        'weekly_reports': pref[13] or False
                    },
                    'financial_goals': pref[14] or '',
                    'age': pref[15],
                    'annual_income': float(pref[16]) if pref[16] else 0.0,
                    'dependents': pref[17] or 0,
                    'debt_amount': float(pref[18]) if pref[18] else 0.0
                }
    
    except SQLAlchemyError as e:
        st.error(f"Error getting user preferences: {str(e)}")
    
    return {}

def save_user_preferences(username, preferences):
    """Save user preferences to database"""
    user_id = get_user_id(username)
    if not user_id:
        return False
    
    engine = get_database_connection()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            # Check if preferences exist
            result = conn.execute(
                text("SELECT id FROM user_preferences WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            existing = result.fetchone()
            
            notifications = preferences.get('notifications', {})
            
            if existing:
                # Update existing preferences
                conn.execute(
                    text("""
                        UPDATE user_preferences SET
                            risk_tolerance = :risk_tolerance,
                            investment_timeline = :investment_timeline,
                            investment_goals = :investment_goals,
                            monthly_investment = :monthly_investment,
                            preferred_assets = :preferred_assets,
                            sector_preferences = :sector_preferences,
                            geographic_preferences = :geographic_preferences,
                            esg_important = :esg_important,
                            email_notifications = :email_notifications,
                            portfolio_alerts = :portfolio_alerts,
                            market_news = :market_news,
                            reminder_notifications = :reminder_notifications,
                            ai_insights = :ai_insights,
                            weekly_reports = :weekly_reports,
                            financial_goals = :financial_goals,
                            age = :age,
                            annual_income = :annual_income,
                            dependents = :dependents,
                            debt_amount = :debt_amount,
                            updated_date = CURRENT_TIMESTAMP
                        WHERE user_id = :user_id
                    """),
                    {
                        "user_id": user_id,
                        "risk_tolerance": preferences.get('risk_tolerance'),
                        "investment_timeline": preferences.get('investment_timeline'),
                        "investment_goals": preferences.get('investment_goals', []),
                        "monthly_investment": preferences.get('monthly_investment', 0),
                        "preferred_assets": preferences.get('preferred_assets', []),
                        "sector_preferences": preferences.get('sector_preferences', []),
                        "geographic_preferences": preferences.get('geographic_preferences', []),
                        "esg_important": preferences.get('esg_important', False),
                        "email_notifications": notifications.get('email_notifications', True),
                        "portfolio_alerts": notifications.get('portfolio_alerts', True),
                        "market_news": notifications.get('market_news', True),
                        "reminder_notifications": notifications.get('reminder_notifications', True),
                        "ai_insights": notifications.get('ai_insights', True),
                        "weekly_reports": notifications.get('weekly_reports', False),
                        "financial_goals": preferences.get('financial_goals', ''),
                        "age": preferences.get('age'),
                        "annual_income": preferences.get('annual_income', 0),
                        "dependents": preferences.get('dependents', 0),
                        "debt_amount": preferences.get('debt_amount', 0)
                    }
                )
            else:
                # Insert new preferences
                conn.execute(
                    text("""
                        INSERT INTO user_preferences (
                            user_id, risk_tolerance, investment_timeline, investment_goals,
                            monthly_investment, preferred_assets, sector_preferences,
                            geographic_preferences, esg_important, email_notifications,
                            portfolio_alerts, market_news, reminder_notifications,
                            ai_insights, weekly_reports, financial_goals, age,
                            annual_income, dependents, debt_amount
                        ) VALUES (
                            :user_id, :risk_tolerance, :investment_timeline, :investment_goals,
                            :monthly_investment, :preferred_assets, :sector_preferences,
                            :geographic_preferences, :esg_important, :email_notifications,
                            :portfolio_alerts, :market_news, :reminder_notifications,
                            :ai_insights, :weekly_reports, :financial_goals, :age,
                            :annual_income, :dependents, :debt_amount
                        )
                    """),
                    {
                        "user_id": user_id,
                        "risk_tolerance": preferences.get('risk_tolerance'),
                        "investment_timeline": preferences.get('investment_timeline'),
                        "investment_goals": preferences.get('investment_goals', []),
                        "monthly_investment": preferences.get('monthly_investment', 0),
                        "preferred_assets": preferences.get('preferred_assets', []),
                        "sector_preferences": preferences.get('sector_preferences', []),
                        "geographic_preferences": preferences.get('geographic_preferences', []),
                        "esg_important": preferences.get('esg_important', False),
                        "email_notifications": notifications.get('email_notifications', True),
                        "portfolio_alerts": notifications.get('portfolio_alerts', True),
                        "market_news": notifications.get('market_news', True),
                        "reminder_notifications": notifications.get('reminder_notifications', True),
                        "ai_insights": notifications.get('ai_insights', True),
                        "weekly_reports": notifications.get('weekly_reports', False),
                        "financial_goals": preferences.get('financial_goals', ''),
                        "age": preferences.get('age'),
                        "annual_income": preferences.get('annual_income', 0),
                        "dependents": preferences.get('dependents', 0),
                        "debt_amount": preferences.get('debt_amount', 0)
                    }
                )
            
            conn.commit()
            return True
    
    except SQLAlchemyError as e:
        st.error(f"Error saving user preferences: {str(e)}")
        return False