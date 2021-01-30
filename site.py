"""The start file for the application
"""

import os 
import sys

from flask import Flask, render_template, g, request, redirect, url_for
from flask.helpers import send_from_directory
from settings import SECRET, ARTICLES_PATH, ARTICLES_STATIC_PATH
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from articles import Article, Paragraph

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, './static/uploads')
socketio = SocketIO(app)


@app.context_processor
def social_links():
    return dict(facebook_link="https://www.facebook.com/Flokami974",
                twitter_link="https://twitter.com/Flo_Okami")


@app.route("/")
def index():
    articles = []
    for article_json in os.listdir(ARTICLES_PATH):
        articles.append(Article(os.path.join(ARTICLES_PATH,article_json)))
    pinned = [Article(os.path.join(ARTICLES_PATH, "bienvenue.json"))]
    return render_template("index.html", home_active="active", games=[],
                           articles=articles, pinned=pinned)

@app.route("/cdn/<id>/<path:filename>")
def custom_static(id,filename):
    return send_from_directory(ARTICLES_STATIC_PATH + "/" + id, filename)

@app.route("/article/<id>")
def article(id):
    if not id or id == "undefined":
        return url_for("index")
    else:
        article = Article(os.path.join(ARTICLES_PATH, id + ".json"))
        print(article.body[0]["title"], flush=True)
        return render_template("article.html", article=article)

@app.route("/articles")
def articles():
    articles = []
    return render_template("list-article.html", article_active="active",
        articles=articles)


@app.route("/me")
def me():
    return render_template("me.html")


@socketio.on('join')
def join(data):
    join_room(data['room'])
    emit("test", "joined_room", room=data["room"])    


@socketio.on('my event')
def handle_my_custom_event(json):
    emit("test", "testmessage")


if __name__ == "__main__":
    app.secret_key = SECRET
    app.debug = True
    app.run(host="0.0.0.0",port=8000)
