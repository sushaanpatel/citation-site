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


# con = sqlite3.connect('cite.db', check_same_thread=False)
# db = con.cursor()

# db.execute("DROP TABLE citation")
# db.execute("""
#            CREATE TABLE citation(
#                id INTEGER PRIMARY KEY,
#                author CHAR(100),
#                web_title CHAR(100),
#                ac_date CHAR(100),
#                pub_year CHAR(100),
#                publisher CHAR(100),
#                url CHAR(200),
#                full_citation CHAR(400),
#                icon CHAR(200)
#            )
#            """)

# con.commit()
class Citation:
     def __init__(self,author,publisher,ac_date,year,url,username):
        self.author = author
        self.ac_date = ac_date
        self.year = year
        self.publisher = publisher
        self.url = url
        self.username = username
    

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
            mongo.db.cites.insert_one({'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon})
        else:
            if 'citation' in session:
                clist = list(session['citation'])
                clist.append({'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon})
                session['citation'] = clist
            else:
                session['citation'] = [{'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon}]

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
        mongo.db.cites.update_one({'_id': ObjectId(cid)},{"$set": {'user': self.username, 'author': self.author, 'web_title': title, 'ac_date': self.ac_date, 'pub_year': self.year, 'publisher': self.publisher, 'url': self.url, 'full_citation': text, 'icon': icon}})
        
#.execute("""
#            CREATE TABLE citation(
#                id INTEGER PRIMARY KEY,
#                author CHAR(100),
#                web_title CHAR(100),
#                ac_date CHAR(100),
#                pub_year CHAR(100),
#                publisher CHAR(100),
#                url CHAR(200),
#                full_citation CHAR(400),
#                icon CHAR(200)
#            )
#            """)        


# db.execute("SELECT * FROM citation")
# x = db.fetchall()
# for i in x:
#         mongo.db.cites.insert_one({'user':'sushaan', 'author': i[1], 'web_title': i[2], 'ac_date': i[3], 'pub_year': i[4], 'publisher': i[5], 'url': i[6], 'full_citation': i[7], 'icon': i[8]})
# mongo.db.cites.delete_many({'user':'sushaan'})