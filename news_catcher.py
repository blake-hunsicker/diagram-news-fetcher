import config
import firebase_admin
from firebase_admin import credentials, firestore
import time
import requests
from datetime import date

# Get today's date

today = date.today()

# Prep Firebase

cred = credentials.Certificate('oracle-5bdbb-firebase-adminsdk-j79ht-3a32c165b8.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'trends')
print(doc_ref)

# Prep MS API key

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
  name = search_result.get('name')

  all_search_terms.append(term)
  
  # doc_ref.document(term).set({
  #   u'trend': term,
  #   u'name': name
  # }, merge=True)

# Get articles for every search term

article_search_url = 'https://api.bing.microsoft.com/v7.0/news/search'
all_articles = []
  
for search_term in all_search_terms:
  params = {'q': search_term, 'textDecorations': True, 'textFormat': 'HTML', 'count': 6}
  response = requests.get(article_search_url, headers=headers, params=params)
  response.raise_for_status()

  cleaned_search_term = today.strftime('%m-%d-%y-') + search_term.replace(' ','-').lower()
  doc_ref.document(cleaned_search_term).set({
    u'trend': search_term,
    u'live': False
  })
  fs_doc = doc_ref.document(cleaned_search_term)
  time.sleep(1)
  i = 0
  while i < 5:
    raw_search_result = response.json()
    # search_result = json.dumps(raw_search_result, indent=2)
    headline = raw_search_result['value'][i]['name']
    publisher = raw_search_result['value'][i]['provider'][0]['name']
    url = raw_search_result['value'][i]['url']
    timestamp = raw_search_result['value'][i]['datePublished']
    # category = raw_search_result['value'][i]['category']

    cleaned_headline = headline.replace('<b>','').replace('</b>','').replace(' ','-').lower()
    
    fs_doc.collection(u'articles').document(cleaned_headline).set({
      u'headline': headline,
      u'publisher': publisher,
      u'url': url,
      u'timestamp': timestamp,
      # u'category': category if category else ''
    })
    all_articles.append(url)
    i += 1
    time.sleep(1)

print(all_articles)