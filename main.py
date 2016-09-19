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

	def render_blog(self, title="", body=""):
		 blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")

		 self.render("blog.html", title = title, body = body, blogs = blogs)

class Blog(db.Model):
	title = db.StringProperty(required = True)
	body = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class ViewPostHandler(Handler):
	def get(self, id):
		
		entry_id = Blog.get_by_id(int(id))
		
		if entry_id:
			self.render("blog.html", blogs = [entry_id])

		else:
			error="There is no post with this ID"
			self.response.out.write(error)

		
# Main landing page (incomplete)

class MainPage(Handler):

	
	def get(self):
		self.render_blog()
		

# Last 5 posts

class BlogHandler(Handler):

	def get(self):
		self.render_blog()
		

# New Post Page (incomplete)

class NewPost(Handler):
	
	# Shortcut to re-render blog form and keep inputs
	def render_newpost_form(self, title="", body="", error=""):
		self.render("newpost.html", title=title, body=body, error=error)

	# Landing page for new post
	def get(self):
		self.render_newpost_form()

	# Collects the inputs and responds to interaction
	def post(self):
		title = self.request.get("title")
		body = self.request.get("body")

		if title and body:
		 	b = Blog(title = title, body = body)
			b.put()

			self.redirect("/blog/%s" % str(b.key().id()))

		else:
			error = "Please submit both a title and some blog content."
			self.render_newpost_form(title, body, error)


app = webapp2.WSGIApplication([
	webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
	('/', MainPage),
	('/blog', BlogHandler),
	('/newpost', NewPost),
	
	], debug=True)
	
