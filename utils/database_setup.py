import os
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from datetime import datetime

# Database connection configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_database_connection():
    """Get database connection using SQLAlchemy"""
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None

def create_database_tables():
    """Create all necessary database tables"""
    engine = get_database_connection()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            # Users table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """))
            
            # User preferences table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    risk_tolerance VARCHAR(20),
                    investment_timeline VARCHAR(20),
                    investment_goals TEXT[],
                    monthly_investment DECIMAL(12,2),
                    preferred_assets TEXT[],
                    sector_preferences TEXT[],
                    geographic_preferences TEXT[],
                    esg_important BOOLEAN DEFAULT FALSE,
                    email_notifications BOOLEAN DEFAULT TRUE,
                    portfolio_alerts BOOLEAN DEFAULT TRUE,
                    market_news BOOLEAN DEFAULT TRUE,
                    reminder_notifications BOOLEAN DEFAULT TRUE,
                    ai_insights BOOLEAN DEFAULT TRUE,
                    weekly_reports BOOLEAN DEFAULT FALSE,
                    financial_goals TEXT,
                    age INTEGER,
                    annual_income DECIMAL(12,2),
                    dependents INTEGER DEFAULT 0,
                    debt_amount DECIMAL(12,2) DEFAULT 0,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Portfolio holdings table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS portfolio_holdings (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    symbol VARCHAR(10) NOT NULL,
                    company_name VARCHAR(100),
                    shares DECIMAL(15,6) NOT NULL,
                    purchase_price DECIMAL(10,2),
                    purchase_date DATE,
                    current_price DECIMAL(10,2),
                    market_value DECIMAL(15,2),
                    sector VARCHAR(50),
                    asset_type VARCHAR(20),
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Transactions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    symbol VARCHAR(10) NOT NULL,
                    transaction_type VARCHAR(10) NOT NULL, -- 'BUY', 'SELL'
                    shares DECIMAL(15,6) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    total_amount DECIMAL(15,2) NOT NULL,
                    fees DECIMAL(8,2) DEFAULT 0,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )
            """))
            
            # Reminders table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    title VARCHAR(200) NOT NULL,
                    reminder_type VARCHAR(50),
                    description TEXT,
                    reminder_date DATE NOT NULL,
                    priority VARCHAR(20) DEFAULT 'Medium',
                    is_recurring BOOLEAN DEFAULT FALSE,
                    frequency VARCHAR(20),
                    status VARCHAR(20) DEFAULT 'Active',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_date TIMESTAMP
                )
            """))
            
            # Portfolio performance history table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS portfolio_performance (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    performance_date DATE NOT NULL,
                    total_value DECIMAL(15,2) NOT NULL,
                    daily_change DECIMAL(15,2),
                    daily_change_percent DECIMAL(8,4),
                    total_return DECIMAL(15,2),
                    total_return_percent DECIMAL(8,4),
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # AI chat history table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ai_chat_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    message_role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
                    message_content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_id VARCHAR(100)
                )
            """))
            
            # Market data cache table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS market_data_cache (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(10) NOT NULL,
                    data_type VARCHAR(50) NOT NULL, -- 'stock_info', 'historical', etc.
                    data_json JSONB NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, data_type)
                )
            """))
            
            # User sessions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    session_token VARCHAR(255) UNIQUE NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_date TIMESTAMP NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """))
            
            # Create indexes for better performance
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_portfolio_user_symbol ON portfolio_holdings(user_id, symbol)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_transactions_user_date ON transactions(user_id, transaction_date)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_reminders_user_date ON reminders(user_id, reminder_date)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_performance_user_date ON portfolio_performance(user_id, performance_date)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_chat_user_timestamp ON ai_chat_history(user_id, timestamp)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_market_data_symbol ON market_data_cache(symbol, last_updated)"))
            
            conn.commit()
            return True
            
    except SQLAlchemyError as e:
        st.error(f"Error creating database tables: {str(e)}")
        return False

def test_database_connection():
    """Test database connection and create tables if needed"""
    engine = get_database_connection()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            
        # Create tables if they don't exist
        return create_database_tables()
        
    except Exception as e:
        st.error(f"Database test failed: {str(e)}")
        return False

def initialize_database():
    """Initialize database with tables and basic data"""
    if test_database_connection():
        st.success("Database initialized successfully!")
        return True
    else:
        st.error("Failed to initialize database")
        return False

if __name__ == "__main__":
    # Run this to initialize the database
    initialize_database()