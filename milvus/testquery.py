from pymilvus import MilvusClient, model

# Initialize the Milvus client
client = MilvusClient("milvus_wikirag.db")

user_input = "Who is wiggle bear and what is he like?"

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


print("RETRIEVED DATA:", retrieved_data)
print("--------------------------------")

extracted_text = " ".join([item['entity']['text'] for item in retrieved_data[0]])

print("EXTRACTED TEXT:", extracted_text)
print("--------------------------------")

