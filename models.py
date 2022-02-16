import os
import dotenv
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo, ObjectId
from scraper import scrape

dotenv.load_dotenv()
password = os.environ.get('PASS') 
app = Flask(__name__)
app.config["MONGO_URI"] = f'mongodb+srv://root:{password}@memes.2xsyj.mongodb.net/citation?retryWrites=true&w=majority'
app.config["SECRET_KEY"] = f'secretkeysecretkey'
mongo = PyMongo(app)

class Citation:
     def __init__(self,author,publisher,ac_date,year,url,username, web_title):
        self.author = author
        self.ac_date = ac_date
        self.year = year
        self.publisher = publisher
        self.url = url
        self.username = username
        self.web_title = web_title

class Website(Citation):
    def citeit(self):
        a = self.author.split(' ')
        web = scrape(self.url)
        title = web['title']
        icon = web['icon']
        fname = None
        lname = None
        text = None
        year = self.year.split('-')[0]
        if (len(a) == 1):
            lname = a[0]
            text = (f"""{lname}. "{title}" {self.publisher if self.publisher != "" else "Np"}., {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        else:
            fname = a[0]
            lname = a[1]
            text = (f"""{lname}, {fname}. "{title}" {self.publisher if self.publisher != "" else "Np"}., {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        if (self.author == ""):
            text = (f""""{title}" {self.publisher if self.publisher != "" else "Np"}., {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        if self.username != 'ano':
            mongo.db.cites.insert_one({'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon, 'type': 'web'})
        else:
            if 'citation' in session:
                clist = list(session['citation'])
                clist.append({'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon, 'type': 'web'})
                session['citation'] = clist
            else:
                session['citation'] = [{'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon, 'type': 'web'}]

    def update(self, cid):
        a = self.author.split(' ')
        web = scrape(self.url)
        title = web['title']
        icon = web['icon']
        fname = None
        lname = None
        text = None
        year = self.year.split('-')[0]
        if (len(a) == 1):
            lname = a[0]
            text = (f"""{lname}. "{title}" {self.publisher if self.publisher != "" else "Np"}., {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        else:
            fname = a[0]
            lname = a[1]
            text = (f"""{lname}, {fname}. "{title}" {self.publisher if self.publisher != "" else "Np"}., {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        if (self.author == ""):
            text = (f""""{title}" {self.publisher if self.publisher != "" else "Np"}., {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        mongo.db.cites.update_one({'_id': ObjectId(cid)},{"$set": {'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon, 'type': 'web'}})
        
        
"""Wikipedia. Taking Photo. 2022. Web. 7 Feb. 2022 . <https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/330px-Image_created_with_a_mobile_phone.png>."""
class Image(Citation):
    def citeit(self):
        a = self.author.split(' ')
        title = self.web_title
        icon = self.url
        fname = None
        lname = None
        text = None
        year = self.year.split('-')[0]
        if (len(a) == 1):
            lname = a[0]
            text = (f"""{lname}. {title}. {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        else:
            fname = a[0]
            lname = a[1]
            text = (f"""{lname}, {fname}. {title}. {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        if (self.author == ""):
            text = (f"""{title}. {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        if self.username != 'ano':
            mongo.db.cites.insert_one({'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon, 'type': 'img'})
        else:
            if 'citation' in session:
                clist = list(session['citation'])
                clist.append({'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon, 'type': 'img'})
                session['citation'] = clist
            else:
                session['citation'] = [{'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon, 'type': 'img'}]

    def update(self, cid):
        a = self.author.split(' ')
        title = self.web_title
        icon = self.url
        fname = None
        lname = None
        text = None
        year = self.year.split('-')[0]
        if (len(a) == 1):
            lname = a[0]
            text = (f"""{lname}. {title}. {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        else:
            fname = a[0]
            lname = a[1]
            text = (f"""{lname}, {fname}. {title}. {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        if (self.author == ""):
            text = (f"""{title}. {year + ". " if year != "" else ""}Web. {self.ac_date}. <{self.url}>.""")
        mongo.db.cites.update_one({'_id': ObjectId(cid)},{"$set": {'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon, 'type': 'img'}})
        