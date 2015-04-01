# -*- coding: utf-8 -*-

import os
import tornado

from tornado import web, httpserver, ioloop, escape, auth

from tornado.options import define, options
import pymongo
import time
PORT = 8000
DB_CONFIG = {
	'HOST':'localhost',
	'PORT':27017,
	'DB':'example',
	'USERNAME':'',
	'PASSWORD':''
}

define("port",default=PORT,help='tornado run at %s' % PORT,type=int)






class Application(web.Application):
	def __init__(self):
		handlers = [
			(r'/',IndexHandler),
			(r'/hello',HelloHander),
			(r'/books',RecommendedHander)
			(r'book/edit/([0-9Xx\-]+)',BookEditHandler),
			(r'book/add',BookEditHandler)
		]
		settings = dict(
		template_path=os.path.join(os.path.dirname(__file__),'templates'),
		static_path=os.path.join(os.path.dirname(__file__),'static'),
		ui_modules={'Hello':HelloModule,'Book':BookModule},
		debug = True)
		conn = pymongo.Connection(host=DB_CONFIG['HOST'],port=DB_CONFIG['PORT'])
		self.db = conn['bookstore']
		# web.Application.__init__(self,handlers,**settings)
		super(Application,self).__init__(handlers,**settings)

class BookModule(web.UIModule):
	def render(self,book):
		return self.render_string('modules/book.html',book=book)

	#embedded a javascript text into html module
	def embedded_javascript(self):
		return "document.write(\"hi!\")"

	def embedded_css(self):
		return ".book {background-color:#F5F5F5}"

	def html_body(self):
		return "<script>document.write(\"Hello!\")</script>"

	def css_files(self):
		return "/static/css/newreleases.css"

	def javascript_files(self):
		return "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.min.js"

class RecommendedHander(web.RequestHandler):

	def get(self):
		coll = self.application.db.books
		books = coll.find()[:10]
		self.render('recommended.html',page_title="Books | Recommend Reading",
			header_text="Recommend Reading",books = books)

class BookEditHandler(web.RequestHandler):
	def get(self,isbn=None):
		book = dict()
		if isbn:
			coll = self.application.db.books
			query = {'isbn':isbn}
			book = coll.find_one(query)
		self.render('book_edit.html',
			page_title='Edit Book',
			header_text="Edit Book",
			book = book
			)

	def post(self,isbn=None):
		import time
		book_fields = ['isbn','title','subtitle','image','author','date_realsed','description']
		coll = self.application.db.books
		book = dict()
		if isbn:
			book = coll.find_one({'isbn':isbn})
		for key in book_fields:
			book[key] = self.get_argument(key,None)
		if isbn:
			coll.save(book)
		else:
			book['date_added'] = int(time.time())
			coll.insert(book)
		self.redirect("/recommended")



class HelloHander(web.RequestHandler):
	def get(self):
		self.render('hello.html')

class HelloModule(web.UIModule):
	def render(self):
		return '<h1>Hello World</h1>'

class IndexHandler(web.RequestHandler):
	def get(self):
		return self.render('index.html',page_title="Home",header_text="Books")

if __name__ == "__main__":
	options.parse_command_line()
	httpserver.HTTPServer(Application()).listen(options.port)
	ioloop.IOLoop.instance().start()
