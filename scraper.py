import requests
import favicon
from bs4 import BeautifulSoup

def scrape(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.head.title.text
        icon = favicon.get(url)
        return {'title': title, 'icon': icon[0].url}
    except Exception as e:
        print(e)
        return {'title': 'No Title', 'icon': '../static/noicon.png'}
    # author = soup.find_all(attrs={'rel': 'author'}