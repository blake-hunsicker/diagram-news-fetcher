import config
import time
import json
import requests
from bs4 import BeautifulSoup
# import openai

# Prepare MS API key

ms_subscription_key = config.ms_subscription_key
assert ms_subscription_key
headers = {'Ocp-Apim-Subscription-Key': ms_subscription_key}

# Get search terms

trending_search_url = 'https://api.bing.microsoft.com/v7.0/news/trendingtopics'
trending_search_term = ''

params = {'q': trending_search_term, 'textDecorations': True, 'textFormat': 'HTML', 'count': 5}
response = requests.get(trending_search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

all_search_terms = []

for search_result in search_results.get('value'):
  term = search_result.get('query').get('text')
  all_search_terms.append(term)

# Get articles for every search term

article_search_url = 'https://api.bing.microsoft.com/v7.0/news/search'
all_articles= []
  
for search_term in all_search_terms:
  params = {'q': search_term, 'textDecorations': True, 'textFormat': 'HTML', 'count': 5}
  response = requests.get(article_search_url, headers=headers, params=params)
  response.raise_for_status()
  search_results = response.json()
  json_results = json.dumps(search_results, indent=2)
  print('🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝🏝')
  i = 0
  while i < 5:
    url = response.json()['value'][i]['url']
    article = requests.get(url)
    soup = BeautifulSoup(article.content, 'html.parser')
    print('--------------------------------------')
    print(i)
    print(url)
    print(soup.get_text())
    print('--------------------------------------')
    i += 1
  time.sleep(5)