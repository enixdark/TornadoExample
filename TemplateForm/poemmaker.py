import os.path
import random

import tornado
from tornado import httpserver,ioloop,options,web


from tornado.options import define,options

PORT = 8000

define("port",default=PORT,help='tornado run at %s' % PORT,type=int)

class IndexHander(web.RequestHandler):
	def get(self):
		self.render('index.html')

class IndexHandler2(web.RequestHandler):
	def get(self):
		self.render('index2.html')

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

class MungedPageHandler(web.RequestHandler):
	def map_by_first_letter(self,text):
		mapped = dict()
		for line in text.split('\r\n'):
			for word in [x for x in line.split(' ') if len(x) > 0]:
				if word[0] not in mapped:
					mapped[word[0]] = []
				mapped[word[0]].append(word)
		return mapped

	def post(self):
		source_text = self.get_argument('source')
		text_to_change = self.get_argument('change')
		source_map = self.map_by_first_letter(source_text)
		change_lines = text_to_change.split('\r\n')
		self.render('munged.html',source_map=source_map,change_lines=change_lines,choice=random.choice)

if __name__ == "__main__":
	options.parse_command_line()
	app = web.Application(
		handlers=[
			(r'/',IndexHander),
			(r'/poem',PoemHandler),
			(r'/book',BookHandler),
			(r'/home',IndexHandler2),
			(r'/munged',MungedPageHandler)
		],
		template_path=os.path.join(os.path.dirname(__file__),'templates'),
		static_path=os.path.join(os.path.dirname(__file__),'static'),
		debug = True
		)
	httpserver.HTTPServer(app).listen(options.port)
	ioloop.IOLoop.instance().start()


