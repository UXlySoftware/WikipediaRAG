from pymilvus import MilvusClient, model

# Initialize the Milvus client
client = MilvusClient("milvus_wikirag.db")

user_input = "Mummy"

print("USER INPUT:", user_input)
print("--------------------------------")

embedding_fn = model.DefaultEmbeddingFunction()

query_vectors = embedding_fn.encode_queries([user_input])

retrieved_data = client.search(
    collection_name="revisions_collection",  # target collection
    data=query_vectors,  # query vectors
    limit=8,  # number of returned entities
    output_fields=["text", "subject"],  # specifies fields to be returned
)

for item in retrieved_data:
    print("RETRIEVED DATA:")
    for value in item:
        print(value)
    print("--------------------------------")




