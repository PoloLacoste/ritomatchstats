class Match(object):

	def __init__(self, data):
		self._data = data
		self._players = {}
		self._playersname = {}
		self._processPlayers()

	def _processPlayers(self):
		try:
			for identities in self._data["participantIdentities"]:
				self._players[identities["participantId"]] = identities["player"]
				self._playersname[identities["player"]["summonerName"]] = identities["participantId"]
		except:
			return
		
		winnerTeamId = None

		for team in self._data["teams"]:
			if team["win"] == "Win":
				winnerTeamId = team["teamId"]
		
		for participant in self._data["participants"]:
			participantId = participant["participantId"]

			self._players[participantId]["teamId"] = participant["teamId"]

			if participant["teamId"] == winnerTeamId:
				self._players[participantId]["win"] = True
			else:
				self._players[participantId]["win"] = False
	
	def getPlayerWin(self, playerName):
		playerName = playerName.decode("latin1")
		return self._players[self._playersname[playerName]]["win"] if playerName in self._playersname else None
	
	def getTeamPlayers(self, playerName):
		playerName = playerName.decode("latin1")
		if playerName not in self._playersname:
			return []
		teamId = self._players[self._playersname[playerName]]["teamId"]
		teamPlayers = []
		for player in self._players.values():
			if player["teamId"] == teamId and player["summonerName"] != playerName:
				teamPlayers.append(player["summonerName"])
		return teamPlayers

class Matchs(list):

	def __init__(self, player):
		self.player = player

	def stats(self):
		lastTeamMates = []
		winDuo = 0
		gameDuo = 0

		winSolo = 0
		gameSolo = 0

		first = True

		for match in self:
			players = match.getTeamPlayers(self.player)
			duo = False

			for player in players:
				if player is not self.player:
					if player in lastTeamMates:
						duo = True
						gameDuo += 1
						if match.getPlayerWin(self.player):
							winDuo += 1
						break
			
			if not duo:
				gameSolo += 1
				if match.getPlayerWin(self.player):
					winSolo += 1
			
			lastTeamMates = players

		return {
			"winDuo": winDuo,
			"gameDuo": gameDuo,
			"winSolo": winSolo,
			"gameSolo": gameSolo
		}	