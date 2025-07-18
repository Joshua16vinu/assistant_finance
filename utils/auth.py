import streamlit as st
import hashlib
import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from utils.database_setup import get_database_connection

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user with username and password"""
    engine = get_database_connection()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id, password_hash FROM users WHERE username = :username AND is_active = TRUE"),
                {"username": username}
            )
            user = result.fetchone()
            
            if user and user[1] == hash_password(password):
                # Update last login
                conn.execute(
                    text("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = :user_id"),
                    {"user_id": user[0]}
                )
                conn.commit()
                return True
    
    except SQLAlchemyError as e:
        st.error(f"Authentication error: {str(e)}")
    
    return False

def register_user(username, email, password):
    """Register a new user"""
    engine = get_database_connection()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            # Check if user already exists
            result = conn.execute(
                text("SELECT id FROM users WHERE username = :username OR email = :email"),
                {"username": username, "email": email}
            )
            existing_user = result.fetchone()
            
            if existing_user:
                return False  # User already exists
            
            # Create new user
            conn.execute(
                text("""
                    INSERT INTO users (username, email, password_hash, created_date)
                    VALUES (:username, :email, :password_hash, CURRENT_TIMESTAMP)
                """),
                {
                    "username": username,
                    "email": email,
                    "password_hash": hash_password(password)
                }
            )
            conn.commit()
            return True
    
    except SQLAlchemyError as e:
        st.error(f"Registration error: {str(e)}")
        return False

def check_authentication():
    """Check if user is authenticated, redirect to login if not"""
    if not st.session_state.get('authenticated', False):
        st.error("Please log in to access this page.")
        st.switch_page("app.py")
        st.stop()

def logout_user():
    """Logout user and clear session state"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_data = {}
    
    # Clear other session state variables
    for key in list(st.session_state.keys()):
        if key not in ['authenticated', 'username', 'user_data']:
            del st.session_state[key]

def get_user_info(username):
    """Get user information"""
    engine = get_database_connection()
    if not engine:
        return {}
    
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id, username, email, created_date, last_login FROM users WHERE username = :username"),
                {"username": username}
            )
            user = result.fetchone()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'created_date': user[3].isoformat() if user[3] else None,
                    'last_login': user[4].isoformat() if user[4] else None
                }
    
    except SQLAlchemyError as e:
        st.error(f"Error getting user info: {str(e)}")
    
    return {}

def get_user_id(username):
    """Get user ID by username"""
    engine = get_database_connection()
    if not engine:
        return None
    
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id FROM users WHERE username = :username"),
                {"username": username}
            )
            user = result.fetchone()
            return user[0] if user else None
    
    except SQLAlchemyError as e:
        st.error(f"Error getting user ID: {str(e)}")
        return None

def update_user_info(username, info):
    """Update user information"""
    engine = get_database_connection()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            # Update basic user info (email, etc.)
            if 'email' in info:
                conn.execute(
                    text("UPDATE users SET email = :email WHERE username = :username"),
                    {"email": info['email'], "username": username}
                )
            conn.commit()
            return True
    
    except SQLAlchemyError as e:
        st.error(f"Error updating user info: {str(e)}")
        return False
