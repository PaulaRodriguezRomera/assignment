import mysql.connector

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="our_user",
    password="password123",
    auth_plugin='mysql_native_password'
)

my_cursor = mydb.cursor()

# Check if the database 'our_user' already exists
my_cursor.execute("SHOW DATABASES")
databases = my_cursor.fetchall()
database_exists = any('our_user' in db for db in databases)

if not database_exists:
    # Create the 'our_user' database
    my_cursor.execute("CREATE DATABASE our_user")
    print("Database 'our_user' created.")
else:
    print("Database 'our_user' already exists.")

# Show all databases
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db[0])

# Close the cursor and connection
my_cursor.close()
mydb.close()
