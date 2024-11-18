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
