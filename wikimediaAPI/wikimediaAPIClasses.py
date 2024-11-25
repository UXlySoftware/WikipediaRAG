import requests

class WikimediaAPI:
    def fetch_revision_metadata_by_user_and_title(self, user_name, title):
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={user_name}&ucprop=title&titles={title}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def fetch_revisions_by_username(self, user_name, limit):
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={user_name}&uclimit={limit}&ucprop=ids|title|timestamp|comment|tags&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def fetch_revision_by_id(self, rev_id):
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&revids={rev_id}&rvslots=main&rvprop=ids|timestamp|flags|comment|content&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def fetch_limited_revisions_by_title(self, page_title, limit):
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={page_title}&rvlimit={limit}&rvprop=ids|userid|timestamp|flags|content&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def fetch_all_revisions_by_title(self, page_title):
        revisions = []
        rvcontinue = None
        base_url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={}&rvlimit=1&rvprop=ids|userid|timestamp|flags&format=json"

        while True:
            url = base_url.format(page_title)
            if rvcontinue:
                url += f"&rvcontinue={rvcontinue}"

            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Error fetching data: {response.status_code}")

            data = response.json()
            print(data)
            print("--------------------------------")
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                revisions.extend(page_data.get('revisions', []))

            if 'continue' in data:
                rvcontinue = data['continue']['rvcontinue']
            else:
                break

        return revisions
    
    ## includes: article title, revision id, timestamp, comment, tags
    def fetch_revisions_by_username(self, user_name, limit):
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={user_name}&uclimit={limit}&ucprop=ids|title|timestamp|comment|tags&format=json"
        response = requests.get(url)
        if response.status_code == 200:
                return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")
    
    ## includes: revision id, timestamp, flags, comment, content
    def fetch_revision_by_id(self, rev_id):
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&revids={rev_id}&rvslots=main&rvprop=ids|timestamp|flags|comment|content&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")