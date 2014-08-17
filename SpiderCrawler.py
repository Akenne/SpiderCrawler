import urllib.request as urllib2
import xml.etree.ElementTree as ET
import requests
from xml.dom.minidom import parseString
import pickle
import App
import threading
import ctypes

STEAM_API_KEY = '32EADD85E6F53CB6AAF6D21558ED6C73' #your steam api key
gameid = '440' #tf2 is 440
itemschema = {}
run = True
got = ''

def schema(tf):#get item schema to find item names
	global STEAM_API_KEY
	if tf:
		ctypes.windll.user32.MessageBoxW(0, 'Updating schema, please wait ~ 30 secs', "Hold on", 0)
		try:
			schema_r = urllib2.urlopen(('http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key={}&format=xml').format(STEAM_API_KEY))
		except:
			ctypes.windll.user32.MessageBoxW(0, 'Steam is acting slow, please wait', "Hold on", 0)
			return schema(tf)
		owned = schema_r.read()
		data = ET.fromstring(owned)
		itemschema = {}
		for item in data.findall("./items/item"):
			defindex = item.find('defindex').text
			itemschema[defindex] = item.find('name').text
		pickle.dump(itemschema, open(".\data\save.p", "wb"))
		return itemschema
	else:
		try:
			return pickle.load(open(".\data\save.p", "rb" ))
		except:
			return schema(True)

def reset(tf): #resets text files that contain steam ids
	global past, future, found
	if tf:
		past = []
		future = []
		found = []
	else:
		with open('.\data\past.txt', 'r+') as in_file:
			past = in_file.read().split('\n')
		with open('.\data\\future.txt', 'r+') as in_file:
			future = in_file.read().split('\n')
		with open('.\data\\found.txt', 'r+') as in_file:
			found = in_file.read().split('\n')

def getid(vanity): #converts vanity url to steam id
	global STEAM_API_KEY
	try:
		username_r = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}&format=xml'.format(STEAM_API_KEY, vanity))
		return str(parseString(username_r.text.encode('utf-8')).getElementsByTagName('steamid')[0].firstChild.wholeText)
	except:
		ctypes.windll.user32.MessageBoxW(0, 'Steam is acting slow, please wait', "Hold on", 0)
		return getid(vanity)


def getfriend(id): #get user ids of friends
	global future
	global STEAM_API_KEY
	try:
		friends_r = requests.get(('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend&format=xml').format(STEAM_API_KEY, id))
		for i in (parseString(friends_r.text.encode('utf-8')).getElementsByTagName('steamid')):
			future.append(i.firstChild.data)
	except:
		pass

def hours(id): #find steam hours
	global STEAM_API_KEY, gameid
	ownedgames_r = urllib2.urlopen(('http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={}&steamid={}&include_played_free_games=1&format=xml').format(STEAM_API_KEY, id))
	owned = ownedgames_r.read()
	data = ET.fromstring(owned)
	for message in data.findall("./games/message"):
		if message.find('appid').text.startswith(gameid):
			minutes = int(message.find('playtime_forever').text) 
			return minutes/60
	return 0

def backpack(id, gen, bud, bill, unu, maxs, bmoc, salv, traded): # check backpack
	global STEAM_API_KEY, gameid, found, fcount, got
	try:
		backpack_r = urllib2.urlopen(('http://api.steampowered.com/IEconItems_{}/GetPlayerItems/v0001/?key={}&steamid={}&format=xml').format(gameid, STEAM_API_KEY, id))
	except:
		ctypes.windll.user32.MessageBoxW(0, 'Steam is acting slow, please wait', "Hold on", 0)
		return backpack(id, gen, bud, bill, unu, maxs, bmoc, salv, traded)
	backpack = backpack_r.read()
	data = ET.fromstring(backpack)
	got = ''
	for item in data.findall("./items/item"):
		if (item.find('quality').text.startswith('5') and int(item.find('defindex').text) not in [267, 266] and unu):
			pass
		elif(item.find('quality').text.startswith('1') and gen):
			pass
		elif(int(item.find('defindex').text) == 143 and bud):
			pass
		elif(int(item.find('defindex').text) == 126 and bill):
			pass
		elif(int(item.find('defindex').text) in [160,161,162] and maxs):
			pass
		elif(int(item.find('defindex').text) == 666 and bmoc):
			pass
		elif(int(item.find('defindex').text) == 5068 and salv):
			pass
		else:
			continue
		if traded and not int(item.find('id').text) == int(item.find('original_id').text):
			continue
		found.append(id)
		if got != '':
			got+= ', '
		got += itemschema[item.find('defindex').text]
	if got != '':
		fcount+= 1
		return True
	else:
		return False

def original(item):
	if int(item.find('id').text) == int(item.find('original_id').text):
		return True
	else:
		return False

def files(): #save lists to files
	global past, future, found
	with open('.\past.txt', 'w') as out_file:
	    out_file.write('\n'.join(past))
	with open('.\data\\future.txt', 'w') as out_file:
	    out_file.write('\n'.join(future))
	with open('.\data\\found.txt', 'w') as out_file:
	    out_file.write('\n'.join(found))

if __name__ == '__main__':
	global app
	app = App.Application()

def start(schea, res, id):
	global past, future, found, itemschema, count, fcount
	itemschema = schema(schea)
	reset(res)
	count = 0
	fcount = 0
	if id != '':
		if id.startswith("7656"):
			tempid = id
		else:
			tempid = getid(id)
		if tempid not in past:
			future.append(tempid)

def go(gen, bud, bill, unu, maxs, bmoc, salv, hour, traded):
	global past, future, temschema, run, count
	while len(future) != 0:
		for i in future:
			if run:
				count +=1
				files()
				future.remove(i)
				if i not in past:
					past.append(i)
					getfriend(i)
					uhour = hours(i)
					if uhour<hour:
						if backpack(i, gen, bud, bill, unu, maxs, bmoc, salv, traded):
							return(i, int(uhour), got)
				return