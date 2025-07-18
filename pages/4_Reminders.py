import streamlit as st
from utils.auth import check_authentication
from utils.reminders import get_user_reminders, add_reminder, delete_reminder
from datetime import datetime, timedelta
import pandas as pd

# Check authentication
check_authentication()

st.set_page_config(
    page_title="Financial Reminders",
    page_icon="⏰",
    layout="wide"
)

st.title("⏰ Financial Reminders")

# Initialize session state
if 'reminders_updated' not in st.session_state:
    st.session_state.reminders_updated = False

# Load existing reminders
try:
    user_reminders = get_user_reminders(st.session_state.username)
except Exception as e:
    st.error(f"Error loading reminders: {str(e)}")
    user_reminders = []

# Add new reminder section
with st.expander("➕ Add New Reminder", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        reminder_title = st.text_input("Reminder Title", placeholder="e.g., Monthly SIP Investment")
        
        reminder_type = st.selectbox(
            "Reminder Type",
            ["SIP Investment", "Tax Filing", "Portfolio Review", "Bill Payment", 
             "Insurance Premium", "Loan EMI", "Investment Maturity", "Custom"]
        )
        
        reminder_date = st.date_input(
            "Reminder Date",
            value=datetime.now().date() + timedelta(days=7)
        )
    
    with col2:
        reminder_description = st.text_area(
            "Description",
            height=100,
            placeholder="Enter detailed description of the reminder..."
        )
        
        reminder_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Critical"]
        )
        
        recurring = st.checkbox("Recurring Reminder")
        
        if recurring:
            frequency = st.selectbox(
                "Frequency",
                ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"]
            )
        else:
            frequency = "One-time"
    
    if st.button("💾 Add Reminder", type="primary"):
        if reminder_title and reminder_description:
            try:
                reminder_data = {
                    'title': reminder_title,
                    'type': reminder_type,
                    'description': reminder_description,
                    'date': reminder_date.isoformat(),
                    'priority': reminder_priority,
                    'recurring': recurring,
                    'frequency': frequency,
                    'status': 'Active',
                    'created_date': datetime.now().isoformat()
                }
                
                add_reminder(st.session_state.username, reminder_data)
                st.success("✅ Reminder added successfully!")
                st.session_state.reminders_updated = True
                st.rerun()
            except Exception as e:
                st.error(f"Error saving reminder: {str(e)}")
        else:
            st.error("Please fill in all required fields")

st.markdown("---")

# Display existing reminders
st.subheader("📋 Your Reminders")

if user_reminders:
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📅 Upcoming", "🔄 Recurring", "✅ All Reminders"])
    
    with tab1:
        st.subheader("Upcoming Reminders (Next 30 Days)")
        
        # Filter upcoming reminders
        upcoming_reminders = []
        current_date = datetime.now().date()
        
        for reminder in user_reminders:
            reminder_date = datetime.fromisoformat(reminder.get('date', '')).date()
            if reminder_date >= current_date and reminder_date <= current_date + timedelta(days=30):
                upcoming_reminders.append(reminder)
        
        if upcoming_reminders:
            for reminder in sorted(upcoming_reminders, key=lambda x: x['date']):
                reminder_date = datetime.fromisoformat(reminder['date']).date()
                days_until = (reminder_date - current_date).days
                
                # Color code based on urgency
                if days_until <= 1:
                    priority_color = "🔴"
                elif days_until <= 7:
                    priority_color = "🟡"
                else:
                    priority_color = "🟢"
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    {priority_color} **{reminder['title']}**  
                    📅 {reminder_date.strftime('%B %d, %Y')} ({days_until} days)  
                    📝 {reminder['description']}  
                    🏷️ {reminder['type']} | 🎯 {reminder['priority']} Priority
                    """)
                
                with col2:
                    if st.button(f"✅ Complete", key=f"complete_{reminder.get('id', hash(reminder['title']))}"):
                        # Mark as completed
                        st.success("Reminder marked as complete!")
                
                with col3:
                    if st.button(f"🗑️ Delete", key=f"delete_{reminder.get('id', hash(reminder['title']))}"):
                        try:
                            delete_reminder(st.session_state.username, reminder.get('id', reminder['title']))
                            st.success("Reminder deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting reminder: {str(e)}")
                
                st.markdown("---")
        else:
            st.info("No upcoming reminders in the next 30 days.")
    
    with tab2:
        st.subheader("Recurring Reminders")
        
        recurring_reminders = [r for r in user_reminders if r.get('recurring', False)]
        
        if recurring_reminders:
            for reminder in recurring_reminders:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    **{reminder['title']}**  
                    🔄 {reminder['frequency']} | 📅 Next: {reminder['date']}  
                    📝 {reminder['description']}  
                    🏷️ {reminder['type']} | 🎯 {reminder['priority']} Priority
                    """)
                
                with col2:
                    if st.button(f"⚙️ Edit", key=f"edit_{reminder.get('id', hash(reminder['title']))}"):
                        st.info("Edit functionality coming soon!")
                
                st.markdown("---")
        else:
            st.info("No recurring reminders set up.")
    
    with tab3:
        st.subheader("All Reminders")
        
        # Create a DataFrame for better display
        df_data = []
        for reminder in user_reminders:
            df_data.append({
                'Title': reminder['title'],
                'Type': reminder['type'],
                'Date': reminder['date'],
                'Priority': reminder['priority'],
                'Recurring': 'Yes' if reminder.get('recurring', False) else 'No',
                'Status': reminder.get('status', 'Active')
            })
        
        if df_data:
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No reminders found.")

else:
    st.info("No reminders found. Add your first reminder above!")

# Suggested Reminders Section
st.markdown("---")
st.subheader("💡 Suggested Reminders")

suggested_reminders = [
    {
        'title': 'Monthly SIP Investment',
        'type': 'SIP Investment',
        'description': 'Monthly systematic investment plan contribution',
        'frequency': 'Monthly'
    },
    {
        'title': 'Quarterly Portfolio Review',
        'type': 'Portfolio Review',
        'description': 'Review and rebalance portfolio allocation',
        'frequency': 'Quarterly'
    },
    {
        'title': 'Annual Tax Filing',
        'type': 'Tax Filing',
        'description': 'Complete annual tax return filing',
        'frequency': 'Yearly'
    },
    {
        'title': 'Emergency Fund Check',
        'type': 'Portfolio Review',
        'description': 'Review emergency fund adequacy',
        'frequency': 'Monthly'
    }
]

col1, col2 = st.columns(2)

for i, suggestion in enumerate(suggested_reminders):
    with col1 if i % 2 == 0 else col2:
        with st.container():
            st.markdown(f"""
            **{suggestion['title']}**  
            🏷️ {suggestion['type']} | 🔄 {suggestion['frequency']}  
            📝 {suggestion['description']}
            """)
            
            if st.button(f"➕ Add This Reminder", key=f"suggest_{i}"):
                # Pre-fill the form with suggested data
                st.session_state.suggested_reminder = suggestion
                st.info("Scroll up to customize and add this reminder!")
