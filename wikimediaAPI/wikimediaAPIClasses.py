import requests
from mysqlDatabaseTools.mysqlDBToolsClasses import MySQLDBTools
from pprint import pprint
import os
from datetime import datetime

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
        
    def fetch_page_categories(self, page_title):
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={page_title}&prop=categories&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")
            
    def fetch_articles_by_category(self, category, limit):
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category}&cmlimit={limit}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")
        
    def fetch_article_content_by_pageid(self, pageid):
        url = f"https://en.wikipedia.org/w/api.php?action=query&pageids={pageid}&prop=revisions&rvprop=content&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")
        
    def add_articles_to_articles_table_by_category(self, category, limit):
        articles = self.fetch_articles_by_category(category, limit)
        for article in articles['query']['categorymembers']:
            pageid = article['pageid']
            title = article['title']
            content = self.fetch_article_content_by_pageid(pageid)
            api = MySQLDBTools()
            api.add_article_to_articles_table(pageid, title, content)

    def fetch_article_content_by_title(self, title):
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&prop=revisions&rvprop=content&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")
        
    def add_articles_by_title_to_articles_table(self, title):
        content = self.fetch_article_content_by_title(title)
        pages = content['query']['pages']
        page_id, page_data = next(iter(pages.items()))
        api = MySQLDBTools()
        api.add_article_to_articles_table(page_id, title, page_data)

    def add_revs_to_revs_table_by_article_title(self, page_title, limit):
        # Fetch the revisions by title
        result = self.fetch_limited_revisions_by_title(page_title, limit)
        with open("wikimediaAPI/result_log.txt", "w") as log_file:
            pprint(result, log_file)
        print("Result logged to wikimediaAPI/result_log.txt")
        
        # Get the pages dictionary
        pages = result.get('query', {}).get('pages', {})
        
        # Iterate over pages to find the correct page
        for page_id, page_data in pages.items():
            if 'revisions' in page_data:
                for rev in page_data['revisions']:
                    # Convert timestamp to MySQL format
                    timestamp = rev.get('timestamp')
                    formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Add to db
                    api = MySQLDBTools()
                    api.add_revs_to_revs_table(
                        page_id, 
                        page_data.get('title'), 
                        rev.get('revid'), 
                        rev.get('parentid'), 
                        formatted_timestamp,
                        rev.get('userid'), 
                        rev.get('sha1'), 
                        rev.get('content'), 
                        rev.get('comment'), 
                        rev.get('contentformat')
                    )
                    print("--------------------------------")
            else:
                print(f"No revisions found for page title: {page_title}")
        
