import os
import tornado

from tornado import web,httpserver,ioloop

from tornado.options import define, options

PORT = 8000

define("port",default=PORT,help='tornado run at %s' % PORT,type=int)

class IndexHandler(web.RequestHandler):
	def get(self):
		return self.render('index.html')
if __name__ == "__main__":
	options.parse_command_line()
	app = web.Application(
		handlers=[

		],
		template_path=os.path.join(os.path.dirname(__file__),'templates'),
		static_path=os.path.join(os.path.dirname(__file__),'static'),
		debug = True
	)

	httpserver.HTTPServer(app).listen(options.port)
	ioloop.IOLoop.instance().start()