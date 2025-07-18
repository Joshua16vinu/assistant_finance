import streamlit as st
import hashlib
import json
import os
from datetime import datetime

# Simple file-based user database for MVP
USER_DATA_FILE = "user_data.json"

def load_user_data():
    """Load user data from file"""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_user_data(data):
    """Save user data to file"""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user with username and password"""
    user_data = load_user_data()
    
    if username in user_data:
        stored_hash = user_data[username]['password_hash']
        if stored_hash == hash_password(password):
            # Update last login
            user_data[username]['last_login'] = datetime.now().isoformat()
            save_user_data(user_data)
            return True
    
    return False

def register_user(username, email, password):
    """Register a new user"""
    user_data = load_user_data()
    
    if username in user_data:
        return False  # User already exists
    
    user_data[username] = {
        'email': email,
        'password_hash': hash_password(password),
        'created_date': datetime.now().isoformat(),
        'last_login': None,
        'preferences': {},
        'portfolio': [],
        'reminders': []
    }
    
    save_user_data(user_data)
    return True

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
    user_data = load_user_data()
    return user_data.get(username, {})

def update_user_info(username, info):
    """Update user information"""
    user_data = load_user_data()
    if username in user_data:
        user_data[username].update(info)
        save_user_data(user_data)
        return True
    return False
