from pymilvus import MilvusClient, CollectionSchema, FieldSchema, DataType
from ollama import Client
from mysqlDatabaseTools.mysqlDBToolsClasses import MySQLDBTools

class MilvusDBTools:
    def start_milvus(self):
        client = MilvusClient("milvus_wikirag.db")

        # Create a collection with metadata
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

    def restart_milvus_collection(self):
        client = MilvusClient("milvus_wikirag.db")
        client.drop_collection(collection_name="revisions_collection")
        self.start_milvus() 
    
    def add_ollama_vectors(self, data):
        client_embed = Client(host='http://localhost:1337')

        # pull data from mysql
        mysql_api = MySQLDBTools()
        docs = mysql_api.get_articles_table_data()

        #data is a list of tuples, where each tuple contains (id, pageid, title, content)

        for doc in docs:
            output = client_embed.embed('nomic-embed-text', doc[2])
            vector = output['embeddings'][0]

            # Check vector dimensions
            expected_dimension = 768  # This should match the dimension in startmilvus.py
            if len(vector) != expected_dimension:
                raise ValueError(f"Vector dimension mismatch: expected {expected_dimension}, got {len(vector)}")

            # Prepare data for insertion
            data = [
                {"id": doc['id'], "vector": vector, "text": doc['text'], "subject": "example"}
            ]

            # Insert embedding into Milvus
            client_milvus = MilvusClient("milvus_wikirag.db")
            res = client_milvus.insert(collection_name="revisions_collection", data=data)

        # Check collection
        ids = client_milvus.query("revisions_collection", filter="id > 0", output_fields=["id"])

        print("ids = ", ids)
        print("###########################")
            
