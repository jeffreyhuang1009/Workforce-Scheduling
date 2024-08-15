# utility.py
import streamlit as st
from schedule2 import main as generate_schedule_main

def generate_schedule():
    try:
        result = generate_schedule_main()  # Call the main function from schedule2.py
        
        if result == "OPTIMAL":
            st.success("Schedule generated successfully with all demands met!")
        elif result.startswith("SUBOPTIMAL"):
            total_lack = float(result.split(":")[1])
            st.warning(f"Schedule generated with unmet demands. Total lack: {total_lack}. Please review constraints and demands.")
        elif result == "INFEASIBLE":
            st.error("Failed to generate a feasible schedule. Please review constraints and demands.")
        else:
            st.error("Unexpected result from schedule generation.")
        
        # You might want to add a link to download the CSV file here
        st.info("The schedule has been saved as 'csr_schedule.csv'.")
        
    except Exception as e:
        st.error(f"Failed to generate schedule: {e}")