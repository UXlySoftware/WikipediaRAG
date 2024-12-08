import mysql.connector
import json
import os
class MySQLDBTools:
    def __init__(self):
        self.client = mysql.connector.connect(
            host=os.getenv("mysql_host"),
            user=os.getenv("mysql_user"),
            password=os.getenv("mysql_password"),
            database=os.getenv("mysql_database")
        )
    
    def view_schemas(self):
        client = self.client
        cursor = client.cursor()

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            schema = cursor.fetchone()
            print(f"Schema for {table_name}:")
            print(schema[1])
            print("\n")
        
        cursor.close()
        client.close()
    def check_wikirag_db(self):
        client = self.client
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
        client = self.client
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
        client = self.client
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
        client = self.client
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
        client = self.client
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

    def restart_articles_table(self):
        client = self.client
        cursor = client.cursor()
        # Drop the wikipedia_users table if it exists
        cursor.execute("DROP TABLE IF EXISTS articles")
        # Create the wikipedia_users table
        cursor.execute("""
        CREATE TABLE articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pageid INT,
            title VARCHAR(255),
            content MEDIUMTEXT
        )
        """)
        client.commit()
        cursor.close()
        client.close()

        print("Articles table recreated successfully")

    def view_articles_table(self):
        client = self.client
        cursor = client.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()    
        if len(rows) > 0:
            for row in rows:
                print(row)
        else:
            print("No rows found")
        cursor.close()
        client.close()

    def add_article_to_articles_table(self, pageid, title, content):
        # Convert content to a string if it's a dictionary
        if isinstance(content, dict):
            content = json.dumps(content)
        
        client = self.client
        cursor = client.cursor()
        cursor.execute("INSERT INTO articles (pageid, title, content) VALUES (%s, %s, %s)", (pageid, title, content))
        client.commit() 
        cursor.close()
        client.close()
        print("Article added to articles table successfully")
    
    def get_articles_table_data(self):
        client = self.client
        cursor = client.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        cursor.close()
        client.close()
        return rows