#!/usr/bin/env python

import os
import webapp2
import jinja2
import re
import string
import random
import hashlib

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = False)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)

class MainPageHandler(Handler):
    def get(self):
        self.render("insecure.html")

    def post(self):
        self.response.headers.add_header('X-XSS-Protection', '0')
        comment = self.request.get("comment")
        self.render("insecure.html", comment = comment)

class SignInHandler(Handler):
    def get(self):
        self.render("insecurelogin.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        info = db.GqlQuery("SELECT * FROM User WHERE username = '%s'" % username)
        check_password = False
        for i in info:
            if i.password == password:
                check_password = True
                break
        if check_password:
            self.render("displayinfo.html", user_info = info)
        else:
            self.render("insecurelogin.html", error = "Incorrect Password")

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/signin', SignInHandler)
], debug=True)
