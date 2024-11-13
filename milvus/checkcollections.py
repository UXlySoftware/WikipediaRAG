from pymilvus import MilvusClient

client = MilvusClient("milvus_wikirag.db")

print(client.list_collections())
