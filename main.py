from core import *
import json, os, argparse

apiKey = "RGAPI-c4fb8f13-8e51-425e-98ce-e726c2c93020"
region = "euw1"

rito = Rito(apiKey, region)

def getLeaguePlayerData(queue, tier, division, season):	
	leagueData = rito.league(queue, tier, division)
	for player in leagueData:
		try:
			playerName = player["summonerName"]
			getPlayerData(playerName, season)
			
		except:
			pass

def getPlayerData(playerName, season):
	folder = "data/%s" % playerName
	if not os.path.exists(folder):
		os.mkdir(folder)

	if not os.path.exists("%s/player.json" % folder):
		playerData = rito.player(playerName)
		rito.saveFile("%s/player.json" % folder, playerData)
	else:
		playerData = json.loads(open("%s/player.json" % folder, "r").read())

	accountId = playerData["accountId"]
	if not os.path.exists("%s/matchs.json" % folder):
		matchs = rito.matchList(accountId, 420, season)
		rito.saveFile("%s/matchs.json" % folder, matchs)
	else:
		matchs = json.loads(open("%s/matchs.json" % folder, "r").read())

	matchFolder = "%s/matchs" % folder
	if not os.path.exists(matchFolder):
		os.mkdir(matchFolder)
	
	if matchs["endIndex"] > len(os.listdir(matchFolder)):
		for match in matchs["matches"]:
			gameId = match["gameId"]
			if not os.path.exists("%s/%s.json" % (matchFolder, gameId)):
				rito.saveFile("%s/%s.json" % (matchFolder, gameId), rito.match(gameId))

def processPlayerData():
	totalMatch = 0
	totalWinDuo = 0
	totalWinSolo = 0
	totalDuo = 0
	totalSolo = 0

	for playerName in os.listdir("data/"):
		folder = "data/%s" % playerName

		if os.path.exists("%s/player.json" % folder):
			player = json.loads(open("%s/player.json" % folder, 'r').read())
			print("\nPlayer : %s" % playerName)

			matchFolder = "%s/matchs/" % folder
			matchs = Matchs(playerName)
			
			for matchFile in os.listdir(matchFolder):
				match = Match(json.loads(open("%s%s" % (matchFolder, matchFile), 'r').read()))
				matchs.append(match)
			
			stats = matchs.stats()
			matchsCount = stats["gameDuo"] + stats["gameSolo"]

			totalMatch += matchsCount
			totalWinDuo += stats["winDuo"]
			totalWinSolo += stats["winSolo"]
			totalDuo += stats["gameDuo"]
			totalSolo += stats["gameSolo"]

			winCount = stats["winDuo"] + stats["winSolo"]

			print("All - Win / Lose / Total : %d / %d / %d" % (winCount, matchsCount - winCount, matchsCount))
			print("Duo - Win / Lose / Total : %d / %d / %d" % (stats["winDuo"], stats["gameDuo"] - stats["winDuo"], stats["gameDuo"]))
			print("Solo - Win / Lose / Total : %d / %d / %d" % (stats["winSolo"], stats["gameSolo"] - stats["winSolo"], stats["gameSolo"]))
	
	print("\nTotal matchs : %d" % totalMatch)
	print("Total - win duo / duo : %d / %d" % (totalWinDuo, totalDuo))
	print("Total - win solo / solo : %d / %d" % (totalWinSolo, totalSolo))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Make stats on rito ranked algorithm')
	parser.add_argument('--player', action='store', type=str, help="Fetch data for a player")
	parser.add_argument('--league', action='store_true', help="Fetch league data")
	parser.add_argument('--process', action='store_true', help="Process the data in the data folder")
	
	args, rem_args = parser.parse_known_args()

	if args.player or args.league:
		parser.add_argument('--season', action='store', type=int, help="Fetch data for this season", required=True)

	if args.league:
		parser.add_argument('--queue', action='store', type=str, choices=["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"], required=True)
		parser.add_argument('--tier', action='store', type=str, choices=["IRON", "BRONZE", "SILVER", "GOLD", "DIAMOND"], required=True)
		parser.add_argument('--division', action='store', type=str, choices=["I", "II", "III", "IV"], required=True)
	
	parser.parse_args(rem_args, namespace = args)

	if args.player:
		getPlayerData(args.player, args.season)
	elif args.league:
		getLeaguePlayerData(args.queue, args.tier, args.division, args.season)
	elif args.process:
		processPlayerData()