"""The start file for the application
"""

from flask import Flask, render_template, g
from .settings import DB_NAME, DB_PASSWORD, DB_USER, DB_HOST
from . import models

app = Flask(__name__)


@app.route("/")
def index():
    articles = models.session.query(models.Article).all()
    print(articles[0].name)
    if not articles:
        article = models.Article(name="TestArticle")
        models.session.add(article)
        models.session.commit()
    else:
        article = articles[0]
        article.name = "ModifArticle3"
    g.article = article
    g.about = "active"
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)
