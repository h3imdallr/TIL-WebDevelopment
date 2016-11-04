# -*- coding: utf-8 -*-

# http://derrickgilland.com/posts/demystifying-flask-sqlalchemy/
## Postgresql
# http://postgresapp.com/documentation/configuration-python.html
# http://jonnung.blogspot.kr/2014/12/osx-postgresql-install.html

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# Tut-4
from flask import render_template, request, redirect, url_for

app = Flask(__name__)

# SQLAlchemy Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/Josh'

app.debug = True # Tut-4 debug mode

db = SQLAlchemy(app)

# DataBase model for Tut 1~6
class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique= True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
# def index(): # Tut-1
#     return "<h1 style = 'color:red'> Hello Flask! </h1>" # Tut-1
#
# def index(): # Tut-4
#     return render_template('add_user.html')
#
def index(): # Tut-5: Querying the Database
    # retrieve list of objects
    myUser = User.query.all()
    oneItem = User.query.filter_by(username="test2").first()
    # pass the list inside the template
    return render_template('add_user.html',myUser = myUser, oneItem = oneItem )

""" Tut-6: Dynamic URL Querying """
@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()

    return render_template('profile.html', user = user)

""" Tut-4: HTTP methods """
@app.route('/post_user', methods = ['POST'])
def post_user():
    user = User(request.form['username'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index')) # 웹서버 어플리케이션에서 아무 리턴도 없으면 value 에러.


if __name__ == '__main__':
    app.run()
