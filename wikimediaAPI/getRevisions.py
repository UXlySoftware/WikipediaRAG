import requests  #requirement for making HTTP requests

# fetch revision metadata by user and article title
## includes: article title, revision id, timestamp, comment, size
def fetch_revision_metadata_by_user_and_title(user_name, title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={user_name}&ucprop=title&titles={title}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
    
    
# fetch revisions by username
## includes: article title, revision id, timestamp, comment, tags
def fetch_revisions_by_username(user_name, limit):
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={user_name}&uclimit={limit}&ucprop=ids|title|timestamp|comment|tags&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
    



#fetch revision by revision id 
## includes: revision id, timestamp, flags, comment, content
def fetch_revision_by_id(rev_id):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&revids={rev_id}&rvslots=main&rvprop=ids|timestamp|flags|comment|content&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")


# fetch a limited number of full text revisions by page title (up to 500)
## includes: revision id, user id, timestamp, flags, content
def fetch_limited_revisions_by_title(page_title, limit):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={page_title}&rvlimit={limit}&rvprop=ids|userid|timestamp|flags|content&format=json"
    response = requests.get(url)  # Make the API request
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        raise Exception(f"Error fetching data: {response.status_code}")  # Handle errors

# fetch all revisions by page title, loops through the api (not limited to 500)
## WARNING: this will be a very large request and may take a while to complete
## includes: revision id and user id 
## For testing, change the rvlimit to 1 to demonstrate the api call looping through pages without overloading your system

def fetch_all_revisions_by_title(page_title):
    revisions = []
    rvcontinue = None
    base_url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={}&rvlimit=1&rvprop=ids|userid|timestamp|flags&format=json"

    while True:
        # Construct the URL with or without rvcontinue
        url = base_url.format(page_title)
        if rvcontinue:
            url += f"&rvcontinue={rvcontinue}"

        # Make the API request
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code}")

        # Parse the JSON response
        data = response.json()
        print(data)
        print("--------------------------------")
        # Append the revisions to the list
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            revisions.extend(page_data.get('revisions', []))

        # Check for the 'continue' key to see if more data is available
        if 'continue' in data:
            rvcontinue = data['continue']['rvcontinue']
        else:
            break

    return revisions

fetch_all_revisions_by_title("Barack Obama")