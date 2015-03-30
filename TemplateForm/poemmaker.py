import os.path

import tornado
from tornado import httpserver,ioloop,options,web


from tornado.options import define,options

PORT = 8000

define("port",default=PORT,help='tornado run at %s' % PORT,type=int)

class IndexHander(web.RequestHandler):
	def get(self):
		self.render('index.html')

class PoemHandler(web.RequestHandler):
	def post(self):
		noun1 = self.get_argument('noun1')
		noun2 = self.get_argument('noun2')
		verb = self.get_argument('verb')
		noun3 = self.get_argument('noun3')
		self.render('poem.html',roads=noun1,wood=noun2,made=verb,difference=noun3)

class BookHandler(web.RequestHandler):
	def get(self):
		self.render('book.html',title='Book Home Pgae',header="Books",books=["Ebook","Manga","Game"])

if __name__ == "__main__":
	options.parse_command_line()
	app = web.Application(
		handlers=[
			(r'/',IndexHander),
			(r'/poem',PoemHandler),
			(r'/book',BookHandler)
		],
		template_path=os.path.join(os.path.dirname(__file__),'templates'),
		static_path=os.path.join(os.path.dirname(__file__),'static')
		)
	httpserver.HTTPServer(app).listen(options.port)
	ioloop.IOLoop.instance().start()