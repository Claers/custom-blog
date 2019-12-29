#! /usr/bin/python3

from site import app
import logging
import sys
from settings import SECRET, APP_DIR
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, )
app.secret_key = SECRET
