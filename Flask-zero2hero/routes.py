# -*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template
from app import app
import redis

#Connect to redis data store
# r = redis.StrictRedis(host='localhost', port=6379, db=0)
r = redis.StrictRedis(host='localhost', port=6379, db=0, charset = 'utf-8', decode_responses=True)

# server/
@app.route('/')
def hello():
    # url 바뀌더라도, url_for(함수이름)을 통해서 유연하게 운영가능
    createLink = "<a href = '" + url_for('create') + "'>Create a question</a>"

    return """<html><body>"""+ createLink+ """</body></html>"""

# server/create
@app.route('/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        #send the user the form
        return render_template('CreateQuestion.html')
    elif request.method == 'POST' :
        #read form data and save it
        title = request.form['title'] # CreatedQuestion.html 에서 <input name= 'title' ~ >에 해당
        question = request.form['question']
        answer = request.form['answer']

        #Store data in data store
        """ Keay name will be whatever title they typed in: Question"""
        # e.g. music:question countries:question (콜론 쓰는 것은 redis에서 convention)
        # e.g. music:answer countries:answer
        r.set(title + ':question', question)
        r.set(title + ':answer', answer)
        return render_template('CreatedQuestion.html', question = question)

    else:
        return "<h2> Invliad request </h2>"


# server/question/<title>
@app.route('/question/<title>', methods = ['GET','POST']) # parameter 전달 가능
# @app.route('/question/<int:title>')
def question(title):
    if request.method == 'GET':
        #send the user the form
        question = r.get(title+':question')

        # Read Question from the data store


        return render_template('AnswerQuestion.html', question = question)

    elif request.method == 'POST':
        # User has attempted answer. Check if they're correct
        submittedAnswer = request.form['submittedAnswer']

        #Read answer from data store
        answer = r.get(title+':answer')

        if submittedAnswer == answer:
            # return render_template('Correct.html')
            return "Correct!" # a way of debugging
        else:
            return render_template('Incorrect.html', submittedAnswer = submittedAnswer, answer = answer)

    else:
        return '<h2> Invalid request</h2>'

