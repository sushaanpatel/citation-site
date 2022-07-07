import os
import dotenv
import favicon
from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient

dotenv.load_dotenv()
api = os.environ.get('APIKEY')
client = ScraperAPIClient(api)

def scrape(url):
    try:
        page = client.get(url = url)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.head.title.text
        icon = favicon.get(url)
        con = None
        for i in icon:
            if i.format == 'ico':
                con = i.url
        return {'title': title, 'icon': con}
    except Exception as e:
        print(e)
        return {'title': 'No Title', 'icon': '../static/noicon.png'}
    # author = soup.find_all(attrs={'rel': 'author'}