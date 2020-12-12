from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab.db'
db = SQLAlchemy(application)

from models import User


@application.route('/')
def hello():
    return "Hello World!"


@application.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/user/login', methods=['GET'])
def user_login():
    return 'You are log in'


@app.route('/user/logout', methods=['GET'])
def user_logout():
    return 'You are log out'


@app.route('/announcement', methods=['GET'])
def blog():
    if request.method == 'GET':
        all_announcements = Announcement.query.all()
        if all_articles is None:
            abort(404, description="Resource not found")
        result = announcements_schema.dump(all_announcements)
        return jsonify(result)


@app.route('/user/<username>', methods=['GET'])
def blog_username(username):
    if request.method == 'GET':
        user = User.query.filter_by(username=username).first()
        if user is None:
            abort(404, description="Resource not found")
        user_articles = UsersArticles.query.filter_by(user_ID=user.user_ID).all()
        if user_articles is None:
            abort(404, description="Resource not found")

        result = user_articles_schema.dump(user_articles)
        return jsonify(result)


@app.route('/announcements/local>', methods=['GET'])
def blog_article(ids):
    if request.method == 'GET':
        articles = UsersArticles.query.filter_by(article_ID=ids).all()
        if articles is None:
            abort(404, description="Resource not found")

        result = user_articles_schema.dump(articles)
        return jsonify(result)
if __name__ == '__main__':
    application.run(debug=True)
