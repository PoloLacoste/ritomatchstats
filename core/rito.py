import requests, json, logging
logging.basicConfig()

class Rito(object):

	def __init__(self, apiKey, region):
		self.apiKey = apiKey
		self.region = region
		self.url = "https://%s.api.riotgames.com/" % self.region
		self.headers = {
			"X-Riot-Token": self.apiKey
		}
		self.logger = logging.getLogger("Rito")
		self.logger.setLevel(logging.DEBUG)
	
	def request(self, uri):
		reqUrl = "%s%s" % (self.url, uri)
		req = requests.get(reqUrl, headers=self.headers)
		if req.status_code == 200:
			self.logger.debug("Code %d on %s" % (req.status_code, reqUrl))
		else:
			self.logger.error("Error requesting : %s" % reqUrl)
			self.logger.error("Status code : %d" % req.status_code)
			self.logger.error("Reason : %s" % req.reason)
	
	def saveFile(self, path, data):
		with open(path, 'w') as w:
			w.write(json.dumps(data))