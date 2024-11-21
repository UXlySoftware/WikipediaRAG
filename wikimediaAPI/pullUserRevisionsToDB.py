import requests  #requirement for making HTTP requests
import json
# import mysql.connector

# make sure you run the docker compose file before running this script

# # connect to mysql database
# client = mysql.connector.connect(
#     host="localhost",
#     user="wikirag",
#     password="wikirag123",
#     database="wikirag"
# )

# cursor = client.cursor()

# set query details
user_name = "Good_Olfactory"
limit = 2 # number of revisions to pull

# define object to store revision content
revisions = []

# fetch revisions by username
## includes: revision id list 
def fetch_revision_metadata_by_username(user_name, limit):
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={user_name}&uclimit={limit}&ucprop=ids|title|comment&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
    

revisionMetadata = fetch_revision_metadata_by_username(user_name, limit)

print("User revision metadata: ", json.dumps(revisionMetadata, indent=4))
print("--------------------------------")

    
#update revisions object with revision ids
def update_revisions_with_ids(revisions, revisionMetadata):
    for rev in revisionMetadata['query']['usercontribs']:
        revisions.append({
            "user": rev["user"],
            "revision_id": rev["revid"],
            "parent_id": rev["parentid"],
            "page_id": rev["pageid"],
            "page_title": rev["title"],
            "comment": rev["comment"]
        })

update_revisions_with_ids(revisions, revisionMetadata)

print("User revision object: ", json.dumps(revisions, indent=4))
print("--------------------------------")

#fetch revision by revision id 
## includes: revision id, parent revision id,timestamp, comment, content
def fetch_revision_by_id(rev_id):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&revids={rev_id}&rvslots=main&rvprop=ids|timestamp|content|sha1&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

# print("Fetching revision by id: ", fetch_revision_by_id(1111064426))
# print("--------------------------------")

for rev in revisions:
    revisionContent = fetch_revision_by_id(rev["revision_id"])
    # Check if 'pages' key exists in the response
    if "pages" in revisionContent["query"]:
        page_id = next(iter(revisionContent["query"]["pages"]))
        revisions_data = revisionContent["query"]["pages"][page_id].get("revisions", [])
        if revisions_data:
            slots = revisions_data[0].get("slots", {})
            main_slot = slots.get("main", {})
            rev["content"] = main_slot.get("*", "")
            rev["timestamp"] = revisions_data[0].get("timestamp", "")
            rev["sha1"] = revisions_data[0].get("sha1", "")
        else:
            print(f"Warning: No revisions found for revision_id {rev['revision_id']}")
            print("--------------------------------")
    else:
        print(f"Warning: No pages found for revision_id {rev['revision_id']}")
        print("--------------------------------")

print("User revision object with content: ", json.dumps(revisions, indent=4))
print("--------------------------------")


# add revision metadata to user table

revisionIDsArray = {} # JSON object to store revision ids

# Add revision id paired with parent revision id to JSON object with labels
for rev in revisions:
    revisionIDsArray[rev['revision_id']] = {
        "parent_revision_id": rev['parent_id']
    }

print("Revision IDs array: ", json.dumps(revisionIDsArray, indent=4))
print("--------------------------------")

# add revision content to revisions table
