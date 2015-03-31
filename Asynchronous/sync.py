
from tornado import httpserver, web, httpclient, ioloop
from tornado.options import options, define

import urllib
import json
import datetime
import time

PORT = 8000

from tornado.options import define, options
define("port",default=PORT,help="run on at %s" % PORT, type=int)

class Application(web.Application):
	def __init__(self):
		handlers = [
		(r'/',IndexHandler)
		]
		settings = dict(debug=True)
		super(Application,self).__init__(handlers,**settings)

class IndexHandler(web.RequestHandler):
	def get(self):
	
		query = self.get_argument('q')
		client = httpclient.HTTPClient()
		response = client.fetch("http://www.reddit.com/search.json?" + \
			urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}))
		body = json.loads(response.body)
		# import ipdb; ipdb.set_trace()
		result_count = len(body['data'])
		now = datetime.datetime.utcnow()
		raw_oldest_tweet_at = body['data']['children'][-1]['data']['created']
		# oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
		# 	"%a, %d %b %Y %H:%M:%S +0000")
		# seconds_diff = time.mktime(now.timetuple()) - \
		# time.mktime(raw_oldest_tweet_at.timetuple())
		# tweets_per_second = float(result_count) / seconds_diff

		self.write("""
			<div style="text-align: center">
			<div style="font-size: 72px">%s</div>
			<div style="font-size: 144px">%.02f</div>
			<div style="font-size: 24px">tweets per second</div>
			</div>""" % (query, time.time() - raw_oldest_tweet_at))

if __name__ == "__main__":
	options.parse_command_line()
	httpserver.HTTPServer(Application()).listen(options.port)
	ioloop.IOLoop.instance().start()

