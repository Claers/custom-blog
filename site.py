"""The start file for the application
"""

from flask import Flask, render_template, g
import models

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
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)
