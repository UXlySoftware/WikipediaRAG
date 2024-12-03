import mysql.connector

# make sure you run the docker compose file before running this script

client = mysql.connector.connect(
    host="mysql_service",
    user="wikirag",
    password="wikirag123",
    database="wikirag"
)

cursor = client.cursor()

# Drop the wikipedia_users table if it exists
cursor.execute("DROP TABLE IF EXISTS wikipedia_users")

# Create the wikipedia_users table
cursor.execute("""
CREATE TABLE wikipedia_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(255),
    revision_ids JSON
)
""")

# Commit the changes
client.commit()

# Close the cursor and connection
cursor.close()
client.close()

print("Wikipedia users table recreated successfully")