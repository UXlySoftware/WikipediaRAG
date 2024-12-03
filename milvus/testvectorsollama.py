from ollama import Client
from pymilvus import MilvusClient

client_embed = Client(host='http://ollama_service:11434')

docs = [
    {"id": 1, "text": "Hello, World!"},
    {"id": 2, "text": "This is a test document."}
]

for doc in docs:
    output = client_embed.embed('nomic-embed-text', doc['text'])
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