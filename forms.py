from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea



class ArticleForm(FlaskForm):
    name = StringField("Article name")
    pinned = BooleanField("Pinned Article ?")
    categories = StringField("Categories")
    description = StringField("Article Description", widget=TextArea())
    desc_img = FileField("Little Img")
    img = FileField("Image")
    desc_img_url = StringField("Little Img Url")
    img_url = StringField("Image Url")
    content = StringField("Content", widget=TextArea())
    submit = SubmitField("Post")
