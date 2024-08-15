from sqlalchemy import create_engine, Column, Integer, String, Date, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load database URL from config
from config import DATABASE_URL

# Create an engine and base
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the Users model
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)  # Required (primary key)
    name = Column(String)                        # Optional (defaults to nullable=True)
    email = Column(String)                       # Optional (defaults to nullable=True)
    role = Column(String)                        # Optional (defaults to nullable=True)

# Define Shift Definitions model
class ShiftDefinition(Base):
    __tablename__ = 'shift_definitions'
    shift_def_id = Column(Integer, primary_key=True)
    type = Column(String)  # Type of shift (e.g., "Morning", "Afternoon", "Night", "Leave")
    name = Column(String)  # Name or identifier for the shift (e.g., "0", "1", "2", etc.)
    periods = Column(JSON)  # JSON array representing the 30-minute intervals

# Define the CSR Shifts model
class Shift(Base):
    __tablename__ = 'shifts'
    shift_id = Column(Integer, primary_key=True)
    csr_id = Column(Integer, ForeignKey('users.user_id'))
    shift_def_id = Column(Integer, ForeignKey('shift_definitions.shift_def_id'))
    date = Column(Date)

# Define the Requests model
class Request(Base):
    __tablename__ = 'requests'
    request_id = Column(Integer, primary_key=True)
    csr_id = Column(Integer, ForeignKey('users.user_id'))
    shift_def_id = Column(Integer, ForeignKey('shift_definitions.shift_def_id'))  # Requested shift definition
    status = Column(String)
    requested_date = Column(Date)
    notes = Column(String)

# Define the Constraint model
class Constraint(Base):
    __tablename__ = 'constraints'
    id = Column(Integer, primary_key=True)
    
    # General Days Off Constraints
    min_days_off = Column(Integer)
    max_days_off = Column(Integer)
    min_days_off_in_period = Column(Integer)
    max_days_off_in_period = Column(Integer)
    exact_days_off_per_month = Column(Integer)
    
    # Morning Shifts Constraints
    min_morning_shifts = Column(Integer)
    max_morning_shifts = Column(Integer)
    min_morning_shifts_in_period = Column(Integer)
    max_morning_shifts_in_period = Column(Integer)
    
    # Afternoon Shifts Constraints
    min_afternoon_shifts = Column(Integer)
    max_afternoon_shifts = Column(Integer)
    min_afternoon_shifts_in_period = Column(Integer)
    max_afternoon_shifts_in_period = Column(Integer)
    
    # Night Shifts Constraints
    min_night_shifts = Column(Integer)
    max_night_shifts = Column(Integer)
    min_night_shifts_in_period = Column(Integer)
    max_night_shifts_in_period = Column(Integer)

# Define the Demand model with new format
class Demand(Base):
    __tablename__ = 'demands'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    demand = Column(ARRAY(Integer), nullable=False)  # Array of 24 integers


# Create all tables
Base.metadata.create_all(engine)