
import pymongo

import tornado

from tornado import web, ioloop, httpserver

from tornado.options import define, options

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
		(r'/(\w+)',WordHandler)
		]
		conn = pymongo.Connection(DB_CONFIG['HOST'],DB_CONFIG['PORT'])
		self.db = conn[DB_CONFIG['DB']]
		super(Application,self).__init__(handlers,debug=True)

class WordHandler(web.RequestHandler):
	def get(self,word):
		coll = self.application.db.words
		query = {'word':word}
		word_doc = coll.find_one(query)
		if word_doc:
			del word_doc['_id']
			self.write(word_doc)
		else:
			self.set_status(404)
			self.write({'error':'word not found'})

	def post(self,word):
		definition = self.get_argument('definition')
		coll = self.application.db.words
		query = {'word':word}
		word_doc = coll.find_one(query)
		if word_doc:
			word_doc['definition'] = definition
			coll.save(word_doc)
		else:
			word_doc = {'word':word,'definition':definition}
			coll.insert(word_doc)
		del word_doc["_id"]
		self.write(word_doc)

if __name__ == "__main__":
	options.parse_command_line()
	httpserver.HTTPServer(Application()).listen(options.port)
	ioloop.IOLoop.instance().start()
