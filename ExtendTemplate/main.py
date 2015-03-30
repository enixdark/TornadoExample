# -*- coding: utf-8 -*-

import os
import tornado

from tornado import web,httpserver,ioloop

from tornado.options import define, options

PORT = 8000

define("port",default=PORT,help='tornado run at %s' % PORT,type=int)






class Application(web.Application):
	def __init__(self):
		handlers = [
			(r'/',IndexHandler),
			(r'/hello',HelloHander),
			(r'/books',RecommendedHander)
		]
		settings = dict(
		template_path=os.path.join(os.path.dirname(__file__),'templates'),
		static_path=os.path.join(os.path.dirname(__file__),'static'),
		ui_modules={'Hello':HelloModule,'Book':BookModule},
		debug = True)
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
		self.render('recommended.html',page_title="Books | Recommend Reading",
			header_text="Recommend Reading",books = [
			{
				"title":"Programming Collective Intelligence",
				"subtitle": "Building Smart Web 2.0 Applications",
				"image":"/static/images/collective_intelligence.gif",
				"author": "Toby Segaran",
				"date_added":1310248056,
				"date_released": "August 2007",
				"isbn":"978-0-596-52932-1",
				"description":"<p>This fascinating book demonstrates how you" + 
				"can build web applications to mine the enormous amount of data created by people" +
				"on the Internet. With the sophisticated algorithms in this book, you can write" +
				"smart programs to access interesting datasets from other web sites, collect data"+
				"from users of your own applications, and analyze and understand the data once"+
				"you've found it.</p>"
			}
			])




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
