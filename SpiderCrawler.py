try:
    import urllib.request as urllib2
except:
    import urllib2
import xml.etree.ElementTree as ET
import requests
from xml.dom.minidom import parseString


reset = False #If you want to contiinue where you left off or reset?
fake = ['267', '266']
STEAM_API_KEY = '32EADD85E6F53CB6AAF6D21558ED6C73' #your steam api key
BACKPACK_TF_API_KEY = '53e1698f4f96f4977e8b4567'
STEAM_USERNAME = 'Lotorens' #initial steam name
target = 250 #maximum hours
gameid = '440' #tf2 is 440

if reset == False:
	with open('past.txt', 'r+') as in_file:
		past = in_file.read().split('\n')
	with open('future.txt', 'r+') as in_file:
		future = in_file.read().split('\n')
	with open('found.txt', 'r+') as in_file:
		found = in_file.read().split('\n')
else:
	past = []
	future = []
	found = []

def getid(vanity): #converts vanity url to steam id
	global STEAM_API_KEY
	username_r = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}&format=xml'.format(STEAM_API_KEY, vanity))
	return str(parseString(username_r.text.encode('utf-8')).getElementsByTagName('steamid')[0].firstChild.wholeText)


def getfriend(id):
	global future
	global STEAM_API_KEY
	friends_r = requests.get(('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend&format=xml').format(STEAM_API_KEY, id))
	try:
		for i in (parseString(friends_r.text.encode('utf-8')).getElementsByTagName('steamid')):
			future.append(i.firstChild.data)
	except:
		pass


def hours(id):
	global STEAM_API_KEY, gameid
	ownedgames_r = urllib2.urlopen(('http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={}&steamid={}&include_played_free_games=1&format=xml').format(STEAM_API_KEY, id))
	owned = ownedgames_r.read()
	data = ET.fromstring(owned)
	for message in data.findall("./games/message"):
		if message.find('appid').text.startswith(gameid):
			minutes = int(message.find('playtime_forever').text) 
			return minutes/60
	return 0

def backpack(id):
	global STEAM_API_KEY, gameid, found
	backpack_r = urllib2.urlopen(('http://api.steampowered.com/IEconItems_{}/GetPlayerItems/v0001/?key={}&steamid={}&format=xml').format(gameid, STEAM_API_KEY, id))
	backpack = backpack_r.read()
	data = ET.fromstring(backpack)
	for item in data.findall("./items/item"):
		if item.find('quality').text.startswith('5') and item.find('defindex').text not in fake:
			found.append(id)
			print("Found")
			break

def files():
	global past, future, found
	with open('past.txt', 'w') as out_file:
	    out_file.write('\n'.join(past))
	with open('future.txt', 'w') as out_file:
	    out_file.write('\n'.join(future))
	with open('found.txt', 'w') as out_file:
	    out_file.write('\n'.join(found))

if __name__ == '__main__':
	if STEAM_USERNAME != '':
		future.append(getid(STEAM_USERNAME))
	count = 0
	while len(future) != 0:
		for i in future:
			count +=1
			if count%25 == 0:
				print (count)
			files()
			future.remove(i)
			if i in past:
				break
			else:
				past.append(i)
				getfriend(i)
				if hours(i)<target:
					backpack(i)




#check if id is proper
#check friends list
#check hours
#check items worth value
#