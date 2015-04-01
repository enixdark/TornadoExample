from tornado import web, ioloop, httpserver
from tornado.options import define, options
import os

PORT = 8000

define("port",default=PORT,help='tornado run at %s' % PORT,type=int)






class Application(web.Application):
	def __init__(self):
		handlers = [
			(r'/',MainHandler),
		]
		settings = dict(
		cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
		template_path=os.path.join(os.path.dirname(__file__),'templates'),
		static_path=os.path.join(os.path.dirname(__file__),'static'),
		debug = True)
		super(Application,self).__init__(handlers,**settings)

class MainHandler(web.RequestHandler):
	def get(self):
		cookie = self.get_secure_cookie('count')
		count = (int(cookie) + 1) if cookie else 1
		countString = "1 time" if count ==1 else "%d times" % count

		self.set_secure_cookie('count',str(count))

		self.write(
			'<html><head><title>Cookie Counter</title></head>' +
			'<body><h1>You&rsquo;ve viewed this page %s times.</h1>' % countString +
			'</body></html>'
		)

if __name__ == "__main__":
	options.parse_command_line()
	httpserver.HTTPServer(Application()).listen(options.port)
	ioloop.IOLoop.instance().start()