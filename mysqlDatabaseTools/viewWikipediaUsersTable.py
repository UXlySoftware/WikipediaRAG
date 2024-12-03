import mysql.connector

# make sure you run the docker compose file before running this script

client = mysql.connector.connect(
    host="mysql_service",
    user="wikirag",
    password="wikirag123",
    database="wikirag"
)

cursor = client.cursor()

# show all rows in wikipedia_users table  
cursor.execute("SELECT * FROM wikipedia_users")

# print the rows if rows are greater than 0, else return "No rows found"
rows = cursor.fetchall()

if len(rows) > 0:
    for row in rows:
        print(row)
else:
    print("No rows found")

# close the cursor and connection
cursor.close()
client.close()
