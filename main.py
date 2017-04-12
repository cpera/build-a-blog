#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
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

def blog_key(name = 'default'):
	return db.Key.from_path('blogs', name)
	
class BlogPost(db.Model):
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
	""" Handles requests coming in to '/' or '/blog' (the root of our site)
		e.g. www.myblogpost.com/
	"""

	def get(self):
		t = jinja_env.get_template("frontpage.html")
		error = cgi.escape(self.request.get("error"), quote=True)
		latest_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created_on DESC LIMIT 5")
		content = t.render(posts=latest_posts, error=error)
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
		
		# 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
		new_blog_title_escaped = cgi.escape(new_blog_title, quote=True)
		new_blog_content_escaped = cgi.escape(new_blog_content, quote=True)
		
		'''		
		# construct a blogpost object for the new BlogPost
		blogpost = BlogPost(title = new_blog_title_escaped, content = new_blog_content_escaped)
		blogpost.put()
		
		self.redirect("/blog")
		'''
		
		if new_blog_title_escaped and new_blog_content_escaped:
			blogpost = BlogPost(title = new_blog_title_escaped, content = new_blog_content_escaped)
			blogpost.put()
			self.redirect("/blog")
			#self.redirect('/blog/%s' % str(blogpost.key().id()))
		else:
			error = "Title and content must be given before posting!"
			#self.render("newpost.html", title = new_blog_title_escaped, content = new_blog_content_escaped, error=error)
			t = jinja_env.get_template("newpost.html")
			content = t.render(title = new_blog_title_escaped, content = new_blog_content_escaped, error=error)
			self.response.write(content)
			
		# self.response.write("Your post has been submitted...")
		'''
		# render the confirmation message
		t = jinja_env.get_template("add-confirmation.html")
		content = t.render(movie = movie)
		self.response.write(content)
		'''

class ViewPostHandler(Handler):
	def get(self, id):
		#pass #replace this with some code to handle the request
		self.response.write(id)
		
app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/blog', MainHandler),	
	('/newpost', NewPost),
	('/blog/([0-9]+)', ViewPostHandler)
	], debug=True)