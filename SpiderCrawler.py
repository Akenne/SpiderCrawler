import urllib.request as urllib2
import xml.etree.ElementTree as ET
import requests
from xml.dom.minidom import parseString
import pickle
import App
import threading
import ctypes
import json
import queue
import time

gameid = '440' #tf2 is 440
itemschema = {}
run = True
restart = True
count = 0
fcount = 0
ecount = 0

def schema(tf):#get item schema to find item names
    global API
    if tf:
        ctypes.windll.user32.MessageBoxW(0, 'Updating schema, please wait', "Hold on", 0)
        itemschema = {}
        try:
            url = 'http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key={}&format=json'.format(API)
            data = json.loads(((urllib2.urlopen(url)).read()).decode("utf8"))
        except:
            ctypes.windll.user32.MessageBoxW(0, 'Steam is acting slow, please wait', "Hold on", 0)
            return schema(tf)
        for i in data["result"]["items"]:
            print(i['name'])
            itemschema[i['defindex']] = i['name']
        itemschema[126] = 'Bill\'s hat'
        itemschema[143] = 'Earbuds'
        itemschema[160] = 'Vintage Lugermorph'
        itemschema[161] = 'Big Kill'
        itemschema[162] = 'Max\'s head'
        pickle.dump(itemschema, open(".\data\save.p", "wb"))
        ctypes.windll.user32.MessageBoxW(0, 'Schema updated', "Done", 0)
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
        try:
            with open('.\data\past.txt', 'r+') as in_file:
                past = in_file.read().split('\n')
        except:
            past = []
        try:
            with open('.\data\\future.txt', 'r+') as in_file:
                future = in_file.read().split('\n')
        except:
            future = []
        try:
            with open('.\data\\found.txt', 'r+') as in_file:
                found = in_file.read().split('\n')
        except:
            found = []

def getid(vanity): #converts vanity url to steam id
    global API
    try:
        url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}&format=json'.format(API, vanity)
        data = json.loads(((urllib2.urlopen(url)).read()).decode("utf8"))
        if('steamid' not in data["response"]):
            ctypes.windll.user32.MessageBoxW(0, 'Please enter a correct steamid or vanityurl', "Error", 0)
            return "0"
        return data['response']['steamid']
    except:
        ctypes.windll.user32.MessageBoxW(0, 'Steam is acting slow, please wait', "Hold on", 0)
        return getid(vanity)

def getfriend(id): #get user ids of friends
    global future
    global API
    count = 0
    try:
        url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend&format=json'.format(API, id)
        data = json.loads(((urllib2.urlopen(url)).read()).decode("utf8"))
        for i in data['friendslist']['friends']:
            count += 1
            if count >25:
                return
            future.append(i['steamid'])
    except Exception as e:
        print(e)
        pass

def hours(id): #find steam hours
    global API, gameid, ecount, future
    try:
        url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&format=json&input_json={{"appids_filter":[{}],"include_played_free_games":1,"steamid":{}}}'.format(API, gameid, id)
        data = json.loads(((urllib2.urlopen(url)).read()).decode("utf8"))
        hours = ((data['response']['games'][0]['playtime_forever'])/60)
        try:
            rhours = (data['response']['games'][0]['playtime_2weeks'])/60
        except:
            rhours = 0
        if len(future) < 200 and hours>500:
            getfriend(id)
        return hours, rhours
    except:
        return 50000, 0

def backpack(id, gen, bud, bill, unu, maxs, bmoc, salv, traded, f2p, untradable): # check backpack
    global API, gameid, found, fcount, run, ecount, itemschema
    try:
        url = 'http://api.steampowered.com/IEconItems_{}/GetPlayerItems/v0001/?key={}&steamid={}&format=json'.format(gameid, API, id)
        data = json.loads(((urllib2.urlopen(url)).read()).decode("utf8"))
    except Exception as e:
        return ''
    got = ''
    if 'num_backpack_slots' in data['result']:
        if (data['result']['num_backpack_slots'] < 150) and f2p:
            return got
    if 'items' in data['result']:
        for item in data['result']['items']:
            if ('flag_cannot_trade' in item) and untradable:
                continue
            elif (item['quality'] == 5 and item['defindex'] not in [267, 266] and unu):
                pass
            elif (item['quality'] == 1 and gen):
                pass
            elif (item['defindex'] == 143 and bud):
                pass
            elif (item['defindex'] == 126 and bill):
                pass
            elif (item['defindex'] in [160,161,162] and maxs):
                pass
            elif (item['defindex'] == 666 and bmoc):
                pass
            elif (item['defindex'] == 5068 and salv):
                pass
            else:
                continue
            if traded and not (item['id'] == item['original_id']):
                continue
            if got != '':
                got+= ', '
            if item['quality'] == 5:
                got+= 'Unusual '
            got += itemschema[int(item['defindex'])]
        if got != '':
            found.append(id)
            fcount+= 1
    return got

def files(): #save lists to files
    global past, future, found
    with open('.\data\past.txt', 'w') as out_file:
        out_file.write('\n'.join(past))
    with open('.\data\\future.txt', 'w') as out_file:
        out_file.write('\n'.join(future))
    with open('.\data\\found.txt', 'w') as out_file:
        out_file.write('\n'.join(found))


def online(id, online, onlinedays, offline):
    global API
    a = False
    b = False
    try:
        url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json'.format(API, id)
        data = json.loads(((urllib2.urlopen(url)).read()).decode("utf8"))
    except Exception as e:
        return a, b
    if online:
        if (onlinedays < ((time.time() - data['response']['players'][0]['lastlogoff'])/86400)):
            a = True
    if offline: 
        if data['response']['players'][0]['personastate'] == 0:
            b = True
    return a, b


if __name__ == '__main__':
    global app
    app = App.Application()

def start(schea, res, id):
    global past, future, found, itemschema, run, qid, qhour, qgot, qcount, iq, run
    itemschema = schema(schea)
    reset(res)
    if id != '':
        if id.startswith("7656"):
            tempid = id
        else:
            tempid = getid(id)
        if tempid.startswith("7656"):
            future.append(tempid)
        else:
            run = False
    else:
        reset(False)
    qid = queue.Queue()
    qhour = queue.Queue()
    qgot = queue.Queue()
    qcount = 0
    iq = queue.Queue()

def hunt(a, iq, gen, bud, bill, unu, maxs, bmoc, salv, maxhours, traded, f2p, untradable, minrhours, minhours, maxrhours, on, onlinedays, offline):
    global past, run, count, qid, qhour, qgot, future, restart, API
    while iq.qsize() != 0 and run and restart:
        i = iq.get()
        if i in future:
            try:
                future.remove(i)
            except:
                pass
        if i == "":
            ctypes.windll.user32.MessageBoxW(0, 'Please enter an ID', "Error", 0)
            run = False
        if run:
            count +=1
            a.updateGUI()
            if i not in past:
                past.append(i)
                if len(past) % 51 == 0:
                        files()
                if on or offline:
                    onl, off = online(i, on, onlinedays, offline)
                    if onl or off:
                        continue
                uhour, rhours = hours(i)
                if minhours<=uhour<=maxhours and minrhours<=rhours<=maxrhours:
                    got = backpack(i, gen, bud, bill, unu, maxs, bmoc, salv, traded, f2p, untradable)
                    if got != '':
                        item = [i, int(uhour), got]
                        a.graph.tree.insert('', 'end', values=item)  

def go(threads, a, gen, bud, bill, unu, maxs, bmoc, salv, maxhours, traded, f2p, untradable, minrhours, minhours, maxrhours, on, onlinedays, offline):
    global future, run, qid, qcount, iq, past, restart,fcounts
    while len(future) != 0:
        for i in future:
            if run:
                while i in future:
                    if not qid.empty():
                        item = [str(qid.get()), str(qhour.get()), str(qgot.get())]
                        a.graph.tree.insert('', 'end', values=item) 
                    if len(future) < 100:
                        getfriend(i)
                    if 100 >(iq.qsize()):
                        iq.put(i)
                        try:
                            future.remove(i)
                        except:
                            pass
                    if (qid.empty() and qcount<threads):
                        qcount += 1
                        t = threading.Thread(target=hunt, args = (a, iq, gen, bud, bill, unu, maxs, bmoc, salv, maxhours, traded, f2p, untradable, minrhours, minhours, maxrhours, on, onlinedays, offline))
                        t.daemon = True
                        t.start()
            else:
                a.stop()
                return
            if not restart:
                restart = True
                a.stop()
                a.start()
                return
    if run:
        a.stop()
        a.start()
    else:
        a.stop()