import mysql.connector

# make sure you run the docker compose file before running this script

client = mysql.connector.connect(
    host="localhost",
    user="wikirag",
    password="wikirag123",
    database="wikirag"
)

cursor = client.cursor()

# show all rows in revisions table  
cursor.execute("SELECT * FROM revisions")

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
