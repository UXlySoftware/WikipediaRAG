from pymilvus import MilvusClient, model
from ollama import Client
import requests

client_milvus = MilvusClient("milvus_wikirag.db")

user_input = "Tell me about the Fayum mummy portraits"

print("USER INPUT:", user_input)
print("--------------------------------")

client_embed = Client(host='http://ollama_service:11434')

output = client_embed.embed('nomic-embed-text', user_input)

# Ensure the embeddings are a list of floats
embeddings = output['embeddings']
if isinstance(embeddings[0], list):
    embeddings = embeddings[0]

query_vectors = [embeddings]

retrieved_data = client_milvus.search(
    collection_name="revisions_collection",  # target collection
    data=query_vectors,  # query vectors
    limit=8,  # number of returned entities
    output_fields=["text"],  # specifies fields to be returned
)

print("RETRIEVED DATA:", retrieved_data)
print("--------------------------------")


extracted_text = " ".join([item['entity']['text'] for item in retrieved_data[0]])

print("EXTRACTED TEXT:", extracted_text)
print("--------------------------------")


url = "http://ollama_service:11434/api/chat"
data = '{"model": "llama3.2", "messages": [{"role": "user", "content": "' + user_input + '"}], "stream": false}'  

response = requests.post(url, data=data, headers={'Content-Type': 'application/json'}) 

print("RESPONSE WITHOUT RAG:", response.json()['message']['content'])
print("--------------------------------")

url = "http://ollama_service:11434/api/chat"  #
data = '{"model": "llama3.2", "messages": [{"role": "user", "content": "User question: ' + user_input.replace('\n', '') + ' Context to consider in your response: ' + extracted_text.replace('\n', '') + '"}], "stream": false}'  

response2 = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

print("RESPONSE WITH RAG:", response2.json()['message']['content'])
print("--------------------------------")
