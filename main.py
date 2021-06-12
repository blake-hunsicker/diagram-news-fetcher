import config
import time
import json
import requests
# from bs4 import BeautifulSoup
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

search_terms = []

for search_result in search_results.get('value'):
  term = search_result.get('query').get('text')
  search_terms.append(term)

print(search_terms)

# Get articles for every search term

article_search_url = 'https://api.bing.microsoft.com/v7.0/news/search'
allArticles= []
  
for search_term in search_terms:
  params = {'q': search_term, 'textDecorations': True, 'textFormat': 'HTML', 'count': 1}
  response = requests.get(article_search_url, headers=headers, params=params)
  response.raise_for_status()
  search_results = response.json()['value'][0]['url']
  json_results = json.dumps(search_results, indent=2)
  print(json_results)
  time.sleep(5)