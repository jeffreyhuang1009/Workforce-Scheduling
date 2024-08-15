import pulp
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ShiftDefinition, Demand, Constraint
from config import DATABASE_URL

def main():
    # Set up the database connection
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Number of CSRs
    num_csrs = 40

    # Fetch shift definitions, demand records, and constraints from the database
    shift_definitions = session.query(ShiftDefinition).all()
    demand_records = session.query(Demand).all()
    constraints = session.query(Constraint).first()  # Assuming there's only one set of constraints

    # Define the shifts from the ShiftDefinition table
    shifts = {sd.shift_def_id: sd.periods for sd in shift_definitions}

    # Define the demand from the Demand table
    demand = {dr.date.day: dr.demand for dr in demand_records}

    # Initialize the problem
    prob = pulp.LpProblem("CSR_Scheduling", pulp.LpMinimize)

    # Map shift_def_id to continuous indices
    shift_id_to_index = {shift_def.shift_def_id: idx for idx, shift_def in enumerate(shift_definitions)}

    # Define decision variables
    # x[i][j][k] = 1 if CSR i is assigned to shift j on day k, 0 otherwise
    x = [[[pulp.LpVariable(f"x_{i}_{j}_{k}", cat='Binary') for k in range(31)] for j in shift_id_to_index.values()] for i in range(num_csrs)]

    # Define auxiliary variables for lack amount
    lack = [[pulp.LpVariable(f"lack_{k}_{t}", lowBound=0, cat='Continuous') for t in range(24)] for k in range(31)]

    # Define the objective function
    # Minimize the total lack amount
    prob += pulp.lpSum([lack[k][t] for k in range(31) for t in range(24)])

    # Add constraints for the lack amount
    for k in range(31):
        for t in range(24):
            prob += lack[k][t] >= demand[k+1][t] - pulp.lpSum([x[i][shift_id_to_index[j]][k] * shifts[j][t] for i in range(num_csrs) for j in shifts.keys()])

    # Constraint 1: Each CSR is assigned to exactly one shift per day
    for i in range(num_csrs):
        for k in range(31):
            prob += pulp.lpSum([x[i][j][k] for j in shift_id_to_index.values()]) == 1

    # Constraint 2: Each CSR gets exactly 8 days off per month
    leave_shift_index = shift_id_to_index[min(shift_id_to_index.keys())]  # Assuming the first shift definition is for 'leave'
    for i in range(num_csrs):
        prob += pulp.lpSum([x[i][leave_shift_index][k] for k in range(31)]) == constraints.exact_days_off_per_month

    # Define shift types based on the shift definitions
    morning_shifts = [shift.shift_def_id for shift in shift_definitions if shift.type == "Morning"]
    afternoon_shifts = [shift.shift_def_id for shift in shift_definitions if shift.type == "Afternoon"]
    night_shifts = [shift.shift_def_id for shift in shift_definitions if shift.type == "Night"]
    leave_shifts = [shift.shift_def_id for shift in shift_definitions if shift.type == "Leave"]

    # Convert to indices
    morning_shifts_indices = [shift_id_to_index[id] for id in morning_shifts]
    afternoon_shifts_indices = [shift_id_to_index[id] for id in afternoon_shifts]
    night_shifts_indices = [shift_id_to_index[id] for id in night_shifts]
    leave_shift_index = shift_id_to_index[leave_shifts[0]]  # Assuming there's only one leave shift

    # Assume 31 days for now
    num_days = 31

    # Constraint 3: At most one night shift in every seven consecutive days
    for i in range(num_csrs):
        for k in range(num_days - constraints.max_night_shifts_in_period + 1):
            prob += pulp.lpSum([x[i][j][k + m] for j in night_shifts_indices for m in range(constraints.max_night_shifts_in_period) if k + m < num_days]) <= constraints.max_night_shifts

    # Constraint 4: At most two afternoon shifts in every seven consecutive days
    for i in range(num_csrs):
        for k in range(num_days - constraints.max_afternoon_shifts_in_period + 1):
            prob += pulp.lpSum([x[i][j][k + m] for j in afternoon_shifts_indices for m in range(constraints.max_afternoon_shifts_in_period) if k + m < num_days]) <= constraints.max_afternoon_shifts

    # Constraint 5: At least one day off in every seven consecutive working days
    for i in range(num_csrs):
        for k in range(num_days - constraints.max_days_off_in_period + 1):
            prob += pulp.lpSum([x[i][j][k + m] for j in shift_id_to_index.values() if j != leave_shift_index for m in range(constraints.max_days_off_in_period) if k + m < num_days]) <= (constraints.max_days_off_in_period - 1)

    # Create index_to_shift_name mapping
    index_to_shift_name = {idx: shift_definitions[idx].name for idx in range(len(shift_definitions))}

    # Number of unique shifts
    num_shifts = len(shift_definitions)

    # Solve the optimization problem
    prob.solve()

    # Print the status of the solution
# schedule2.py

import pulp
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ShiftDefinition, Demand, Constraint
from config import DATABASE_URL

def main():
    # Set up the database connection
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Number of CSRs
    num_csrs = 40

    # Fetch shift definitions, demand records, and constraints from the database
    shift_definitions = session.query(ShiftDefinition).all()
    demand_records = session.query(Demand).all()
    constraints = session.query(Constraint).first()  # Assuming there's only one set of constraints

    # Define the shifts from the ShiftDefinition table
    shifts = {sd.shift_def_id: sd.periods for sd in shift_definitions}

    # Define the demand from the Demand table
    demand = {dr.date.day: dr.demand for dr in demand_records}

    # Initialize the problem
    prob = pulp.LpProblem("CSR_Scheduling", pulp.LpMinimize)

    # Map shift_def_id to continuous indices
    shift_id_to_index = {shift_def.shift_def_id: idx for idx, shift_def in enumerate(shift_definitions)}

    # Define decision variables
    x = [[[pulp.LpVariable(f"x_{i}_{j}_{k}", cat='Binary') for k in range(31)] for j in shift_id_to_index.values()] for i in range(num_csrs)]

    # Define auxiliary variables for lack amount
    lack = [[pulp.LpVariable(f"lack_{k}_{t}", lowBound=0, cat='Continuous') for t in range(24)] for k in range(31)]

    # Define the objective function
    prob += pulp.lpSum([lack[k][t] for k in range(31) for t in range(24)])

    # Add constraints for the lack amount
    for k in range(31):
        for t in range(24):
            prob += lack[k][t] >= demand[k+1][t] - pulp.lpSum([x[i][shift_id_to_index[j]][k] * shifts[j][t] for i in range(num_csrs) for j in shifts.keys()])

    # Constraint 1: Each CSR is assigned to exactly one shift per day
    for i in range(num_csrs):
        for k in range(31):
            prob += pulp.lpSum([x[i][j][k] for j in shift_id_to_index.values()]) == 1

    # Constraint 2: Each CSR gets exactly 8 days off per month
    leave_shift_index = shift_id_to_index[min(shift_id_to_index.keys())]
    for i in range(num_csrs):
        prob += pulp.lpSum([x[i][leave_shift_index][k] for k in range(31)]) == constraints.exact_days_off_per_month

    # Define shift types based on the shift definitions
    morning_shifts = [shift.shift_def_id for shift in shift_definitions if shift.type == "Morning"]
    afternoon_shifts = [shift.shift_def_id for shift in shift_definitions if shift.type == "Afternoon"]
    night_shifts = [shift.shift_def_id for shift in shift_definitions if shift.type == "Night"]
    leave_shifts = [shift.shift_def_id for shift in shift_definitions if shift.type == "Leave"]

    # Convert to indices
    morning_shifts_indices = [shift_id_to_index[id] for id in morning_shifts]
    afternoon_shifts_indices = [shift_id_to_index[id] for id in afternoon_shifts]
    night_shifts_indices = [shift_id_to_index[id] for id in night_shifts]
    leave_shift_index = shift_id_to_index[leave_shifts[0]]

    num_days = 31

    # Constraint 3: At most one night shift in every seven consecutive days
    for i in range(num_csrs):
        for k in range(num_days - constraints.max_night_shifts_in_period + 1):
            prob += pulp.lpSum([x[i][j][k + m] for j in night_shifts_indices for m in range(constraints.max_night_shifts_in_period) if k + m < num_days]) <= constraints.max_night_shifts

    # Constraint 4: At most two afternoon shifts in every seven consecutive days
    for i in range(num_csrs):
        for k in range(num_days - constraints.max_afternoon_shifts_in_period + 1):
            prob += pulp.lpSum([x[i][j][k + m] for j in afternoon_shifts_indices for m in range(constraints.max_afternoon_shifts_in_period) if k + m < num_days]) <= constraints.max_afternoon_shifts

    # Constraint 5: At least one day off in every seven consecutive working days
    for i in range(num_csrs):
        for k in range(num_days - constraints.max_days_off_in_period + 1):
            prob += pulp.lpSum([x[i][j][k + m] for j in shift_id_to_index.values() if j != leave_shift_index for m in range(constraints.max_days_off_in_period) if k + m < num_days]) <= (constraints.max_days_off_in_period - 1)

    # Create index_to_shift_name mapping
    index_to_shift_name = {idx: shift_definitions[idx].name for idx in range(len(shift_definitions))}

    # Number of unique shifts
    num_shifts = len(shift_definitions)

    # Solve the optimization problem
    prob.solve()

    # Get the status of the solution
    status = pulp.LpStatus[prob.status]
    print(f"Status: {status}")

    if status == 'Optimal':
        # Check if all demands are met
        demand_met = True
        total_lack = 0
        tolerance = 1e-6  # Small tolerance to account for floating-point errors
        for k in range(31):
            for t in range(24):
                lack_value = pulp.value(lack[k][t])
                if lack_value > tolerance:
                    demand_met = False
                    total_lack += lack_value
                    print(f"Unmet demand on day {k+1}, hour {t}: {lack_value}")

        if demand_met:
            result = "OPTIMAL"
            print("Success: Optimal solution found with all demands met.")
        else:
            result = f"SUBOPTIMAL:{total_lack}"
            print(f"Warning: Suboptimal solution. Not all demands are met. Total lack: {total_lack}")

        # Extract the results into a schedule array
        schedule = np.zeros((num_csrs, 31), dtype=int)

        for i in range(num_csrs):
            for j in range(num_shifts):
                for k in range(31):
                    if pulp.value(x[i][j][k]) == 1:
                        schedule[i][k] = j

        # Convert the indices to shift names
        schedule_names = np.array([[index_to_shift_name[shift] for shift in csr] for csr in schedule])

        # Create a DataFrame for the schedule
        schedule_df = pd.DataFrame(schedule_names, columns=[f'Day {k}' for k in range(1, 32)])
        schedule_df.index = [f'CSR {i+1}' for i in range(num_csrs)]

        # Print the schedule for verification
        print(schedule_df)

        # Save the schedule to a CSV file
        schedule_df.to_csv('csr_schedule.csv', index=True)
        print("Schedule saved to 'csr_schedule.csv'")
    else:
        result = "INFEASIBLE"
        print("No feasible solution found.")

    return result

if __name__ == '__main__':
    result = main()
    print(f"Result: {result}")