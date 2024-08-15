import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Constraint
from config import DATABASE_URL
from utility import generate_schedule  # Import the utility function

# Set up the database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Function to load the constraint data from the database
def load_constraints():
    return session.query(Constraint).first()

# Function to initialize or get session state values
def get_state_value(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value
    return st.session_state[key]

# Load the original constraints
if 'original_constraints' not in st.session_state:
    st.session_state.original_constraints = load_constraints()

# If the cancel button was pressed, reset values and rerun the script before rendering the inputs
if st.session_state.get('cancel_pressed', False):
    constraint = st.session_state.original_constraints
    for field in [
        "min_days_off", "max_days_off", "min_days_off_in_period", "max_days_off_in_period",
        "exact_days_off_per_month", "min_morning_shifts", "max_morning_shifts",
        "min_morning_shifts_in_period", "max_morning_shifts_in_period",
        "min_afternoon_shifts", "max_afternoon_shifts", "min_afternoon_shifts_in_period",
        "max_afternoon_shifts_in_period", "min_night_shifts", "max_night_shifts",
        "min_night_shifts_in_period", "max_night_shifts_in_period"
    ]:
        st.session_state[field] = str(getattr(constraint, field, 0))
    st.session_state.cancel_pressed = False
    st.rerun()

# Set up the Streamlit app
st.title("Manage Constraints")
st.subheader("Edit the Constraints for Scheduling")

# Display input fields for each constraint
def create_input(label, key):
    constraint = st.session_state.original_constraints
    default_value = getattr(constraint, key, 0)
    return st.text_input(label, value=get_state_value(key, str(default_value)), key=key)

# General Days Off Constraints
st.markdown("### General Days Off Constraints")
create_input("Min Days Off", "min_days_off")
create_input("Max Days Off", "max_days_off")
create_input("Min Days Off in Period", "min_days_off_in_period")
create_input("Max Days Off in Period", "max_days_off_in_period")
create_input("Exact Days Off Per Month", "exact_days_off_per_month")

# Morning Shifts Constraints
st.markdown("### Morning Shifts Constraints")
create_input("Min Morning Shifts", "min_morning_shifts")
create_input("Max Morning Shifts", "max_morning_shifts")
create_input("Min Morning Shifts in Period", "min_morning_shifts_in_period")
create_input("Max Morning Shifts in Period", "max_morning_shifts_in_period")

# Afternoon Shifts Constraints
st.markdown("### Afternoon Shifts Constraints")
create_input("Min Afternoon Shifts", "min_afternoon_shifts")
create_input("Max Afternoon Shifts", "max_afternoon_shifts")
create_input("Min Afternoon Shifts in Period", "min_afternoon_shifts_in_period")
create_input("Max Afternoon Shifts in Period", "max_afternoon_shifts_in_period")

# Night Shifts Constraints
st.markdown("### Night Shifts Constraints")
create_input("Min Night Shifts", "min_night_shifts")
create_input("Max Night Shifts", "max_night_shifts")
create_input("Min Night Shifts in Period", "min_night_shifts_in_period")
create_input("Max Night Shifts in Period", "max_night_shifts_in_period")

# Adjust the layout of the save and cancel buttons
save_button, cancel_button = st.columns([1, 9])  # Reduced the width of the cancel button column to bring it closer to the save button

with save_button:
    if st.button("Save"):
        try:
            # Fetch the constraint from the database
            constraint = session.query(Constraint).first()
            if not constraint:
                constraint = Constraint()
                session.add(constraint)

            # Update the constraint fields
            for field in [
                "min_days_off", "max_days_off", "min_days_off_in_period", "max_days_off_in_period",
                "exact_days_off_per_month", "min_morning_shifts", "max_morning_shifts",
                "min_morning_shifts_in_period", "max_morning_shifts_in_period",
                "min_afternoon_shifts", "max_afternoon_shifts", "min_afternoon_shifts_in_period",
                "max_afternoon_shifts_in_period", "min_night_shifts", "max_night_shifts",
                "min_night_shifts_in_period", "max_night_shifts_in_period"
            ]:
                setattr(constraint, field, int(st.session_state[field]))

            # Commit the changes to the database
            session.commit()

            # Refresh the constraint in the session
            session.refresh(constraint)

            # Update the original constraints in the session state
            st.session_state.original_constraints = constraint
        except Exception as e:
            st.error(f"An error occurred while saving changes: {e}")
        else:
            st.rerun()

with cancel_button:
    if st.button("Cancel"):
        st.session_state.cancel_pressed = True
        st.rerun()

# Add the "Generate New Schedule" button
st.markdown("---")
if st.button("Generate New Schedule"):
    generate_schedule()

#good version