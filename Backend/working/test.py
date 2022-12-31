from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.engine import Inspector
# Create a connection to the database
engine = create_engine('mysql://root:root@localhost/FIVER')

# Create a MetaData object
metadata = MetaData()

# Define the table structure
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('email', String(100))
)

# Create the table
metadata.create_all(engine)

connection = engine.connect()

# Create an Inspector object
inspector = Inspector.from_engine(engine)

# Get the list of table names in the database
table_names = inspector.get_table_names()

# Check if the table you want to check for exists in the list of table names
if 'movie' in table_names:
    print("Table exists")
else:
    print("Table does not exist")

# Close the connection
connection.close()
