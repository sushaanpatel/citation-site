import requests
import favicon
from bs4 import BeautifulSoup

def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.head.title.text
    icon = favicon.get(url)
    return {'title': title, 'icon': icon[0].url}
    # author = soup.find_all(attrs={'rel': 'author'}