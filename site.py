"""The start file for the application
"""

import os 
import sys
import random

from flask import Flask, render_template, g, request, redirect, url_for
from flask.helpers import send_from_directory
from settings import SECRET, ARTICLES_PATH, ARTICLES_STATIC_PATH
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from articles import Article
from flask_sitemap import Sitemap

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, './static/uploads')
socketio = SocketIO(app)


@app.context_processor
def social_links():
    return dict(facebook_link="https://www.facebook.com/Flokami974",
                twitter_link="https://twitter.com/Flo_Okami")

def get_articles():
    articles = []
    for article_json in os.listdir(ARTICLES_PATH):
        articles.append(Article(os.path.join(ARTICLES_PATH,article_json)))
    active_articles = [article for article in articles if article.active]
    return active_articles

def get_pinned(articles):
    pinned = [article for article in articles if article.pinned]
    return pinned

def get_categories(articles):
    categories = [article.tags for article in articles]
    flat_categories = [item.capitalize() for sublist in categories for item in sublist]
    flat_categories = list(set(flat_categories))
    return flat_categories

def filter_tags(articles, tags):
    if type(tags) is not list:
        tags = [tags]
    filtered_articles = []
    for tag in tags:
        filtered_articles = [article for article in articles if tag in article.tags]
    return filtered_articles

@app.route("/")
def index():
    articles = get_articles()
    pinned = get_pinned(articles)
    flat_categories = get_categories(articles)
    rand_categories = random.choices(flat_categories, k=5)
    return render_template("index.html", home_active="active", games=[],
                           articles=articles, pinned=pinned, categories=rand_categories)

@app.route("/cdn/<id>/<path:filename>")
def custom_static(id,filename):
    return send_from_directory(ARTICLES_STATIC_PATH + "/" + id, filename)

@app.route("/article/<id>")
def article(id):
    if not id or id == "undefined":
        return url_for("index")
    else:
        try:
            article = Article(os.path.join(ARTICLES_PATH, id + ".json"))
        except FileNotFoundError:
            return redirect(url_for("index"))
        return render_template("article.html", article=article)

@app.route("/articles")
def articles():
    articles = get_articles()
    pinned = get_pinned(articles)
    flat_categories = get_categories(articles)
    rand_categories = random.choices(flat_categories, k=5)
    return render_template("list-article.html", article_active="active",
        articles=articles, pinned=pinned, categories=rand_categories)

@app.route("/articles/category/<category>")
def articles_category(category):
    articles = get_articles()
    filtered_articles = filter_tags(articles, category)
    pinned = get_pinned(filtered_articles)
    return render_template("list-article.html", article_active="active",
        articles=filtered_articles, pinned=pinned, category=category)

@app.route("/categories")
def categories_list():
    articles = get_articles()
    categories = [article.tags for article in articles]
    flat_categories = [item.capitalize() for sublist in categories for item in sublist]
    flat_categories = list(set(flat_categories))
    return render_template("list-categories.html", categories_active="active", categories=flat_categories)


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

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))

@app.route("/sitemap", methods=['GET'])
@app.route("/sitemap/", methods=['GET'])
@app.route("/sitemap.xml", methods=['GET'])
def sitemap():
    """
        Route to dynamically generate a sitemap of your website/application.
        lastmod and priority tags omitted on static pages.
        lastmod included on dynamic content such as blog posts.
    """
    from flask import make_response, request, render_template
    import datetime
    from urllib.parse import urlparse

    host_components = urlparse(request.host_url)
    host_base = "http" + "://" + host_components.netloc
    # Static routes with static content
    static_urls = list()
    for rule in app.url_map.iter_rules():
        if not str(rule).startswith("/admin") and not str(rule).startswith("/user"):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {
                    "loc": f"{host_base}{str(rule)}",
                    "priority": 1
                }
                static_urls.append(url)

    # Dynamic routes with dynamic content
    dynamic_urls = list()
    articles = get_articles()
    for article in articles:
        url = {
            "loc": f"{host_base}/article/{article.name}",
            "lastmod": article.date,
            "priority": 0.8
            }
        dynamic_urls.append(url)

    xml_sitemap = render_template("sitemap.xml", static_urls=static_urls, dynamic_urls=dynamic_urls, host_base=host_base)
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response

@app.route("/stat/sitemap.xml")
def static_sitemap():
     return send_from_directory("/home/","sitemap.xml")

if __name__ == "__main__":
    app.secret_key = SECRET
    app.debug = True
    app.run(host="0.0.0.0",port=8000)
