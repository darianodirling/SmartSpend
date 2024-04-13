from sqlalchemy import create_engine, MetaData, select, column, Float
import os

script_directory = os.path.dirname(os.path.abspath(__file__))

database_path = os.path.join(script_directory, 'instance', 'database.db')

engine = create_engine('sqlite:///' + database_path)

metadata = MetaData()

metadata.reflect(bind=engine)

table_names = metadata.tables.keys()

print("Table Names:")
for table_name in table_names:
    print(table_name)

user_table = metadata.tables['user']

connection = engine.connect()

# Select all usernames from the user table
select_query = select(user_table.columns.username)

# Execute the query
result = connection.execute(select_query)

# Fetch all the usernames
usernames = result.fetchall()

print ("\nUsernames:")
for username in usernames:
    print(username[0])

# Get the user table
user_table = metadata.tables['expense']

# Create a connection
connection = engine.connect()

# Select all savings from the user table
select_query = select(user_table.columns.owner)

# Execute the query
result = connection.execute(select_query)

# Fetch all the usernames
usernames = result.fetchall()

print ("\nSavings:")
for username in usernames:
    print(username[0])

