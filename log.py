#!/usr/bin/env python

# Minecraft server.log parser
# Version 0.2
# Author: ShadowPrince (5Shadow7Prince at bukkit.org)

CHAT_EXP = r'^(.+) \[INFO\] \[(.*)\] (\S+): (.+)'
# my server chat expression

CHAT_EXP = r'^(.+) \[INFO\] ()\<(\S+)\> (.+)'
# standart MC chat expression
# must return: rank, player, message
# in my server, players rank displays prev name, in []
# there is empty var

PM_EXP = r'^(.+) \[INFO\] \[HeroChat\] (\S+) -> (\S+): (.*)'
# hero chat personal message standart expression

import sys, os, re
def in_(val, arr):
	if arr:
		if val in arr:
			return True
		else:
			return False
	else:
		if not ips+players:
			return True
		else:
			return False

def ipin(*ipss):
	add = False
	if not ips:
		return false
	for ip in ipss:
		ip = ip.split(':')[0]
		if ips:
			for iip in ips:
				iip = iip.replace('*', '.+')
				if re.search(iip, ip):
					add = True
		else:
			add = True
	return add

def pin(*pls):
	add = False
	for pl in pls:
		if in_(pl, players):
			add = True
		else:
			if 'pstrict' in config:
				return False
	return add

lines = []
players = []
logs = []
paths = []
outputs = []
config = []
ips = []
commands = {
	'/p': players, # for player
	'/l': logs,    # for log type
	'/f': paths,   # input file
	'/o': outputs, # output file
	'/i': ips,		 # ips
	'/c': config,  # config
}
for arg in sys.argv[1:]:
	commands[arg[:2]].append(arg[3:])
if not logs+players+ips:
	config.append('help')

print '=== Start reading files ==='
if not paths:
	print '[!] Empty paths, added server.log for default.'
	paths.append('server.log')
for path in paths:
	try:
		lines += open(path, 'r').readlines()
	except IOError:
		print '[!] File %s not found!' % path
result = []
if 'help' in config:
	print '=== Help =='
	result.append("""Arguments:
	/l=LOGTYPE: prints logs of LOGTYPE
		Types: start: on server start
					 login: on player login'
					 shop: on player used ChestShop
					 chat: on player chat
					 pm: on player pm
					 pv_cmd: PlayerViser command logs,
					 pv_pd: PlayerViser on drop/pickup logs,
					 pv_tp: PlayerViser teleport logs,
					 pv_death: PlayerViser death logs
	/p=PLAYER: prints logs of PLAYER
	/i=IP: prints logs of IP (only login logs!)
	/f=FILEPATH: opens server log on FILEPATH
	/o=OUTPATH: writes file on OUTPATH with output
	/c=CONFIGPARAM: adds CONFIGPARAM to the config
		Parameters:
			'adminshop': logs with 'Admin Shop'
			'pstrict': logs with ALL players defined with /p
Arguments can be multiple!
This help can also available with '/c=help'.
Working with minecraft server 1.1, ChestShop, HeroChat (with rank in '[]') or default MC chat (configuring in first lines of the script).
You also can write regexp by yourself, all information at the first lines.
Log types, what starts with 'pv_' requires plugin PlayerViser (dev.bukkit.org/server-mods/playerviser/).

Example queryes:
	./log.py /p=5Shadow7Prince /l=chat - display all chat by ShadowPrince
	./log.py /p=5Shadow7Prince /p=Devil_Chrono /l=shop /c=pstrict - display all ChestShop histrory BETWEEN 5Shadow7Prince and Devil_Chrono
	./log.py /p=5Shadow7Prince /l=login /l=pv_cmd - displays all 5Shadow7Prince login logs and entered commands (by plugin PlayerViser)


by ShadowPrince, 2012.
	""")
else:
	print '=== Start parsing lines ==='
	for line in lines:
		if in_('pv_death', logs):
			search = re.search(r'^(.+) \[INFO\] \[PV\] \[LOG\] Player (\S+) (death) (.+)', line)
			if search:
				time = search.group(1)
				player = search.group(2)
				tt = search.group(3)
				info = search.group(4)
				if pin(player):
					result.append( '%s %s %s, at %s' % (player, tt, info, time) )
		if in_('pv_tp', logs):
			search = re.search(r'^(.+) \[INFO\] \[PV\] \[LOG\] Player (\S+) (teleported) (.+)', line)
			if search:
				time = search.group(1)
				player = search.group(2)
				tt = search.group(3)
				info = search.group(4)
				if pin(player):
					result.append( '%s %s %s, at %s' % (player, tt, info, time) )
		if in_('pv_pd', logs):
			search = re.search(r'^(.+) \[INFO\] \[PV\] \[LOG\] Player (\S+) ([drop pickup]+) (.+)', line)
			if search:
				time = search.group(1)
				player = search.group(2)
				tt = search.group(3)
				info = search.group(4)
				if pin(player):
					result.append( '%s %s %s, at %s' % (player, tt, info, time) )
		if in_('pv_cmd', logs):
			search = re.search(r'^(.+) \[INFO\] \[PV\] \[LOG\] Player (\S+) ([command]+) (.+)', line)
			if search:
				time = search.group(1)
				player = search.group(2)
				tt = search.group(3)
				info = search.group(4)
				if pin(player):
					result.append( '%s %s %s, at %s' % (player, tt, info, time) )
		if in_('login', logs):
			search = re.search(r'^(.+) \[INFO\] (\S+) (\S+) logged', line)
			if search:
				time = search.group(1)
				player = search.group(2)
				ip = search.group(3)[2:-1]
				if pin(player) or ipin(ip):
					result.append( '%s logged from %s, at %s' % (player, ip, time) )
		if in_('chat', logs):
			search = re.search(CHAT_EXP, line)
			if search:
				time = search.group(1)
				letter = search.group(2)
				player = search.group(3)
				message = search.group(4)
				if pin(player):
					result.append( '[%s] [%s] %s: %s' % (time, letter, player, message))
		if in_('start', logs):
			search = re.search(r'^(.+) \[INFO\] Starting minecraft', line)
			if search:
				time = search.group(1)
				result.append('Server started at %s' % time)
		if in_('shop', logs):
			if 'adminshop' in config:
				search = re.search(r'^(.+) \[INFO\] \[ChestShop\] (\S+) (\S+) (\d+) (\S+) (\S+) (\S+) \S+ Admin Shop$', line)
			else:
				search = re.search(r'^(.+) \[INFO\] \[ChestShop\] (\S+) (\S+) (\d+) (\S+) (\S+) (\S+) \S+ (\S+)$', line)
			if search:
				time = search.group(1)
				player1 = search.group(2)
				t = search.group(3)
				count = search.group(4)
				item = search.group(5)
				tt = search.group(6)
				price = search.group(7)
				if 'adminshop' in config:
					player2 = 'Admin Shop'
				else:
					player2 = search.group(8)
				if pin(player1, player2):
					result.append( '%s %s %s(%s)[%s] %s %s at %s' % (player1, t, item, count, price, tt, player2, time) )
					# 		
		if in_('pm', logs):
			search = re.search(r'^(.+) \[INFO\] \[HeroChat\] (\S+) -> (\S+): (.*)', line)
			if search:
				time = search.group(1)
				player1 = search.group(2)
				player2 = search.group(3)
				msg = search.group(4)

				if in_(player1, players) or in_(player2, players):
					result.append('[%s] %s->%s: %s' % (time, player1, player2, msg))
		    
print '=== Start outputting ==='
if not result:
	print '[!] Empty result!'
else:
	if not outputs:
		for line in result:
			print line
	else:
		print '[.] Output in files.'
		for out in outputs:
			print '[.] Writting file %s...' % out
			f = open(out, 'wb')
			f.write('\n'.join(result))
			f.close()

