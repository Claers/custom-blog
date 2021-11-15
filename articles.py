"""Article Class that will contains all info to build an article from a json
"""
import json

class Article():
    """Article class
    """
    
    def __init__(self, article_json) -> None:
        with open(article_json) as f:
            data = json.load(f)
        for key in data:
            setattr(self, key, data[key])


    