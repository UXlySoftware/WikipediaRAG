import mysql.connector

# make sure you run the docker compose file before running this script

client = mysql.connector.connect(
    host="localhost",
    user="wikirag",
    password="wikirag123",
    database="wikirag"
)

cursor = client.cursor()

# show current tables
cursor.execute("SHOW TABLES")

tables = []

print("Current tables in the database:")
for table in cursor:
    tables.append(table[0])
    print(table)

print("--------------------------------")


# check number of rows in each table
for table in tables:        
    cursor.execute("SELECT COUNT(*) FROM " + table)
    print(f"Number of rows in {table[0]} table:", cursor.fetchone()[0]) 
    print("--------------------------------")


# close the cursor and connection
cursor.close()
client.close()