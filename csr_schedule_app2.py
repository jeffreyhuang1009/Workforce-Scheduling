import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ShiftDefinition
from config import DATABASE_URL

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

# Set up the database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Fetch shift definitions from the database
shift_definitions = session.query(ShiftDefinition).all()
shifts = {str(sd.name): sd.periods for sd in shift_definitions}  # Ensure shift names are strings

# Load the schedule data from the CSV file
schedule_df = pd.read_csv('csr_schedule.csv', index_col=0)

# Set up the Streamlit app
st.title("CSR Schedule Viewer")

# Create a selectbox for selecting a CSR with an initial empty option
csr_list = [""] + schedule_df.index.tolist()
selected_csr = st.selectbox("Select a CSR:", csr_list)

if selected_csr:
    # Display the schedule for the selected CSR in a table format
    st.subheader(f"Schedule for {selected_csr}")
    st.dataframe(schedule_df.loc[selected_csr].to_frame().T)

    # Function to generate a visual representation of the shifts
    def generate_shift_heatmap(csr_schedule):
        # Create a DataFrame to hold the shift schedule
        days = csr_schedule.index.tolist()
        heatmap_data = []

        for day in days:
            shift_name = str(csr_schedule[day])  # Convert to string to ensure correct lookup
            if shift_name not in shifts:
                st.error(f"Shift Name {shift_name} not found in shifts dictionary")
                return
            shift_pattern = shifts[shift_name]
            heatmap_data.append(shift_pattern)

        time_labels = [f'{hour:02}:{minute:02}' for hour in range(9, 21) for minute in (0, 30)]
        heatmap_df = pd.DataFrame(heatmap_data, index=days, columns=time_labels)

        # Create a custom colormap
        cmap = LinearSegmentedColormap.from_list("custom_cmap", ["gray", "green"], N=2)

        plt.figure(figsize=(15, 10))
        sns.heatmap(heatmap_df, cmap=cmap, cbar=False, linewidths=.5)
        plt.title(f'Shift Schedule for {selected_csr}')
        plt.xlabel('Time')
        plt.ylabel('Day')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        st.pyplot(plt)

    # Display the shift schedule in a heatmap
    generate_shift_heatmap(schedule_df.loc[selected_csr])

# Option to download the schedule as a CSV file
csv = schedule_df.to_csv().encode('utf-8')
st.download_button(
    label="Download full schedule as CSV",
    data=csv,
    file_name='csr_schedule.csv',
    mime='text/csv',
)

# Shift Definitions Table at the end of the page
shift_columns = ["Shift Name"] + [f"{9 + i//2:02}:{(i%2)*30:02}-{9 + (i+1)//2:02}:{((i+1)%2)*30:02}" for i in range(24)]
shift_data = []
for shift_name, periods in shifts.items():
    shift_data.append([shift_name] + periods)

shift_definitions_df = pd.DataFrame(shift_data, columns=shift_columns)

# Function to apply custom styles and hide values
def color_work_periods(val):
    if val == 1:
        return 'background-color: green; color: transparent'
    else:
        return 'background-color: transparent; color: transparent'

# Apply styles to the DataFrame using Styler
styled_shift_definitions_df = shift_definitions_df.style.map(color_work_periods, subset=shift_columns[1:])

# Display the styled table at the end of the page
st.markdown("### Shift Definitions Table")
st.dataframe(styled_shift_definitions_df)
