#!/usr/bin/env python
from google.appengine.api import memcache, users
from google.appengine.ext import deferred
from flask import Flask, render_template, redirect
import utils

app = Flask(__name__)

@app.route('/admin')
def admin():
    """
    - If the logged in user is an admin, displays the admin page.
    - Otherwise, redirects to the root page
    """
    if users.is_current_user_admin():
        context = utils.get_context()

        return render_template('admin.html', **context)
    else:
        return redirect("/")

@app.route('/admin/<method>', methods=['POST'])
def admin_action():
    """Post request handler for the /admin/([^/])? path

    Args:
        method  (optional) - the operation to perform
            - clearmemcache - clears the Memcache
    """
    if users.is_current_user_admin() and method:
        if method == "clearmemcache":
            # Clear memcache
            memcache.Client().flush_all()

    # Always redirect to admin
    return redirect("/admin")
