from pymilvus import MilvusClient
from ollama import Client
from mysqlDatabaseTools.mysqlDBToolsClasses import MySQLDBTools
from pprint import pprint
from ollama import Client
import mysql.connector
import requests
class MilvusDBTools:
    def start_milvus(self):
        client = MilvusClient("milvus_wikirag.db")

        # Create a Revisions collection with metadata
        revisions_collection = "revisions_collection"
        if client.has_collection(collection_name="revisions_collection"):
            client.drop_collection(collection_name="revisions_collection")
        client.create_collection(
            collection_name=revisions_collection,
            dimension=768,  # The vectors we will use in this demo has 768 dimensions
        )


        print("Milvus revisions_collection exists:", client.has_collection(revisions_collection))

        # check if the collection is empty by quering ids
        print("Milvus revisions_collection ", client.query(revisions_collection, filter="id > 0", output_fields=["id"]))

        # Create an Articles collection with metadata
        articles_collection = "articles_collection"
        if client.has_collection(collection_name="articles_collection"):
            client.drop_collection(collection_name="revisions_collection")
        client.create_collection(
            collection_name=articles_collection,
            dimension=768,  # The vectors we will use in this demo has 768 dimensions
        )


        print("Milvus articles_collection exists:", client.has_collection(articles_collection))

        # check if the collection is empty by quering ids
        print("Milvus articles_collection ", client.query(articles_collection, filter="id > 0", output_fields=["id"]))

    def restart_milvus_collections(self):
        client = MilvusClient("milvus_wikirag.db")
        client.drop_collection(collection_name="revisions_collection")
        client.drop_collection(collection_name="articles_collection")
        self.start_milvus() 

    def check_milvus_collections(self):
        client = MilvusClient("milvus_wikirag.db")

        print("Milvus revisions_collection exists:", client.has_collection("revisions_collection"))
 # Check collection
        revisions_ids = client.query("revisions_collection", filter="id > 0", output_fields=["id"])

        print("ids = ", revisions_ids)
        print("----------------------")  

        print("Milvus articles_collection exists:", client.has_collection("articles_collection"))
        articles_ids = client.query("articles_collection", filter="id > 0", output_fields=["id"])
        print("ids = ", articles_ids)

    def embed_articles_table(self):
        # connect to wikirag db
        db = mysql.connector.connect(
            host="localhost",
            user="wikirag",
            password="wikirag123",
            database="wikirag",
        )

        # connect to ollama
        client_embed = Client(host='http://localhost:1337')

        # Pull objects from the articles table
        cursor = db.cursor()
        cursor.execute("SELECT id, content FROM articles")
        articles = cursor.fetchall()

        # Convert articles objects
        docs = [{"id": int(article[0]), "text": article[1]} for article in articles]

        limited_docs = docs  # Limit to a smaller set for testing if needed

        for doc in limited_docs:
            output = client_embed.embed('nomic-embed-text', doc['text'])
            vector = output['embeddings'][0]

            # Check vector dimensions
            expected_dimension = 768  # This should match the dimension in startmilvus.py
            if len(vector) != expected_dimension:
                raise ValueError(f"Vector dimension mismatch: expected {expected_dimension}, got {len(vector)}")

            # Prepare data for insertion
            data = [
                {"id": doc['id'], "vector": vector, "text": doc['text'], "subject": ""}
            ]

            # Insert embedding into Milvus
            client_milvus = MilvusClient("milvus_wikirag.db")
            res = client_milvus.insert(collection_name="articles_collection", data=data)

            print("Inserted article vector into Milvus:", res)

        articles_ids = client_milvus.query("articles_collection", filter="id > 0", output_fields=["id"])
        print("ids = ", articles_ids)
        

    def rag_query_articles(self, user_query):

        client_milvus = MilvusClient("milvus_wikirag.db")

        print("USER INPUT:", user_query)
        print("--------------------------------")

        client_embed = Client(host='http://localhost:1337')

        output = client_embed.embed('nomic-embed-text', user_query)

        # Ensure the embeddings are a list of floats
        embeddings = output['embeddings']
        if isinstance(embeddings[0], list):
            embeddings = embeddings[0]

        query_vectors = [embeddings]

        retrieved_data = client_milvus.search(
            collection_name="articles_collection",  # target collection
            data=query_vectors,  # query vectors
            limit=8,  # number of returned entities
            output_fields=["text"],  # specifies fields to be returned
        )

        extracted_text = " ".join([item['entity']['text'] for item in retrieved_data[0]])

        print("EXTRACTED TEXT:", extracted_text)
        print("--------------------------------")

        url = "http://localhost:11434/api/chat"
        data = '{"model": "llama3.2", "messages": [{"role": "user", "content": "' + user_query + '"}], "stream": false}'  

        response = requests.post(url, data=data, headers={'Content-Type': 'application/json'}) 

        print("RESPONSE WITHOUT RAG:", response.json())
        print("--------------------------------")

        url = "http://localhost:11434/api/chat"  #
        data = '{"model": "llama3.2", "messages": [{"role": "user", "content": "User question: ' + user_query + ' Context to consider in your response: ' + extracted_text.replace('\n', '') + '"}], "stream": false}'  

        response2 = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

        print("RESPONSE WITH RAG:", response2.json())
        print("--------------------------------")

       