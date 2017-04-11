#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

def getMyPosts():
	""" Returns the list of posts """

	return [ "My first post", "My second post" ]

class Posts(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created_on = db.DateTimeProperty(auto_now_add = True)
	#watched = db.BooleanProperty(required = True, default = False)
	#rating = db.StringProperty()

	
class Handler(webapp2.RequestHandler):
	""" A base RequestHandler class for our app.
		The other handlers inherit form this one.
	"""

	def renderError(self, error_code):
		""" Sends an HTTP error code and a generic "oops!" message to the client. """

		self.error(error_code)
		self.response.write("Oops! Something went wrong.")
		
class MainHandler(Handler):
	""" Handles requests coming in to '/' (the root of our site)
		e.g. www.myblogpost.com/
	"""

	def get(self):
		t = jinja_env.get_template("frontpage.html")
		error = cgi.escape(self.request.get("error"), quote=True)
		content = t.render(posts=getMyPosts(), error=error)
		self.response.write(content)


class NewPost(Handler):

	def get(self):		
		# watched_movies = db.GqlQuery("SELECT * FROM Movie where watched = True ORDER BY title")
		t = jinja_env.get_template("newpost.html")
		content = t.render()
		self.response.write(content)
	def post(self):
		new_blog_title = self.request.get("title")
		new_blog_content = self.request.get("content")

		# if the user typed nothing at all, redirect and yell at them
		if (not new_blog_title) or (new_movie_title.strip() == ""):
			error = "Please specify the title and content you want to post in the blog."
			self.redirect("/?error=" + cgi.escape(error))

		# if the user wants to add a terrible movie, redirect and yell at them
		if new_movie_title in terrible_movies:
			error = "Trust me, you don't want to add '{0}' to your Watchlist.".format(new_movie_title)
			self.redirect("/?error=" + cgi.escape(error, quote=True))

		# 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
		new_movie_title_escaped = cgi.escape(new_movie_title, quote=True)

		# construct a movie object for the new movie
		movie = Movie(title = new_movie_title_escaped)
		movie.put()

		# render the confirmation message
		t = jinja_env.get_template("add-confirmation.html")
		content = t.render(movie = movie)
		self.response.write(content)
		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/newpost', NewPost)
], debug=True)
