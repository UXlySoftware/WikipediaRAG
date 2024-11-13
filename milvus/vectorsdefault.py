from pymilvus import model, MilvusClient


embedding_fn = model.DefaultEmbeddingFunction()

docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
    "The best color is blue",
    "Wiggle Bear is a dog",
    "Wiggle Bear is a Old English Sheepdog",
    "Wiggle Bear is extremely fluffy and loves to wag his tail",
    "Old English Sheepdogs are a breed of dog",
    "Old English Sheepdogs are known for their fluffy coats and wagging tails",
    "Old English Sheepdogs are friendly and loyal dogs",
    "Old English Sheepdogs are often used as therapy dogs",
    "Old English Sheepdogs are often used as guide dogs",
]

vectors = embedding_fn.encode_documents(docs)
print("Dim:", embedding_fn.dim, vectors[0].shape)  # Dim: 768 (768,)

data = [
    {"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"}
    for i in range(len(vectors))
]

print("Data has", len(data), "entities, each with fields: ", data[0].keys())
print("Vector dim:", len(data[0]["vector"]))

client = MilvusClient("milvus_wikirag.db")

res = client.insert(collection_name="revisions_collection", data=data)

print(res)

client.close()  # Free up resources