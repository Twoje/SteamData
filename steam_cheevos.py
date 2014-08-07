import urllib2
import simplejson
from collections import OrderedDict
import privatedata


api_key = privatedata.api_key
owned_games_api_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
achievements_api_url = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?"
steam_id = "76561197961862413"

# Get list of games user owns
req = urllib2.Request(owned_games_api_url + "key=" + api_key + "&steamid=" + steam_id);
opener = urllib2.build_opener()
f = opener.open(req)
data = simplejson.load(f)
games = []
for game in data["response"]["games"]:
	games.append(game['appid'])

# Get achievement percentages for all games
games_and_achievements = {}
print("Loading data"),
for game in games:
	print("."),
	appid = str(game)
	req = urllib2.Request(achievements_api_url + "appid=" + appid + "&key=" + api_key + "&steamid=" + steam_id)

	# Make sure game has achievements
	try:
		f = opener.open(req)
	except urllib2.HTTPError, error:
		continue
	data = simplejson.load(f)

	# Get Achievement Counts
	achieved_count = total_count = 0
	if data['playerstats'].get('achievements') != None:
		for achievement in data['playerstats']['achievements']:
			total_count += 1
			if achievement['achieved'] == 1:
				achieved_count += 1
	else:
		continue

	if achieved_count == 0:
		continue

	# Get percentage of achievements earned
	percent_achieved = round(float(achieved_count) / float(total_count) * 100, 2)

	game_name = data['playerstats']['gameName'].encode('utf-8')

	# Store percentage in list
	games_and_achievements[game_name] = percent_achieved
print(".")
sorted_games_and_achievements = OrderedDict(sorted(games_and_achievements.items(), key=lambda x: x[1]))
for game, percent_achieved in sorted_games_and_achievements.iteritems():
	print game + ' - ' + str(percent_achieved) + '% achieved'