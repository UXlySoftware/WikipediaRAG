from pymilvus import MilvusClient

client = MilvusClient("milvus_wikirag.db")

# Create a collection with metadata
revisions_collection = "revisions_collection"
if client.has_collection(revisions_collection):
    client.drop_collection(revisions_collection)
client.create_collection(
    collection_name=revisions_collection,
    dimension=768,  # Adjust based on your embedding model
)

# check if the collection exists
print(client.has_collection(revisions_collection))

# check if the collection is empty by quering ids
print(client.query(revisions_collection, filter="id > 0", output_fields=["id"]))
