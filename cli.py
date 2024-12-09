import click
from wikimediaAPI.wikimediaAPIClasses import WikimediaAPI
from mysqlDatabaseTools.mysqlDBToolsClasses import MySQLDBTools
from milvus.milvusClasses import MilvusDBTools
import subprocess
from pprint import pprint
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

# OLLAMA COMMANDS
## use "python3 cli.py ollama [command]" to run a ollama command

@cli.group(help="Milvus vector db commands.")
def milvus():
    pass

@milvus.command(help="Starts the milvus vector db.")
def start():
    api = MilvusDBTools()
    api.start_milvus()

@milvus.command(help="Embeds the articles table data.")
def embed_articles_table():
    api = MilvusDBTools()
    api.embed_articles_table()

@milvus.command(help="Checks the state of the Milvus collections.")
def check_collections():
    api = MilvusDBTools()
    api.check_milvus_collections()

@milvus.command(help="Restarts the Milvus collections.")
def restart_collections():
    api = MilvusDBTools()
    api.restart_milvus_collections()

@milvus.command(help="Run a rag query on the articles collection.")
@click.argument('user_query')
def rag_query_articles(user_query):
    api = MilvusDBTools()
    api.rag_query_articles(user_query)

@milvus.command(help="Embeds the revisions table data.")
def embed_revs():
    api = MilvusDBTools()
    api.embed_revisions()

@milvus.command(help="Logs the revision vectors.")
def log_rev_vectors():
    api = MilvusDBTools()
    api.log_rev_vectors()

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

@database.command(help="Restarts the articles table.")
def restart_articles_table():
    api = MySQLDBTools()
    api.restart_articles_table()

@database.command(help="Views the revisions table.")
def view_revisions_table():
    api = MySQLDBTools()
    api.view_revisions_table()

@database.command(help="Views the wikipedia_users table.")
def view_wiki_users_table():
    api = MySQLDBTools()
    api.view_wiki_users_table()

@database.command(help="Views the articles table.")
def view_articles_table():
    api = MySQLDBTools()
    api.view_articles_table()
    
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
    result = api.fetch_limited_revisions_by_title(page_title, limit)
    with open("wikimediaAPI/result_log.txt", "w") as log_file:
        pprint(result, log_file)
    print("Result logged to wikimediaAPI/result_log.txt")
    

@wikimedia.command(help="Fetches all revisions for a given page title. Arguments: title")
@click.argument('title')
def fetch_all_revisions_by_title(title):
    """Fetches all revisions for a given page title. Arguments: title"""
    api = WikimediaAPI()
    revisions = api.fetch_all_revisions_by_title(title)
    print(revisions)

@wikimedia.command(help="Fetches articles by topic and adds them to the database. Arguments: topic")
@click.argument('category')
@click.argument('limit', type=int)
def fetch_articles_by_category(category, limit):
    """Fetches articles by category and adds them to the database. Arguments: category, limit"""
    api = WikimediaAPI()
    result = api.fetch_articles_by_category(category, limit)
    
    # Filter articles with namespace 0
    articles = [item for item in result['query']['categorymembers'] if item['ns'] == 0]
    
    # Fetch content for each article
    for article in articles:
        pageid = article['pageid']
        content = api.fetch_article_content(pageid)
        article['content'] = content
        
        # Print only the title and content
        print(f"Title: {article['title']}")
        print(f"Content: {article['content']}")
        print("--------------------------------")

@wikimedia.command(help="Fetches articles by category and adds them to the database. Arguments: category, limit")
@click.argument('category')
@click.argument('limit', type=int)
def fetch_articles_by_category_to_db(category, limit):
    """Fetches articles by category and adds them to the database. Arguments: category, limit"""
    api = WikimediaAPI()
    api.add_articles_to_articles_table_by_category(category, limit)

@wikimedia.command(help="Fetches categories for a given page title. Arguments: title")
@click.argument('page_title')
def fetch_page_categories(page_title):
    """Fetches categories for a given page title. Arguments: page_title"""
    api = WikimediaAPI()
    result = api.fetch_page_categories(page_title)
    pprint(result)

@wikimedia.command(help="Fetches article content by title and adds it to the articles table. Arguments: title")
@click.argument('title')
def article_by_title_to_db(title):
    """Fetches article content by title and adds it to the articles table. Arguments: title"""
    api = WikimediaAPI()
    api.add_articles_by_title_to_articles_table(title)

@wikimedia.command(help="Fetches revisions by article title and adds them to the revisions table. Arguments: title")
@click.argument('title')
@click.argument('limit', type=int)
def add_revs_by_title(title, limit):
    """Fetches revisions by article title and adds them to the revisions table. Arguments: title"""
    api = WikimediaAPI()
    api.add_revs_to_revs_table_by_article_title(title, limit)

if __name__ == "__main__":
    cli() 