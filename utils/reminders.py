import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from utils.database_setup import get_database_connection
from utils.auth import get_user_id
from datetime import datetime, date

def get_user_reminders(username):
    """Get user reminders from database"""
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
                    SELECT id, title, reminder_type, description, reminder_date, 
                           priority, is_recurring, frequency, status, created_date
                    FROM reminders 
                    WHERE user_id = :user_id AND status = 'Active'
                    ORDER BY reminder_date ASC
                """),
                {"user_id": user_id}
            )
            reminders = result.fetchall()
            
            reminder_list = []
            for reminder in reminders:
                reminder_list.append({
                    'id': reminder[0],
                    'title': reminder[1],
                    'type': reminder[2],
                    'description': reminder[3],
                    'date': reminder[4].isoformat() if reminder[4] else None,
                    'priority': reminder[5],
                    'is_recurring': reminder[6],
                    'frequency': reminder[7],
                    'status': reminder[8],
                    'created_date': reminder[9].isoformat() if reminder[9] else None
                })
            
            return reminder_list
    
    except SQLAlchemyError as e:
        st.error(f"Error getting reminders: {str(e)}")
        return []

def add_reminder(username, reminder_data):
    """Add a new reminder to database"""
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
                    INSERT INTO reminders (
                        user_id, title, reminder_type, description, reminder_date,
                        priority, is_recurring, frequency, status
                    ) VALUES (
                        :user_id, :title, :reminder_type, :description, :reminder_date,
                        :priority, :is_recurring, :frequency, 'Active'
                    )
                """),
                {
                    "user_id": user_id,
                    "title": reminder_data.get('title'),
                    "reminder_type": reminder_data.get('type'),
                    "description": reminder_data.get('description', ''),
                    "reminder_date": reminder_data.get('date'),
                    "priority": reminder_data.get('priority', 'Medium'),
                    "is_recurring": reminder_data.get('is_recurring', False),
                    "frequency": reminder_data.get('frequency')
                }
            )
            conn.commit()
            return True
    
    except SQLAlchemyError as e:
        st.error(f"Error adding reminder: {str(e)}")
        return False

def delete_reminder(username, reminder_id):
    """Delete a reminder (mark as inactive)"""
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
                    UPDATE reminders 
                    SET status = 'Deleted', completed_date = CURRENT_TIMESTAMP
                    WHERE id = :reminder_id AND user_id = :user_id
                """),
                {"reminder_id": reminder_id, "user_id": user_id}
            )
            conn.commit()
            return True
    
    except SQLAlchemyError as e:
        st.error(f"Error deleting reminder: {str(e)}")
        return False

def complete_reminder(username, reminder_id):
    """Mark a reminder as completed"""
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
                    UPDATE reminders 
                    SET status = 'Completed', completed_date = CURRENT_TIMESTAMP
                    WHERE id = :reminder_id AND user_id = :user_id
                """),
                {"reminder_id": reminder_id, "user_id": user_id}
            )
            conn.commit()
            return True
    
    except SQLAlchemyError as e:
        st.error(f"Error completing reminder: {str(e)}")
        return False

def get_upcoming_reminders(username, days_ahead=7):
    """Get upcoming reminders within specified days"""
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
                    SELECT id, title, reminder_type, reminder_date, priority
                    FROM reminders 
                    WHERE user_id = :user_id 
                    AND status = 'Active'
                    AND reminder_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL ':days days'
                    ORDER BY reminder_date ASC
                """),
                {"user_id": user_id, "days": days_ahead}
            )
            reminders = result.fetchall()
            
            upcoming = []
            for reminder in reminders:
                upcoming.append({
                    'id': reminder[0],
                    'title': reminder[1],
                    'type': reminder[2],
                    'date': reminder[3].isoformat() if reminder[3] else None,
                    'priority': reminder[4]
                })
            
            return upcoming
    
    except SQLAlchemyError as e:
        st.error(f"Error getting upcoming reminders: {str(e)}")
        return []