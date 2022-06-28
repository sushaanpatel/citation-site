from bson.objectid import ObjectId
from models import Website, app, mongo, Image
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

# Function to format list output
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

# Main route
@app.route('/')
def folders():
    session['cp'] = '/'
    if 'username' in session:
        folders = list(mongo.db.folders.find({'user': session['username']}))
        temp = list(mongo.db.cites.find({'user': session['username'], 'tags': 'default'}))
        temp2 = temp
        all_cites = """"""
        cites = sorted(temp2, key=lambda x: x['full_citation'].split('.')[0].lower())
        for i in cites:
            all_cites = all_cites + i['full_citation'] + '\n'
        temp = temp[::-1]
        temp = format(temp)
        return render_template('index.html', cites=cites, all=all_cites, temp=temp, session=session, login_r=False, folders=folders)
    else:
        if 'citation' in session:
            temp = list(session['citation'])
            temp2 = temp
            all_cites = """"""
            cites = sorted(temp2, key=lambda x: x['full_citation'].split('.')[0].lower())
            for i in cites:
                all_cites = all_cites + i['full_citation'] + '\n\n'
            temp = temp[::-1]
            temp = format(temp)
            err = request.args.get('err')
            return render_template('index.html', session=session, cites=cites, temp=temp, all=all_cites, login_r=True, err = err, folders=[])
        else:
            err = request.args.get('err')
            return render_template('index.html', session=session, cites=[], temp=[], all="", login_r=True, err = err, folders=[])

@app.route('/citations/<folder>')
def index(folder):
    session['cp'] = f'/citations/{folder}'
    if 'username' in session:
        if folder == "" or folder == "default":
            return redirect('/')
        folders = list(mongo.db.folders.find({'user': session['username']}))
        for i in folders:
            if i['name'] == folder:
                temp = list(mongo.db.cites.find({'user': session['username'], 'tags': folder}))
                temp2 = temp
                all_cites = """"""
                cites = sorted(temp2, key=lambda x: x['full_citation'].split('.')[0].lower())
                for i in cites:
                    all_cites = all_cites + i['full_citation'] + '\n'
                temp = temp[::-1]
                temp = format(temp)
                return render_template('folders.html', cites=cites, all=all_cites, temp=temp, session=session, login_r=False, err='0', delop=True, fol=folder, folders=folders)
        else:
            return render_template('folders.html', cites=[], all="", temp=[], session=session, login_r=False, err='3', delop=False)

@app.route('/addfolder', methods=['POST'])
def addf():
    if request.method == 'POST':
        name = request.form['fname']
        f = list(mongo.db.folders.find({'user': session['username']}))
        n = 0
        for i in f:
            if i['name'] == name:
                n += 1
                name = name + f'({n})'
        mongo.db.folders.insert_one({'name': name, 'user': session['username']})
        return redirect('/')
    
@app.route('/deletefolder/<folder>')
def delf(folder):
    if 'username' in session:
        f = list(mongo.db.folders.find({'name': folder, 'user': session['username']}))
        if f != []:
            mongo.db.folders.delete_one({'name': folder, 'user': session['username']})
        return redirect('/')
    
@app.route('/login', methods=['POST'])
def login():
    try:
        if request.method == "POST":
            if 'username' not in session:
                username = request.form['username'].lower()
                password = request.form['password']
                if username == "" or password == "":
                    return redirect('/?err=1')
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
        username = request.form['username'].lower()
        password = request.form['password']
        if email == "" or username == "" or password == "":
            return redirect('/?err=2')
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
        ctype = request.form['type']
        url = request.form['url']
        try:
            title = request.form['title']
        except:
            title = ""
        author = request.form['author']
        publisher = request.form['publisher']
        ac_date = request.form['ac_date']
        year = request.form['pub_date']
        f = request.form['folder']
        folder = f if f != "" else 'default'
        if 'username' in session:
            c = Website(author, publisher, ac_date, year, url, session['username'], "", folder) if ctype == 'web' else Image(author, publisher, ac_date, year, url, session['username'], title, folder)
            c.citeit()
            return redirect(f'/citations/{folder}')
        else:
            c = Website(author, publisher, ac_date, year, url, "ano", "", '') if ctype == 'web' else Image(author, publisher, ac_date, year, url, "ano", title, '')
            c.citeit()
            return redirect('/')

@app.route('/edit/<cid>', methods=['POST'])
def edit(cid):
    if request.method == 'POST':
        url = request.form['url']
        try:
            title = request.form['title']
        except:
            title = ""
        author = request.form['author']
        publisher = request.form['publisher']
        ac_date = request.form['ac_date']
        year = request.form['pub_date']
        folder = request.form['folder']
        x = mongo.db.cites.find_one({'_id': ObjectId(cid)})
        c = Website(author, publisher, ac_date, year, url, session['username'], title, folder) if x['type'] == 'web' else Image(author, publisher, ac_date, year, url, session['username'], title, folder)
        c.update(str(cid))
        return redirect(f'/citations/{folder}')

@app.route('/delete/<cid>')
def delete(cid):
    mongo.db.cites.delete_one({'_id': ObjectId(cid)})
    return redirect(session['cp'])

@app.route('/dac')
def deleteacc():
    if 'username' in session:
        allc = list(mongo.db.cites.find({'user': session['username']}))
        for i in allc:
            mongo.db.cites.delete_one(i)
        mongo.db.users.delete_one({'username': session['username']})
        session.pop('username')
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'secretkeysecretkey'
    app.run(debug=True)