from ollama import Client
from pprint import pprint

client = Client(host='http://localhost:1337')

output = client.embed('nomic-embed-text', "hello world")
pprint(output)
