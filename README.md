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