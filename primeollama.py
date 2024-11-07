# from ollama import Client
# from pprint import pprint

# client = Client(host='http://localhost:1337')

# pprint("Pulling nomic-embed-text")
# client.pull('nomic-embed-text')
# pprint(client.list())

from tqdm import tqdm
from ollama import Client

client = Client(host='http://localhost:1337')


current_digest, bars = '', {}
for progress in client.pull('nomic-embed-text', stream=True):
  digest = progress.get('digest', '')
  if digest != current_digest and current_digest in bars:
    bars[current_digest].close()

  if not digest:
    print(progress.get('status'))
    continue

  if digest not in bars and (total := progress.get('total')):
    bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

  if completed := progress.get('completed'):
    bars[digest].update(completed - bars[digest].n)

  current_digest = digest