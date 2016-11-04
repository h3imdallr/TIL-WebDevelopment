# -*- coding: utf-8 -*-
"""
for Tut6 ~
"""

# http://derrickgilland.com/posts/demystifying-flask-sqlalchemy/
## Postgresql
# http://postgresapp.com/documentation/configuration-python.html
# http://jonnung.blogspot.kr/2014/12/osx-postgresql-install.html

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# Tut-4
from flask import render_template, request, redirect, url_for
# Tut-6
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

# Create app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/Josh' # SQLAlchemy Config

# (****) Key commands for security
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True

app.debug = True # Tut-4 debug mode

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# # Create a user to test with
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='noobniche@gmail.com', password='test123')
#     db.session.commit()


@app.route('/')
# def index(): # Tut-7~
#     return render_template('add_user.html')

def index(): # Tut-9 : Boostrap Theme
    return render_template('index.html')


""" Tut-6: Dynamic URL Querying """
@app.route('/profile/<email>')
@login_required
def profile(email):
    user = User.query.filter_by(email=email).first()

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
