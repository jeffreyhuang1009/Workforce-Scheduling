import streamlit as st
import pandas as pd

# Home Page Content
st.title("Welcome to the Scheduling App")

st.write("""
This app helps you manage your company's shift schedules and demands efficiently.
Use the navigation menu on the left to access different features.
""")

st.markdown("### Available Features:")
st.markdown("- **Shift Definitions:** Define and manage shifts.")
st.markdown("- **Demand Management:** Set and manage demand for shifts.")
st.markdown("- **Constraint Management:** Edit constraints for shifts.")
st.markdown("More features will be added soon!")

# Load the CSR schedule from the CSV file
schedule_df = pd.read_csv('csr_schedule.csv', index_col=0)

# Display the CSR schedule at the bottom of the page
st.markdown("### Current Shift Schedule for CSRs")
st.dataframe(schedule_df)
