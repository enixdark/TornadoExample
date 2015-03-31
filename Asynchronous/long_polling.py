from tornado import httpserver, web, httpclient, ioloop
from tornado.options import options, define
from uuid import uuid4
import os
PORT = 8000

class Cart(object):
	total = 10
	callbacks = []
	carts = {}

	def register(self,callback):
		self.callbacks.append(callback)

	def moveItemToCart(self,session):
		if session in self.carts:
			return 
		self.carts[session] = True
		self.notifiCallbacks()

	def removeItemFormCart(self,session):

		if session not in self.carts:
			return
		del self.carts[session]
		self.notifiCallbacks()

	def notifiCallbacks(self):
		for c in self.callbacks:
			self.callbackHelper(c)
		self.callbacks = []

	def callbackHelper(self,callback):
		callback(self.getCount())

	def getCount(self):
		return self.total - len(self.carts)

class Application(web.Application):
	def __init__(self):
		self.Cart = Cart()
		handlers = [
			(r'/',DetailHandler),
			(r'/cart',CartHandler),
			(r'/cart/status',StatusHandler)
		]

		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__),'templates'),
			static_path=os.path.join(os.path.dirname(__file__),'static'),
			debug=True
			)
		super(Application,self).__init__(handlers,**settings)



class DetailHandler(web.RequestHandler):
	def get(self):
		session = uuid4()
		count = self.application.Cart.getCount()
		self.render('index.html',session=session,count=count)

class CartHandler(web.RequestHandler):

	def post(self):
		action = self.get_argument('action')
		session = self.get_argument('session')

		if not session:
			self.set_status(400)
			return
		# import ipdb; ipdb.set_trace()
		if action == 'add':
			self.set_status(200)
			self.application.Cart.moveItemToCart(session)
		elif action == 'remove':
			self.set_status(200)
			self.application.Cart.removeItemFormCart(session)
		else:
			self.set_status(400)

class StatusHandler(web.RequestHandler):
	@web.asynchronous
	def get(self):
		self.application.Cart.register(self.on_message)

	# @web.asynchronous
	def on_message(self,count):
		self.write('{"Count":"%d"}' % count)
		self.finish()


define("port",default=PORT,help='tornado run at %s' % PORT,type=int)


if __name__ == "__main__":
	options.parse_command_line()
	httpserver.HTTPServer(Application()).listen(options.port)
	ioloop.IOLoop.instance().start()