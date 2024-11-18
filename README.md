# WikipediaRAG
Retrieval Augmented Generation (RAG) project for Wikipedia revisions

## Requirements

You'll need Docker Desktop installed on you machine. 

## Running the stack

To start the RAG, run the following commands:

```sh
docker compose pull
docker compose up -d
```

To tear down the stack, run:

```sh
docker compose down
```

## Startup

After you've started the stack with `docker compose`, you'll need to configure ollama with a model:

```sh
python3 primeollama.py
```

This will pull an embedding model that can be used for creating vector embeddings of text. 

Test the embedding model like this:

```sh
python3 test.py
```

## directly querying the mysql database 

After startup of the stack, you can directly query the mysql database with the following command:

```sh
docker exec -it mysql_service mysql -u wikirag -p
```
Enter password: wikirag123
```

Then you can query the database with the following command:

```sh
USE wikirag; SHOW TABLES;
```

View the wikirag database:

```sh
USE wikirag; SELECT * FROM revisions;
```

Show revisions table schema:

```sh
USE wikirag; DESCRIBE revisions;
```
## Milvus

clear the revisions_collection in Milvus:

```sh
python3 milvus/startmilvus.py
```

### Milvus queries from CLI

install Milvs CLI client

```sh
pip install milvus-cli
```
connect to milvus

```sh
milvus-cli connect --host localhost --port 19530
```


## Demo instructions 

1. start the stack 
    ```sh
    docker compose up -d
    ```

2. wipe mysql database

    ```sh
    docker exec -it mysql_service mysql -u wikirag -p
    ```
    USE wikirag; DELETE FROM revisions;
    ```

3. clear Milvus collection

    ```sh
    python3 milvus/startmilvus.py
    ```

4. pull revisions from xml file to mysql database 

    ```sh
    python3 pullxml.py
    ```

    3.1 (optional) check number of revisions in mysql database
        in the mysql container 

        ```sh
        USE wikirag; SELECT COUNT(*) FROM revisions;
        ```

5. create embeddings and insert into Milvus

    ```sh
    python3 milvus/vectorsollama.py
    ```
6. query Milvus to show vectors

    ```sh
    python3 milvus/testquery.py
    ```
7. (optional) show rag chat demo 

    ```sh
    python3 wikiragdemo.py
    ```

## Wikimedia API

https://en.wikipedia.org/w/api.php?action=query


### prop=revisions: Requests revision data for the specified page(s).


    Additional Paramaters for revisions:
        - titles:	A pipe-separated list of page titles to query (e.g., Donkey_Kong_Country).
        - revids:   	A pipe-separated list of specific revision IDs to query (e.g., `123456
        - rvlimit:	The maximum number of revisions to return per page (default: 10, max: 50 for anonymous users, 500 for logged-in users).
        - rvstart	Start querying from this timestamp (ISO 8601 format, e.g., 2024-01-01T00:00:00Z).
        - rvend	End querying at this timestamp (ISO 8601 format).
        - rvstartid	Start querying from this revision ID.
        - rvendid	End querying at this revision ID.
        - rvdir	Direction to query revisions:
            - newer: Oldest to newest.
            - older (default): Newest to oldest.
        - rvprop	Properties of each revision to retrieve (pipe-separated list):
            - ids: Includes the revision ID and parent ID.
            - flags: Includes flags like minor for minor edits.
            - timestamp: Includes the revision timestamp.
            - user: Includes the username of the contributor.
            - userid: Includes the user ID of the contributor.
            - size: Includes the size of the revision in bytes.
            - slotsize: Includes the size of content slots.
            - sha1: Includes the SHA-1 hash of the revision content.
            - contentmodel: Includes the content model (e.g., wikitext, json).
            - comment: Includes the edit summary.
            - parsedcomment: Includes a pre-parsed version of the edit summary for HTML display.
            - tags: Includes tags applied to the revision (e.g., mobile edit, visual editor).
            - content: Includes the full revision text content in its raw format.
            - roles: Includes content role information for the revision (if supported by the wiki).
        - rvslots	Specifies which content slots to query (e.g., main for the primary content).
        - rvcontentformat	Requests content in a specific format (e.g., application/json, text/x-wiki).

    Example use cases:
        Retrive basic revision metadata for a page:
            https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Donkey_Kong_Country&rvlimit=50&rvprop=ids|timestamp|user|comment|size|content&format=json
        Retrive full revision content by article title:
            https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Donkey_Kong_Country&rvlimit=1&rvprop=content&format=json
        Query revisions within a specific time range:
            https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Donkey_Kong_Country&rvstart=2024-01-01T00:00:00Z&rvend=2023-01-01T00:00:00Z&rvdir=newer&format=json
        Fetch revisions by revision ID:
            https://en.wikipedia.org/w/api.php?action=query&prop=revisions&revids=123456|654321&rvprop=content&format=json

### list=usercontribs: Requests user contribution data for the specified user.

    Additional Parameters for usercontribs:
        - ucuser: Specifies the username whose contributions you want to fetch. (No default, required)
        - ucuserids: Specifies the user ID (numeric) whose contributions you want to fetch. (No default)
        - uclimit: Limits the number of contributions returned. (Default: 10)
        - ucstart: Only include contributions made after this timestamp (ISO 8601 format). (No default)
        - ucend: Only include contributions made before this timestamp (ISO 8601 format). (No default)
        - ucnamespace: Filters contributions by namespace (e.g., 0 for articles). (Default: All namespaces)
        - ucdir: Direction to list contributions: newer (oldest first) or older (newest first). (Default: older)
        - ucshow: Filters contributions by flags (e.g., minor, !minor, anon, !anon, patrolled, !patrolled). (No default)
        - ucprop: Specifies which properties to include for each contribution (pipe-separated list):
            - ids, title (Default: ids|title).
        - format: Specifies the output format (e.g., json, xml). (Default: json)
        - formatversion: Specifies the JSON format version (1 or 2). (No default)
        - utf8: Ensures UTF-8 encoding for the response. (No default)

    Use cases:
        Fetch 500 Contributions for User Good_Olfactory
            https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser=Good_Olfactory&uclimit=500&format=json
        Fetch Contributions with Comments and Tags
            https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser=Good_Olfactory&uclimit=500&ucprop=ids|title|timestamp|comment|tags&format=json
        Filter Only Minor Edits
            https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser=Good_Olfactory&uclimit=500&ucshow=minor&format=json

### additional notes
    - format options include json, xml, jsonfm (default is json)
    - response size is limited to 500 revisions per request, use uccontinue to fetch additional pages with the same query, use the uccontinue value from the previous response to fetch the next page. 
    
