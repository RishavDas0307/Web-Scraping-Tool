import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

base_url = 'https://github.com'
topics_url = 'https://github.com/topics'

response = requests.get(topics_url)
page_contents = response.text
doc = BeautifulSoup(page_contents, 'html.parser')
topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-1 d-flex flex-column'})

topic_url = []
base_url = 'https://github.com'
for url in topic_link_tags:
    topic_url.append(base_url + url['href'])
topic_url



response = requests.get(topics_url)


h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
star_selection_class = 'Counter js-social-count'




def parse_star_count(star_str):
    if star_str[-1] == 'k':
        return int(float(star_str[:-1])*1000)
    return int(star_str)

def get_topic_page(topic_url):
    # Download the page
    response = requests.get(topic_url)
    
    # Check Successful response
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
        
    # Parse using Beautiful Soup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def get_repo_info(h3_tag, star_tag):
    #returns all the required info
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text)
    return username, repo_name, repo_url, stars

def get_topic_repos(topic_doc):
    # Get h3 tags containing repo info
    repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})
    
    # Get star tags containing star info
    star_tags = topic_doc.find_all('span', {'class' : star_selection_class})
    
    # Get repo info
    topics_repos_dict = {
        'username' : [],
        'repo_name': [],
        'repo_url': [],
        'stars': []
    }

    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topics_repos_dict['username'].append(repo_info[0])
        topics_repos_dict['repo_name'].append(repo_info[1])
        topics_repos_dict['repo_url'].append(repo_info[2])
        topics_repos_dict['stars'].append(repo_info[3])
    return pd.DataFrame(topics_repos_dict)

def scrape_topic(topic_url, path):
    if os.path.exists(path):
        print('The file {} already exists. Skipping....'.format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path, index = None)
def get_topic_titles(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class': selection_class})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles

def get_topic_desc(doc):
    desc_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class': desc_selector})
    topic_desc = []
    for desc in topic_desc_tags:
        topic_desc.append(desc.text.strip())
    return topic_desc

def get_topic_url(doc):
    topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-1 d-flex flex-column'})
    topic_url = []
    base_url = 'https://github.com'
    for url in topic_link_tags:
        topic_url.append(base_url + url['href'])
    return topic_url
            
def scrape_topics():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    topics_dict = {
        'title': get_topic_titles(doc),
        'description': get_topic_desc(doc),
        'URL': get_topic_url(doc)
    }
    
    return pd.DataFrame(topics_dict)

def scrape_topic_repos():
    print('Scraping list of topics')
    topics_df = scrape_topics()
    
    # Create Folder here
    os.makedirs('data', exist_ok=True)
    
    for index, row in topics_df.iterrows():
        print('Scraping top repositories for "{}" '.format(row['title']))
        scrape_topic(row['URL'], 'data/{}.csv'.format(row['title']))
scrape_topic_repos()
