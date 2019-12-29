"""The start file for the application
"""

from flask import Flask, render_template, g
import models
from settings import SECRET

app = Flask(__name__)


@app.route("/")
def index():
    articles = models.session.query(models.Article).all()
    if not articles:
        article = models.Article(name="TestArticle")
        models.session.add(article)
        models.session.commit()
    else:
        article = articles[0]
        article.name = "ModifArticle3"
    return render_template("base.html")


if __name__ == "__main__":
    app.secret_key = SECRET
    app.run(debug=True, host="0.0.0.0", port="8000")
