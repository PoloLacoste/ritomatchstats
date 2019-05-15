import requests, json, logging, time
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
		time.sleep(1.1)

		reqUrl = "%s%s" % (self.url, uri)
		req = requests.get(reqUrl, headers=self.headers)
		
		if req.status_code == 200:
			self.logger.debug("TS : %d Code %d on %s" % (time.time(), req.status_code, reqUrl))
		else:
			self.logger.error("Error requesting : %s" % reqUrl)
			self.logger.error("Status code : %d" % req.status_code)
			self.logger.error("Reason : %s" % req.reason)
			return None
		
		return req.json()
	
	def saveFile(self, path, data):
		with open(path, 'w') as w:
			w.write(json.dumps(data))
	
	def player(self, playername):
		return self.request("/lol/summoner/v4/summoners/by-name/%s" % playername)
	
	def matchList(self, accountid, queue=None, season=None, endIndex=100):
		url = "/lol/match/v4/matchlists/by-account/%s?" % accountid

		if queue is not None:
			url += "queue=%s&" % queue
		if season is not None:
			url += "season=%s&" % season
		if endIndex is not None:
			url += "endIndex=%s" % endIndex
		
		return self.request(url)
	
	def match(self, gameid):
		return self.request("/lol/match/v4/matches/%s" % gameid)
	
	def matchTimeline(self, gameid):
		return self.request("/lol/match/v4/timelines/by-match/%s" % gameid)
	
	def league(self, queue, tier, division):
		return self.request("/lol/league/v4/entries/%s/%s/%s" % (queue, tier, division))