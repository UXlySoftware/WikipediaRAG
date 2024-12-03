import mysql.connector

# make sure you run the docker compose file before running this script

client = mysql.connector.connect(
    host="mysql_service",
    user="wikirag",
    password="wikirag123",
    database="wikirag"
)

cursor = client.cursor()

# Drop the revisions table if it exists
cursor.execute("DROP TABLE IF EXISTS revisions")

# Create the revisions table
cursor.execute("""
CREATE TABLE revisions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    page_id INT,
    page_title VARCHAR(255),
    revision_id VARCHAR(255),
    parent_revision_id INT,
    timestamp DATETIME,
    user VARCHAR(255),
    sha1 VARCHAR(255),
    text MEDIUMTEXT,
    comment VARCHAR(255),
    format VARCHAR(50)
)
""")

# Commit the changes
client.commit()

# Close the cursor and connection
cursor.close()
client.close()

print("Revisions table recreated successfully")