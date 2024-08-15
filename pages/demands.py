import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Demand
from config import DATABASE_URL
from utility import generate_schedule  # Import the utility function

# Set up the database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Function to load the demand data from the database
def load_demand_data():
    demand_records = session.query(Demand).all()
    data = []
    dates = []
    for record in demand_records:
        data.append(record.demand)
        dates.append(record.date.strftime("%Y-%m-%d"))
    
    time_periods = [f"{9 + i//2:02}:{(i%2)*30:02}-{9 + (i+1)//2:02}:{((i+1)%2)*30:02}" for i in range(24)]
    demand_df = pd.DataFrame(data, index=dates, columns=time_periods)
    demand_df = demand_df.sort_index()  # Sort by dates
    return demand_df

# Load the original demand data
if 'original_demand_df' not in st.session_state:
    st.session_state.original_demand_df = load_demand_data()

# Initialize a key for the data editor
if 'data_editor_key' not in st.session_state:
    st.session_state.data_editor_key = 0

# Set up the Streamlit app
st.title("Manage CSR Demands")
st.subheader("Edit Demands for Specific Days and Periods")

# Display the demand table with direct editing
edited_df = st.data_editor(
    st.session_state.original_demand_df,
    hide_index=False,
    key=f"demand_table_{st.session_state.data_editor_key}"
)

# Buttons to save or cancel changes
save_col, cancel_col, _ = st.columns([1, 1, 6.5])

with save_col:
    if st.button("Save"):
        # Update the database with the new values
        for date, row in edited_df.iterrows():
            demand_record = session.query(Demand).filter_by(date=date).first()
            if demand_record:
                demand_record.demand = row.tolist()
        session.commit()
        # Update the original data in session state
        st.session_state.original_demand_df = edited_df.copy()
        # Increment the key to force a refresh
        st.session_state.data_editor_key += 1
        st.rerun()

with cancel_col:
    if st.button("Cancel"):
        # Increment the key to force a refresh
        st.session_state.data_editor_key += 1
        st.rerun()

# Add the "Generate New Schedule" button
st.markdown("---")
if st.button("Generate New Schedule"):
    generate_schedule()
