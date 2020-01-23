"""The start file for the application
"""

import os 

from flask import Flask, render_template, g, request, redirect, url_for
import models
from settings import SECRET, TOKEN
from flaskext.markdown import Markdown
from forms import ArticleForm
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_uploads import patch_request_class
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)
Markdown(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, './static/uploads')
socketio = SocketIO(app)

uploads = UploadSet('photos', IMAGES)
configure_uploads(app, uploads)
patch_request_class(app)  # set maximum file size, default is 16MB


@app.context_processor
def social_links():
    return dict(facebook_link="https://www.facebook.com/Flokami974",
                twitter_link="https://twitter.com/Flo_Okami")


@app.route("/")
def index():
    articles = models.session.query(models.Article).order_by(
        models.Article.id.asc()).all()
    print([article.pinned for article in articles])
    articles = articles[len(articles)-3:len(articles)]
    pinned = models.session.query(models.Article).filter(models.Article.pinned == True).order_by(
        models.Article.id.asc()).all()
    print(pinned)
    return render_template("index.html", home_active="active", games=[],
                           articles=articles, pinned=pinned)


@app.route("/edit-article/<id>/<token>", methods=['GET', 'POST'])
def edit_article(id, token):
    if token != TOKEN:
        return "Fuck off"
    else:
        article = models.session.query(models.Article).get(id)
        article_edit = ArticleForm(obj=article)
        if article_edit.validate_on_submit():
            article = models.session.query(models.Article).get(id)
            name = article_edit.name.data
            content = article_edit.content.data
            pinned = article_edit.pinned.data
            categories = article_edit.categories.data
            if article_edit.desc_img.data:
                desc_img = uploads.save(article_edit.desc_img.data)
            if article_edit.img.data:
                img = uploads.save(article_edit.img.data)
            if article:
                article.name = name
                article.content = content
                article.pinned = pinned
                article.categories = categories
                try:
                    article.desc_img_url = uploads.url(desc_img)
                except:
                    pass
                try:
                    article.img_url = uploads.url(img)
                except:
                    pass
            else:
                article = models.Article(id=id, name=name, content=content,
                                         desc_img_url=uploads.url(desc_img),
                                         img_url=uploads.url(img),
                                         pinned=pinned, categories=categories)
                models.session.add(article)
        else:
            return render_template("edit-article.html", form=article_edit)
        models.session.commit()
        return redirect(url_for("edit_article", id=id, token=token))


@app.route("/article/<id>")
def article(id):
    if not id or id == "undefined":
        return url_for("index")
    else:
        article = models.session.query(models.Article).get(id)
        return render_template("article.html", article=article)


@app.route("/articles")
def articles():
    articles = models.session.query(models.Article).order_by(
       models.Article.id.asc()).all()
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
    app.run(port=8000)
