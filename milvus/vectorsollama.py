from ollama import Client
from pymilvus import MilvusClient
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="wikirag",
    password="wikirag123",
    database="wikirag",
)

client_embed = Client(host='http://localhost:1337')

## pull objects from mysqlrevisions table 

cursor = db.cursor()
cursor.execute("SELECT revision_id, text FROM revisions")
revisions = cursor.fetchall()

## convert revisions objects to 

docs = [{"id": int(rev[0]), "text": rev[1]} for rev in revisions]


limited_docs = docs[:2]


for doc in limited_docs:
    print("doc = ", doc)
    print("###########################")

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
    res = client_milvus.insert(collection_name="revisions_collection", data=data)

# Check collection
ids = client_milvus.query("revisions_collection", filter="id > 0", output_fields=["id"])

print("ids = ", ids)
print("###########################")
