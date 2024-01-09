import os
import requests
import json
import dotenv
import favicon
from bs4 import BeautifulSoup

dotenv.load_dotenv()
apiKey = os.environ.get('APIKEY')
apiuser = os.environ.get('APIUSER')


def scrape(url):
    try:
        payload = json.dumps({"url":url})
        headers = {
            'Content-Type': "application/json"
        }
        # page = requests.request("POST", 'http://api.scraping-bot.io/scrape/raw-html', data=payload, auth=(apiuser,apiKey), headers=headers)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.head.title.text
        # author = soup.find_all(attrs={'rel': 'author'})
        # print(author[0])
        icon = favicon.get(url)
        con = None
        for i in icon:
            if i.format == 'ico':
                con = i.url
        return {'title': title, 'icon': con}
    except Exception as e:
        print(e)
        return {'title': 'No Title', 'icon': '../static/noicon.png'}