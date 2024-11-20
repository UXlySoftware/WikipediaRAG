import requests  #requirement for making HTTP requests
import json

# NOT COMPLETE 
    
# fetch revisions by username
## includes: article title, revision id, timestamp, comment, tags
def fetch_revisions_by_username(user_name, limit):
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={user_name}&uclimit={limit}&ucprop=ids|title|timestamp|comment|tags&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
    

print(json.dumps(fetch_revisions_by_username("Good_Olfactory", 2), indent=4))
print("--------------------------------")

#fetch revision by revision id 
## includes: revision id, timestamp, flags, comment, content
def fetch_revision_by_id(rev_id):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&revids={rev_id}&rvslots=main&rvprop=ids|timestamp|flags|comment|content&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

print(json.dumps(fetch_revision_by_id("1172099374"), indent=4))
print("--------------------------------")