import time
import requests
from bs4 import BeautifulSoup

print('What story do you want to scrape?')
url = input()
print('🪐 OK 🪐 will try scraping' + url)

article = requests.get(url, headers={"content-type":"text"})
soup = BeautifulSoup(article.content, 'html.parser')
allPTags = soup.findAll('p')
fullText = ' '.join([item.text for item in allPTags])
print('How does this look?')
print(fullText)
print('👍')