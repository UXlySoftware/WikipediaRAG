import click
from wikimediaAPI.wikimediaAPIClasses import WikimediaAPI

#GETTING STARTED
# use "python3 cli.py --help" to see all commands
# use "python3 cli.py <command> --help" to see arguments for a specific command

@click.group()
def cli():
    pass

@cli.command(help="Lists all commands and their arguments.")
def list_commands():
    commands = {
        "fetch_revision_metadata": "user_name, title",
        "fetch_revisions_by_user": "user_name, limit",
        "fetch_revision": "rev_id",
        "fetch_limited_revisions": "page_title, limit",
        "fetch_revisions": "title"
    }
    for command, args in commands.items():
        print(f"{command}: {args}")

@cli.command(help="Fetches revision metadata by user and title. Arguments: user_name, title")
@click.argument('user_name')
@click.argument('title')
def fetch_revision_metadata(user_name, title):
    """Fetches revision metadata by user and title. Arguments: user_name, title"""
    api = WikimediaAPI()
    result = api.fetch_revision_metadata_by_user_and_title(user_name, title)
    print(result)

@cli.command(help="Fetches revisions by username with a limit. Arguments: user_name, limit")
@click.argument('user_name')
@click.argument('limit', type=int)
def fetch_revisions_by_user(user_name, limit):
    """Fetches revisions by username with a limit. Arguments: user_name, limit"""
    api = WikimediaAPI()
    result = api.fetch_revisions_by_username(user_name, limit)
    print(result)

@cli.command(help="Fetches a revision by its ID. Arguments: rev_id")
@click.argument('rev_id', type=int)
def fetch_revision(rev_id):
    """Fetches a revision by its ID. Arguments: rev_id"""
    api = WikimediaAPI()
    result = api.fetch_revision_by_id(rev_id)
    print(result)

@cli.command(help="Fetches limited revisions by page title. Arguments: page_title, limit")
@click.argument('page_title')
@click.argument('limit', type=int)
def fetch_limited_revisions(page_title, limit):
    """Fetches limited revisions by page title. Arguments: page_title, limit"""
    api = WikimediaAPI()
    result = api.fetch_limited_revisions_by_title(page_title, limit)
    print(result)

@cli.command(help="Fetches all revisions for a given page title. Arguments: title")
@click.argument('title')
def fetch_revisions(title):
    """Fetches all revisions for a given page title. Arguments: title"""
    api = WikimediaAPI()
    revisions = api.fetch_all_revisions_by_title(title)
    print(revisions)

@cli.command(help="Fetches revisions by username. Arguments: user_name, limit")
@click.argument('user_name')
@click.argument('limit', type=int)
def fetch_revisions_by_username(user_name, limit):
    """Fetches revisions by username. Arguments: user_name, limit"""
    api = WikimediaAPI()
    result = api.fetch_revisions_by_username(user_name, limit)
    print(result)

@cli.command(help="Fetches a revision by its ID. Arguments: rev_id")
@click.argument('rev_id', type=int)
def fetch_revision_by_id(rev_id):
    """Fetches a revision by its ID. Arguments: rev_id"""
    api = WikimediaAPI()
    result = api.fetch_revision_by_id(rev_id)
    print(result)


if __name__ == "__main__":
    cli()    
