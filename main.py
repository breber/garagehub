#!/usr/bin/env python
from google.appengine.api import users
from flask import Flask, render_template
import utils

app = Flask(__name__)

@app.route('/')
def main():
    context = utils.get_context()

    if context['user']:
        path = 'garage.html'
    else:
        path = 'welcome.html'

    return render_template(path, **context)
