# Import necessary modules and functions from SQLAlchemy and the os module
from sqlalchemy.ext.declarative import declarative_base  # Base class for declarative class definitions
from sqlalchemy import create_engine  # Function to create a new SQLAlchemy engine instance
from sqlalchemy.orm import sessionmaker  # Function to create a new session factory
import os  # Module to interact with the operating system, useful for accessing environment variables

# Get the database URL from the environment variables
DATABASE_URL = os.getenv("POSTGRES_URL")
print("DATABASE_URL", DATABASE_URL)  # Debugging print statement to verify the retrieved database URL

# Create an SQLAlchemy engine that will manage the connection to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create a session factory, which will be used to create new database sessions
# - autocommit=False: Transactions need to be explicitly committed
# - autoflush=False: Changes to the database won't be automatically flushed (written) to the database
# - bind=engine: Binds the session to the engine created above
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models; this is used to define database tables in SQLAlchemy
Base = declarative_base()

#below code was used to create db instance outside docker
# from dotenv import load_dotenv
# import os
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# load_dotenv()  # Load environment variables from .env file

# DATABASE_URL = os.getenv("POSTGRES_URL")
# print("DATABASE_URL", DATABASE_URL)
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
