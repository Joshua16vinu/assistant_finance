import json
import os
from datetime import datetime
import streamlit as st

# File-based database for MVP - in production, use PostgreSQL
USER_PREFERENCES_FILE = "user_preferences.json"
USER_REMINDERS_FILE = "user_reminders.json"
PORTFOLIO_DATA_FILE = "portfolio_data.json"

def load_json_file(filename):
    """Load JSON data from file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_json_file(filename, data):
    """Save JSON data to file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def get_user_preferences(username):
    """Get user preferences from database"""
    try:
        preferences_data = load_json_file(USER_PREFERENCES_FILE)
        return preferences_data.get(username, {})
    except Exception as e:
        st.error(f"Error loading user preferences: {str(e)}")
        return {}

def save_user_preferences(username, preferences):
    """Save user preferences to database"""
    try:
        preferences_data = load_json_file(USER_PREFERENCES_FILE)
        preferences_data[username] = preferences
        preferences_data[username]['updated_date'] = datetime.now().isoformat()
        save_json_file(USER_PREFERENCES_FILE, preferences_data)
        return True
    except Exception as e:
        st.error(f"Error saving user preferences: {str(e)}")
        return False

def get_user_reminders(username):
    """Get user reminders from database"""
    try:
        reminders_data = load_json_file(USER_REMINDERS_FILE)
        return reminders_data.get(username, [])
    except Exception as e:
        st.error(f"Error loading user reminders: {str(e)}")
        return []

def save_reminder(username, reminder_data):
    """Save a new reminder to database"""
    try:
        reminders_data = load_json_file(USER_REMINDERS_FILE)
        
        if username not in reminders_data:
            reminders_data[username] = []
        
        # Add unique ID to reminder
        reminder_data['id'] = len(reminders_data[username]) + 1
        reminder_data['created_date'] = datetime.now().isoformat()
        
        reminders_data[username].append(reminder_data)
        save_json_file(USER_REMINDERS_FILE, reminders_data)
        return True
    except Exception as e:
        st.error(f"Error saving reminder: {str(e)}")
        return False

def delete_reminder(username, reminder_id):
    """Delete a reminder from database"""
    try:
        reminders_data = load_json_file(USER_REMINDERS_FILE)
        
        if username in reminders_data:
            # Filter out the reminder with the specified ID
            reminders_data[username] = [
                r for r in reminders_data[username] 
                if r.get('id') != reminder_id and r.get('title') != reminder_id
            ]
            save_json_file(USER_REMINDERS_FILE, reminders_data)
            return True
        return False
    except Exception as e:
        st.error(f"Error deleting reminder: {str(e)}")
        return False

def update_reminder(username, reminder_id, updated_data):
    """Update an existing reminder"""
    try:
        reminders_data = load_json_file(USER_REMINDERS_FILE)
        
        if username in reminders_data:
            for i, reminder in enumerate(reminders_data[username]):
                if reminder.get('id') == reminder_id:
                    reminders_data[username][i].update(updated_data)
                    reminders_data[username][i]['updated_date'] = datetime.now().isoformat()
                    save_json_file(USER_REMINDERS_FILE, reminders_data)
                    return True
        return False
    except Exception as e:
        st.error(f"Error updating reminder: {str(e)}")
        return False

def get_portfolio_data(username):
    """Get user's portfolio data"""
    try:
        portfolio_data = load_json_file(PORTFOLIO_DATA_FILE)
        return portfolio_data.get(username, {})
    except Exception as e:
        st.error(f"Error loading portfolio data: {str(e)}")
        return {}

def save_portfolio_data(username, portfolio):
    """Save user's portfolio data"""
    try:
        portfolio_data = load_json_file(PORTFOLIO_DATA_FILE)
        portfolio_data[username] = portfolio
        portfolio_data[username]['updated_date'] = datetime.now().isoformat()
        save_json_file(PORTFOLIO_DATA_FILE, portfolio_data)
        return True
    except Exception as e:
        st.error(f"Error saving portfolio data: {str(e)}")
        return False

def add_portfolio_holding(username, holding):
    """Add a new holding to user's portfolio"""
    try:
        portfolio_data = load_json_file(PORTFOLIO_DATA_FILE)
        
        if username not in portfolio_data:
            portfolio_data[username] = {'holdings': []}
        
        if 'holdings' not in portfolio_data[username]:
            portfolio_data[username]['holdings'] = []
        
        # Add unique ID to holding
        holding['id'] = len(portfolio_data[username]['holdings']) + 1
        holding['added_date'] = datetime.now().isoformat()
        
        portfolio_data[username]['holdings'].append(holding)
        save_json_file(PORTFOLIO_DATA_FILE, portfolio_data)
        return True
    except Exception as e:
        st.error(f"Error adding portfolio holding: {str(e)}")
        return False

def remove_portfolio_holding(username, holding_id):
    """Remove a holding from user's portfolio"""
    try:
        portfolio_data = load_json_file(PORTFOLIO_DATA_FILE)
        
        if username in portfolio_data and 'holdings' in portfolio_data[username]:
            portfolio_data[username]['holdings'] = [
                h for h in portfolio_data[username]['holdings'] 
                if h.get('id') != holding_id
            ]
            save_json_file(PORTFOLIO_DATA_FILE, portfolio_data)
            return True
        return False
    except Exception as e:
        st.error(f"Error removing portfolio holding: {str(e)}")
        return False

def get_user_transactions(username):
    """Get user's transaction history"""
    try:
        # In a real app, this would be a separate transactions table
        portfolio_data = load_json_file(PORTFOLIO_DATA_FILE)
        user_data = portfolio_data.get(username, {})
        return user_data.get('transactions', [])
    except Exception as e:
        st.error(f"Error loading transaction history: {str(e)}")
        return []

def save_transaction(username, transaction):
    """Save a new transaction"""
    try:
        portfolio_data = load_json_file(PORTFOLIO_DATA_FILE)
        
        if username not in portfolio_data:
            portfolio_data[username] = {'transactions': []}
        
        if 'transactions' not in portfolio_data[username]:
            portfolio_data[username]['transactions'] = []
        
        transaction['id'] = len(portfolio_data[username]['transactions']) + 1
        transaction['date'] = datetime.now().isoformat()
        
        portfolio_data[username]['transactions'].append(transaction)
        save_json_file(PORTFOLIO_DATA_FILE, portfolio_data)
        return True
    except Exception as e:
        st.error(f"Error saving transaction: {str(e)}")
        return False

def get_user_analytics(username):
    """Get user analytics and insights"""
    try:
        # Calculate basic analytics from portfolio and transaction data
        portfolio_data = get_portfolio_data(username)
        transactions = get_user_transactions(username)
        
        analytics = {
            'total_holdings': len(portfolio_data.get('holdings', [])),
            'total_transactions': len(transactions),
            'portfolio_value': sum(h.get('value', 0) for h in portfolio_data.get('holdings', [])),
            'last_updated': portfolio_data.get('updated_date', 'Never')
        }
        
        return analytics
    except Exception as e:
        st.error(f"Error calculating user analytics: {str(e)}")
        return {}
