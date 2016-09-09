import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

# Shortcuts from Udacity example

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Blog(db.Model):
	title = db.StringProperty(required = True)
	body = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

# Main landing page (incomplete)

class MainPage(Handler):
	#def render_blog(self, title="", body=""):
		#blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
	def get(self):
		self.render("blog.html")

# Full Blog Archive (incomplete)

class Blog(Handler):
	def get(self):
		self.render("blog.html")

# New Post Page (incomplete)

class NewPost(Handler):
	
	# Shortcut to re-render blog form and keep inputs
	def render_newpost_form(self, title="", body="", error=""):
		self.render("newpost.html", title=title, body=body, error=error)

	# Landing page for new post
	def get(self):
		self.render_newpost_form()

	# Collects the inputs (where I left off)
	def post(self):
		title = self.request.get("title")
		body = self.request.get("body")

		if title and body:
			self.write("Success!")
		else:
			error = "Please submit both a title and some blog content."
			self.render_newpost_form(title, body, error = error)


app = webapp2.WSGIApplication([('/', MainPage),
	('/blog', Blog),
	('/newpost', NewPost)], debug=True)
