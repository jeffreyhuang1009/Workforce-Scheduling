import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ShiftDefinition
from config import DATABASE_URL
from utility import generate_schedule  # Import the utility function

# Set up the database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Fetch shift definitions from the database
shift_definitions = session.query(ShiftDefinition).all()

# Create a DataFrame for shift definitions
data = []
for shift in shift_definitions:
    row = [False, shift.name, shift.type] + shift.periods
    data.append(row)

# Create time period labels
time_periods = [f"{9 + i//2:02}:{(i%2)*30:02}-{9 + (i+1)//2:02}:{((i+1)%2)*30:02}" for i in range(24)]
columns = ["Select", "Shift Name", "Shift Type"] + time_periods

shift_df = pd.DataFrame(data, columns=columns)

# Set up the Streamlit app
st.title("Manager's Shift Definitions")
st.subheader("Shift Definitions")

# Function to apply custom styles
def color_work_periods(val):
    return 'background-color: green' if val == 1 else 'background-color: transparent'

# Hide values by setting the text color to match the background color
def hide_values(val):
    return 'color: transparent' if val in [0, 1] else ''

# Apply styles to the DataFrame
styled_shift_df = shift_df.style.applymap(color_work_periods, subset=shift_df.columns[3:])
styled_shift_df = styled_shift_df.applymap(hide_values, subset=shift_df.columns[3:])

# Custom CSS to ensure the table fills the width and scrolls horizontally
st.markdown("""
<style>
    .dataframe {
        width: 100%;
    }
    .dataframe [data-testid="stHorizontalBlock"] {
        overflow-x: auto;
        white-space: nowrap;
    }
    .button-row .stButton > button {
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Display the styled DataFrame and collect the selected rows
edited_df = st.data_editor(
    shift_df,
    column_config={
        "Select": st.column_config.CheckboxColumn(
            label="Select",
            help="Select the shifts to delete",
            default=False
        )
    },
    hide_index=True,
    key="shift_table"
)

# Delete selected rows
if st.button("Delete Selected"):
    selected_indices = edited_df[edited_df["Select"] == True].index.tolist()
    if selected_indices:
        for index in selected_indices:
            shift_to_delete = session.query(ShiftDefinition).filter_by(name=edited_df.loc[index, "Shift Name"]).first()
            if shift_to_delete:
                session.delete(shift_to_delete)
                session.commit()
        st.rerun()

# Add new shift definition
if st.button("Add New Shift"):
    st.session_state.show_form = True

if st.session_state.get('show_form', False):
    st.subheader("New Shift Definition")
    
    new_shift_name = st.text_input("Shift Name", key="new_shift_name")
    new_shift_type = st.selectbox("Shift Type", ["Morning", "Afternoon", "Night", "Leave"], key="new_shift_type")
    
    # Display the new shift row for input using checkboxes in three columns
    cols = st.columns(4)
    checkbox_values = []
    for i, period in enumerate(time_periods):
        col = cols[i % 4]
        checkbox_values.append(col.checkbox(period, key=f"period_{i}"))

    # Collect the input values
    periods = [1 if st.session_state.get(f"period_{i}") else 0 for i in range(24)]

    # Create a row for the Save and Cancel buttons
    button_cols = st.columns([1, 9.6])
    with button_cols[0]:
        save_button = st.button("Save")
    with button_cols[1]:
        cancel_button = st.button("Cancel")

    if save_button:
        # Add the new shift definition to the database
        new_shift = ShiftDefinition(
            name=new_shift_name,
            type=new_shift_type,
            periods=periods
        )
        session.add(new_shift)
        session.commit()
        st.session_state.show_form = False  # Close the form immediately
        st.rerun()

    if cancel_button:
        # Clear form
        for key in list(st.session_state.keys()):
            if "period_" in key or key in ["new_shift_name", "new_shift_type", "show_form"]:
                del st.session_state[key]
        # Rerun the script to refresh the page immediately
        st.rerun()

# Add the "Generate New Schedule" button
st.markdown("---")
if st.button("Generate New Schedule"):
    generate_schedule()
