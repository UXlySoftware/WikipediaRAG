import mysql.connector

class MySQLDBTools:
    def check_wikirag_db(self):
        client = mysql.connector.connect(
            host="localhost",
            user="wikirag",
            password="wikirag123",
            database="wikirag"
        )
        cursor = client.cursor()
        cursor.execute("SHOW TABLES")
        tables = []
        print("Current tables in the database:")
        for table in cursor:
            tables.append(table[0])
            print(table)
        print("--------------------------------")
        for table in tables:
            cursor.execute("SELECT COUNT(*) FROM " + table)
            print(f"Number of rows in {table} table:", cursor.fetchone()[0])
            print("--------------------------------")

        cursor.close()
        client.close()
    def restart_revisions_table(self):
        client = mysql.connector.connect(
            host="localhost",
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
        
    def restart_wiki_users_table(self):
        client = mysql.connector.connect(
            host="localhost",
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

    def view_revisions_table(self):

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


    def view_wiki_users_table(self):
            # make sure you run the docker compose file before running this script

        client = mysql.connector.connect(
            host="localhost",
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


    

