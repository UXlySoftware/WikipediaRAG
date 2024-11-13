from pymilvus import MilvusClient, CollectionSchema, FieldSchema, DataType

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


