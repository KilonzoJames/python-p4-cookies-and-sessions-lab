#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
CORS(app, origins = "http://localhost:4000")

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles', methods = ['GET'])
def index_articles():
    articles = []
    for article in Article.query.all():
        article_list = {
            "id": article.id,
            "title": article.title,
            "date": article.date,
            "minutes_to_read": article.minutes_to_read,
            "preview": article.preview
        }
        articles.append(article_list)
    response = make_response(jsonify(articles), 200)
    return response

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize session['page_views'] to 0 if not set
    session['page_views'] = session.get('page_views', 0)
    print("Current page views:", session['page_views'])  # Add this line

    # Increment the value of session['page_views']
    session['page_views'] += 1
    
    # Check if the user has viewed more than 3 pages
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    else:
        return jsonify({'article_id': id, 'page_views': session['page_views']}), 200

if __name__ == '__main__':
    app.run(port=5555)