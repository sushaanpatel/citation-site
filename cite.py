from bson.objectid import ObjectId
from models import Website, app, mongo
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

def format(unformat):
    lenght = len(unformat)
    count = 0
    formated_list = []
    while count < lenght:
        try:
            temp = []
            temp.append(unformat[count])
            temp.append(unformat[count+1])
            formated_list.append(temp)
            count += 2
        except IndexError:
            x = unformat[::-1]
            y = []
            y.append(x[0])
            formated_list.append(y)
            count += 2
    return formated_list

@app.route('/')
def index():
    if 'username' in session:
        temp = list(mongo.db.cites.find({'user': session['username']}))
        temp2 = temp
        all_cites = """"""
        cites = sorted(temp2, key=lambda x: x['full_citation'])
        for i in cites:
            all_cites = all_cites + i['full_citation'] + '\n'
        temp = temp[::-1]
        temp = format(temp)
        return render_template('index.html', cites=cites, all=all_cites, temp=temp, session=session, login_r=False)
    else:
        if 'citation' in session:
            temp = list(session['citation'])
            temp2 = temp
            all_cites = """"""
            cites = sorted(temp2, key=lambda x: x['full_citation'])
            for i in cites:
                all_cites = all_cites + i['full_citation'] + '\n'
            temp = temp[::-1]
            temp = format(temp)
            err = request.args.get('err')
            return render_template('index.html', session=session, cites=cites, temp=temp, all=all_cites, login_r=True, err = err)
        else:
            err = request.args.get('err')
            return render_template('index.html', session=session, cites=[], temp=[], all="", login_r=True, err = err)

@app.route('/login', methods=['POST'])
def login():
    try:
        if request.method == "POST":
            if 'username' not in session:
                username = request.form['username']
                password = request.form['password']
                user = mongo.db.users.find_one({'username': username})
                if user['username'] is not None:
                    if check_password_hash(user['password'], password):
                        session['username'] = username
                        return redirect('/')
                    else:
                        return redirect('/?err=1')
                else:
                    return redirect('/?err=1')
            else:
                return redirect('/')
    except Exception as e:
        print(e)
        return redirect('/?err=1')
        

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})
        if user is None:
            mongo.db.users.insert_one({'username': username, 'password': generate_password_hash(password, "sha256"), 'email': email})
            session['username'] = username
            return redirect('/')
        else:
            return redirect('/?err=2')

@app.route('/cite', methods=['POST'])
def add():
    if request.method == 'POST':
        url = request.form['url']
        author = request.form['author']
        publisher = request.form['publisher']
        ac_date = request.form['ac_date']
        year = request.form['pub_date']
        if 'username' in session:
            web = Website(author, publisher, ac_date, year, url, session['username'])
            web.citeit()
        else:
            web = Website(author, publisher, ac_date, year, url, "ano")
            web.citeit()
        return redirect('/')

@app.route('/edit/<cid>', methods=['POST'])
def edit(cid):
    if request.method == 'POST':
        url = request.form['url']
        author = request.form['author']
        publisher = request.form['publisher']
        ac_date = request.form['ac_date']
        year = request.form['pub_date']
        web = Website(author, publisher, ac_date, year, url, session['username'])
        print(cid)
        web.update(str(cid))
        return redirect('/')

@app.route('/delete/<cid>')
def delete(cid):
    mongo.db.cites.delete_one({'_id': ObjectId(cid)})
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'secretkeysecretkey'
    app.run(debug=True)