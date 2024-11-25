import click
from wikimediaAPI.wikimediaAPIClasses import WikimediaAPI
from mysqlDatabaseTools.mysqlDBToolsClasses import MySQLDBTools
from milvus.milvusClasses import MilvusDBTools
import subprocess

#GETTING STARTED
## use "python3 cli.py --help" to see all commands

@click.group()
def cli():
    pass

# STARTING THE STACK
## use "python3 cli.py start [command]" to run a start command

@cli.group(help="Manage docker stack.")
def docker():
    pass

@docker.command(help="Use the first time to pull images.")
def first_start():
    # Pull the latest images
    subprocess.run(["docker", "compose", "pull"], check=True)
    
    # Start the stack
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    
    # Configure ollama with a model
    subprocess.run(["python3", "primeollama.py"], check=True)
   
@docker.command(help="Restart the stack.") 
def restart():
    
    # Start the stack
    subprocess.run(["docker", "compose", "up", "-d"], check=True)

     # Configure ollama with a model
    subprocess.run(["python3", "primeollama.py"], check=True)

# MILVUS VECTOR DB COMMANDS
## use "python3 cli.py milvus [command]" to run a milvus command

@cli.group(help="Milvus vector db commands.")
def milvus():
    pass

@milvus.command(help="Starts the milvus vector db.")
def start():
    api = MilvusDBTools()
    api.start_milvus()

# MYSQL DATABASE COMMANDS
## use "python3 cli.py database [command]" to run a database command

@cli.group(help="Database management commands.")
def database():
    pass

@database.command(help="Views table schemas for all tables.")
def view_schemas():
    api = MySQLDBTools()
    api.view_schemas()

@database.command(help="Checks current state of the database.")
def check_wikirag_db():
    api = MySQLDBTools()
    api.check_wikirag_db()

@database.command(help="Restarts the revisions table.")
def restart_revisions_table():
    api = MySQLDBTools()
    api.restart_revisions_table()

@database.command(help="Restarts the wikipedia_users table.")
def restart_wiki_users_table():
    api = MySQLDBTools()
    api.restart_wiki_users_table()

@database.command(help="Views the revisions table.")
def view_revisions_table():
    api = MySQLDBTools()
    api.view_revisions_table()

@database.command(help="Views the wikipedia_users table.")
def view_wiki_users_table():
    api = MySQLDBTools()
    api.view_wiki_users_table()
    
# WIKIMEDIA API COMMANDS
## use "python3 cli.py wikimedia [command]" to run a wikimedia api command

@cli.group(help="Wikimedia API commands.")
def wikimedia():
    pass

@wikimedia.command(help="Fetches revision metadata by user and title. Arguments: user_name, title")
@click.argument('user_name')
@click.argument('title')
def fetch_revision_metadata(user_name, title):
    """Fetches revision metadata by user and title. Arguments: user_name, title"""
    api = WikimediaAPI()
    result = api.fetch_revision_metadata_by_user_and_title(user_name, title)
    print(result)

@wikimedia.command(help="Fetches revisions by username with a limit. Arguments: user_name, limit")
@click.argument('user_name')
@click.argument('limit', type=int)
def fetch_revisions_by_username(user_name, limit):
    """Fetches revisions by username with a limit. Arguments: user_name, limit"""
    api = WikimediaAPI()
    result = api.fetch_revisions_by_username(user_name, limit)
    print(result)

@wikimedia.command(help="Fetches a revision by its ID. Arguments: rev_id")
@click.argument('rev_id', type=int)
def fetch_revision_by_id(rev_id):
    """Fetches a revision by its ID. Arguments: rev_id"""
    api = WikimediaAPI()
    result = api.fetch_revision_by_id(rev_id)
    print(result)

@wikimedia.command(help="Fetches limited revisions by page title. Arguments: page_title, limit")
@click.argument('page_title')
@click.argument('limit', type=int)
def fetch_limited_revs_by_title(page_title, limit):
    """Fetches limited revisions by page title. Arguments: page_title, limit"""
    api = WikimediaAPI()
    result = api.fetch_limited_revs_by_title(page_title, limit)
    print(result)

@wikimedia.command(help="Fetches all revisions for a given page title. Arguments: title")
@click.argument('title')
def fetch_all_revisions_by_title(title):
    """Fetches all revisions for a given page title. Arguments: title"""
    api = WikimediaAPI()
    revisions = api.fetch_all_revisions_by_title(title)
    print(revisions)

if __name__ == "__main__":
    cli()    
