#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
	from pip import main as pipmain
except:
	from pip._internal import main as pipmain

'''

Copyright 2019. Aurelio Somarriba Lucas

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''


import os, getopt, select, re, errno, copy, signal
import sys, time, random, string, socket, struct, os.path, datetime
from datetime import timedelta
from optparse import OptionParser
from optparse import OptionGroup
from urlparse import urljoin
from collections import OrderedDict
from time import sleep
import subprocess
import json #as simplejson
import getpass
import csv
from os.path import expanduser
import pprint
import calendar
import urllib
import base64
import locale
import time
import curses
import random
from collections import namedtuple
from HTMLParser import HTMLParser

class bcolors:
	HEADER = '\033[95m'
	TURQUO = '\033[96m'
	WHITEGREY = '\033[100m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	WHITE = '\033[97m'
	BROWN = '\033[33m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	BIG = '\033#3'
	BLINK = '\033[5m'
	BLINKF = '\033[6m'
	CLEAR = '\033[2J'
	ALIGN = '\033#8'
	BACKWHITE = '\033[37m'

autoInstall = False
try:
	reqFile = open('requirements.txt', 'r')
	contents = reqFile.readlines()
	#print contents[0]
	reqReDo = False
	if '==' in contents[0]:
		#print contents[0].split('==')[1].strip()
		if contents[0].split('==')[1].strip() == '3.2':
			pass
		else:
			reqReDo = True
	else:
		reqReDo = True
	if reqReDo == True:
		f = open('requirements.txt', 'w+')
		libraries = '''# version==3.2
nose==1.3.7
xlrd==1.2.0
pandas==0.24.2
requests==2.18.4
texttable==0.8.7
pyopenssl==17.2.0
dnspython==1.15.0
Pygments==2.2.0
paramiko==2.3.1
edgegrid-python==1.0.10
XlsxWriter==1.1.1
beautifulsoup4==4.6.0
pyfiglet==0.8.post1
#
'''
		f.write(libraries)
		f.close()
except:
	f = open('requirements.txt', 'w+')
	libraries = '''# version==3.2
nose==1.3.7
xlrd==1.2.0
pandas==0.24.2
requests==2.18.4
texttable==0.8.7
pyopenssl==17.2.0
dnspython==1.15.0
Pygments==2.2.0
paramiko==2.3.1
edgegrid-python==1.0.10
XlsxWriter==1.1.1
beautifulsoup4==4.6.0
pyfiglet==0.8.post1
#
'''
	f.write(libraries)
	f.close()

try:
	import pandas
	import xlsxwriter
	import texttable as tt
	from requests import Request, Session
	import requests
	from pygments import highlight, lexers, formatters
	from akamai.edgegrid import EdgeGridAuth, EdgeRc
	from bs4 import BeautifulSoup
	from pyfiglet import Figlet
except:
	print bcolors.TURQUO+"[Auto Install]"+bcolors.WARNING+" Required libraries not found. Auto Install initiated... "+bcolors.ENDC
	failed = pipmain(['install','--user','-q','-r','requirements.txt'])
	if failed == True:
		print bcolors.TURQUO+"[Auto Install]"+bcolors.WARNING+" Auto Install failed. Please try to install manually. "+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.TURQUO+"[Auto Install]"+bcolors.WARNING+" Auto Install completed successfully. "+bcolors.ENDC
		print bcolors.TURQUO+"[Auto Install]"+bcolors.WARNING+" How far down the whiteRabbit hole are you willing to go? "+bcolors.ENDC
		sys.exit()

import xlsxwriter
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import texttable as tt
from requests import Request, Session
import requests
from bs4 import BeautifulSoup
from pygments import highlight, lexers, formatters
try:
	from akamai.edgegrid import EdgeGridAuth, EdgeRc
except:
	pass


PYTHON2 = sys.version_info.major < 3
locale.setlocale(locale.LC_ALL, '')
encoding = locale.getpreferredencoding()


VERSION = '3.1.5'
'''

Created by: Aurelio Somarriba Lucas
Name: SWaPI
CodeName: whiteRabbit
Version: RC3.1.5 - Aug 20, 2019

New in 3.x.x:
- Dockerize!!
docker pull ausomarr/swapi:v1
docker run -it --name swapi 303c8febd7c8
- Configuration Peer Review
- Auto Install Feature
- API Client File support
- Fast DNS
- PLX Analytics
- Application Security Clone Feature
- Patch command support on PAPI
- Alerts API
- Network Lists V2
- Contracts APIs
	* Audit report included
- Minor bugs fixed

- SWaPI Links:
Main Blog:
https://collaborate.akamai.com/confluence/pages/viewpage.action?pageId=115908115

GIT:
https://stash.akamai.com/projects/GSS/repos/swapi/browse


Installation:

SWaPI should auto-install all necessary libraries.

'''


########################################################################
# TUNABLES

DROPPING_CHARS = 50
MIN_SPEED = 1
MAX_SPEED = 7
RANDOM_CLEANUP = 100
WINDOW_CHANCE = 50
WINDOW_SIZE = 25
WINDOW_ANIMATION_SPEED = 3
FPS = 25
SLEEP_MILLIS = 1.0/FPS
USE_COLORS = False
SCREENSAVER_MODE = True
MATRIX_CODE_CHARS = "{}[]\|';/>?<.,SWaPI=whiteRbcodn!@#$%^&*+-~ɀɁɂŧϢϣϤϥϦϧϨϫϬϭϮϯϰϱϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰ߃߄༣༤༥༦༧༩༪༫༬༭༮༯༰༱༲༳༶"

########################################################################
# CODE

COLOR_CHAR_NORMAL = 1
COLOR_CHAR_HIGHLIGHT = 2
COLOR_WINDOW = 3

class FallingChar(object):
    matrixchr = list(MATRIX_CODE_CHARS)
    normal_attr = curses.A_NORMAL
    highlight_attr = curses.A_REVERSE

    def __init__(self, width, MIN_SPEED, MAX_SPEED):
        self.x = 0
        self.y = 0
        self.speed = 1
        self.char = ' '
        self.reset(width, MIN_SPEED, MAX_SPEED)

    def reset(self, width, MIN_SPEED, MAX_SPEED):
        self.char = random.choice(FallingChar.matrixchr).encode(encoding)
        self.x = randint(1, width - 1)
        self.y = 0
        self.speed = randint(MIN_SPEED, MAX_SPEED)
        # offset makes sure that chars with same speed don't move all in same frame
        self.offset = randint(0, self.speed)

    def tick(self, scr, steps):
        height, width = scr.getmaxyx()
        if self.advances(steps):
            # if window was resized and char is out of bounds, reset
            self.out_of_bounds_reset(width, height)
            # make previous char curses.A_NORMAL
            if USE_COLORS:
                scr.addstr(self.y, self.x, self.char, curses.color_pair(COLOR_CHAR_NORMAL))
            else:
                scr.addstr(self.y, self.x, self.char, curses.A_NORMAL)

            # choose new char and draw it A_REVERSE if not out of bounds
            self.char = random.choice(FallingChar.matrixchr).encode(encoding)
            self.y += 1
            if not self.out_of_bounds_reset(width, height):
                if USE_COLORS:
                    scr.addstr(self.y, self.x, self.char, curses.color_pair(COLOR_CHAR_HIGHLIGHT))
                else:
                    scr.addstr(self.y, self.x, self.char, curses.A_REVERSE)

    def out_of_bounds_reset(self, width, height):
        if self.x > width-2:
            self.reset(width, MIN_SPEED, MAX_SPEED)
            return True
        if self.y > height-2:
            self.reset(width, MIN_SPEED, MAX_SPEED)
            return True
        return False

    def advances(self, steps):
        if steps % (self.speed + self.offset) == 0:
            return True
        return False

    def step(self, steps, scr):

        return -1, -1, None

class WindowAnimation(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.step = 0

    def tick(self, scr, steps):
        if self.step > WINDOW_SIZE:
            #stop window animation after some steps
            self.draw_frame(scr, self.x - self.step, self.y - self.step,
                            self.x + self.step, self.y + self.step,
                            curses.A_NORMAL)
            return False

        # clear all characters covered by the window frame
        for i in range(WINDOW_ANIMATION_SPEED):
            anistep = self.step + i
            self.draw_frame(scr, self.x - anistep, self.y - anistep,
                            self.x + anistep, self.y + anistep,
                            curses.A_NORMAL, ' ')
        #cancel last animation
        self.draw_frame(scr, self.x - self.step, self.y - self.step,
                        self.x + self.step, self.y + self.step,
                        curses.A_NORMAL)
        #next step
        self.step += WINDOW_ANIMATION_SPEED

        #draw outer frame
        self.draw_frame(scr, self.x - self.step, self.y - self.step,
                        self.x + self.step, self.y + self.step,
                        curses.A_REVERSE)
        return True

    def draw_frame(self, scr, x1, y1, x2, y2, attrs, clear_char=None):
        if USE_COLORS:
            if attrs == curses.A_REVERSE:
                attrs = curses.color_pair(COLOR_WINDOW)
        h, w = scr.getmaxyx()
        for y in (y1, y2):
            for x in range(x1, x2+1):
                if x < 0 or x > w-1 or y < 0 or y > h-2:
                    continue
                if clear_char is None:
                    scr.chgat(y, x, 1, attrs)
                else:
                    scr.addstr(y, x, clear_char, attrs)
        for x in (x1, x2):
            for y in range(y1, y2+1):
                if x < 0 or x > w-1 or y < 0 or y > h-2:
                    continue
                if clear_char is None:
                    scr.chgat(y, x, 1, attrs)
                else:
                    scr.addstr(y, x, clear_char, attrs)

# we don't need a good PRNG, just something that looks a bit random.
def rand():
    # ~ 2 x as fast as random.randint
    a = 9328475634
    while True:
        a ^= (a << 21) & 0xffffffffffffffff;
        a ^= (a >> 35);
        a ^= (a << 4) & 0xffffffffffffffff;
        yield a
r = rand()
def randint(_min, _max):
    if PYTHON2:
        n = r.next()
    else:
        n = r.__next__()
    return (n % (_max - _min)) + _min
def codeRain():
    steps = 0
    scr = curses.initscr()
    scr.nodelay(1)
    curses.curs_set(0)
    curses.noecho()

    if USE_COLORS:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(COLOR_CHAR_NORMAL, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_CHAR_HIGHLIGHT, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(COLOR_WINDOW, curses.COLOR_GREEN, curses.COLOR_GREEN)

    height, width = scr.getmaxyx()
    window_animation = None
    lines = []
    for i in range(DROPPING_CHARS):
        l = FallingChar(width, MIN_SPEED, MAX_SPEED)
        l.y = randint(0, height-2)
        lines.append(l)

    scr.refresh()
    while True:
        height, width = scr.getmaxyx()
        for line in lines:
            line.tick(scr, steps)
        for i in range(RANDOM_CLEANUP):
            x = randint(0, width-1)
            y = randint(0, height-1)
            scr.addstr(y, x, ' ')
        #if randint(0, WINDOW_CHANCE) == 1:
        #    if window_animation is None:
                #start window animation
        #        line = random.choice(lines)
        #        window_animation = WindowAnimation(line.x, line.y)
        #if not window_animation is None:
        #   still_active = window_animation.tick(scr, steps)
        #   if not still_active:
        #       window_animation = None

        scr.refresh()
        time.sleep(SLEEP_MILLIS)
        if SCREENSAVER_MODE:
            key_pressed = scr.getch() != -1
            if key_pressed:
                raise KeyboardInterrupt()
        steps += 1


def errorHandling(respjson,errorJson):
	if respjson:
		print errorJson.content
		sys.exit()
	print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
	print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Code: "+bcolors.FAIL+str(errorJson['status'])+bcolors.ENDC
	print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Title: "+bcolors.FAIL+errorJson['title']+bcolors.ENDC
	print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Detail: "+bcolors.FAIL+errorJson['detail']+bcolors.ENDC
	try:
		print bcolors.TURQUO+"[ERROR]"+bcolors.ENDC+bcolors.WARNING+" Object Type: "+bcolors.FAIL+errorJson['objectType']+bcolors.ENDC
		print bcolors.TURQUO+"[ERROR]"+bcolors.ENDC+bcolors.WARNING+" Zone: "+bcolors.FAIL+errorJson['zone']+bcolors.ENDC
	except:
		pass
	#formatted_json = json.dumps(errorJson, indent=4, sort_keys=True)
	#colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
	#print colorful_json
	#pprint.pprint(result.json())
	print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	sys.exit()



def setUp():
	home = expanduser("~")
	filename = home+'/.edgercNew'
	#print filename
	try:
		open(filename, 'r')
	except IOError:
		createEdge = raw_input(bcolors.TURQUO+'[SETUP]'+bcolors.ENDC+' EdgeGrid Authentication file, .edgerc, has not been found. Do you want to create it with a default section? [y/N] ')
		if createEdge == 'y':
			credentials = raw_input(bcolors.TURQUO+'[SETUP]'+bcolors.ENDC+' Please enter credentials down below: \n')
			print "please copy and paste your charge discharge data.\n"
      			"To end recording Press Ctrl+d on Linux/Mac on Crtl+z on Windows"
			lines = ['default']
			try:
			    while True:
			        lines.append(raw_input())
			except EOFError:
			    pass
			lines = "\n".join(lines)
			outputfile = open(filename, 'w+')
			#entry = "[default]\n"+credentials+"\n"
			try:
				outputfile.writelines(lines)
				#print outputfile
				outputfile.close()
				print bcolors.TURQUO+"[SETUP]"+bcolors.ENDC+bcolors.WARNING+" Successfully created edgerc file. "+bcolors.ENDC
			except:
				print bcolors.TURQUO+"[SETUP]"+bcolors.ENDC+bcolors.WARNING+" There was a problem creating the edgerc file"+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
		'''
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.WARNING+'[IAM] SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.WARNING+'[IAM] Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	pass'''


def SIEMModule(automation,AccountSwitch,propertyName,creds,configId,offset,limit,start,end,respjson):
	def convert_to_epoch(date_time):
	    """

	    :param date_time:
	    :return:
	    """
	    pattern = '%m/%d/%Y %H:%M:%S'
	    utc_epoch = calendar.timegm(time.strptime(date_time, pattern))
	    return utc_epoch


	def epoch_to_datetime(epoch_time):
	    """

	    :param epoch_time:
	    :return:
	    """
	    pattern = '%Y-%m-%d %H:%M:%S'
	    return datetime.datetime.fromtimestamp(epoch_time).strftime(pattern)


	def get_local_time_gmt():
	    """

	    :return:
	    """
	    ts = calendar.timegm(time.gmtime())
	    return ts


	def decode_attack_data_payload(payload_string):
	    """

	    :param payload_string:
	    :return:
	    """
	    decode_payload_string = urllib.unquote(payload_string).decode('utf-8')
	    chunks = decode_payload_string.split(";")
	    decoded_chunks = []
	    for _i in chunks:
	        b64_decoded_chunk = base64.b64decode(_i)
	        decoded_chunks.append(b64_decoded_chunk.decode('utf-8'))
	    return ";".join(decoded_chunks)


	def decode_headers(payload_string):
	    """

	    :param payload_string:
	    :return:
	    """
	    decode_payload_string = urllib.unquote(payload_string).decode('utf-8')
	    headers = decode_payload_string.split("\n")
	    return headers


	def map_rules(payload):
	    """

	    :param payload:
	    :return:
	    """
	    list_rule_actions = payload['attackData']['ruleActions'].split(";")[:-1]
	    list_rule_data = payload['attackData']['ruleData'].split(";")[:-1]
	    list_rule_messages = payload['attackData']['ruleMessages'].split(";")[:-1]
	    list_rule_selectors = payload['attackData']['ruleSelectors'].split(";")
	    if len(list_rule_selectors) != 1:
	        list_rule_selectors = payload['attackData']['ruleSelectors'].split(";")[:-1]
	    list_rule_tags = payload['attackData']['ruleTags'].split(";")[:-1]
	    list_rule_versions = payload['attackData']['ruleVersions'].split(";")[:-1]
	    list_rules = payload['attackData']['rules'].split(";")[:-1]

	    dict_rules = []

	    for j in list_rules:
	        item_index = list_rules.index(j)
	        dict_rules.append(
	            {
	                "action": list_rule_actions[item_index],
	                "data": list_rule_data[item_index],
	                "message": list_rule_messages[item_index],
	                "selector": list_rule_selectors[item_index],
	                "tag": list_rule_tags[item_index],
	                "version": list_rule_versions[item_index],
	                "id": list_rules[item_index],
	            }
	        )
	    return dict_rules


	def dictionary_rules(payload):
	    """

	    :param payload:
	    :return:
	    """
	    list_rule_actions = payload['attackData']['ruleActions'].split(";")[:-1]
	    list_rule_data = payload['attackData']['ruleData'].split(";")[:-1]
	    list_rule_messages = payload['attackData']['ruleMessages'].split(";")[:-1]
	    list_rule_selectors = payload['attackData']['ruleSelectors'].split(";")
	    if len(list_rule_selectors) != 1:
	        list_rule_selectors = payload['attackData']['ruleSelectors'].split(";")[:-1]
	    list_rule_tags = payload['attackData']['ruleTags'].split(";")[:-1]
	    list_rule_versions = payload['attackData']['ruleVersions'].split(";")[:-1]
	    list_rules = payload['attackData']['rules'].split(";")[:-1]

	    dict_rules = {}

	    for j in list_rules:
	        item_index = list_rules.index(j)
	        dict_rules[list_rules[item_index]] = {
	                "action": list_rule_actions[item_index],
	                "data": list_rule_data[item_index],
	                "message": list_rule_messages[item_index],
	                "selector": list_rule_selectors[item_index],
	                "tag": list_rule_tags[item_index],
	                "version": list_rule_versions[item_index],
	                "id": list_rule_versions[item_index]
	            }

	    return dict_rules
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print '[IAM] Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.WARNING+'[IAM] SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.WARNING+'[IAM] Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if configId:
		query = {'offset':offset,'limit':limit,'from':start,'to':end}
		url = "/siem/v1/configs/"+configId
		result = s.get(urljoin(baseurl, url),params=query)
		if result.status_code == 200 or result.status_code == 201:
			if not respjson and not automation:
				#print result.content
				#sys.exit()
				print bcolors.TURQUO+"[SIEM]"+bcolors.ENDC+bcolors.WARNING+" SIEM Logs "+bcolors.ENDC
			#print result.content
			logs = result.text.split("\n")[:-2]
			#print logs
			offset_line = result.text.split("\n")[-2]
			if logs:
				for i in logs:
					ParentTable = tt.Texttable()
					ParentTable.set_cols_width([20,135])
					ParentTable.set_cols_align(['c','l'])
					ParentTable.set_cols_valign(['m','m'])
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					Parentheader = ['Field','Value']
					ParentTable.header(Parentheader)
					event = json.loads(i)
					Parentrow = [ 'Policy ID',event['attackData']['policyId'] ]
					ParentTable.add_row(Parentrow)
					Parentrow = [ 'Method',event['httpMessage']['method'] ]
					ParentTable.add_row(Parentrow)
					Parentrow = [ 'Host',event['httpMessage']['host'] ]
					ParentTable.add_row(Parentrow)
					Parentrow = [ 'Path',event['httpMessage']['path'] ]
					ParentTable.add_row(Parentrow)
					try:
						event['httpMessage']['query']
						Parentrow = [ 'Query',event['httpMessage']['query'] ]
						ParentTable.add_row(Parentrow)
					except:
						pass
					Parentrow = [ 'Request ID',event['httpMessage']['requestId'] ]
					ParentTable.add_row(Parentrow)
					Parentrow = [ 'Client IP',event['attackData']['clientIP'] ]
					ParentTable.add_row(Parentrow)
					Parentrow = [ 'GEO',event['geo'] ]
					ParentTable.add_row(Parentrow)
					event['attackData']['ruleActions'] = decode_attack_data_payload(event['attackData']['ruleActions'])
					Parentrow = [ 'Rule Actions',event['attackData']['ruleActions'] ]
					ParentTable.add_row(Parentrow)
					event['attackData']['ruleData'] = decode_attack_data_payload(event['attackData']['ruleData'])
					Parentrow = [ 'Rule Data',event['attackData']['ruleData'] ]
					ParentTable.add_row(Parentrow)
					event['attackData']['ruleMessages'] = decode_attack_data_payload(event['attackData']['ruleMessages'])
					Parentrow = [ 'Rule Messages',event['attackData']['ruleMessages'] ]
					ParentTable.add_row(Parentrow)
					event['attackData']['ruleSelectors'] = decode_attack_data_payload(event['attackData']['ruleSelectors'])
					Parentrow = [ 'Rule Selector',event['attackData']['ruleSelectors'] ]
					ParentTable.add_row(Parentrow)
					event['attackData']['ruleTags'] = decode_attack_data_payload(event['attackData']['ruleTags'])
					Parentrow = [ 'Rule Tags',event['attackData']['ruleTags'] ]
					ParentTable.add_row(Parentrow)
					event['attackData']['ruleVersions'] = decode_attack_data_payload(event['attackData']['ruleVersions'])
					Parentrow = [ 'Rule Versions',event['attackData']['ruleVersions'] ]
					ParentTable.add_row(Parentrow)
					event['attackData']['rules'] = decode_attack_data_payload(event['attackData']['rules'])
					Parentrow = [ 'Rules',event['attackData']['rules'] ]
					ParentTable.add_row(Parentrow)
					event['httpMessage']['requestHeaders'] = decode_headers(event['httpMessage']['requestHeaders'])
					Parentrow = [ 'Requests Headers',event['httpMessage']['requestHeaders'] ]
					ParentTable.add_row(Parentrow)
					event['httpMessage']['responseHeaders'] = decode_headers(event['httpMessage']['responseHeaders'])
					Parentrow = [ 'Response Headers',event['httpMessage']['responseHeaders'] ]
					ParentTable.add_row(Parentrow)
					event['timestamp'] = int(event['httpMessage']['start'])
					event['httpMessage']['start'] = epoch_to_datetime(int(event['httpMessage']['start']))
					Parentrow = [ 'Time',event['httpMessage']['start'] ]
					ParentTable.add_row(Parentrow)
					if not respjson and not automation:
						#print event
						MainParentTable = ParentTable.draw()
						print MainParentTable
						print bcolors.TURQUO+bcolors.BOLD+"\n\t\t\t\t\t\t\t   ------------------------Log Separator------------------------\n"+bcolors.ENDC
					else:
						print json.dumps(event)
		else:
			if respjson or automation:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[SIEM] "+bcolors.ENDC+bcolors.WARNING+result.content+bcolors.ENDC
		if respjson or automation:
			sys.exit()
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you fetch logs from your Akamai SIEM Collector\n"+bcolors.ENDC
		print bcolors.WARNING+"Security Information and Event Management\n"+bcolors.ENDC
		print "--creds 	- Use this option to specify your SIEM credentials section of your EdgeRC file"
		print "--configId 	- Unique identifier for each security configuration (semicolon separated)"
		print "--offset 	- Fetch only security events that have occurred from offset"
		print "--limit 	- Maximum number of security events each fetch returns"
		print "--start 	- The start of a specified time range, expressed in Unix epoch seconds"
		print "--end 		- The end of a specified time range, expressed in Unix epoch seconds"
		print bcolors.TURQUO+"\nMain Blog: https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/20/swapi-siem"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def IAMModule(sqa,automation,host,AccountSwitch,propertyName,creds,groupId,apiObject,respjson,propertyId,userId,sendEmail,passwd):
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print '[IAM] Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.WARNING+'[IAM] SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.WARNING+'[IAM] Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if AccountSwitch:
		filename = '.map'
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		for item in contents:
			if "[" and "]" in item:
				accountCheck = item[1:-2]
				if accountCheck == AccountSwitch:
					AccountSwitch = contents[contents.index(item)+1].strip()
					if not respjson:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
	#print AccountSwitch
	params = {'accountSwitchKey':AccountSwitch}
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if apiObject == 'groups':
		params.update({'actions':True})
		if groupId:
			url = "/identity-management/v2/user-admin/groups/"+groupId
		else:
			url = "/identity-management/v2/user-admin/groups/"
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			#print result.json()
			if groupId:
				print bcolors.WARNING+'[IAM] Parent Group '+bcolors.ENDC
				ParentTable = tt.Texttable()
				ParentTable.set_cols_width([35,10,25,30,25,30])
				ParentTable.set_cols_align(['c','c','c','c','c','c'])
				ParentTable.set_cols_valign(['m','m','m','m','m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Parentheader = ['Group Name','Group ID','Created By','Created Date','Modified By','Modified Date']
				ParentTable.header(Parentheader)
				Parentrow = [ result.json()['groupName'],result.json()['groupId'],result.json()['createdBy'],result.json()['createdDate'],result.json()['modifiedBy'],result.json()['modifiedDate'] ]
				ParentTable.add_row(Parentrow)
				MainParentTable = ParentTable.draw()
				print MainParentTable
				for subgroup in result.json()['subGroups']:
					SubGroupTable = tt.Texttable()
					SubGroupTable.set_cols_width([35,10,25,30,25,30])
					SubGroupTable.set_cols_align(['c','c','c','c','c','c'])
					SubGroupTable.set_cols_valign(['m','m','m','m','m','m'])
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					SubGroupheader = ['Group Name','Group ID','Created By','Created Date','Modified By','Modified Date']
					SubGroupTable.header(SubGroupheader)
					SubGrouprow = [ subgroup['groupName'],subgroup['groupId'],subgroup['createdBy'],subgroup['createdDate'],subgroup['modifiedBy'],subgroup['modifiedDate'] ]
					SubGroupTable.add_row(SubGrouprow)
				if len(result.json()['subGroups']) > 0:
					print bcolors.WARNING+'[IAM] Sub Groups '+bcolors.ENDC
					MainSubGroupTable = SubGroupTable.draw()
					print MainSubGroupTable
				if len(result.json()['subGroups']) > 1:
					print bcolors.TURQUO+'\n\n----------- Group Separator -----------\n\n'+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			for item in result.json():
				print bcolors.WARNING+'[IAM] Parent Group '+bcolors.ENDC
				ParentTable = tt.Texttable()
				ParentTable.set_cols_width([35,10,25,30,25,30])
				ParentTable.set_cols_align(['c','c','c','c','c','c'])
				ParentTable.set_cols_valign(['m','m','m','m','m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Parentheader = ['Group Name','Group ID','Created By','Created Date','Modified By','Modified Date']
				ParentTable.header(Parentheader)
				Parentrow = [ item['groupName'],item['groupId'],item['createdBy'],item['createdDate'],item['modifiedBy'],item['modifiedDate'] ]
				ParentTable.add_row(Parentrow)
				MainParentTable = ParentTable.draw()
				print MainParentTable
				if item['subGroups']:
					SubGroupTable = tt.Texttable()
					SubGroupTable.set_cols_width([35,10,25,30,25,30])
					SubGroupTable.set_cols_align(['c','c','c','c','c','c'])
					SubGroupTable.set_cols_valign(['m','m','m','m','m','m'])
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					SubGroupheader = ['Group Name','Group ID','Created By','Created Date','Modified By','Modified Date']
					SubGroupTable.header(SubGroupheader)
					for subgroup in item['subGroups']:
						SubGrouprow = [ subgroup['groupName'],subgroup['groupId'],subgroup['createdBy'],subgroup['createdDate'],subgroup['modifiedBy'],subgroup['modifiedDate'] ]
						SubGroupTable.add_row(SubGrouprow)
					print bcolors.WARNING+'[IAM] Sub Groups '+bcolors.ENDC
					MainSubGroupTable = SubGroupTable.draw()
					print MainSubGroupTable
				else:
					pass
				if len(result.json()) > 1:
					print bcolors.TURQUO+'\n\n----------- Group Separator -----------\n\n'+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'roles':
		url = "/identity-management/v2/user-admin/roles"
		params.update({'actions':True,'users':True})
		if groupId:
			params.update({'groupId':groupId})
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 201 or result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			RolesTable = tt.Texttable()
			RolesTable.set_cols_width([8,40,20,40,50])
			RolesTable.set_cols_align(['c','c','c','c','c'])
			RolesTable.set_cols_valign(['m','m','m','m','m'])
			Rolesheader = ['Role ID','Role Name','Created By','3rd Party Access','Role Description']
			RolesTable.header(Rolesheader)
			for item in result.json():
				userinfo = []
				try:
					item['users']
					for users in item['users']:
						userinfo.append(users['uiIdentityId']+": "+users['firstName']+" "+users['lastName'])
				except:
					pass
				Rolesrow = [ item['roleId'],item['roleName'],item['createdBy'],userinfo,item['roleDescription'] ]
				RolesTable.add_row(Rolesrow)
			MainRolesTable = RolesTable.draw()
			print MainRolesTable
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.WARNING+" There was a problem retrieving roles information. "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'apiclient':
		filename = '.apiclient'
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		if not userId:
			print bcolors.TURQUO+"[IAM]"+bcolors.WARNING+" You need to provide your API Client ID: "+bcolors.ENDC+"--userId ml5u5oman7w4d"
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			if sqa:
				for item in contents:
					if 'SQA:' in item:
						index = contents.index(item)
				entry = "SQA: "+userId+"\n"
			else:
				for item in contents:
					if 'PROD:' in item:
						index = contents.index(item)
				entry = "PROD: "+userId+"\n"
			try:
				index
				del contents[index]
			except:
				pass
			contents.append(entry)
			try:
				with open(filename, 'w') as f:
					for item in contents:
						f.write(item)
				#outputfile = open(filename, 'w')
				#outputfile.writelines(contents)
				print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" Successfully added your API Client ID to .apiclient file."+bcolors.ENDC
			except:
				print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem adding your API Client ID to the .apiclient file"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'search':
		filename = '.apiclient'
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		for item in contents:
			if sqa:
				if 'SQA:' in item:
					userId = item.split(':')[1].strip()
			else:
				if 'PROD:' in item:
					userId = item.split(':')[1].strip()
		if not host:
			print bcolors.TURQUO+"[IAM]"+bcolors.WARNING+" You need to provide a target to search: -t 'IBM Bluemix'"+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			url = "/identity-management/v1/open-identities/"+userId+"/account-switch-keys"
			params.update({'search':host})
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 404 or result.status_code == 403:
			if result.json()['title'].strip() == 'invalid open identity':
				print bcolors.TURQUO+'[IAM] '+bcolors.WARNING+'You need to enter your API Client ID: '+bcolors.ENDC+' python swapi.py iam apiclient --userId <ID>'
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if result.status_code == 201 or result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[IAM]"+bcolors.WARNING+" Account Search Result"+bcolors.ENDC
			AccountsTable = tt.Texttable()
			AccountsTable.set_cols_width([60,30])
			AccountsTable.set_cols_align(['c','c'])
			AccountsTable.set_cols_valign(['m','m'])
			#HostnameTable.set_deco(tt.Texttable.HEADER)
			Accountsheader = ['Account Name','Account Switch Key']
			AccountsTable.header(Accountsheader)
			for accountdata in result.json():
				Accountsrow = [ accountdata['accountName'],accountdata['accountSwitchKey'] ]
				AccountsTable.add_row(Accountsrow)
			AllAccountsTable = AccountsTable.draw()
			print AllAccountsTable
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem retrieving account information. "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'reset':
		if not userId:
			print bcolors.WARNING+'[IAM] You need to provide a uiIdentity ID: --userId 19807'+section+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not passwd:
			url = "/identity-management/v2/user-admin/ui-identities/"+userId+"/reset-password"
		else:
			url = "/identity-management/v2/user-admin/ui-identities/"+userId+"/restricted/set-password"
			body = {'newPassword':passwd}
			headers = {'Content-Type':'application/json'}
		params.update({'sendEmail':sendEmail})
		if not passwd:
			result = s.post(urljoin(baseurl, url),params=params)
		else:
			result = s.post(urljoin(baseurl, url),json=body,headers=headers,params=params)
		if result.status_code == 204 or result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+result.content+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem resetting password User's password. "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'unlock' or apiObject == 'lock':
		if not userId:
			print bcolors.WARNING+'[IAM] You need to provide a uiIdentity ID: --userId 19807'+section+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if apiObject == 'unlock':
			url = "/identity-management/v2/user-admin/ui-identities/"+userId+"/unlock"
		else:
			url = "/identity-management/v2/user-admin/ui-identities/"+userId+"/lock"
		result = s.post(urljoin(baseurl, url),params=params)
		if result.status_code == 204:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			if apiObject == 'unlock':
				print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" User Unlocked successfully."+bcolors.ENDC
			else:
				print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" User Locked successfully."+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem with your request. "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'users':
		params.update({'actions':True})
		params.update({'authGrants':True})
		if groupId:
			query.update({'groupId':groupId})
		if userId:
			url = "/identity-management/v2/user-admin/ui-identities/"+userId
		else:
			url = "/identity-management/v2/user-admin/ui-identities"
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200 or result.status_code == 201:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			#print result.json()
			if userId:
				print bcolors.TURQUO+'[IAM] '+bcolors.WARNING+'User: '+userId+bcolors.ENDC
			#else:
			#	print bcolors.TURQUO+'[IAM] '+bcolors.WARNING+'Users '+bcolors.ENDC
			ParentTable = tt.Texttable()
			ParentTable.set_cols_width([25,15,20,30,20,10,15,12])
			ParentTable.set_cols_align(['c','c','c','c','c','c','c','c'])
			ParentTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
			#HostnameTable.set_deco(tt.Texttable.HEADER)
			if userId:
				ParentTable.set_cols_width([23,15,20,30,12,10,28,12])
				Parentheader = ['Username','First Name','Last Name','Email','Contact Type','Role Id','Last Login Date','Preferred Language']
				ParentTable.header(Parentheader)
				ActionsTable = tt.Texttable()
				ActionsTable.set_cols_width([25,15,20,30,20,10])
				ActionsTable.set_cols_align(['c','c','c','c','c','c'])
				ActionsTable.set_cols_valign(['m','m','m','m','m','m'])
				Actionsheader = ['Edit','API Client','Reset Password','3rd Party Access','is Cloneable','Delete']
				ActionsTable.header(Actionsheader)
				GrantsTable = tt.Texttable()
				GrantsTable.set_cols_width([10,20,72,60])
				GrantsTable.set_cols_align(['c','c','c','c'])
				GrantsTable.set_cols_valign(['m','m','m','m'])
				Grantsheader = ['Role ID','Role Name','subGroups','roleDescription']
				GrantsTable.header(Grantsheader)
				subGroups = []
				for item in result.json()['authGrants'][0]['subGroups']:
					subGroups.append(item['groupName'])
				Parentrow = [ result.json()['uiUserName'],result.json()['firstName'],result.json()['lastName'],result.json()['email'],result.json()['contactType'],result.json()['authGrants'][0]['roleId'],result.json()['lastLoginDate'],result.json()['preferredLanguage'] ]
				Actionsrow = [ str(result.json()['actions']['edit']),str(result.json()['actions']['apiClient']),str(result.json()['actions']['resetPassword']),str(result.json()['actions']['thirdPartyAccess']),str(result.json()['actions']['isCloneable']),str(result.json()['actions']['delete']) ]
				Grantsrow = [ result.json()['authGrants'][0]['roleId'],result.json()['authGrants'][0]['roleName'],subGroups,result.json()['authGrants'][0]['roleDescription'] ]
				ParentTable.add_row(Parentrow)
				ActionsTable.add_row(Actionsrow)
				GrantsTable.add_row(Grantsrow)
			else:
				Parentheader = ['Username','First Name','Last Name','Email','Role','Role Id','uiIdentity ID','API Client']
				ParentTable.header(Parentheader)
				for item in result.json():
					try:
						item['phone']
						phone = item['phone']
					except:
						phone = None
					try:
						item['country']
						country = item['country']
					except:
						country = None
					try:
						item['jobTitle']
						jobTitle = item['jobTitle']
					except:
						jobTitle = None
					try:
						item['mobilePhone']
						mobilePhone = item['mobilePhone']
					except:
						mobilePhone = None
					try:
						item['authGrants'][0]['roleName']
						roleName = item['authGrants'][0]['roleName']
					except:
						roleName = None
					try:
						item['authGrants'][0]['roleId']
						roleId = item['authGrants'][0]['roleId']
					except:
						roleId = None
					Parentrow = [ item['uiUserName'],item['firstName'],item['lastName'],item['email'],roleName,roleId,item['uiIdentityId'],str(item['actions']['apiClient']) ]
					ParentTable.add_row(Parentrow)
			MainParentTable = ParentTable.draw()
			print bcolors.TURQUO+'[IAM] '+bcolors.WARNING+'Parent Table '+bcolors.ENDC
			print MainParentTable
			if userId:
				MainGrantsTable = GrantsTable.draw()
				print bcolors.TURQUO+'[IAM] '+bcolors.WARNING+'Grants Table '+bcolors.ENDC
				print MainGrantsTable
				MainActionTable = ActionsTable.draw()
				print bcolors.TURQUO+'[IAM] '+bcolors.WARNING+'Actions Table '+bcolors.ENDC
				print MainActionTable
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem retrieving Users Information. "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'create' or apiObject == 'rename':
		headers = {'Content-Type':'application/json'}
		if not propertyName:
			if apiObject == 'rename':
				print bcolors.WARNING+'[IAM] You need to provide a new Group Name: -N "New Group Name"'+section+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			else:
				print bcolors.WARNING+"You need to specify the new Group Name: -N 'New Sub Group'\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not groupId:
			if apiObject == 'rename':
				print bcolors.WARNING+'[IAM] You need to provide groupId to rename: --group 19807'+section+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			else:
				print bcolors.WARNING+'[IAM] You need to provide a Top Level Group in which to create new group: --group 19807'+section+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		url = "/identity-management/v2/user-admin/groups/"+groupId
		body = {'groupName':propertyName}
		if apiObject == 'rename':
			result = s.put(urljoin(baseurl, url),headers=headers,json=body,params=params)
		else:
			result = s.post(urljoin(baseurl, url),headers=headers,json=body,params=params)
		if result.status_code == 201 or result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			#print result.json()
			print bcolors.WARNING+'[IAM] New Group '+bcolors.ENDC
			ParentTable = tt.Texttable()
			ParentTable.set_cols_width([35,10,25,30,25,30])
			ParentTable.set_cols_align(['c','c','c','c','c','c'])
			ParentTable.set_cols_valign(['m','m','m','m','m','m'])
			#HostnameTable.set_deco(tt.Texttable.HEADER)
			Parentheader = ['Group Name','Group ID','Created By','Created Date','Modified By','Modified Date']
			ParentTable.header(Parentheader)
			Parentrow = [ result.json()['groupName'],result.json()['groupId'],result.json()['createdBy'],result.json()['createdDate'],result.json()['modifiedBy'],result.json()['modifiedDate'] ]
			ParentTable.add_row(Parentrow)
			MainParentTable = ParentTable.draw()
			print MainParentTable
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem creating a new Group: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'delete':
		if not groupId:
			print bcolors.WARNING+'[IAM] You need to provide a Sub Group to delete: --group 19807'+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		url = "/identity-management/v2/user-admin/groups/"+groupId
		result = s.delete(urljoin(baseurl, url),params=params)
		if result.status_code == 204:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" Group deleted successfully."+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem deleting group. "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'properties':
		if groupId:
			params.update({'groupId':groupId})
		if propertyId:
			url = "/identity-management/v2/user-admin/properties/"+propertyId
		else:
			url = "/identity-management/v2/user-admin/properties"
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			#print result.json()
			if propertyId:
				print bcolors.WARNING+'[IAM] Property Information:'+bcolors.ENDC
				PropertiesTable = tt.Texttable()
				PropertiesTable.set_cols_width([12,35,35,20,20,25])
				PropertiesTable.set_cols_align(['c','c','c','c','c','c'])
				PropertiesTable.set_cols_valign(['m','m','m','m','m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Propertiesheader = ['Property ID','Property Name','ARL Config File','Created By','Modified By','Modified Date']
				PropertiesTable.header(Propertiesheader)
				Propertiesrow = [ result.json()['propertyId'],result.json()['propertyName'],result.json()['arlConfigFile'],result.json()['createdBy'],result.json()['modifiedBy'],result.json()['modifiedDate'] ]
				PropertiesTable.add_row(Propertiesrow)
				MainPropertiesTable = PropertiesTable.draw()
				print MainPropertiesTable
			else:
				if groupId:
					print bcolors.WARNING+'[IAM] Properties in Group'+bcolors.ENDC
				else:
					print bcolors.WARNING+'[IAM] ALL Properties'+bcolors.ENDC
				PropertiesTable = tt.Texttable()
				PropertiesTable.set_cols_width([30,15,15,60,35])
				PropertiesTable.set_cols_align(['c','c','c','c','c'])
				PropertiesTable.set_cols_valign(['m','m','m','m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Propertiesheader = ['Group Name','Group ID','Property ID','Property Name','Property Description']
				PropertiesTable.header(Propertiesheader)
				for item in result.json():
					Propertiesrow = [ item['groupName'],item['groupId'],item['propertyId'],item['propertyName'],item['propertyTypeDescription'] ]
					PropertiesTable.add_row(Propertiesrow)
				MainPropertiesTable = PropertiesTable.draw()
				print MainPropertiesTable
		else:
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[IAM]"+bcolors.ENDC+bcolors.WARNING+" There was a problem getting information about this Property. "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you search for Account Switch Keys and other User Account Roles\n"+bcolors.ENDC
		print bcolors.WARNING+"IAM List Group Information\n"+bcolors.ENDC
		print "apiclient 	- Set API Client ID to be able to search for different Account Keys."
		print "search 		- Search accounts and Account Switch Keys by providing a string with the '-t' option."
		print "groups 		- List all Groups"
		print "properties 	- List all Versions for a specific Security Configuration"
		print "users 		- List all users"
		print "roles 		- List roles for current account and contract"
		print bcolors.WARNING+"\nIAM Actions\n"+bcolors.ENDC
		print "create 		- Create a new Sub Group un Parent"
		print "delete 		- Delete a Sub Group (only works if no user is configured)"
		print "rename 		- Renames a Sub Group"
		print "reset 		- Resets User's password"
		print "unlock 		- Unlock User's account"
		print "lock 		- Lock User's account"
		print bcolors.WARNING+"\nIAM Options\n"+bcolors.ENDC
		print "--t 		- This option is used to search accounts using a specific string"
		print "--userId 	- Used by multiple calls, however, use this option to add your API Client ID to SWaPI"
		print "--groupId 	- Used to provide a Group ID"
		print bcolors.TURQUO+"\nMain Blog: https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/20/swapi-identity-access-management-iam-main"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def queryWhois(query, server='whois.ripe.net'):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while 1:
		try:
			s.connect((server, 43))
		except socket.error, (ecode, reason):
			if ecode==errno.EINPROGRESS:
				continue
			elif ecode==errno.EALREADY:
				continue
			else:
				raise socket.error, (ecode, reason)
			pass
		break

	ret = select.select ([s], [s], [], 30)

	if len(ret[1])== 0 and len(ret[0]) == 0:
		s.close()
		raise TimedOut, "on data"

	s.setblocking(1)

	s.send("%s\n" % query)
	page = ""
	while 1:
		data = s.recv(8196)
		if not data: break
		page = page + data
		pass


def Diagnostic(automation,AccountSwitch,host,apiModule,edge,refId,cpcode,creds,respjson):
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if apiModule == 'checkip':
		if not edge:
			print bcolors.WARNING+"You need to specify an Edge IP address with the -E flag: -E 23.200.255.173\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		url = "/diagnostic-tools/v2/ip-addresses/"+edge+"/is-cdn-ip"
		result = s.get(urljoin(baseurl, url))
		json_data = result.json()
		formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiModule == 'crawl':
		if edge:
			url = "/diagnostic-tools/v2/ip-addresses/"+edge+"/log-lines"
			#print url
			#print host
			#print datetime.datetime.now().replace(microsecond=0).isoformat()
			#print datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
			#print datetime.datetime.now().isoformat()
			#print datetime.datetime.utcnow().replace(microsecond=0).isoformat()
			d = datetime.datetime.utcnow().replace(microsecond=0) - timedelta(hours=2)
			#print d
			#utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
			#utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
			#print datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()
			params = {'endTime':d.isoformat()+"Z","duration":360}
			if cpcode:
				params.update({"cpCode":cpcode})
			if host:
				params.update({"hostHeader":host})
			if refId:
				params.update({"requestId":refId})
			#print params
			result = s.get(urljoin(baseurl, url),params=params)
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			sys.exit()
		#print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
		#print result.content
		if not refId:
			print bcolors.WARNING+"You need to specify a Reference Number: --refId 9.6f64d440.1318965461.2f2b078\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if '&#' in refId:
			htmlEncode = HTMLParser()
			refId = htmlEncode.unescape(refId)
		if 'Reference' in refId:
			refId = refId.replace('Reference #','')
		if not respjson:
			print bcolors.TURQUO+"[Reference Number] "+bcolors.WARNING+refId+bcolors.ENDC
		result = s.get(urljoin(baseurl, '/diagnostic-tools/v2/errors/'+refId+'/translated-error'))
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
			else:
				#print result.json()['configurations']
				print bcolors.TURQUO+"\n[Overall Request] "+bcolors.ENDC
				HeaderTable = tt.Texttable()
				Headerheader = ['Reason','Origin Hostname','Client IP', 'Time','Response Code']
				HeaderTable.header(Headerheader)
				HeaderTable.set_cols_width([35,40,20,28,18])
				HeaderTable.set_cols_align(['c','c','c','c','c'])
				HeaderTable.set_cols_valign(['m','m','m','m','m'])
				try:
					result.json()['translatedError']['wafDetails']
					if result.json()['translatedError']['wafDetails'] == '-':
						wafDetails = None
					else:
						wafDetails = result.json()['translatedError']['wafDetails']
				except:
					wafDetails = None
				Headerrow = [result.json()['translatedError']['reasonForFailure'],result.json()['translatedError']['originHostname'],result.json()['translatedError']['connectingIp'],result.json()['translatedError']['timestamp'],result.json()['translatedError']['httpResponseCode']]
				HeaderTable.add_row(Headerrow)
				HeadTable = HeaderTable.draw()
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['translatedError']['logs']:
					#print item
					Hostnameheader = ['Line', 'Ghost IP','Method','Status Code','User Agent','More Info']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([5,20,8,15,40,50])
					HostnameTable.set_cols_align(['c','c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m','m'])
					try:
						item['fields']['Client Request']
						clientRequest = item['fields']['Client Request']
					except:
						try:
							item['fields']['Forward Request']
							clientRequest = item['fields']['Forward Request']
						except:
							clientRequest = None
					try:
						item['fields']['HTTP method']
						method = item['fields']['HTTP method']
					except:
						method = None
					try:
						item['fields']['user-agent']
						UA = item['fields']['user-agent']
					except:
						UA = None
					try:
						item['fields']['error']
						error = item['fields']['error']
					except:
						error = ''
					Hostnamerow = [clientRequest,item['fields']['Edge server IP'],method,item['fields']['HTTP status code'],UA,item['description']+'\n'+error]
					HostnameTable.add_row(Hostnamerow)
				HostTable = HostnameTable.draw()
				print HeadTable
				print bcolors.TURQUO+"[Log Lines] "+bcolors.ENDC
				print HostTable
				if wafDetails:
					print bcolors.TURQUO+"WAF: "+bcolors.ENDC
					#print wafDetails
					WAFArray = wafDetails.split('|')
					#print WAFArray
					WAFTable = tt.Texttable()
					WAFheader = ['Policy', 'Rules','Risk Group']
					WAFTable.header(WAFheader)
					WAFTable.set_cols_width([15,92,40])
					WAFTable.set_cols_align(['c','c','c'])
					WAFTable.set_cols_valign(['m','m','m'])
					WAFrow = [WAFArray[0],WAFArray[1],WAFArray[2]]
					WAFTable.add_row(WAFrow)
					BlockTable = WAFTable.draw()
					print BlockTable
				print bcolors.TURQUO+"URL: "+bcolors.ENDC
				URLTable = tt.Texttable()
				#URLheader = ['URL']
				#URLTable.header(URLheader)
				URLTable.set_cols_width([153])
				URLTable.set_cols_align(['c'])
				URLTable.set_cols_valign(['m'])
				URLrow = [result.json()['translatedError']['url']]
				URLTable.add_row(URLrow)
				URITable = URLTable.draw()
				print URITable
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def ContractsAPI(sqa,AccountSwitch,propertyName,creds,respjson,apiObject,contractId,depth,fromField,toField):
	if not respjson:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	if apiObject != 'products':
		if AccountSwitch:
			filename = '.map'
			readfile = open(filename, 'r')
			contents = readfile.readlines()
			for item in contents:
				if "[" and "]" in item:
					accountCheck = item[1:-2]
					if accountCheck == AccountSwitch:
						AccountSwitch = contents[contents.index(item)+1].strip()
						if not respjson:
							print bcolors.TURQUO+"[Contract]"+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
		#print AccountSwitch
		params = {'accountSwitchKey':AccountSwitch}
	elif apiObject == 'products' and contractId:
		if AccountSwitch:
			filename = '.map'
			readfile = open(filename, 'r')
			contents = readfile.readlines()
			for item in contents:
				if "[" and "]" in item:
					accountCheck = item[1:-2]
					if accountCheck == AccountSwitch:
						AccountSwitch = contents[contents.index(item)+1].strip()
						if not respjson:
							print bcolors.TURQUO+"[Contract]"+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
		#print AccountSwitch
		params = {'accountSwitchKey':AccountSwitch}
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if apiObject == 'list':
		payloadAppend = {"depth":depth}
		params.update(payloadAppend)
		url = '/contract-api/v1/contracts/identifiers'
		#print payload
		result = s.get(urljoin(baseurl, url), params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				contractTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				contractheader = ['Contracts']
				contractTable.header(contractheader)
				contractTable.set_cols_width([45])
				contractTable.set_cols_align(['c'])
				contractTable.set_cols_valign(['m'])
				for contract in result.json():
					contractRow = [contract]
					contractTable.add_row(contractRow)
				KtTable = contractTable.draw()
				print KtTable
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		else:
			print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
			#print result.content
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	elif apiObject == 'groups':
		url = '/contract-api/v1/reportingGroups/'
		#print payload
		result = s.get(urljoin(baseurl, url), params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				repGroupTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				repGroupheader = ['ID','Name']
				repGroupTable.header(repGroupheader)
				repGroupTable.set_cols_width([20,80])
				repGroupTable.set_cols_align(['c','c'])
				repGroupTable.set_cols_valign(['m','m'])
				for contract in result.json():
					repGroupRow = [contract['id'],contract['name']]
					repGroupTable.add_row(repGroupRow)
				reportingTable = repGroupTable.draw()
				print reportingTable
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		else:
			print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
			#print result.content
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	elif apiObject == 'groups':
		url = '/contract-api/v1/reportingGroups/'
		#print payload
		result = s.get(urljoin(baseurl, url), params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				repGroupTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				repGroupheader = ['ID','Name']
				repGroupTable.header(repGroupheader)
				repGroupTable.set_cols_width([20,80])
				repGroupTable.set_cols_align(['c','c'])
				repGroupTable.set_cols_valign(['m','m'])
				for contract in result.json():
					repGroupRow = [contract['id'],contract['name']]
					repGroupTable.add_row(repGroupRow)
				reportingTable = repGroupTable.draw()
				print reportingTable
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		else:
			print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
			#print result.content
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	elif apiObject == 'products':
		if fromField:
			payloadAppend = {"from":fromField}
			params.update(payloadAppend)
		if toField:
			payloadAppend = {"to":toField}
			params.update(payloadAppend)
		if contractId:
			url = '/contract-api/v1/contracts/'+contractId+'/products/summaries'
			#print payload
			result = s.get(urljoin(baseurl, url), params=params)
			if result.status_code == 200:
				if respjson:
					json_data = result.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					#print colorful_json
					print result.content
					sys.exit()
				else:
					productsTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					contractheader = ['Contract','Product Name','Product Id']
					productsTable.header(contractheader)
					productsTable.set_cols_width([45,85,45])
					productsTable.set_cols_align(['c','c','c'])
					productsTable.set_cols_valign(['m','m','m'])
					for product in result.json()['products']['marketing-products']:
						productRow = [result.json()['products']['contractId'],product['marketingProductName'],product['marketingProductId']]
						productsTable.add_row(productRow)
					PrdTable = productsTable.draw()
					print PrdTable
			else:
				print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
				#print result.content
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		else:
			if ',' in AccountSwitch:
				AccountSwitch = AccountSwitch.split(',')
			else:
				AccountSwitch = AccountSwitch.split('\n')
			#print AccountSwitch
			prdFile = 'files/'+AccountSwitch[0]+'-products'+'.xlsx'
			workbook = xlsxwriter.Workbook(prdFile)
			prdSheet = workbook.add_worksheet('Products')
			prdHeader = ['Account ID','Account Name','Contract ID', 'Product Name', 'Product ID']
			row = 0
			# Add a bold format to use to highlight cells.
			table_format = workbook.add_format()
			table_format.set_center_across()
			table_format.set_align('center')
			table_format.set_align('vcenter')
			table_format.set_font_size(12)
			table_format.set_border()
			header_format = workbook.add_format()
			header_format.set_bold()
			header_format.set_center_across()
			header_format.set_align('center')
			header_format.set_align('vcenter')
			header_format.set_font_size(12)
			header_format.set_border()
			for i in range(0,len(prdHeader)):
				prdSheet.set_column(i, 50)
				prdSheet.write(row,i, prdHeader[i],header_format)
			row = 1
			for account in AccountSwitch:
				#print account
				filename = '.map'
				readfile = open(filename, 'r')
				contents = readfile.readlines()
				for item in contents:
					if "[" and "]" in item:
						accountCheck = item[1:-2]
						if accountCheck == account:
							AccountSwitchKey = contents[contents.index(item)+1].strip()
							#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name "+account+" found and mapped to Account "+contents[contents.index(item)+1].strip()+bcolors.ENDC
				#print AccountSwitch
				try:
					AccountSwitchKey
					key = AccountSwitchKey
					AccountSwitchKey = None
				except:
					 key = account
				mapFile = '.apiclient'
				readMap = open(mapFile, 'r')
				mapContents = readMap.readlines()
				for item in mapContents:
					if sqa:
						if 'SQA:' in item:
							userId = item.split(':')[1].strip()
					else:
						if 'PROD:' in item:
							userId = item.split(':')[1].strip()
				searchUrl = "/identity-management/v1/open-identities/"+userId+"/account-switch-keys"
				if ':' in key:
					searchKey = key.split(':')[0]
				else:
					searchKey = key
				accountSearch = {'search':searchKey}
				accountSearchresult = s.get(urljoin(baseurl, searchUrl),params=accountSearch)
				if accountSearchresult.status_code == 201 or accountSearchresult.status_code == 200:
					#print key
					accountName = accountSearchresult.json()[0]['accountName']
				else:
					accountName = 'Not Found'
				params = {'accountSwitchKey':key}
				payloadAppend = {"depth":depth}
				params.update(payloadAppend)
				url = '/contract-api/v1/contracts/identifiers'
				#print payload
				result = s.get(urljoin(baseurl, url), params=params)
				if result.status_code == 200:
					productsTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					contractheader = ['Account ID','Account Name','Contract','Product Name','Product Id']
					productsTable.header(contractheader)
					productsTable.set_cols_width([20,35,20,85,20])
					productsTable.set_cols_align(['c','c','c','c','c'])
					productsTable.set_cols_valign(['m','m','m','m','m'])
					for contract in result.json():
						urlPRD = '/contract-api/v1/contracts/'+contract+'/products/summaries'
						prdResult = s.get(urljoin(baseurl, urlPRD), params=params)
						if prdResult.status_code == 200:
							if respjson:
								json_data = prdResult.json()
								formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
								colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
								#print colorful_json
								print prdResult.content
								for product in prdResult.json()['products']['marketing-products']:
									array = [key,accountName,prdResult.json()['products']['contractId'],product['marketingProductName'],product['marketingProductId']]
									for i in range(0,len(array)):
										prdSheet.set_column(i, 50)
										prdSheet.write(row,i, array[i],table_format)
									row += 1
							else:
								for product in prdResult.json()['products']['marketing-products']:
									productRow = [key,accountName,prdResult.json()['products']['contractId'],product['marketingProductName'],product['marketingProductId']]
									productsTable.add_row(productRow)
									array = [key,accountName,prdResult.json()['products']['contractId'],product['marketingProductName'],product['marketingProductId']]
									for i in range(0,len(array)):
										prdSheet.set_column(i, 50)
										prdSheet.write(row,i, array[i],table_format)
									row += 1
						else:
							print bcolors.WARNING+"StatusCode: "+str(prdResult.status_code)+bcolors.ENDC
							#print result.content
							json_data = prdResult.json()
							formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
							colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
							print colorful_json
					if not respjson:
						PrdTable = productsTable.draw()
						print PrdTable
						if len(AccountSwitch) > 1:
							print bcolors.TURQUO+'\n\t\t\t\t\t\t\t\t------------------------------ Separator ------------------------------\n'+bcolors.ENDC
				else:
					print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
					#print result.content
					json_data = result.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					print colorful_json
					print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			workbook.close()
			if not respjson:
				print bcolors.TURQUO+'\n------------------------------------------------------------------------------------------------------------------------'
				print bcolors.TURQUO+'[Contract]'+bcolors.WARNING+' Excel report generated. File location: '+bcolors.WHITE+prdFile+bcolors.ENDC
				print bcolors.TURQUO+'------------------------------------------------------------------------------------------------------------------------'
				print bcolors.TURQUO+"\n[Contract] "+bcolors.WARNING+"Status: "+bcolors.WHITE+"Successful"+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()

	else:
		print bcolors.WHITE+"This module allows you to view Contract and More!\n"+bcolors.ENDC
		print bcolors.WARNING+"Contracts Retrieve Information:\n"+bcolors.ENDC
		print "list 		- List Contracts"
		print "products 	- List products per contract or all contracts"
		print "groups 		- List CP code reporting groups"
		print bcolors.WARNING+"\nContract Automations:\n"+bcolors.ENDC
		print "audit 		- Audits contracts and Products"
		print bcolors.WARNING+"\nSWaPI Options:\n"+bcolors.ENDC
		print "-A 		- Provide an Account Switch Key or friendly name"
		print "--depth 	- Returns a specific set of contracts. Select 'TOP' to return only parent contracts or 'ALL' to return both parent and child contracts."
		print "--contractId 	- Unique contract identifier when displaying products. "
		print "--from 		- The start date, in UTC, to use when looking for products associated with a contract. The default start date is 30 days prior to the current date."
		print "--to 		- The end date, in UTC, to use when looking for products associated with a contract. The default end date is the current date."
		print "--json 		- Return JSON response. Boolean."
	print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	sys.exit()


def auditModule(automation,AccountSwitch,propertyName,creds):
	print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	CNAMEHolder = []
	StagingStatus = []
	ProductionStatus = []
	PMConfigurations = []
	PMConfigurationBool = []
	if not propertyName:
		print bcolors.WARNING+"You need to specify a filename using the following option: -N onboardingHostnames.txt\n\n"+bcolors.ENDC
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	# Parse hostname file
	filename = propertyName
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.WARNING+"Couldn't find that file. Ar you sure this file exists?"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	filelines = open(filename, 'r').readlines()
	readfile = []
	initialreadfile = []
	#	readfile = open(filename, 'r').readlines()
	for i in range (0,len(filelines)):
		if filelines[i].rstrip():
			initialreadfile.insert(i,filelines[i].strip())
	#print initialreadfile
	AuditTable = tt.Texttable()
	Auditheader = ['Hostname','CNAMEd','PM Configuration','Production','WAF Config','WAF PROD Version']
	AuditTable.header(Auditheader)
	AuditTable.set_cols_width([40,10,40,15,30,10])
	AuditTable.set_cols_align(['c','c','c','c','c','c'])
	AuditTable.set_cols_valign(['m','m','m','m','m','m'])
	for hostname in initialreadfile:
		dynhost = hostname
		dynhost2 = hostname
		GTM = False
		AkamaiFastDNS = False
		EDGECNAME = False
		StagingHost = False
		PRODHost = False
		EdgeHostname = None
		PMBool = False
		initconfigName = None
		WAFHOST = False
		WAFProd = None
		WAFName = None
		PRODVersion = None
		for i in range(0,4):
			try:
				GTMFinder = dns.resolver.query(dynhost2, 'CNAME')
				for g in GTMFinder.response.answer:
					for n in g.items:
						if ('akadns.net') in n.to_text():
							#EdgeHostname = j.to_text()
							GTM = True
							EDGECNAME = True
							break
						else:
							dynhost2 = n.to_text()
			except:
				pass
		if EDGECNAME == False:
			try:
				answers = dns.resolver.query(dynhost, 'A')
				for i in answers.response.answer:
					for j in i.items:
			#			print j.to_text()
						for server in ['whois.arin.net', 'whois.ripe.net', 'whois.apnic.net', 'whois.lacnic.net', 'whois.afrinic.net']:
							try:
								ipwhois = queryWhois(j.to_text(), server)
				#				print ipwhois
								whoissplit = ipwhois.split('\n')
				#				print whoissplit
								for descriptor in whoissplit:
									#print descriptor
									if 'NetName' in descriptor:
										NetNameSplit = descriptor.split('        ')
								#print NetNameSplit
								if 'AKAMAI' or 'NTTA-165-254' in NetNameSplit[1]:
			#							print NetNameSplit[1]
										AkamaiFastDNS = True
										EDGECNAME = True
										EdgeHostname = "FastDNS"
								break # we only need the info once
							except:
								pass
			except:
			#	print ARecord
				pass
		if EDGECNAME == False:
			for i in range(0,4):
				try:
					answers = dns.resolver.query(dynhost, 'CNAME')
					for i in answers.response.answer:
						for j in i.items:
							if ('edgekey') in j.to_text():
								EdgeHostname = j.to_text()
								Protocol = 'edgekey'
								EDGECNAME = True
								break
							elif ('edgesuite') in j.to_text():
								EdgeHostname = j.to_text()
								Protocol = 'edgesuite'
								EDGECNAME = True
								break
							elif ('akamai.net') in j.to_text():
								EdgeHostname = j.to_text()
								Protocol = 'akamai.net'
								EDGECNAME = True
								break
							elif ('akamaiedge.net') in j.to_text():
								EdgeHostname = j.to_text()
								Protocol = 'akamaiedge.net'
								EDGECNAME = True
								break
							else:
								dynhost = j.to_text()
				except:
					pass
		#print bcolors.TURQUO+hostname+bcolors.ENDC
		#if AkamaiFastDNS == False:
		#	if EDGECNAME == True:
		#		print bcolors.WHITE+"CNAMEd"+bcolors.ENDC
		#	else:
		#		print bcolors.WARNING+"NOT CNAMEd"+bcolors.ENDC
		#else:
		#	print bcolors.WHITE+"FastDNS Customer"+bcolors.ENDC
		headers = {'Content-Type':'application/json',"PAPI-Use-Prefixes":"false"}
		body = {"hostname":hostname}
		result = s.post(urljoin(baseurl, '/papi/v1/search/find-by-value'),headers=headers,json=body)
		#print "StatusCode: "+str(result.status_code)
		#print result.content
		if result.status_code == 200:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			#print colorful_json
			for item in result.json()["versions"]["items"]:
				try:
					item["propertyName"]
					PMBool = True
					initconfigName = item["propertyName"]
					PMConfigurations.append(item["propertyName"])
					if item["stagingStatus"] == "ACTIVE":
						StagingHost = True
					if item["productionStatus"] == "ACTIVE":
						PRODHost = True
						PRODVersion = str(item["propertyVersion"])
				except:
					PMConfigurations.append(None)
				#if PMBool == True:
				#	print bcolors.WHITE+"PM Configuration Found: "+item["propertyName"]+bcolors.ENDC
				PMConfigurationBool.append(PMBool)
				StagingStatus.append(StagingHost)
				ProductionStatus.append(PRODHost)
				secresult = s.get(urljoin(baseurl, '/appsec/v1/configs'))
				if secresult.status_code == 200:
					for item in secresult.json()['configurations']:
						#print item
						try:
							item["productionHostnames"]
							if hostname in item["productionHostnames"]:
								WAFHOST = True
								WAFProd = item["productionVersion"]
								try:
									item["name"]
									WAFName = item["name"]
								except:
									WAFName = "WAF Security File"
								#print bcolors.WHITE+"WAF Configuration Found: "+WAFName+bcolors.ENDC
						except:
							pass
			Auditrow = [hostname,str(EDGECNAME),initconfigName,PRODVersion,WAFName,WAFProd]
			AuditTable.add_row(Auditrow)
		else:
			print bcolors.WARNING+"Error with host: "+hostname+bcolors.ENDC
			print bcolors.WARNING+"Status Code: "+str(result.status_code)+bcolors.ENDC
			continue
		#print "\n"
	FinalTable = AuditTable.draw()
	print bcolors.WARNING+"[Audit] Audit Table:"+bcolors.ENDC
	print FinalTable
	print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	sys.exit()


def mapping(AccountSwitch,propertyName,apiObject):
	print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	filename = '.map'
	readfile = []
	#except IOError:
	#	print bcolors.TURQUO+'[MAPPING]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
	#	print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	#	sys.exit()
	if apiObject == 'add':
		outputfile = open(filename, 'a')
		if not propertyName:
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" You need to provide a friendly name to this account: -N nasdaq\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not AccountSwitch:
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" You need to provide an Account Switch Key: -A AANA-35EV8X\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		for item in contents:
			if "[" and "]" in item:
				accountCheck = item[1:-2]
				if accountCheck == propertyName:
					print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.FAIL+" Name already exists and is mapped to Account: "+contents[contents.index(item)+1]+bcolors.ENDC
					print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
			else:
				if item.strip() == AccountSwitch:
					print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.FAIL+" Account already exists and is mapped to Name: "+contents[contents.index(item)-1]+bcolors.ENDC
					print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
		entry = "["+propertyName+"]\n"+AccountSwitch+"\n\n"
		try:
			outputfile.writelines(entry)
			#print outputfile
			outputfile.close()
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Successfully added friendly name to .map file."+bcolors.ENDC
		except:
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" There was a problem adding friendly name to .map file"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'delete':
		if not propertyName and not AccountSwitch:
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" You need to provide a Name or an Account to delete: -N nasdaq / -A AANA-35EV8X\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		if propertyName:
			for item in contents:
				if "[" and "]" in item:
					accountCheck = item[1:-2]
					if accountCheck == propertyName:
						index = contents.index(item)
						print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Name FOUND in .map file"+bcolors.ENDC
			try:
				index
				del contents[index:index+3]
			except:
				print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Name NOT found in .map file."+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		else:
			for item in contents:
				if "[" and "]" in item:
					pass
				else:
					if item.strip() == AccountSwitch:
						index = contents.index(item)
						print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Account FOUND in .map file"+bcolors.ENDC
			try:
				index
				del contents[index-1:index+2]
			except:
				print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Account NOT found in .map file."+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		try:
			outputfile = open(filename, 'w')
			outputfile.writelines(contents)
			#print outputfile
			#outputfile.close()
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Successfully Removed Map"+bcolors.ENDC
		except:
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" There was a problem removing name from .map file"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'search':
		if not propertyName and not AccountSwitch:
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" You need to provide a Name or an Account to search: -N nasdaq / -A AANA-35EV8X\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		found = False
		if propertyName:
			for item in contents:
				if "[" and "]" in item:
					accountCheck = item[1:-2]
					if accountCheck == propertyName:
						found = True
						print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Name found and mapped to Account: "+contents[contents.index(item)+1]+bcolors.ENDC
						print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
						sys.exit()
		else:
			for item in contents:
				if "[" and "]" in item:
					pass
				else:
					if item.strip() == AccountSwitch:
						found = True
						print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Account found and mapped to Name: "+contents[contents.index(item)-1]+bcolors.ENDC
						print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
						sys.exit()
		if found == False:
			print bcolors.TURQUO+"[MAPPING]"+bcolors.ENDC+bcolors.WARNING+" Not found in .map file"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you to map a friendly name to your Account Switch Keys\n"+bcolors.ENDC
		print bcolors.WARNING+"SWaPI Mapping:\n"+bcolors.ENDC
		print "add 	- Add a new friendly name in your .map file"
		print "delete 	- Delete an existing map"
		print "search 	- Search account or names in your .map file"
		print bcolors.WARNING+"\nAvailable Options:\n"+bcolors.ENDC
		print "-N 	- Used to specify a friendly name"
		print "-A 	- Used to specify the Account Switch Key"
		print bcolors.WARNING+"\n\nNOTE: SWaPI creates a hidden file called '.map' which is used as read/write for this function\n"+bcolors.ENDC
		print bcolors.TURQUO+"\nMain Blog: https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/09/swapi-application-security-main"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def SecMon(automation,AccountSwitch,retrieveobj,reportPackId,respjson,creds):
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print '[IAM] Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.WARNING+'[IAM] SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.WARNING+'[IAM] Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if retrieveobj == 'reports':
		if reportPackId:
			result = s.get(urljoin(baseurl, '/security-monitor/v1/report-packs/'+reportPackId))
		else:
			result = s.get(urljoin(baseurl, '/security-monitor/v1/report-packs/'))
		if result.status_code == 200:
			if respjson:
				print result.content
				sys.exit()
			if not reportPackId:
				print bcolors.TURQUO+'[SecMon]'+bcolors.WARNING+' Report Packs '+bcolors.ENDC
				ParentTable = tt.Texttable()
				ParentTable.set_cols_width([10,70,30,10,6,10])
				ParentTable.set_cols_align(['c','c','c','c','c','c'])
				ParentTable.set_cols_valign(['m','m','m','m','m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Parentheader = ['Report ID','Name','SubType','Timezone','Type','Active']
				ParentTable.header(Parentheader)
				for item in result.json():
					Parentrow = [ item['id'],item['name'],item['subType'],item['timezone'],item['type'],str(item['isActive']) ]
					ParentTable.add_row(Parentrow)
				MainParentTable = ParentTable.draw()
				print MainParentTable
			else:
				print result.json()
				print bcolors.TURQUO+'[SecMon]'+bcolors.WARNING+' Main Table '+bcolors.ENDC
				Main = tt.Texttable()
				Main.set_cols_width([15,70,15,15,15,15,15])
				Main.set_cols_align(['c','c','c','c','c','c','c'])
				Main.set_cols_valign(['m','m','m','m','m','m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Mainheader = ['Report Pack ID','Name','SubType','Filters','Timezone','Type','Active']
				Main.header(Mainheader)
				Mainrow = [ result.json()['id'],result.json()['name'],result.json()['subType'],result.json()['filters'],result.json()['timezone'],result.json()['type'],str(result.json()['isActive']) ]
				Main.add_row(Mainrow)
				MainTable = Main.draw()
				print MainTable
				print bcolors.TURQUO+'[SecMon]'+bcolors.WARNING+' Data Stores '+bcolors.ENDC
				DataStore = tt.Texttable()
				DataStore.set_cols_width([15,70,15,50])
				DataStore.set_cols_align(['c','c','c','c'])
				DataStore.set_cols_valign(['m','m','m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				DataStoreheader = ['DataStore ID','Name','Type','Description']
				DataStore.header(DataStoreheader)
				for item in result.json()['dataStores']:
					DataStorerow = [ item['id'],item['name'],item['type'],item['description'] ]
					DataStore.add_row(DataStorerow)
				DataStoreTable = DataStore.draw()
				print DataStoreTable
				print bcolors.TURQUO+'\n[SecMon]'+bcolors.WARNING+' Metrics '+bcolors.ENDC
				Metrics = tt.Texttable()
				Metrics.set_cols_width([15,50])
				Metrics.set_cols_align(['c','c'])
				Metrics.set_cols_valign(['m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Metricsheader = ['ID','Name']
				Metrics.header(Metricsheader)
				for item in result.json()['dimensions']:
					Metricsrow = [ item['id'],item['name'] ]
					Metrics.add_row(Metricsrow)
				MetricsTable = Metrics.draw()
				print MetricsTable
				print bcolors.TURQUO+'\n[SecMon]'+bcolors.WARNING+' Dimensions '+bcolors.ENDC
				Dimensions = tt.Texttable()
				Dimensions.set_cols_width([15,50,15])
				Dimensions.set_cols_align(['c','c','c'])
				Dimensions.set_cols_valign(['m','m','m'])
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Dimensionsheader = ['ID','Name','Type']
				Dimensions.header(Dimensionsheader)
				for item in result.json()['dimensions']:
					Dimensionsrow = [ item['id'],item['name'],item['type'] ]
					Dimensions.add_row(Dimensionsrow)
				DimensionsTable = Dimensions.draw()
				print DimensionsTable
		else:
			if respjson:
				print result.content
				sys.exit()
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'data':
		if not reportPackId:
			print bcolors.WARNING+"You need to specify a Report Pack Id: --reportId 104247\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			headers = {"Accept":"application/json"}
			#now = datetime.datetime.now().strftime('%b-%d-%I%M%p-%G')
			#now = t.strftime("%H:%M:%S %Z")
			#endDate = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
			#startDate = datetime.datetime.utcnow().replace(microsecond=0) - timedelta(hours=2)
			endDate = "05/07/2019:05:57"
			startDate = "05/07/2019:02:00"
			print endDate
			print startDate
			params = {"aggregation":"month","dimensions":"991,996","metrics":"987,2621,991,995","startDate":startDate,"endDate":endDate}
			result = s.get(urljoin(baseurl, '/security-monitor/v1/report-packs/'+reportPackId+'/data'),headers=headers, params=params)
		print "StatusCode: "+str(result.status_code)
		json_data = result.json()
		formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you to leverage Akamai's Security Monitor API\n"+bcolors.ENDC
		print bcolors.WARNING+"SecMon Retrieve Information:\n"+bcolors.ENDC
		print "reports 	- List Report Packs"
		print "data 		- List data sets"
		print bcolors.TURQUO+"\nMain Blog: #"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def NetworkListAPI(automation,AccountSwitch,host,retrieveobj,creds,propertyName,netId,listType,includeElements,extended,respjson,netlist,emails,cdn):
	def DeleteFromNL(host,netId,respjson):
		if "," in host:
			hosts = host.split(",")
			for element in hosts:
				params.update({"element":element})
				ANLresult = s.delete(urljoin(baseurl, "/network-list/v2/network-lists/"+netId+"/elements"),params=params)
				if ANLresult.status_code == 200:
					if respjson:
						json_data = ANLresult.json()
						formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
						colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
						#print colorful_json
						print ANLresult.content
						sys.exit()
					print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"Element succesfully removed: "+element+bcolors.ENDC
				else:
					if respjson:
						print ANLresult.content
						sys.exit()
					print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"There was a problem deleting the Element from your NL."+bcolors.ENDC
					print ANLresult.status_code
					print ANLresult.content
		else:
			params.update({"element":host})
			ANLresult = s.delete(urljoin(baseurl, "/network-list/v2/network-lists/"+netId+"/elements"),params=params)
			if ANLresult.status_code == 200:
				if respjson:
					json_data = ANLresult.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					#print colorful_json
					print ANLresult.content
					sys.exit()
				print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"Element has been removed successfully from NL."+bcolors.ENDC
			else:
				if respjson:
					print ANLresult.content
					sys.exit()
				print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"There was a problem deleting the Element from your NL."+bcolors.ENDC
				print ANLresult.status_code
				print ANLresult.content
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def AddtoNL(extended,host,netId,respjson):
		ANLheader = {"Content-Type":"application/json"} #,"X-ECWS-ACG":"ACG_ID"
		params.update({"extended":extended})
		if "," in host:
			host = host.split(",")
		else:
			host = host.split("\n")
		body = {"list":host}
		ANLresult = s.post(urljoin(baseurl, "/network-list/v2/network-lists/"+netId+"/append"),params=params,headers=ANLheader,json=body)
		if ANLresult.status_code == 202:
			if respjson:
				json_data = ANLresult.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print ANLresult.content
				sys.exit()
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"NL has been updated successfully."+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		else:
			if respjson:
				print ANLresult.content
				sys.exit()
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"There was a problem updating your NL."+bcolors.ENDC
			print ANLresult.status_code
			print ANLresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def ActivateNL(cdn,netId,emails,respjson):
		ANLheader = {"Content-Type":"application/json"} #,"X-ECWS-ACG":"ACG_ID"
		if cdn == "prod":
			url = "/network-list/v2/network-lists/"+netId+"/environments/PRODUCTION/activate"
		else:
			url = "/network-list/v2/network-lists/"+netId+"/environments/STAGING/activate"
		if emails:
			if "," in emails:
				emails = emails.split(",")
			else:
				emails = emails.split("\n")
		body = {"notificationRecipients":emails}
		ANLresult = s.post(urljoin(baseurl, url),params=params,headers=ANLheader,json=body)
		if ANLresult.status_code == 200:
			if respjson:
				json_data = ANLresult.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print ANLresult.content
				sys.exit()
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"Activation has been sent successfully to Platform: "+cdn+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		else:
			if respjson:
				print ANLresult.content
				sys.exit()
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"There was a problem activating your NL."+bcolors.ENDC
			print ANLresult.status_code
			print ANLresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def CreateANL(name,listType,extended,includeElements,host,respjson):
		CNLheader = {"Content-Type":"application/json"} #,"X-ECWS-ACG":"ACG_ID"
		params.update({"listType":listType,"extended":extended,"includeElements":includeElements})
		body = {"name":name,"type":listType}
		if host:
			if "," in host:
				host = host.split(",")
			else:
				host = host.split("\n")
			netlistAppend = {"list":host}
			body.update(netlistAppend)
		CNLresult = s.post(urljoin(baseurl, "/network-list/v2/network-lists"),params=params,headers=CNLheader,json=body)
		if CNLresult.status_code == 201:
			if respjson:
				json_data = CNLresult.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print CNLresult.content
				sys.exit()
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"Status Code: 201"+bcolors.ENDC
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"Your Network list has been created successfully."+bcolors.ENDC
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"Unique ID: "+CNLresult.json()["uniqueId"]+bcolors.ENDC
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"HREF: "+CNLresult.json()['links']['retrieve']['href']+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		else:
			if respjson:
				print CNLresult.content
				sys.exit()
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"There was a problem creating your NL."+bcolors.ENDC
			print CNLresult.status_code
			print CNLresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def SearchFunction(listType,extended,host,respjson):
		headers = {"Accept":"application/json"}
		url = '/network-list/v2/network-lists'
		params.update({"listType":listType,"extended":"true","includeElements":"true","search":host})
		result = s.get(urljoin(baseurl, url), headers=headers, params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			try:
				result.json()["networkLists"]
				lstindex = len(result.json()["networkLists"])
				for index,item in enumerate(result.json()["networkLists"]):
					HostnameTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					print bcolors.WARNING+str(index+1)+"."+bcolors.ENDC
					Hostnameheader = ['Name', 'Type','Entries', 'Created By', 'Production', 'Staging','Updated By']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([55,5,10,25,12,12,25])
					HostnameTable.set_cols_align(['c','c','c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m','m','m'])
					try:
						result.json()['readOnly']
						readOnly = str(item['readOnly'])
					except:
						readOnly = str(False)
					epochUpdate = str(item['updateDate'])
					epochCreate = str(item['createDate'])
					msepochUpdate = epochUpdate[:len(epochUpdate)-3] + "." + epochUpdate[len(epochUpdate)-3:]
					msepochCreate = epochCreate[:len(epochCreate)-3] + "." + epochCreate[len(epochCreate)-3:]
					#updateDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(msepochUpdate)))
					#createDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(msepochCreate)))
					Hostnamerow = [item['name'],item['type'],item['elementCount'],item['createdBy']+"\n"+str(item['createDate']),item['productionActivationStatus'],item['stagingActivationStatus'],item['updatedBy']+"\n"+str(item['updateDate'])]
					HostnameTable.add_row(Hostnamerow)
					ElementTable = tt.Texttable()
					ElementTable.set_cols_width([162])
					ElementTable.set_cols_align(['c'])
					ElementTable.set_cols_valign(['m'])
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					if item["type"] == "IP":
						Elementheader = ['IPs']
					else:
						Elementheader = ['GEO']
					ElementTable.header(Elementheader)
					listArray = []
					for value in item['list']:
						listArray.append(value)
					Elementrow = [ ','.join(item['list']) ]
					ElementTable.add_row(Elementrow)
					HostTable = HostnameTable.draw()
					print HostTable
					ListTable = ElementTable.draw()
					print ListTable
					print '\n'
			except:
				print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"No Results found.\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"There was a problem retrieving Network List information.\n\n"+bcolors.ENDC
			print "StatusCode: "+str(result.status_code)
			print result.json()
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		return netId
	def searchNL(netId):
		headers = {"Accept":"application/json"}
		url = '/network-list/v2/network-lists'
		params.update({"extended":"true"})
		result = s.get(urljoin(baseurl, url), headers=headers, params=params)
		if result.status_code == 200:
			for i in range(0,len(result.json()["networkLists"])):
				#print result.json()["networkLists"][i]["name"]
				#print propertyName.decode('utf-8')
				if result.json()["networkLists"][i]["name"].strip() == propertyName.decode('utf-8').strip():
					netId = result.json()["networkLists"][i]["uniqueId"]
					continue
			if netId == None:
				print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"We could not find your Network List. Are you sure about the name?\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		else:
			print bcolors.TURQUO+"[NL] "+bcolors.WARNING+"There was a problem retrieving Network List information.\n\n"+bcolors.ENDC
			print "StatusCode: "+str(result.status_code)
			print result.json()
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		return netId
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n'+bcolors.ENDC
	if AccountSwitch:
		filename = '.map'
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		for item in contents:
			if "[" and "]" in item:
				accountCheck = item[1:-2]
				if accountCheck == AccountSwitch:
					AccountSwitch = contents[contents.index(item)+1].strip()
					if not respjson:
						print bcolors.TURQUO+"[NL]"+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
	#print AccountSwitch
	params = {'accountSwitchKey':AccountSwitch}
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if retrieveobj == 'create':
		if not propertyName:
			print bcolors.TURQUO+"[NL]"+bcolors.WARNING+" You need to specify the name of your New Network List: -N 'IP Blacklist'\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not listType:
			print bcolors.TURQUO+"[NL]"+bcolors.WARNING+" You need to specify what type of Network List you are creating: --type IP/GEO\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		CreateANL(propertyName,listType,extended,includeElements,host,respjson)
	elif retrieveobj == 'activate':
		#print netId
		if netId:
			ActivateNL(cdn,netId,emails,respjson)
		if not propertyName:
			print bcolors.TURQUO+"[NL]"+bcolors.WARNING+" You need to specify a Network List Name: -N 'WAF Bypass List'\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		netId = searchNL(netId)
		#print cdn,netId,emails
		ActivateNL(cdn,netId,emails,respjson)
	elif retrieveobj == 'search':
		#print netId
		if not host:
			print bcolors.TURQUO+"[NL]"+bcolors.WARNING+" You need to specify an object to search: -t 1.1.1.1 / -t CN\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		SearchFunction(listType,extended,host,respjson)
	elif (retrieveobj == 'add') or (retrieveobj == 'remove'):
		if not netId:
			if not propertyName:
				print bcolors.TURQUO+"[NL]"+bcolors.WARNING+" You need to specify a Network List Name: -N 'WAF Bypass List'\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			else:
				netId = searchNL(netId)
		if not host:
			print bcolors.TURQUO+"[NL]"+bcolors.WARNING+" You can add multiple items to a NL: -t 64.16.23.0/24,64.10.10.10\nOR\n"+bcolors.ENDC
			print bcolors.TURQUO+"[NL]"+bcolors.WARNING+" You can remove an single element from the NL: -t 64.10.10.10\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print extended,netlist,netId
		if retrieveobj == "add":
			AddtoNL(extended,host,netId,respjson)
		else:
			DeleteFromNL(host,netId,respjson)
	elif retrieveobj == 'list':
		if listType == "IP" or listType == "GEO":
			payloadAppend = {"listType":listType}
			params.update(payloadAppend)
		payloadAppend = {"includeElements":includeElements,"extended":extended}
		params.update(payloadAppend)
		headers = {"Accept":"application/json"}
		if propertyName:
			netId = searchNL(netId)
			url = '/network-list/v2/network-lists/'+netId
			params["extended"] = "true"
		elif netId:
			url = '/network-list/v2/network-lists/'+netId
			params["extended"] = "true"
		else:
			url = '/network-list/v2/network-lists'
		#print payload
		result = s.get(urljoin(baseurl, url), headers=headers, params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			elif propertyName or netId:
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Hostnameheader = ['Name', 'Type','Entries', 'Created By', 'Production', 'Staging','Updated By']
				HostnameTable.header(Hostnameheader)
				HostnameTable.set_cols_width([55,5,10,22,20,20,40])
				HostnameTable.set_cols_align(['c','c','c','c','c','c','c'])
				HostnameTable.set_cols_valign(['m','m','m','m','m','m','m'])
				try:
					result.json()['readOnly']
					readOnly = str(item['readOnly'])
				except:
					readOnly = str(False)
				epochUpdate = str(result.json()['updateDate'])
				epochCreate = str(result.json()['createDate'])
				msepochUpdate = epochUpdate[:len(epochUpdate)-3] + "." + epochUpdate[len(epochUpdate)-3:]
				msepochCreate = epochCreate[:len(epochCreate)-3] + "." + epochCreate[len(epochCreate)-3:]
				#updateDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(msepochUpdate)))
				#createDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(msepochCreate)))
				Hostnamerow = [result.json()['name'],result.json()['type'],result.json()['elementCount'],result.json()['createdBy']+"\n"+str(result.json()['createDate']),result.json()['productionActivationStatus'],result.json()['stagingActivationStatus'],result.json()['updatedBy']+"\n"+str(result.json()['updateDate'])]
				HostnameTable.add_row(Hostnamerow)
				HostTable = HostnameTable.draw()
				print HostTable
				if includeElements:
					ElementTable = tt.Texttable()
					ElementTable.set_cols_width([190])
					ElementTable.set_cols_align(['c'])
					ElementTable.set_cols_valign(['m'])
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					if result.json()["type"] == "IP":
						Elementheader = ['IPs']
					else:
						Elementheader = ['GEO']
					ElementTable.header(Elementheader)
					listArray = []
					for value in result.json()['list']:
						listArray.append(value)
					Elementrow = [ ','.join(result.json()['list']) ]
					ElementTable.add_row(Elementrow)
					ListTable = ElementTable.draw()
					print ListTable
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			else:
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['networkLists']:
					#print item
					Hostnameheader = ['Name', 'Type','Num Entries', 'Read Only', 'Unique ID']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([65,10,15,15,35])
					HostnameTable.set_cols_align(['c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m'])
					try:
						item['readOnly']
						readOnly = str(item['readOnly'])
					except:
						readOnly = str(False)
					Hostnamerow = [item['name'],item['type'],item['elementCount'],readOnly,item['uniqueId']]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
				print HostTable
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
			#print result.content
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	else:
		print bcolors.WHITE+"This module allows you to view/create/modify/activate Network Lists\n"+bcolors.ENDC
		print bcolors.WARNING+"Network Lists Retrieve Information:\n"+bcolors.ENDC
		print "list 		- List Multi Security Configuration"
		print "search 		- Search and retrieve information about IP's and GEO's"
		print bcolors.WARNING+"\nNetwork Lists Actions:\n"+bcolors.ENDC
		print "create 		- Create a new Network List"
		print "add 		- Add items to a Network List"
		print "remove 		- Remove items from a Network List"
		print "activate 	- Activate Security Configuration to Staging or Production"
		print "new 		- Create a new Network List"
		print bcolors.WARNING+"\nSWaPI Options:\n"+bcolors.ENDC
		print "-N 		- Provide a Network List Name"
		print "--netId 	- Provide a Network List ID"
		print "--type 		- Filters by the network list type,  either GEO or IP"
		print "--t 		- Used when adding and removing elements from Network Lists. Also used when searching for NL information"
		print "--items 	- Provides a full list of elements. Boolean."
		print "--extended 	- Verbose Data. Boolean."
		print "--json 		- Return JSON response. Boolean."
		print bcolors.TURQUO+"\nMain Blog: https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/15/swapi-network-lists"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	sys.exit()


def SiteShield(automation,AccountSwitch,apiObject,mapId,creds,respjson):
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if apiObject == 'ack':
		if not mapId:
			print bcolors.TURQUO+"[SiteShield]"+bcolors.ENDC+bcolors.WARNING+" You need to provide a mapId to acknowledge: --mapId 123455 "+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	if mapId:
		if apiObject == 'ack':
			result = s.post(urljoin(baseurl, '/siteshield/v1/maps/'+mapId+'/acknowledge'))
		else:
			result = s.get(urljoin(baseurl, '/siteshield/v1/maps/'+mapId))
	else:
		result = s.get(urljoin(baseurl, '/siteshield/v1/maps'))
	#print result.content
	if result.status_code == 200 or result.status_code == 201:
		if respjson:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			#print colorful_json
			print result.content
			sys.exit()
		else:
			if apiObject == 'ack':
				print bcolors.TURQUO+"[SiteShield] "+bcolors.WARNING+"Acknowledging SS Map "+mapId+" Success!!"+bcolors.ENDC
			else:
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				if mapId:
					print bcolors.TURQUO+"[SiteShield] "+bcolors.WARNING+"Retrieving SS Map: "+mapId+bcolors.ENDC
					Hostnameheader = ['Map', 'Contacts', 'Type', 'Acknowledged' ,'Current Cidrs','Proposed Cidrs']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([20,30,12,15,45,45])
					HostnameTable.set_cols_align(['c','c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m','m'])
					try:
						result.json()['proposedCidrs']
						proposedCidrs = result.json()['proposedCidrs']
					except:
						proposedCidrs = None
					Hostnamerow = [result.json()['ruleName'],result.json()['contacts'],result.json()['type'],str(result.json()['acknowledged']),result.json()['currentCidrs'],proposedCidrs]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
					print HostTable
				else:
					print bcolors.TURQUO+"[SiteShield] "+bcolors.WARNING+"Retrieving SS Maps "+bcolors.ENDC
					for item in result.json()['siteShieldMaps']:
						#print item
						Hostnameheader = ['Map Name', 'Map ID', 'Map', 'Acknowledged', 'SureRoute' ,'Current Cidrs']
						HostnameTable.header(Hostnameheader)
						HostnameTable.set_cols_width([20,10,25,15,25,70])
						HostnameTable.set_cols_align(['c','c','c','c','c','c'])
						HostnameTable.set_cols_valign(['m','m','m','m','m','m'])
						try:
							item['sureRouteName']
							sureRouteName = item['sureRouteName']
						except:
							sureRouteName = None
						Hostnamerow = [item['mapAlias'],item['id'],item['ruleName'],str(item['acknowledged']),sureRouteName,item['currentCidrs']]
						HostnameTable.add_row(Hostnamerow)
						HostTable = HostnameTable.draw()
					try:
						HostTable
						print HostTable
					except:
						print bcolors.TURQUO+"[SiteShield] "+bcolors.WARNING+"No maps found. "+bcolors.ENDC
	else:
		json_data = result.json()
		formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print colorful_json
	print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	sys.exit()


def CPSandSPS(automation,AccountSwitch,apiObject,edge,creds,respjson,productId,contractId,groupId,certId,propertyName):
	def CPSSearch(propertyName):
		Headers = {"Accept": "application/vnd.akamai.cps.enrollments.v1+json"}
		certId = None
		#if not propertyName:
		#		print bcolors.WARNING+"You need to specify a Certificate Name (CN): -N konanow.edgesuite.net\n\n"+bcolors.ENDC
		#		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		#		sys.exit()
		result = s.get(urljoin(baseurl, '/cps/v2/enrollments'), headers=Headers,params=params)
		if result.status_code == 200:
			for i in range(0,len(result.json()["enrollments"])):
				if result.json()["enrollments"][i]["csr"]["cn"] == propertyName:
					certId = result.json()["enrollments"][i]["location"].strip()
					if apiObject == "create":
						print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"Certificate Name already exists. Are you sure about your CN?\n\n"+bcolors.ENDC
						print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
						sys.exit()
					print bcolors.WARNING+"[CPS] Certificate Enrollments Found\n"+bcolors.ENDC
			if certId == None:
				if apiObject == "create":
					return
				print bcolors.WARNING+"[CPS] We could not find any Certificate matching your request.\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			else:
				return certId
		else:
			print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"There was a problem processing your request.\n\n"+bcolors.ENDC
			print bcolors.WARNING+str(result.status_code)+bcolors.ENDC
			print bcolors.WARNING+result.content+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	def CreateNewEnrollment(contractId,CertRequest):
		#CNEquery = {"contractId":contractId}
		CNEheaders = {"Content-Type":"application/vnd.akamai.cps.enrollment.v4+json","Accept":"application/vnd.akamai.cps.enrollment-status.v1+json"}
		CNEresult = s.post(urljoin(baseurl, "/cps/v2/enrollments"),json=CertRequest,headers=CNEheaders,params=params)
		if (CNEresult.status_code == 200) or (CNEresult.status_code == 202):
			print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"New Enrollment created successfully\n\n"+bcolors.ENDC
			print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"Response Code: "+str(CNEresult.status_code)+bcolors.ENDC
			print bcolors.WARNING+CNEresult.content+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"There was a problem processing your request"+bcolors.ENDC
			print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"Response Code: "+str(CNEresult.status_code)+bcolors.ENDC
			print bcolors.WARNING+CNEresult.content+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def CreateANewSecureEdge(productId,contractId,groupId,host,enrollmentId):
		CSEHeaders = {"Content-Type":"application/x-www-form-urlencoded"}
		CSEQuery = {"contractId":contractId,"groupId":groupId}
		params.update({"contractId":contractId})
		params.update({"groupId":groupId})
		form = {"cnameHostname":host,"enrollmentId":enrollmentId,"product":productId}
		CSEresult = s.post(urljoin(baseurl, "/config-secure-provisioning-service/v1/secure-edge-hosts"),params=params,data=form,headers=CSEHeaders)
		if (CSEresult.status_code == 200) or (CSEresult.status_code == 202):
			print bcolors.TURQUO+"[SPS] "+bcolors.WARNING+"New Secure EdgeHostname created successfully\n\n"+bcolors.ENDC
			print bcolors.TURQUO+"[SPS] "+bcolors.WARNING+"Response Code: "+str(CSEresult.status_code)+bcolors.ENDC
			print bcolors.WARNING+CSEresult.content+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[SPS] "+bcolors.WARNING+"There was a problem processing your request"+bcolors.ENDC
			print bcolors.TURQUO+"[SPS] "+bcolors.WARNING+"Response Code: "+str(CSEresult.status_code)+bcolors.ENDC
			print bcolors.WARNING+CSEresult.content+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	if AccountSwitch:
		filename = '.map'
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		for item in contents:
			if "[" and "]" in item:
				accountCheck = item[1:-2]
				if accountCheck == AccountSwitch:
					AccountSwitch = contents[contents.index(item)+1].strip()
					if not respjson and not automation:
						print bcolors.TURQUO+"[CPS]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
	#print AccountSwitch
	params = {'accountSwitchKey':AccountSwitch}
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if apiObject == "secureEdge":
		if not contractId:
			print bcolors.TURQUO+"[SPS] "+bcolors.WARNING+"You need to specify a contractId: --contract ctr_F-MRTALC\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not groupId:
			print bcolors.TURQUO+"[SPS] "+bcolors.WARNING+"You need to specify a groupId: --group grp_109031\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		payload = {"contractId":contractId,"groupId":groupId,"information":"false"}
		params.update({"contractId":contractId,"groupId":groupId,"information":"false"})
		result = s.get(urljoin(baseurl, '/config-secure-provisioning-service/v1/sps-requests'), params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			#print result.content
			#print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == "certs":
		Headers = {"Accept": "application/vnd.akamai.cps.enrollments.v1+json"}
		certId = None
		result = s.get(urljoin(baseurl, '/cps/v2/enrollments'), headers=Headers, params=params)
		#print result.json()
		if not propertyName:
			if result.status_code == 200:
				if respjson:
					print result.content
					sys.exit()
				print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"Found ALL Certificate Enrollments:\n"+bcolors.ENDC
				for i in range(0,len(result.json()["enrollments"])):
					print bcolors.WHITE+"EnrollmentID: "+bcolors.ENDC+result.json()["enrollments"][i]["location"].split("/")[4]
					print bcolors.WHITE+"Certificate Name (CN): "+bcolors.ENDC+result.json()["enrollments"][i]["csr"]["cn"]
					certId = result.json()["enrollments"][i]["location"]
					HeadersGET = {"Accept": "application/vnd.akamai.cps.enrollment.v1+json"}
					Cert = s.get(urljoin(baseurl, certId), headers=HeadersGET, params=params)
					#print Cert.content,"\n\n"
					MainCertTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					print Cert.json()
					MainCertheader = ['CN', 'Type', 'Country', 'State', 'Location', 'Organization', 'Unit', 'SANS']
					MainCertTable.header(MainCertheader)
					MainCertTable.set_cols_width([30,15,8,8,10,20,20,50])
					MainCertTable.set_cols_align(['c','c','c','c','c','c','c','c'])
					MainCertTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
					MainCertrow = [Cert.json()['csr']['cn'],Cert.json()['certificateType'],Cert.json()['csr']['c'],Cert.json()['csr']['st'],Cert.json()['csr']['l'],Cert.json()['csr']['o'],Cert.json()['csr']['ou'],Cert.json()['csr']['sans']]
					MainCertTable.add_row(MainCertrow)
					MainCTable = MainCertTable.draw()
					print MainCTable
					OrgTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					Orgheader = ['Name', 'Country', 'City', 'Region', 'PostalCode', 'Phone', 'Address Line1']
					OrgTable.header(Orgheader)
					print type(Cert.json()['org']['phone'])
					OrgTable.set_cols_width([45,10,10,10,10,20,59])
					OrgTable.set_cols_align(['c','c','c','c','c','c','c'])
					OrgTable.set_cols_valign(['m','m','m','m','m','m','m'])
					Orgrow = [Cert.json()['org']['name'],Cert.json()['org']['country'],Cert.json()['org']['city'],Cert.json()['org']['region'],Cert.json()['org']['postalCode'],str(Cert.json()['org']['phone']),Cert.json()['org']['addressLineOne']]
					OrgTable.add_row(Orgrow)
					OrgCertTable = OrgTable.draw()
					print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"Organization Table"+bcolors.ENDC
					print OrgCertTable
					AdminTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					Adminheader = ['First Name', 'Last Name', 'Phone', 'Email']
					AdminTable.header(Adminheader)
					AdminTable.set_cols_width([20,35,25,30])
					AdminTable.set_cols_align(['c','c','c','c'])
					AdminTable.set_cols_valign(['m','m','m','m'])
					Adminrow = [Cert.json()['adminContact']['firstName'],Cert.json()['adminContact']['lastName'],Cert.json()['adminContact']['phone'],Cert.json()['adminContact']['email']]
					AdminTable.add_row(Adminrow)
					AdminCertTable = AdminTable.draw()
					print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"Admin Contact Table"+bcolors.ENDC
					print AdminCertTable
					TechTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					Techheader = ['First Name', 'Last Name', 'Phone', 'Email']
					TechTable.header(Techheader)
					TechTable.set_cols_width([20,35,25,30])
					TechTable.set_cols_align(['c','c','c','c'])
					TechTable.set_cols_valign(['m','m','m','m'])
					Techrow = [Cert.json()['techContact']['firstName'],Cert.json()['techContact']['lastName'],Cert.json()['techContact']['phone'],Cert.json()['techContact']['email']]
					TechTable.add_row(Techrow)
					TechCertTable = TechTable.draw()
					print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"Tech Contact Table"+bcolors.ENDC
					print TechCertTable
					print bcolors.TURQUO+'\n\n----------- Certificate Separator -----------\n\n'+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			else:
				print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"There was a problem processing your request."+bcolors.ENDC
				print bcolors.WARNING+str(result.status_code)+bcolors.ENDC
				print bcolors.WARNING+result.content+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		else:
			for i in range(0,len(result.json()["enrollments"])):
				if result.json()["enrollments"][i]["csr"]["cn"] == propertyName:
					certId = result.json()["enrollments"][i]["location"].strip()
			if certId == None:
				print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"We could not find any Certificate matching your request.\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			HeadersGET = {"Accept": "application/vnd.akamai.cps.enrollment.v1+json"}
			resultGET = s.get(urljoin(baseurl, certId), headers=HeadersGET, params=params)
			if resultGET.status_code == 200:
				print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"Certificate Enrollment found.\n"+bcolors.ENDC
				print resultGET.content
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			else:
				print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+"There was a problem processing your request."+bcolors.ENDC
				print bcolors.TURQUO+"[CPS] "+bcolors.WARNING+str(resultGET.status_code)+bcolors.ENDC
				print bcolors.WARNING+resultGET.content+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'create':
		if edge:
			if not contractId:
				print bcolors.WARNING+"You need to specify a contractId: --contract ctr_F-MRTALC\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if not groupId:
				print bcolors.WARNING+"You need to specify a groupId: --group grp_109031\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if not enrollmentId:
				print bcolors.WARNING+"You need to specify a enrollmentId: --enroll 22135\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if not productId:
				print bcolors.WARNING+"You need to specify a productId: --product SiteDefender\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			CreateANewSecureEdge(productId,contractId,groupId,host,enrollmentId)
			'''
		if not propertyName:
			print bcolors.WARNING+"You must specify a Certificate Name (CN) with the -N option: -N www.swapi.com\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		CPSSearch (propertyName)
		if not os.path.isfile("cps-module/"+propertyName+".csv"):
			print "You will need to feed SWaPI with an Integration File: files/"+propertyName+".csv"'\n\n'
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		with open("cps-module/"+propertyName+".csv", "rU") as file:
			fieldnames = ("contractId","ra","validationType","certificateType","signatureAlgorithm","changeManagement","CN","SANS","Country","State","Locality","Organization","OrganizationalUnit","orgName","addressL1", "addressL2", "city", "region", "postalCode", "orgCountry","orgPhone", "adminfirstName", "adminlastName", "adminphone", "adminemail", "techfirstName", "techlastName", "techphone", "techemail", "thirdParty", "networkType", "mustHaveCiphers", "preferredCiphers", "sni")
			reader = csv.DictReader(file, fieldnames=fieldnames)
			#print reader
			configCounter = 0
			for row in reader:
				if not row["contractId"]:
					continue
				else:
					if configCounter == 0:
						configCounter = configCounter + 1
						pass
					else:
						contractId = row["contractId"]
						ra = row["ra"]
						validationType = row["validationType"]
						certificateType = row["certificateType"]
						signatureAlgorithm = row["signatureAlgorithm"]
						changeManagement = row["changeManagement"]
						CN = row["CN"]
						SANS = row["SANS"]
						Country = row["Country"]
						State = row["State"]
						Locality = row["Locality"]
						Organization = row["Organization"]
						OU = row["OrganizationalUnit"]
						orgName = row["orgName"]
						addressL1 = row["addressL1"]
						addressL2 = row["addressL2"]
						city = row["city"]
						region = row["region"]
						postalCode = row["postalCode"]
						orgCountry = row["orgCountry"]
						orgPhone = row["orgPhone"]
						adminfirstName = row["adminfirstName"]
						adminlastName = row["adminlastName"]
						adminphone = row["adminphone"]
						adminemail = row["adminemail"]
						techfirstName = row["techfirstName"]
						techlastName = row["techlastName"]
						techphone = row["techphone"]
						techemail = row["techemail"]
						thirdParty = row["thirdParty"]
						networkType = row["networkType"]
						mustHaveCiphers = row["mustHaveCiphers"]
						preferredCiphers = row["preferredCiphers"]
						sni = row["sni"]
						configCounter = configCounter + 1
			if "," in SANS:
				sans = SANS.split(",")
			else:
				sans = SANS.split("\n")
			if sni == "null":
				sni = None
				#sni = """
				#{
				#	"sni":null
				#}
				#"""
			#SNI = json.loads(str(sni))
			#print str(SNI)
			if thirdParty == "null":
				thirdParty == None
				#thirdParty = """
				#{
				#	"thirdParty":null
				#}
				#"""
			#thirdPartyLoad = json.loads(str(thirdParty))
			if changeManagement == "FALSE":
				changeManagement = False
			elif changeManagement == "TRUE":
				changeManagement = True
			org = {"name":orgName,"addressLineOne":addressL1,"addressLineTwo":addressL2,"city":city,"region":region,"postalCode":postalCode,"country":orgCountry,"phone":orgPhone}
			techContact = {"firstName":techfirstName,"lastName":techlastName,"phone":techphone,"email":techemail}
			adminContact = {"firstName":adminfirstName,"lastName":adminlastName,"phone":adminphone,"email":adminemail}
			csr = {"cn":CN,"c":Country,"st":State,"l":Locality,"o":Organization,"ou":OU,"sans":sans}
			networkConfiguration = {"geography": "core","secureNetwork": "enhanced-tls","disallowedTlsVersions": [],"networkType":networkType,"mustHaveCiphers":mustHaveCiphers,"preferredCiphers":preferredCiphers,"sni":sni}
			#networkConfiguration.update(SNI)
			CertRequest = {"enableMultiStackedCertificates": False,"ra":ra,"validationType":validationType,"certificateType":certificateType,"networkConfiguration":networkConfiguration,"signatureAlgorithm":signatureAlgorithm,"changeManagement":changeManagement,"csr":csr,"org":org,"techContact":techContact,"adminContact":adminContact,"thirdParty":thirdParty}
			#CertRequest.update(thirdPartyLoad)
		print CertRequest,"\n\n"
		CreateNewEnrollment(contractId,CertRequest)
		'''
	else:
		print bcolors.WARNING+"CPS/SPS Retrieve Information:\n"+bcolors.ENDC
		print "certs 		- List all certificates"
		print "secureEdge 	- List all Secure Edge Hostnames - NOT IMPLEMENTED"
		print bcolors.WARNING+"\nCPS/SPS Actions:\n"+bcolors.ENDC
		print "create 		- Create a new CPS enrollment or Secure Edge Hostname - EXPERIMENTAL For SecureEdge - NOT IMPLEMENTED for CPS"
		print bcolors.TURQUO+"\nMain Blog: https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/08/swapi-devops-takeover"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def AlertsManagement(AccountSwitch,propertyName,creds,respjson,retrieveobj,fname,fvalue,ids,extended):
	if not respjson:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if retrieveobj != 'audit':
		if AccountSwitch:
			filename = '.map'
			readfile = open(filename, 'r')
			contents = readfile.readlines()
			for item in contents:
				if "[" and "]" in item:
					accountCheck = item[1:-2]
					if accountCheck == AccountSwitch:
						AccountSwitch = contents[contents.index(item)+1].strip()
						if not respjson:
							print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
		#print AccountSwitch
		params = {'accountSwitchKey':AccountSwitch}
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if retrieveobj == 'templates':
		if ids:
			url = '/alerts/v2/alert-templates/'+ids
		else:
			url = '/alerts/v2/alert-templates/'
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				alertsTable = tt.Texttable()
				alertsHeader = ['Template ID', 'Name', 'Origin', 'Products']
				alertsTable.header(alertsHeader)
				alertsTable.set_cols_width([10,65,10,90])
				alertsTable.set_cols_align(['c','c','c','c'])
				alertsTable.set_cols_valign(['m','m','m','m'])
				for item in result.json()['data']:
					product_list = []
					for products in item['products']:
						product_list.append(products['name'])
					alertsRow = [item['templateId'],item['name'],item['origin'],','.join(product_list)]
					alertsTable.add_row(alertsRow)
				alertTable = alertsTable.draw()
				print alertTable
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Alerts]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Alerts]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'list':
		if fname:
			params.update({'fieldName':fname})
		if fvalue:
			params.update({'fieldValue':fvalue})
		if ids:
			params.update({'ids':ids})
		result = s.get(urljoin(baseurl, '/alerts/v2/alert-definitions'),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				if extended:
					for item in result.json()['data']:
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						alertsTable = tt.Texttable()
						alertsHeader = ['Account','Contract','Definition ID','Template ID', 'Active','Created At', 'Created By','Edited At','Edited By']
						alertsTable.header(alertsHeader)
						alertsTable.set_cols_width([13,13,13,13,10,25,25,25,25])
						alertsTable.set_cols_align(['c','c','c','c','c','c','c','c','c'])
						alertsTable.set_cols_valign(['m','m','m','m','m','m','m','m','m'])
						alertsRow = [item['accountId'],item['contractId'],item['definitionId'],item['templateId'],str(item['editInfo']['active']),item['editInfo']['createdAt'],item['editInfo']['createdBy'],item['editInfo']['editAt'],item['editInfo']['editBy']]
						alertsTable.add_row(alertsRow)
						alertTable = alertsTable.draw()
						print alertTable
						fieldsTable = tt.Texttable()
						fieldsHeader = ['Name', 'Value']
						fieldsTable.header(fieldsHeader)
						fieldsTable.set_cols_width([35,148])
						fieldsTable.set_cols_align(['c','c'])
						fieldsTable.set_cols_valign(['m','m'])
						#print item['fields']
						for name,value in item['fields'].iteritems():
							fieldsRow = [name,value]
							fieldsTable.add_row(fieldsRow)
						fieldTable = fieldsTable.draw()
						print bcolors.TURQUO+'\nFields Table\n'+bcolors.ENDC
						print fieldTable
						print bcolors.TURQUO+'\n\t\t\t\t\t\t\t\t------------------------ o ------------------------\n'+bcolors.ENDC
				else:
					alertsTable = tt.Texttable()
					alertsHeader = ['Account','Contract','Definition ID','Name', 'Active','Created At', 'Created By','Edited At','Edited By']
					alertsTable.header(alertsHeader)
					alertsTable.set_cols_width([13,13,13,26,7,20,25,20,25])
					alertsTable.set_cols_align(['c','c','c','c','c','c','c','c','c'])
					alertsTable.set_cols_valign(['m','m','m','m','m','m','m','m','m'])
					for item in result.json()['data']:
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						alertsRow = [item['accountId'],item['contractId'],item['definitionId'],item['fields']['name'],str(item['editInfo']['active']),item['editInfo']['createdAt'],item['editInfo']['createdBy'],item['editInfo']['editAt'],item['editInfo']['editBy']]
						alertsTable.add_row(alertsRow)
					alertTable = alertsTable.draw()
					print alertTable
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Alerts]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Alerts]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'active':
		if ids:
			url = '/alerts/v2/alert-definitions/'+ids+'/alert-firings'
		else:
			url = '/alerts/v2/alert-firings/active'
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				if extended:
					for item in result.json()['data']:
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						alertsTable = tt.Texttable()
						alertsHeader = ['Firing ID','Definition ID','Name', 'Start Time','End Time', 'Service']
						alertsTable.header(alertsHeader)
						alertsTable.set_cols_width([13,13,70,25,25,25])
						alertsTable.set_cols_align(['c','c','c','c','c','c'])
						alertsTable.set_cols_valign(['m','m','m','m','m','m'])
						alertsRow = [item['firingId'],item['definitionId'],item['name'],item['startTime'],item['endTime'],item['service']]
						alertsTable.add_row(alertsRow)
						alertTable = alertsTable.draw()
						print alertTable
						fieldsTable = tt.Texttable()
						fieldsHeader = ['Name', 'Value']
						fieldsTable.header(fieldsHeader)
						fieldsTable.set_cols_width([35,148])
						fieldsTable.set_cols_align(['c','c'])
						fieldsTable.set_cols_valign(['m','m'])
						#print item['fields']
						for name,value in item['fieldMap'].iteritems():
							fieldsRow = [name,value]
							fieldsTable.add_row(fieldsRow)
						fieldTable = fieldsTable.draw()
						print bcolors.TURQUO+'\nFields Table\n'+bcolors.ENDC
						print fieldTable
						print bcolors.TURQUO+'\n\t\t\t\t\t\t\t\t------------------------ o ------------------------\n'+bcolors.ENDC
				else:
					alertsTable = tt.Texttable()
					alertsHeader = ['Firing ID','Definition ID','Name', 'Start Time','End Time', 'Service']
					alertsTable.header(alertsHeader)
					alertsTable.set_cols_width([13,13,70,25,25,25])
					alertsTable.set_cols_align(['c','c','c','c','c','c'])
					alertsTable.set_cols_valign(['m','m','m','m','m','m'])
					for item in result.json()['data']:
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						alertsRow = [item['firingId'],item['definitionId'],item['name'],item['startTime'],item['endTime'],item['service']]
						alertsTable.add_row(alertsRow)
					alertTable = alertsTable.draw()
					print alertTable
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Alerts]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Alerts]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'audit':
		arrayWriter = []
		if ',' in AccountSwitch:
			AccountSwitch = AccountSwitch.split(',')
		else:
			AccountSwitch = AccountSwitch.split('\n')
		#print AccountSwitch
		with open('files/'+AccountSwitch[0]+'-AlertsAudit.csv', 'wb') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			header = ['Account','Contract','Definition ID','Name', 'Active','Created At', 'Created By','Edited At','Edited By']
			for account in AccountSwitch:
				#print account
				filename = '.map'
				readfile = open(filename, 'r')
				contents = readfile.readlines()
				for item in contents:
					if "[" and "]" in item:
						accountCheck = item[1:-2]
						if accountCheck == account:
							AccountSwitchKey = contents[contents.index(item)+1].strip()
							#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name "+account+" found and mapped to Account "+contents[contents.index(item)+1].strip()+bcolors.ENDC
				#print AccountSwitch
				try:
					AccountSwitchKey
					key = AccountSwitchKey
					AccountSwitchKey = None
				except:
					 key = account
				params = {'accountSwitchKey':key}
				result = s.get(urljoin(baseurl, '/alerts/v2/alert-definitions'),params=params)
				if result.status_code == 200:
					if len(AccountSwitch) > 1:
						print bcolors.TURQUO+'\n------------------------------ Separator ------------------------------\n'+bcolors.ENDC
					print bcolors.TURQUO+"[ALERTS]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name: "+account+bcolors.ENDC
					print bcolors.TURQUO+"[ALERTS]"+bcolors.ENDC+bcolors.WHITE+" Account: "+key+bcolors.ENDC
					if result.json()['data']:
						for item in result.json()['data']:
							#HostnameTable.set_deco(tt.Texttable.HEADER)
							mylist =  [item['accountId'],item['contractId'],item['definitionId'],item['fields']['name'],str(item['editInfo']['active']),item['editInfo']['createdAt'],item['editInfo']['createdBy'],item['editInfo']['editAt'],item['editInfo']['editBy']]
							arrayWriter.append(mylist)
					else:
						mylist =  [key,'No Contract','No Alerts','No Alerts','No Alerts','No Alerts','No Alerts','No Alerts','No Alerts']
						arrayWriter.append(mylist)
					print bcolors.TURQUO+"[ALERTS]"+bcolors.ENDC+bcolors.WHITE+" Alerts Information gathered successfully! "+bcolors.ENDC
					if len(AccountSwitch) > 1:
						print bcolors.TURQUO+'\n------------------------------ Separator ------------------------------\n'+bcolors.ENDC
				elif result.status_code == 401:
					print bcolors.TURQUO+"[ALERTS]"+bcolors.ENDC+bcolors.WARNING+" NOT Authorized: "+str(result.status_code)+bcolors.ENDC
					print bcolors.TURQUO+"[ALERTS]"+bcolors.ENDC+bcolors.WARNING+" Are you sure you using the right account? "+bcolors.ENDC
					print bcolors.TURQUO+"[ALERTS]"+bcolors.ENDC+bcolors.WARNING+" Account Name: "+account+bcolors.ENDC
					#print msc.content
				else:
					print bcolors.TURQUO+"[ALERTS]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
					print bcolors.TURQUO+"[ALERTS]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request for account: "+account+bcolors.ENDC
					print msc.content
			arrayWriter.insert(0, header)
			#for line in arrayWriter:
				#print line
				#wr.writerow(line)
			wr.writerows(arrayWriter)
		print bcolors.TURQUO+'\n------------------------------------------------------------------------------------------------------------------------'
		print bcolors.TURQUO+'[ALERTS]'+bcolors.ENDC+' CSV report generated. Filename: files/'+AccountSwitch[0]+'-AlertsAudit.csv'
		print bcolors.TURQUO+'------------------------------------------------------------------------------------------------------------------------'
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you to use the Alerts API to view/modify/create Alerts (Under Construction)\n"+bcolors.ENDC
		print bcolors.WARNING+"Alerts Retrieve Information:\n"+bcolors.ENDC
		print "templates 	- List available Templates"
		print "list 		- List cases"
		print "active 		- List cases"
		print bcolors.WARNING+"\nAutomations:\n"+bcolors.ENDC
		print "-audit 		- Creates a CSV report about enabled Alerts"
		print bcolors.WARNING+"\nAvailable Options:\n"+bcolors.ENDC
		print "-N 		- This option can be used to specify an Alert name"
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()



def caseManagement(duration,AccountSwitch,propertyName,creds,respjson,retrieveobj,category,type,notes):
	if not respjson:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if retrieveobj != 'list':
		if AccountSwitch:
			filename = '.map'
			readfile = open(filename, 'r')
			contents = readfile.readlines()
			for item in contents:
				if "[" and "]" in item:
					accountCheck = item[1:-2]
					if accountCheck == AccountSwitch:
						AccountSwitch = contents[contents.index(item)+1].strip()
						if not respjson:
							print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+bcolors.ENDC+contents[contents.index(item)+1].strip()
	#print AccountSwitch
	params = {'accountSwitchKey':AccountSwitch}
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if retrieveobj == 'categories':
		result = s.get(urljoin(baseurl, '/case-management/v2/categories'),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				categoryTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json():
					#print item
					categoryHeader = ['Type', 'Name', 'Description']
					categoryTable.header(categoryHeader)
					categoryTable.set_cols_width([55,55,55])
					categoryTable.set_cols_align(['c','c','c'])
					categoryTable.set_cols_valign(['m','m','m'])
					categoryRow = [item['categoryType'],item['displayName'],item['description']]
					categoryTable.add_row(categoryRow)
					catTable = categoryTable.draw()
				print catTable
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'create':
		if propertyName != None:
			propertyName
		else:
			print bcolors.TURQUO+'[Case]'+bcolors.WARNING+' You need to provide a file location for case JSON object with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
			exit()
		#print filename
		try:
			with open(propertyName) as json_data:
				rulesJson = json.load(json_data)
			#print(d)
			#rulesJson = open(filename, 'r').readlines()
		except:
			print bcolors.WARNING+"File NOT found:\n"+propertyName+"\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print rulesJson
		headers = {'Content-Type':'application/json'}
		result = s.post(urljoin(baseurl, '/case-management/v2/cases'),params=params,headers=headers,json=rulesJson)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				caseCreateTable = tt.Texttable()
				caseCreateHeader = ['Success', 'Case ID', 'Message']
				caseCreateTable.header(caseCreateHeader)
				caseCreateTable.set_cols_width([20,30,80])
				caseCreateTable.set_cols_align(['c','c','c'])
				caseCreateTable.set_cols_valign(['m','m','m'])
				caseCreateRow = [str(result.json()['success']),result.json()['caseId'],result.json()['message']]
				caseCreateTable.add_row(caseCreateRow)
				#print categoryRow
				createTable = caseCreateTable.draw()
				print createTable
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'add':
		if propertyName != None:
			propertyName
		else:
			print bcolors.TURQUO+'[Case]'+bcolors.WARNING+' You need to provide a case number with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if notes != None:
			notes
		else:
			print bcolors.TURQUO+'[Case]'+bcolors.WARNING+' You need to provide some notes with the --notes option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
			exit()
		notesJson = {'comment':str(notes)}
		headers = {'Content-Type':'application/json'}
		result = s.post(urljoin(baseurl, '/case-management/v2/cases/'+propertyName+'/notes'),params=params,headers=headers,json=notesJson)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				caseCreateTable = tt.Texttable()
				caseCreateHeader = ['Case ID', 'Status Message']
				caseCreateTable.header(caseCreateHeader)
				caseCreateTable.set_cols_width([20,80])
				caseCreateTable.set_cols_align(['c','c'])
				caseCreateTable.set_cols_valign(['m','m'])
				caseCreateRow = [result.json()['caseId'],result.json()['statusMessage']]
				caseCreateTable.add_row(caseCreateRow)
				#print categoryRow
				createTable = caseCreateTable.draw()
				print createTable
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'close':
		if propertyName != None:
			propertyName
		else:
			print bcolors.TURQUO+'[Case]'+bcolors.WARNING+' You need to provide a case number with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
			exit()
		if notes != None:
			notes
		else:
			print bcolors.TURQUO+'[Case]'+bcolors.WARNING+' You need to provide some closure notes with the --notes option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
			exit()
		notesJson = {'comment':str(notes)}
		headers = {'Content-Type':'application/json'}
		result = s.post(urljoin(baseurl, '/case-management/v2/cases/'+propertyName+'/close-request'),params=params,headers=headers,json=notesJson)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				caseCreateTable = tt.Texttable()
				caseCreateHeader = ['Case ID', 'Status Message']
				caseCreateTable.header(caseCreateHeader)
				caseCreateTable.set_cols_width([20,80])
				caseCreateTable.set_cols_align(['c','c'])
				caseCreateTable.set_cols_valign(['m','m'])
				caseCreateRow = [result.json()['caseId'],result.json()['statusMessage']]
				caseCreateTable.add_row(caseCreateRow)
				#print categoryRow
				createTable = caseCreateTable.draw()
				print createTable
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'severities':
		if category != None:
			category
		else:
			print bcolors.TURQUO+'[Case]'+bcolors.WARNING+' You need to provide a Category in order to view it\'s severities.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
			exit()
		result = s.get(urljoin(baseurl, '/case-management/v2/categories/'+category+'/severity-definitions'),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				severityTable = tt.Texttable()
				for item in result.json():
					#print item
					severityHeader = ['Severity Level', 'Description', 'Escalation Instruction','Standard Response Time']
					severityTable.header(severityHeader)
					severityTable.set_cols_width([20,70,60,30])
					severityTable.set_cols_align(['c','c','c','c'])
					severityTable.set_cols_valign(['m','m','m','m'])
					severityRow = [item['severityLevelType'],item['description'],item['escalationInstructions'],item['standardResponseTime']]
					severityTable.add_row(severityRow)
					#print categoryRow
				sevTable = severityTable.draw()
				print sevTable
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'list':
		if ',' in AccountSwitch:
			AccountSwitch = AccountSwitch.split(',')
		else:
			AccountSwitch = AccountSwitch.split('\n')
		#print AccountSwitch
		filename = 'files/'+AccountSwitch[0]+'-cases'+'.xlsx'
		if propertyName:
			pass
		else:
			workbook = xlsxwriter.Workbook(filename)
			caseSheet = workbook.add_worksheet('Cases')
			caseHeader = ['Account','Case ID', 'Severity', 'Subject', 'Category Type','Status','Create Date','Modified Date','Assigned To','Link','Customer']
			row = 0
			# Add a bold format to use to highlight cells.
			table_format = workbook.add_format()
			table_format.set_center_across()
			table_format.set_align('center')
			table_format.set_align('vcenter')
			table_format.set_font_size(12)
			table_format.set_border()
			header_format = workbook.add_format()
			header_format.set_bold()
			header_format.set_center_across()
			header_format.set_align('center')
			header_format.set_align('vcenter')
			header_format.set_font_size(12)
			header_format.set_border()
			for i in range(0,len(caseHeader)):
				caseSheet.set_column(i, 50)
				caseSheet.write(row,i, caseHeader[i],header_format)
			row = 1
		for account in AccountSwitch:
			#print account
			mapfile = '.map'
			readfile = open(mapfile, 'r')
			contents = readfile.readlines()
			for item in contents:
				if "[" and "]" in item:
					accountCheck = item[1:-2]
					if accountCheck == account:
						AccountSwitchKey = contents[contents.index(item)+1].strip()
						#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name "+account+" found and mapped to Account "+contents[contents.index(item)+1].strip()+bcolors.ENDC
			#print AccountSwitch
			try:
				AccountSwitchKey
				key = AccountSwitchKey
				AccountSwitchKey = None
			except:
				 key = account
			params = {'accountSwitchKey':key}
			if type:
				#print type
				params.update({"type":type})
			else:
				pass
			if duration:
				#print type
				params.update({"duration":duration})
			else:
				pass
			if propertyName:
				result = s.get(urljoin(baseurl, '/case-management/v2/cases/'+propertyName),params=params)
			else:
				result = s.get(urljoin(baseurl, '/case-management/v2/cases'),params=params)
			if result.status_code == 200:
				if respjson:
					json_data = result.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					#print colorful_json
					print result.content
					#sys.exit()
				else:
					if propertyName:
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						caseTable = tt.Texttable()
						descriptionTable = tt.Texttable()
						caseHeader = ['Case ID', 'Subject', 'Category Type','Status','Create Date','Modified Date','Assigned To','Severity']
						caseTable.header(caseHeader)
						caseTable.set_cols_width([15,40,15,15,20,20,20,15])
						caseTable.set_cols_align(['c','c','c','c','c','c','c','c'])
						caseTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
						caseRow = [result.json()['ticketInfo']['caseId'],result.json()['ticketInfo']['subject'],result.json()['ticketInfo']['categoryType'],result.json()['ticketInfo']['status'],result.json()['ticketInfo']['createdDate'],result.json()['ticketInfo']['modifiedDate'],result.json()['ticketInfo']['assignedTo'],result.json()['ticketInfo']['severity']]
						caseTable.add_row(caseRow)
						desHeader = ['Description']
						descriptionTable.header(desHeader)
						descriptionTable.set_cols_width([181])
						descriptionTable.set_cols_align(['c'])
						descriptionTable.set_cols_valign(['m'])
						desRow = [result.json()['ticketInfo']['description']]
						descriptionTable.add_row(desRow)
						try:
							result.json()['solution']
							solutionTable = tt.Texttable()
							solHeader = ['Solution Subject','Resolution']
							solutionTable.header(solHeader)
							solutionTable.set_cols_width([89,89])
							solutionTable.set_cols_align(['c','c'])
							solutionTable.set_cols_valign(['m','m'])
							solRow = [result.json()['solution']['solutionSubject'],result.json()['solution']['resolution']]
							solutionTable.add_row(solRow)
						except:
							pass
						try:
							result.json()['activities']
							for item in result.json()['activities']:
								actvitiesTable = tt.Texttable()
								actHeader = ['Activity Subject','Create Date','Created By','Description']
								actvitiesTable.header(actHeader)
								actvitiesTable.set_cols_width([40,30,35,67])
								actvitiesTable.set_cols_align(['c','c','c','c'])
								actvitiesTable.set_cols_valign(['m','m','m','m'])
								actRow = [item['activitySubject'],item['activityCreatedDate'],item['activityCreatedBy'],item['activityDescription']]
								actvitiesTable.add_row(actRow)
						except:
							pass
							#print categoryRow
						catTable = caseTable.draw()
						print catTable
						desTable = descriptionTable.draw()
						print desTable
						try:
							actvitiesTable.draw()
							actTable = actvitiesTable.draw()
							print bcolors.TURQUO+"\n[Case]"+bcolors.ENDC+bcolors.WARNING+" Activities: "+bcolors.ENDC
							print actTable
						except:
							pass
						try:
							solutionTable.draw()
							solTable = solutionTable.draw()
							print bcolors.TURQUO+"\n[Case]"+bcolors.ENDC+bcolors.WARNING+" Solutions: "+bcolors.ENDC
							print solTable
						except:
							pass
					else:
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						categoryTable = tt.Texttable()
						categoryHeader = ['Case ID', 'Subject', 'Category','Status','Create Date','Modified Date','Assigned To','Customer','Severity']
						categoryTable.header(categoryHeader)
						categoryTable.set_cols_width([15,40,15,15,20,20,20,15,10])
						categoryTable.set_cols_align(['c','c','c','c','c','c','c','c','c'])
						categoryTable.set_cols_valign(['m','m','m','m','m','m','m','m','m'])
						allRows = [categoryHeader]
						for item in result.json():
							#print item
							# caseHeader = ['Account','Case ID', 'Severity', 'Subject', 'Category Type','Status','Create Date','Modified Date','Assigned To','Link','Customer']
							if category:
								if category == item['categoryType']:
									categoryRow = [item['caseId'],item['subject'],item['categoryType'],item['status'],item['createdDate'],item['modifiedDate'],item['assignedTo'],item['customer'],item['severity']]
									#categoryTable.add_row(categoryRow)
									allRows.append(categoryRow)
									array = [key,item['caseId'],item['severity'],item['subject'],item['categoryType'],item['status'],item['createdDate'],item['modifiedDate'],item['assignedTo'],item['links'][0]['href'],item['customer']]
									for i in range(0,len(array)):
										caseSheet.set_column(i, 50)
										caseSheet.write(row,i, array[i],table_format)
									row += 1
								else:
									pass
							else:
								categoryRow = [item['caseId'],item['subject'],item['categoryType'],item['status'],item['createdDate'],item['modifiedDate'],item['assignedTo'],item['customer'],item['severity']]
								#categoryTable.add_row(categoryRow)
								allRows.append(categoryRow)
								array = [key,item['caseId'],item['severity'],item['subject'],item['categoryType'],item['status'],item['createdDate'],item['modifiedDate'],item['assignedTo'],item['links'][0]['href'],item['customer']]
								for i in range(0,len(array)):
									caseSheet.set_column(i, 50)
									caseSheet.write(row,i, array[i],table_format)
								row += 1
						#print categoryRow
						print bcolors.TURQUO+'[Case] Account: '+bcolors.ENDC+key
						if len(allRows) == 1:
							print bcolors.TURQUO+'[Case] '+bcolors.WARNING+'No Cases Found...\n'
						else:
							categoryTable.add_rows(allRows)
							catTable = categoryTable.draw()
							print catTable
			else:
				if respjson:
					print result.content
					#sys.exit()
				print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
		#pprint.pprint(result.json())
		if not propertyName:
			workbook.close()
			print bcolors.TURQUO+'\n------------------------------------------------------------------------------------------------------------------------'
			print bcolors.TURQUO+'[Case]'+bcolors.WARNING+' Excel report generated. File location: '+bcolors.WHITE+filename+bcolors.ENDC
			print bcolors.TURQUO+'------------------------------------------------------------------------------------------------------------------------'
			print bcolors.TURQUO+"\n[Case] "+bcolors.WARNING+"Status: "+bcolors.WHITE+"Successful"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'sub':
		if category != None:
			category
		else:
			print bcolors.TURQUO+'[Case]'+bcolors.WARNING+' You need to provide a Top Level Category in order to view sub-categories.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
			exit()
		result = s.get(urljoin(baseurl, '/case-management/v2/categories/'+category+'/sub-categories'),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['subCategory']['subCategories']:
					categoryTable = tt.Texttable()
					#print item
					for subcat in item['subCategory']['subCategories']:
						categoryHeader = ['Sub Level 1', 'Sub Level 2', 'Sub Level 3']
						categoryTable.header(categoryHeader)
						categoryTable.set_cols_width([55,55,55])
						categoryTable.set_cols_align(['c','c','c'])
						categoryTable.set_cols_valign(['m','m','m'])
						categoryRow = [item['subCategoryType'],item['subCategory']['subCategoryType'],subcat['subCategoryType']]
						categoryTable.add_row(categoryRow)
						catTable = categoryTable.draw()
					print catTable
					print bcolors.TURQUO+'\n------------------------ o ------------------------\n'+bcolors.ENDC
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[Case]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you to use the Case Management API to view/modify/activate your active cases\n"+bcolors.ENDC
		print bcolors.WARNING+"Case Management Retrieve Information:\n"+bcolors.ENDC
		print "list 		- List cases. This will automatically generate an Audit Report File will all found cases. Follow link provided when command is completed."
		print "categories 	- List available Top Level Categories"
		print "sub  		- List available sub Categories"
		print "severities  	- List severities for a Category"
		print bcolors.WARNING+"\nCase Management Actions:\n"+bcolors.ENDC
		print "create  	- Create a Support case"
		print "add  		- Add notes to a Support case"
		print "close  		- Close a Support case"
		print bcolors.WARNING+"\nAvailable Options:\n"+bcolors.ENDC
		print "-N 		- This option can be used to specify a case Number or a JSON file in your localsystem, which is used as template to create new support cases"
		print "--category 	- Specify a Top Level Category or filter cases based in 'Category Type'"
		print "--type 		- Filters tickets: user-active/user-closed, or company-active/company-closed. By Defaut, All"
		print "--notes 	- Provide notes to cases, or when closing a Case"
		print "-d 		- When listing cases, this option can be used to request cases before specified amount of days"
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def plxAnalytics(AccountSwitch,propertyName,creds,respjson,apiObject,host,contractId,groupId,start,end,attack):
	if not respjson:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if AccountSwitch:
		filename = '.map'
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		for item in contents:
			if "[" and "]" in item:
				accountCheck = item[1:-2]
				if accountCheck == AccountSwitch:
					AccountSwitch = contents[contents.index(item)+1].strip()
					if not respjson:
						print bcolors.TURQUO+"[DNS]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
	#print AccountSwitch
	params = {'accountSwitchKey':AccountSwitch}
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if apiObject == 'events':
		#print propertyName
		if contractId:
			url = '/prolexic-analytics/v1/events/contract/'+contractId
		else:
			print bcolors.TURQUO+'[PLX]'+bcolors.WARNING+' You need to provide a contract ID with the --contract option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				print bcolors.TURQUO+"[PLX]"+bcolors.WARNING+" Status Message: "+result.json()['statusMsg']+bcolors.ENDC
				print bcolors.TURQUO+"[PLX]"+bcolors.WARNING+" Contract: "+result.json()['currentContract']+bcolors.ENDC
				eTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				eHeader = ['Event Type', 'Service','Severity','is Ongoing','Event Title']
				eTable.header(eHeader)
				eTable.set_cols_width([15,15,15,15,95])
				eTable.set_cols_align(['c','c','c','c','c'])
				eTable.set_cols_valign(['m','m','m','m','m'])
				for item in result.json()['data']:
					#print item
					eRow = [item['eventType'],item['service'],item['severity'],str(item['isOngoing']),item['eventTitle']]
					eTable.add_row(eRow)
					eventTable = eTable.draw()
					print eventTable
					iTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					iHeader = ['Attack ID', 'Last Occurred', 'Event Start Time', 'Event End Time']
					iTable.header(iHeader)
					iTable.set_cols_width([98,20,20,20])
					iTable.set_cols_align(['c','c','c','c'])
					iTable.set_cols_valign(['m','m','m','m'])
					try:
						attackId = item['eventInfo']['attackId']
					except:
						attackId = 'None'
					try:
						lastOccurred = datetime.datetime.fromtimestamp(item['eventInfo']['lastOccurred'])
					except:
						lastOccurred = 'None'
					iRow = [attackId,lastOccurred,datetime.datetime.fromtimestamp(item['eventStartTime']),datetime.datetime.fromtimestamp(item['eventEndTime'])]
					iTable.add_row(iRow)
					infoTable = iTable.draw()
					print infoTable
					print bcolors.TURQUO+"\n	-----------------------------------------------------------------	Separator	-----------------------------------------------------------------\n"+bcolors.ENDC
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Code: "+bcolors.FAIL+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status: "+bcolors.FAIL+str(result.json()['status'])+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Message: "+bcolors.FAIL+str(result.json()['statusMsg'])+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'critical':
		#print propertyName
		if contractId:
			url = '/prolexic-analytics/v1/critical-events/contract/'+contractId
		else:
			print bcolors.TURQUO+'[PLX]'+bcolors.WARNING+' You need to provide a contract ID with the --contract option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				print bcolors.TURQUO+"[PLX]"+bcolors.WARNING+" Status Message: "+result.json()['statusMsg']+bcolors.ENDC
				print bcolors.TURQUO+"[PLX]"+bcolors.WARNING+" Contract: "+result.json()['currentContract']+bcolors.ENDC
				for item in result.json()['data']:
					eTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					eHeader = ['Event Id', 'First Occur','Recent Occur','Importance','Source','IP']
					eTable.header(eHeader)
					eTable.set_cols_width([60,20,20,12,15,20])
					eTable.set_cols_align(['c','c','c','c','c','c'])
					eTable.set_cols_valign(['m','m','m','m','m','m'])
					iTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					iHeader = ['Summary', 'Description']
					iTable.header(iHeader)
					iTable.set_cols_width([60,99])
					iTable.set_cols_align(['c','c'])
					iTable.set_cols_valign(['m','m'])
					#print item
					eRow = [item['eventId'],datetime.datetime.fromtimestamp(item['firstOccur']),datetime.datetime.fromtimestamp(item['recentOccur']),item['importance'],item['source'],item['ip']]
					eTable.add_row(eRow)
					eventTable = eTable.draw()
					print eventTable
					soup = BeautifulSoup(item['description'], 'html.parser')
					iRow = [item['summary'],soup.get_text()]
					iTable.add_row(iRow)
					infoTable = iTable.draw()
					print infoTable
					print bcolors.TURQUO+"\n	-----------------------------------------------------------------	Separator	-----------------------------------------------------------------\n"+bcolors.ENDC
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Code: "+bcolors.FAIL+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status: "+bcolors.FAIL+str(result.json()['status'])+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Message: "+bcolors.FAIL+str(result.json()['statusMsg'])+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'attacks':
		#print propertyName
		if contractId:
			pass
		else:
			print bcolors.TURQUO+'[PLX]'+bcolors.WARNING+' You need to provide a contract ID with the --contract option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if attack != 'None':
			url = '/prolexic-analytics/v1/attack-reports/contract/'+contractId+'/attack-id/'+attack
		elif start and end:
			url = '/prolexic-analytics/v1/attack-reports/contract/'+contractId+'/start/'+str(start)+'/end/'+str(end)
		else:
			print bcolors.TURQUO+'[PLX]'+bcolors.WARNING+' You need to provide a start and an end time (within 90 days): --start 1397049511 --end 1399641518'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				print bcolors.TURQUO+"[PLX]"+bcolors.WARNING+" Status Message: "+result.json()['statusMsg']+bcolors.ENDC
				print bcolors.TURQUO+"[PLX]"+bcolors.WARNING+" Contract: "+result.json()['currentContract']+bcolors.ENDC
				if attack != 'None':
					for item in result.json()['data']:
						eTable = tt.Texttable()
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						eHeader = ['Attack ID', 'Attack Type','Event ID','Ticket ID','Location']
						eTable.header(eHeader)
						eTable.set_cols_width([20,20,20,20,20])
						eTable.set_cols_align(['c','c','c','c','c'])
						eTable.set_cols_valign(['m','m','m','m','m'])
						#print item
						eRow = [item['attackId'],item['attackTypeName'],item['eventId'],item['ticketId'],item['location']]
						eTable.add_row(eRow)
						eventTable = eTable.draw()
						print eventTable
						iTable = tt.Texttable()
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						iHeader = ['IP', 'NetMask','Destination Port','Start Time','End Time','Event Bandwidth','Event PPS','Event Peak ID']
						iTable.header(iHeader)
						iTable.set_cols_width([20,20,20,20,20,20,20,20])
						iTable.set_cols_align(['c','c','c','c','c','c','c','c'])
						iTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
						iRow = [item['peaks'],item['destinations'],item['eventTypes']]
						iTable.add_row(iRow)
						infoTable = iTable.draw()
						print infoTable
						eRow = [item['ip'],item['attackTypeName'],item['eventId'],datetime.datetime.fromtimestamp(item['startTime']),datetime.datetime.fromtimestamp(item['endTime']),datetime.datetime.fromtimestamp(item['eventStartTime']),datetime.datetime.fromtimestamp(item['eventEndTime']),item['ticketId']]
				else:
					for item in result.json()['data']:
						eTable = tt.Texttable()
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						eHeader = ['Attack ID', 'Event ID','Start Time','End Time','Event Start Time','Event End Time','Ticket ID']
						eTable.header(eHeader)
						eTable.set_cols_width([20,20,20,20,20,20,30])
						eTable.set_cols_align(['c','c','c','c','c','c','c'])
						eTable.set_cols_valign(['m','m','m','m','m','m','m'])
						#print item
						eRow = [item['attackId'],item['eventId'],datetime.datetime.fromtimestamp(item['startTime']),datetime.datetime.fromtimestamp(item['endTime']),datetime.datetime.fromtimestamp(item['eventStartTime']),datetime.datetime.fromtimestamp(item['eventEndTime']),item['ticketId']]
						eTable.add_row(eRow)
						eventTable = eTable.draw()
						print eventTable
						iTable = tt.Texttable()
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						iHeader = ['Peaks', 'Destinations','Event Types']
						iTable.header(iHeader)
						iTable.set_cols_width([42,60,60])
						iTable.set_cols_align(['c','c','c'])
						iTable.set_cols_valign(['m','m','m'])
						iRow = [item['peaks'],item['destinations'],item['eventTypes']]
						iTable.add_row(iRow)
						infoTable = iTable.draw()
						print infoTable
						print bcolors.TURQUO+"\n	-----------------------------------------------------------------	Separator	-----------------------------------------------------------------\n"+bcolors.ENDC
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Code: "+bcolors.FAIL+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status: "+bcolors.FAIL+str(result.json()['status'])+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Message: "+bcolors.FAIL+str(result.json()['statusMsg'])+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'metrics':
		#print propertyName
		url = '/prolexic-analytics/v1/metric-types'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				print bcolors.TURQUO+"[PLX]"+bcolors.WARNING+" Status Message: "+result.json()['statusMsg']+bcolors.ENDC
				print bcolors.TURQUO+"[PLX]"+bcolors.WARNING+" Contract: "+result.json()['currentContract']+bcolors.ENDC
				eTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				eHeader = ['Product', 'Bandwidth In','Packets In']
				eTable.header(eHeader)
				eTable.set_cols_width([20,70,70])
				eTable.set_cols_align(['c','c','c'])
				eTable.set_cols_valign(['m','m','m'])
				eRow = ['Routed',result.json()['data']['routed']['metrics']['bandwidthIn']['desc'],result.json()['data']['routed']['metrics']['packetsIn']['desc']]
				eTable.add_row(eRow)
				eRow = ['Connect',result.json()['data']['connect']['metrics']['bandwidthIn']['desc'],result.json()['data']['connect']['metrics']['packetsIn']['desc']]
				eTable.add_row(eRow)
				productTable = eTable.draw()
				print productTable
				print bcolors.TURQUO+"\n	-----------------------------------------------------------------	Separator	-----------------------------------------------------------------\n"+bcolors.ENDC
				mTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				mHeader = ['Mitigation', 'Bandwidth','Packets']
				mTable.header(mHeader)
				mTable.set_cols_width([20,70,70])
				mTable.set_cols_align(['c','c','c'])
				mTable.set_cols_valign(['m','m','m'])
				mRow = ['Mitigation Post',result.json()['data']['mitigationPost']['metrics']['bandwidth']['desc'],result.json()['data']['mitigationPost']['metrics']['packets']['desc']]
				mTable.add_row(mRow)
				mRow = ['Mitigation Pre',result.json()['data']['mitigationPre']['metrics']['bandwidth']['desc'],result.json()['data']['mitigationPre']['metrics']['packets']['desc']]
				mTable.add_row(mRow)
				mitigationTable = mTable.draw()
				print mitigationTable
				print bcolors.TURQUO+"\n	-----------------------------------------------------------------	Separator	-----------------------------------------------------------------\n"+bcolors.ENDC
				fTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				fHeader = ['Product', 'Bandwidth','Packets']
				fTable.header(fHeader)
				fTable.set_cols_width([20,70,70])
				fTable.set_cols_align(['c','c','c'])
				fTable.set_cols_valign(['m','m','m'])
				fRow = ['FBM',result.json()['data']['fbm']['metrics']['bandwidth']['desc']+'\n'+', '.join(result.json()['data']['fbm']['metrics']['bandwidth']['protocols'])+'\n'+'\n'.join(result.json()['data']['fbm']['metrics']['bandwidth']['subnets']),result.json()['data']['fbm']['metrics']['packets']['desc']+'\n'+', '.join(result.json()['data']['fbm']['metrics']['packets']['protocols'])+'\n'+'\n'.join(result.json()['data']['fbm']['metrics']['packets']['subnets'])]
				fTable.add_row(fRow)
				fbmTable = fTable.draw()
				print fbmTable
				print bcolors.TURQUO+"\n	-----------------------------------------------------------------	Separator	-----------------------------------------------------------------\n"+bcolors.ENDC
				pTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				eHeader = ['Product', 'Bandwidth In', 'Bandwidth Out','Packets In','Packets Out']
				pTable.header(eHeader)
				pTable.set_cols_width([22,33,33,33,33])
				pTable.set_cols_align(['c','c','c','c','c'])
				pTable.set_cols_valign(['m','m','m','m','m'])
				aTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				aHeader = ['Connections', 'Latency', 'Requests']
				aTable.header(aHeader)
				aTable.set_cols_width([20,70,70])
				aTable.set_cols_align(['c','c','c'])
				aTable.set_cols_valign(['m','m','m'])
				pRow = ['Proxy',result.json()['data']['proxy']['metrics']['bandwidthIn']['desc'],result.json()['data']['proxy']['metrics']['bandwidthOut']['desc'],result.json()['data']['proxy']['metrics']['packetsIn']['desc'],result.json()['data']['proxy']['metrics']['packetsOut']['desc']]
				pTable.add_row(pRow)
				proxyTable = pTable.draw()
				print proxyTable
				aRow = [result.json()['data']['proxy']['metrics']['connections']['desc'],result.json()['data']['proxy']['metrics']['latency']['desc'],result.json()['data']['proxy']['metrics']['requests']['desc']]
				aTable.add_row(aRow)
				addTable = aTable.draw()
				print addTable
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				'''iTable = tt.Texttable()
				iHeader = ['Summary', 'Description']
				iTable.header(iHeader)
				iTable.set_cols_width([60,99])
				iTable.set_cols_align(['c','c'])
				iTable.set_cols_valign(['m','m'])
				iTable.add_row(iRow)
				infoTable = iTable.draw()
				#print item
				print bcolors.TURQUO+"\n	-----------------------------------------------------------------	Separator	-----------------------------------------------------------------\n"+bcolors.ENDC
				print bcolors.TURQUO+"\n	-----------------------------------------------------------------	Separator	-----------------------------------------------------------------\n"+bcolors.ENDC
				soup = BeautifulSoup(item['description'], 'html.parser')
				iRow = [item['summary'],soup.get_text()]
				print infoTable'''
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Code: "+bcolors.FAIL+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status: "+bcolors.FAIL+str(result.json()['status'])+bcolors.ENDC
			print bcolors.TURQUO+"[ERROR]"+bcolors.WARNING+" Status Message: "+bcolors.FAIL+str(result.json()['statusMsg'])+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you to use the PLX Analytics\n"+bcolors.ENDC
		print bcolors.WARNING+"PLX Analytics Retrieve Information:\n"+bcolors.ENDC
		print "events 		- List all events occurring in the last 90 days"
		print "critical 	- List critical events that have started in the last 90 days"
		print "metrics 	- List metric types"
		print "attacks 	- List attack events per contract, limited to last 90 days"
		print bcolors.WARNING+"\nAvailable Options:\n"+bcolors.ENDC
		print "-N 		- This option is used to specify a Zone Name"
		print "--contract 	- Provide a contract ID"
		print "--attack 	- Provide an Attack ID"
		print "--start 	- Provide a start time (in EPOCH) for the attack reports"
		print "--end 	- Provide an end time (in EPOCH) for the attack reports"
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def fastDNS(AccountSwitch,propertyName,creds,respjson,apiObject,type,host,contractId,groupId,zonesDiff,propertyVersion):
	if not respjson:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if AccountSwitch:
		filename = '.map'
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		for item in contents:
			if "[" and "]" in item:
				accountCheck = item[1:-2]
				if accountCheck == AccountSwitch:
					AccountSwitch = contents[contents.index(item)+1].strip()
					if not respjson:
						print bcolors.TURQUO+"[DNS]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
	#print AccountSwitch
	params = {'accountSwitchKey':AccountSwitch}
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if apiObject == 'zones':
		#print propertyName
		if propertyName:
			url = '/config-dns/v2/zones/'+propertyName
		else:
			url = '/config-dns/v2/zones'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				dnsTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				dnsHeader = ['Contract', 'Zone', 'Type','Last Modified Date','Last Modified By','Last Activation Date','State']
				dnsTable.header(dnsHeader)
				dnsTable.set_cols_width([12,35,12,22,30,22,15])
				dnsTable.set_cols_align(['c','c','c','c','c','c','c'])
				dnsTable.set_cols_valign(['m','m','m','m','m','m','m'])
				if propertyName:
					dnsRow = [result.json()['contractId'],result.json()['zone'],result.json()['type'],result.json()['lastModifiedDate'],result.json()['lastModifiedBy'],result.json()['lastActivationDate'],result.json()['activationState']]
					dnsTable.add_row(dnsRow)
				else:
					for item in result.json()['zones']:
						#print item
						dnsRow = [item['contractId'],item['zone'],item['type'],item['lastModifiedDate'],item['lastModifiedBy'],item['lastActivationDate'],item['activationState']]
						dnsTable.add_row(dnsRow)
				zoneTable = dnsTable.draw()
				print zoneTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'create':
		#print propertyName
		if propertyName:
			url = '/config-dns/v2/zones/'
		else:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide a Zone Name with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not type:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' What type of Zone are you creating: --type "primary" or "secondary"?'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if contractId:
			params.update({'contractId':contractId})
		if groupId:
			params.update({'gid':groupId})
		else:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide a contractId in order to proceed: --contract ctr_P-2KLGVXI'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if type == "secondary" and not host:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide Master Name Servers for to create a Secondary Zone: -t 1.1.1.1,2.2.2.2'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print url
		headers = {'Content-Type':'application/json'}
		body = {'zone':propertyName,'type':type}
		#print host
		if type == "secondary":
			if ',' in host:
				host = host.split(',')
			else:
				host = host.split('\n')
			body.update({'masters':host})
		print body
		createZone = {'zones':[body]}
		print createZone
		result = s.post(urljoin(baseurl, url),params=params,json=body,headers=headers)
		if result.status_code == 200 or result.status_code == 204 or result.status_code == 201:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' Zone has been created successfully.'+bcolors.ENDC
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'records':
		#print propertyName
		if propertyName:
			url = '/config-dns/v2/zones/'+propertyName+'/recordsets'
		else:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide a Zone Name with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print url
		if type:
			params.update({'types':type})
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				dnsTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				dnsHeader = ['Name', 'Type', 'TTL','Record Data']
				dnsTable.header(dnsHeader)
				dnsTable.set_cols_width([50,15,15,80])
				dnsTable.set_cols_align(['c','c','c','c'])
				dnsTable.set_cols_valign(['m','m','m','m'])
				for item in result.json()['recordsets']:
					#print item
					dnsRow = [item['name'],item['type'],item['ttl'],item['rdata']]
					dnsTable.add_row(dnsRow)
				zoneTable = dnsTable.draw()
				print zoneTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'types':
		#print propertyName
		if propertyName:
			params.update({'zone':propertyName})
		else:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide a Zone Name with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		url = '/config-dns/v2/data/recordset-types'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				dnsTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				dnsHeader = ['Record Type']
				dnsTable.header(dnsHeader)
				dnsTable.set_cols_width([30])
				dnsTable.set_cols_align(['c'])
				dnsTable.set_cols_valign(['m'])
				for item in result.json()['types']:
					#print item
					dnsRow = [item]
					dnsTable.add_row(dnsRow)
				zoneTable = dnsTable.draw()
				print zoneTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'contracts':
		#print propertyName
		if propertyName:
			url = '/config-dns/v2/zones/'+propertyName+'/contract'
		else:
			url = '/config-dns/v2/data/contracts'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				ctrTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				ctrHeader = ['Contract ID', 'Contract Name', 'Contract Type','Features','Permissions','Zone Count','Maximum Zones']
				ctrTable.header(ctrHeader)
				ctrTable.set_cols_width([15,25,20,40,30,12,12])
				ctrTable.set_cols_align(['c','c','c','c','c','c','c'])
				ctrTable.set_cols_valign(['m','m','m','m','m','m','m'])
				if propertyName:
					ctrRow = [result.json()['contractId'],result.json()['contractName'],result.json()['contractTypeName'],result.json()['features'],result.json()['permissions'],result.json()['zoneCount'],result.json()['maximumZones']]
					ctrTable.add_row(ctrRow)
					contractTable = ctrTable.draw()
					print contractTable
				else:
					for item in result.json()['contracts']:
						ctrRow = [item['contractId'],item['contractName'],item['contractTypeName'],item['features'],item['permissions'],item['zoneCount'],item['maximumZones']]
						ctrTable.add_row(ctrRow)
					contractTable = ctrTable.draw()
					print contractTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'download':
		#print propertyName
		headers = {'Accept':'text/dns','Context-Type':'text/dns'}
		if propertyName:
			if propertyVersion:
				url = '/config-dns/v2/zones/'+propertyName+'/versions/'+propertyVersion+'/zone-file'
			else:
				url = '/config-dns/v2/zones/'+propertyName+'/zone-file'
		else:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide a Zone Name with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print url
		result = s.get(urljoin(baseurl, url),params=params,headers=headers)
		if result.status_code == 200:
			print result.content
			filename = "files/"+propertyName+".txt"
			f = open(filename,"w+")
			f.write(result.content)
			f.close()
			print bcolors.TURQUO+"-----------------------------------------------------------------"+bcolors.ENDC
			print bcolors.WARNING+"JSON File has been created:",filename+bcolors.ENDC
			print bcolors.TURQUO+"-----------------------------------------------------------------"+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'versions':
		#print propertyName
		if propertyName:
			url = '/config-dns/v2/zones/'+propertyName+'/versions'
		else:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide a Zone Name with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				vTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				vHeader = ['Version ID', 'Type','Last Modified Date','Last Modified By','Last Activation Date','State']
				vTable.header(vHeader)
				vTable.set_cols_width([47,12,22,30,22,15])
				vTable.set_cols_align(['c','c','c','c','c','c'])
				vTable.set_cols_valign(['m','m','m','m','m','m'])
				for item in result.json()['versions']:
					#print item
					vRow = [item['versionId'],item['type'],item['lastModifiedDate'],item['lastModifiedBy'],item['lastActivationDate'],item['activationState']]
					vTable.add_row(vRow)
				versionsTable = vTable.draw()
				print versionsTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'groups':
		url = '/config-dns/v2/data/groups'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				gTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				gHeader = ['Contract', 'Group ID', 'Group Name','Permissions']
				gTable.header(gHeader)
				gTable.set_cols_width([15,15,50,60])
				gTable.set_cols_align(['c','c','c','c'])
				gTable.set_cols_valign(['m','m','m','m'])
				for item in result.json()['groups']:
					#print item
					gRow = [item['contractIds'],item['groupId'],item['groupName'],item['permissions']]
					gTable.add_row(gRow)
				groupTable = gTable.draw()
				print groupTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'edgehostnames':
		url = '/config-dns/v2/data/edgehostnames'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				eTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				eHeader = ['Edge Hostname', 'Zone APEX Support']
				eTable.header(eHeader)
				eTable.set_cols_width([120,30])
				eTable.set_cols_align(['c','c'])
				eTable.set_cols_valign(['m','m'])
				for item in result.json()['edgeHostnames']:
					#print item
					eRow = [item['edgeHostname'],str(item['supportsZoneApexMapping'])]
					eTable.add_row(eRow)
				edgeTable = eTable.draw()
				print edgeTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'authorities':
		url = '/config-dns/v2/data/authorities'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				aTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				aHeader = ['Contract', 'Authoritative Name Servers']
				aTable.header(aHeader)
				aTable.set_cols_width([20,40])
				aTable.set_cols_align(['c','c'])
				aTable.set_cols_valign(['m','m'])
				for item in result.json()['contracts']:
					#print item
					for nserver in item['authorities']:
						aRow = [item['contractId'],nserver]
						aTable.add_row(aRow)
				authoritativeTable = aTable.draw()
				print authoritativeTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'algorithms':
		url = '/config-dns/v2/data/dns-sec-algorithms'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				aTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				aHeader = ['Algorithms']
				aTable.header(aHeader)
				aTable.set_cols_width([60])
				aTable.set_cols_align(['c'])
				aTable.set_cols_valign(['m'])
				for item in result.json()['algorithms']:
					#print item
					aRow = [item]
					aTable.add_row(aRow)
					algorithmTable = aTable.draw()
				print algorithmTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'tsig':
		url = '/config-dns/v2/data/tsig-algorithms'
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				aTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				aHeader = ['Algorithms']
				aTable.header(aHeader)
				aTable.set_cols_width([60])
				aTable.set_cols_align(['c'])
				aTable.set_cols_valign(['m'])
				for item in result.json()['algorithms']:
					#print item
					aRow = [item]
					aTable.add_row(aRow)
					algorithmTable = aTable.draw()
				print algorithmTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif apiObject == 'diff':
		if propertyName:
			url = '/config-dns/v2/zones/'+propertyName+'/versions/diff'
		else:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide a Zone Name with the -N option.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if zonesDiff:
			params.update({'from':zonesDiff[0],'to':zonesDiff[1]})
		else:
			print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' You need to provide the Zone versions to compare: --zones versionID1 versionID2.'+bcolors.ENDC
			print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				sdTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				sdHeader = ['Field Name','Operation','From Value','To Value']
				sdTable.header(sdHeader)
				sdTable.set_cols_width([40,40,40,42])
				sdTable.set_cols_align(['c','c','c','c'])
				sdTable.set_cols_valign(['m','m','m','m'])
				for item in result.json()['diffs']['settingsDiffs']:
					#print item
					sdRow = [item['fieldName'],item['operation'],item['fromValue'],item['toValue']]
					sdTable.add_row(sdRow)
				settingdiffTable = sdTable.draw()
				rdTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				rdHeader = ['Name','Type','Operation','From Value', 'To Value']
				rdTable.header(rdHeader)
				rdTable.set_cols_width([45,10,10,47,47])
				rdTable.set_cols_align(['c','c','c','c','c'])
				rdTable.set_cols_valign(['m','m','m','m','m'])
				for item in result.json()['diffs']['recordSetDiffs']:
					#print item
					try:
						fromValue = 'TTL: '+str(item['fromValue']['ttl'])+'\nRDATA:'+'\n'.join(item['fromValue']['rdata'])
					except:
						fromValue = 'None'
					try:
						toValue = 'TTL: '+str(item['toValue']['ttl'])+'\nRDATA:'+'\n'.join(item['toValue']['rdata'])
					except:
						toValue = 'None'
					rdRow = [item['name'],item['type'],item['operation'],fromValue,toValue]
					rdTable.add_row(rdRow)
				recordiffTable = rdTable.draw()
				print bcolors.TURQUO+'[DNS]'+bcolors.WARNING+' Settings Diff Table'+bcolors.ENDC
				print settingdiffTable
				print bcolors.TURQUO+'\n[DNS]'+bcolors.WARNING+' Records Diff Table'+bcolors.ENDC
				print recordiffTable
		else:
			errorHandling(respjson,result.json())
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you to use the Fast DNS API to view/modify/activate your Zone File Changes\n"+bcolors.ENDC
		print bcolors.WARNING+"Fast DNS Retrieve Information:\n"+bcolors.ENDC
		print "zones 		- List Fast DNS Zones"
		print "records 	- List Record Set for a specific Zone"
		print "authorities 	- List currently assigned Akamai Authoritative Nameservers"
		print "versions 	- List current and prior versions of a specific Zone"
		print "download 	- Downloads Master Zone File"
		print "contracts 	- List all contracts or for a specific Zone"
		print "groups 		- List all groups accessible to current user"
		print "edgehostnames 	- List edge hostnames that have been configured"
		print "types 		- List record types that can be added to requested Zone"
		print "algorithms 	- Retrieves a list of DNSSEC algorithms names"
		print "tsig 		- Retrieves a list of TSIG algorithms names"
		print "diff 		- Displays differences between any two versions of a zone"
		print bcolors.WARNING+"\nFast DNS Actions:\n"+bcolors.ENDC
		print bcolors.WARNING+"\nAvailable Options:\n"+bcolors.ENDC
		print "-N 		- This option is used to specify a Zone Name"
		print "--type 		- Use this option to filter records by its type"
		print "--zones 	- Use this option to perform a diff between two versions"
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()


def APPSEC_MAIN(generate,prefix,bypass,defaultFile,negativePath,negativeFile,path,automation,AccountSwitch,host,retrieveobj,propertyName,propertyVersion,emails,notes,cdn,PRd,cemails,cloneFrom,copyHostnames,ipVersion,creds,policyId,configId,ruleId,respjson,appsec_actions,seq,noactivate,noversion,rateControls,wafrules,customRules,exceptions): # 'groups', 'contracts', 'cpcode', 'properties','version'
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if retrieveobj != 'audit' and retrieveobj != 'ruleaudit':
		if AccountSwitch:
			filename = '.map'
			readfile = open(filename, 'r')
			contents = readfile.readlines()
			for item in contents:
				if "[" and "]" in item:
					accountCheck = item[1:-2]
					if accountCheck == AccountSwitch:
						AccountSwitch = contents[contents.index(item)+1].strip()
						if not respjson and not automation and retrieveobj != 'Integration':
							print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+bcolors.ENDC+contents[contents.index(item)+1].strip()
		#print AccountSwitch
		params = {'accountSwitchKey':AccountSwitch}
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	def newVersionAppsec(configId,propertyVersion):
		headers = {"Content-Type":"application/json"}
		data_json = {"createFromVersion": propertyVersion,"ruleUpdate": False}
		result = s.post(urljoin(baseurl, '/appsec/v1/configs/'+configId+'/versions'),headers=headers,json=data_json,params=params)
		if result.status_code == 200 or result.status_code == 201:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" New version has been created successfully: "+str(result.json()["version"])+bcolors.ENDC
			if retrieveobj == "Integration":
				return result.json()["version"]
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Based On: "+str(result.json()["basedOn"])+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def appsecActivation(configId,notes,propertyVersion,emails,cdn):
		headers = {"Content-Type":"application/json"}
		activationConfigs = [{"configId":configId,"configVersion":propertyVersion}]
		data_json = {"action":"ACTIVATE","network":cdn, "note": notes,"notificationEmails":emails,"activationConfigs":activationConfigs}
		#print data_json
		result = s.post(urljoin(baseurl, '/appsec/v1/activations'),headers=headers,json=data_json,params=params)
		if result.status_code == 200 or result.status_code == 201:
			if respjson:
				print result.content
				sys.exit()
			if cdn == "STAGING":
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Staging - Activation successful. ID: "+str(str(result.json()["activationId"]))+bcolors.ENDC
			else:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Production - Activation successful. ID: "+str(str(result.json()["activationId"]))+bcolors.ENDC
			if retrieveobj == "Integration" and cdn == "PRODUCTION":
				print bcolors.ENDC+bcolors.TURQUO+"\t\t--Integration Complete--"+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if retrieveobj == "Integration":
				return
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def SecClone(configId,propertyVersion,policyId,cloneFrom,respjson,prefix):
		jsonBody = {'createFromSecurityPolicy':cloneFrom,'ruleUpdate':False,'policyName':policyId,'policyPrefix':prefix}
		headers = {'Content-Type':'application/json'}
		url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/security-policies'
		#print url
		#print jsonBody
		#print headers
		result = s.post(urljoin(baseurl, url),params=params, headers=headers,json=jsonBody)
		if result.status_code == 201:
			if retrieveobj == "Integration":
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" Policy Clone operation successful "+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" New Policy Name: "+bcolors.ENDC+result.json()['policyName']+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" New Policy ID: "+bcolors.ENDC+result.json()['policyId']+bcolors.ENDC
				return result.json()['policyId']
			elif respjson:
				print result.content
				sys.exit()
			else:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" Policy Clone operation successful "+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" New Policy Name: "+bcolors.ENDC+result.json()['policyName']+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" New Policy ID: "+bcolors.ENDC+result.json()['policyId']+bcolors.ENDC
		else:
			if respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print result.content
		#print result.json()
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def AppsecExport(configName,propertyVersion,exportjson,respjson):
		#orderedExportjson = json.load(exportjson, object_pairs_hook=OrderedDict)
		filename = "files/"+configName+"-V"+propertyVersion+".json"
		f = open(filename,"w+")
		with f as outfile:
			json.dump(exportjson, outfile, indent=4)
		f.close()
		if respjson != True and retrieveobj != 'peerReview':
			print bcolors.WARNING+"JSON File has been created:",filename+bcolors.ENDC
			print bcolors.TURQUO+"-----------------------------------------------------------------"+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		if retrieveobj == 'peerReview':
			return
		sys.exit()
	def findConfigID(propertyName):
		#print propertyName
		url = '/appsec/v1/configs'
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			for item in result.json()["configurations"]:
				#print item
				try:
					item["name"]
					if propertyName == str(item["name"]):
						foundId = item["id"]
						#print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" Configuration ID: "+str(foundId)+bcolors.ENDC
						break
					else:
						pass
				except:
					if propertyName == "WAF Security File":
						foundId = item["id"]
						break
			try:
				foundId
			except:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Security Configuration was found with that name. Are you sure it's called like that?"+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			return str(foundId)
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Unable to retrieve Security Configurations. The following error message occured: "+bcolors.ENDC
			#print result.content
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	def findAppsecVersion(configId,respjson):
		url = '/appsec/v1/configs/'+configId+'/versions'
		result = s.get(urljoin(baseurl, url),params=params)
		Version = {}
		#print respjson
		if result.status_code == 200:
			if respjson and retrieveobj == "versions":
				#print result.content
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			try:
				result.json()["productionActiveVersion"]
				Version.update({"Production":result.json()["productionActiveVersion"]})
			except:
				Version.update({"Production":None})
			try:
				result.json()["stagingActiveVersion"]
				Version.update({"Staging":result.json()["stagingActiveVersion"]})
			except:
				Version.update({"Staging":None})
			Version.update({"Latest":result.json()["lastCreatedVersion"]})
		else:
			url = '/appsec/v1/configs'
			result = s.get(urljoin(baseurl, url),params=params)
			if result.status_code == 200:
				for item in result.json()["configurations"]:
					#print item
					Version.update({"Latest":item["latestVersion"]})
					try:
						item["productionVersion"]
						Version.update({"Production":result.json()["productionActiveVersion"]})
					except:
						Version.update({"Production":None})
					try:
						item["stagingVersion"]
						Version.update({"Staging":result.json()["stagingVersion"]})
					except:
						Version.update({"Staging":None})
			else:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No valid version was found. Following error occured: "+bcolors.ENDC
				#print result.content
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		return Version
	def grabBypassLists(configId,propertyVersion,policyId):
		bypass = None
		getNLs = s.get(urljoin(baseurl, "/appsec/v1/configs/"+configId+"/versions/"+str(propertyVersion)+"/match-targets"),params=params)
		#print getHosts.json()
		#print getHosts.status_code
		if getNLs.status_code == 200:
			for item in getNLs.json()["matchTargets"]["websiteTargets"]:
				if item["securityPolicy"]["policyId"] == policyId:
					bypass = item["bypassNetworkLists"]
					continue
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			#print result.content
			json_data = getNLs.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#print "Bypass: ",bypass
		return bypass
	def createMatchTarget(configId,newPropertyVersion,policyId,configHostnames,configPaths,bypass,defaultFile,negativePath,negativeFile):
		headers = {"Content-Type": "application/json"}
		securityPolicy = {"policyId":policyId}
		createMatchJSON = {"hostnames":configHostnames,"bypassNetworkLists":bypass,"securityPolicy":securityPolicy,"defaultFile":defaultFile,"filePaths":configPaths,"type":"website","isNegativePathMatch":negativePath,"isNegativeFileExtensionMatch":negativeFile}
		#print createMatchJSON
		createTarget = s.post(urljoin(baseurl, "/appsec/v1/configs/"+configId+"/versions/"+str(newPropertyVersion)+"/match-targets"), headers=headers,json=createMatchJSON,params=params)
		if createTarget.status_code == 200 or createTarget.status_code == 201:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Match Target created successfully."+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" New Match Target ID: "+bcolors.ENDC+str(createTarget.json()['targetId'])+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" New Match Target Sequence #"+str(createTarget.json()['sequence'])+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" StatusCode: "+str(createTarget.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			#print result.content
			json_data = createTarget.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		return
		#print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		#sys.exit()
	def addMatchTargets(configId,propertyVersion,configHostnames,seq,configPaths):
		HostHeader = {"Content-Type": "application/json"}
		getHosts = s.get(urljoin(baseurl, "/appsec/v1/configs/"+configId+"/versions/"+str(propertyVersion)+"/match-targets"),params=params)
		#print getHosts.json()
		#print getHosts.status_code
		if getHosts.status_code == 200:
			for item in getHosts.json()["matchTargets"]["websiteTargets"]:
				if item["sequence"] == seq:
					currentHosts = item["hostnames"]
					currentPaths = item["filePaths"]
					matchJSON = item
					continue
			if retrieveobj == "add" or retrieveobj == "Integration":
				#print configHostnames
				for item in configHostnames:
					currentHosts.append(item)
				try:
					configPaths
					for item in configPaths:
						currentPaths.append(item)
					matchJSON.update({"filePaths":currentPaths})
				except:
					pass
			else:
				#print configHostnames
				for rmhost in configHostnames:
					for item in currentHosts:
						if item == rmhost:
							currentHosts.remove(item)
			#print currentHosts
			#print currentPaths
			#print matchJSON
			matchJSON.update({"hostnames":currentHosts})
			#print matchJSON
			#print hostnamejson
			putHosts = s.put(urljoin(baseurl, "/appsec/v1/configs/"+configId+"/versions/"+str(propertyVersion)+"/match-targets/"+str(matchJSON["targetId"])), headers=HostHeader,json=matchJSON,params=params)
			if putHosts.status_code == 200:
				if retrieveobj == "Integration":
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Hostnames added successfully to Match Target."+bcolors.ENDC
					return
				if retrieveobj == "add":
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Hostnames added successfully to Match Target."+bcolors.ENDC
				else:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Hostnames removed successfully from Match Target."+bcolors.ENDC
			else:
				json_data = putHosts.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			#print result.content
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def NewCustom(configId,ruleId):
		#print filename
		try:
			with open(ruleId) as json_data:
				rulesJson = json.load(json_data)
			#print(d)
			#rulesJson = open(filename, 'r').readlines()
		except:
			print bcolors.WARNING+"File NOT found:\n"+ruleId+"\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print rulesJson
		url = '/appsec/v1/configs/'+configId+'/custom-rules'
		result = s.post(urljoin(baseurl, url), json=rulesJson,params=params)
		if result.status_code == 200:
			if respjson:
				print result.content
				sys.exit()
			CustomRuleTable = tt.Texttable()
			CustomRuleheader = ['Name','Rule ID','Tag','Description']
			CustomRuleTable.header(CustomRuleheader)
			CustomRuleTable.set_cols_width([30,10,40,50])
			CustomRuleTable.set_cols_align(['c','c','c','c'])
			CustomRuleTable.set_cols_valign(['m','m','m','m'])
			#print result.json()
			#for item in result.json():
			#	print item
				#HostnameTable.set_deco(tt.Texttable.HEADER)
			try:
				result.json()["description"]
				description = result.json()["description"]
			except:
				description = None
			Customrow = [result.json()["name"],result.json()['id'],result.json()["tag"],description]
			CustomRuleTable.add_row(Customrow)
			CustomTable = CustomRuleTable.draw()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" New Rule has been created:"+bcolors.ENDC
			print CustomTable
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" Conditions:"+bcolors.ENDC
			ConditionTable = tt.Texttable()
			Conditionheader = ['Type', 'Name','Positive Match','Value Wildcard','Value Case', 'Value']
			ConditionTable.header(Conditionheader)
			ConditionTable.set_cols_width([28,15,15,15,10,50])
			ConditionTable.set_cols_align(['c','c','c','c','c','c'])
			ConditionTable.set_cols_valign(['m','m','m','m','m','m'])
			for item in result.json()['conditions']:
				try:
					item['value']
					value = item['value']
				except:
					value = None
				try:
					item["name"]
					name = item["name"]
				except:
					name = None
				try:
					item["valueWildcard"]
					valueWildcard = str(item["valueWildcard"])
				except:
					valueWildcard = None
				try:
					item["valueCase"]
					valueCase = str(item["valueCase"])
				except:
					valueCase = None
				Customrow = [item["type"],name,str(item['positiveMatch']),valueWildcard,valueCase,value]
				ConditionTable.add_row(Customrow)
			CondTable = ConditionTable.draw()
			print CondTable
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			sys.exit()
	def AddCustom(configId,propertyVersion,ruleId,policyId,appsec_actions):
		headers = {"Content-Type":"application/json"}
		body = {"action":appsec_actions}
		url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/security-policies/'+policyId+'/custom-rules/'+ruleId
		#print url
		#print body
		#print headers
		result = s.put(urljoin(baseurl, url), headers=headers,json=body,params=params)
		if result.status_code == 200:
			if respjson:
				#print result.content
				print result.content
				sys.exit()
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			#print colorful_json
			#print result.content
			if appsec_actions == 'alert':
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Custom Rule Successfully added in Alert Mode: "+ruleId+bcolors.ENDC
			elif appsec_actions == 'none':
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Custom Rule disabled from policy: "+ruleId+bcolors.ENDC
			else:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Custom Rule Successfully added in Deny Mode: "+ruleId+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	def DeleteCustom(configId,ruleId):
		url = '/appsec/v1/configs/'+configId+'/custom-rules/'+ruleId
		result = s.delete(urljoin(baseurl, url),params=params)
		if result.status_code == 204:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Rule removed successfully. "+bcolors.ENDC
		else:
			json_data = result.json()
			print result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def actionMenu():
		if retrieveobj == 'activate':
			print bcolors.UNDERLINE+bcolors.WARNING+"""Available Options"""+bcolors.ENDC+"""

-N 		- Configuration Name
-V 		- Configuration Version
--notes 	- Activation Notes
--emails 	- Activation emails (comma-delimited)
--cdn 		- Akamai Platform (default: staging)

"""+bcolors.UNDERLINE+bcolors.WARNING+"""Examples:"""+bcolors.ENDC+"""

Staging
python swapi.py appsec activate -N asomarri -V7 --notes "Testing API" --emails asomarri@akamai.com

Production
python swapi.py appsec activate -N asomarri -V7 --notes "Testing API" --emails asomarri@akamai.com --cdn prod"""
		elif retrieveobj == 'newVersion':
			print bcolors.UNDERLINE+bcolors.WARNING+"""Available Options"""+bcolors.ENDC+"""

-N 		- Configuration Name
--configId 	- Configuration ID
-V 		- Configuration Version

"""+bcolors.UNDERLINE+bcolors.WARNING+"""Example:"""+bcolors.ENDC+"""

python swapi.py appsec newVersion -N gHost -V10"""
		elif retrieveobj == 'Integration':
			print bcolors.UNDERLINE+bcolors.WARNING+"""Available Options"""+bcolors.ENDC+"""

-N 		- Configuration Name
-V 		- Configuration Version
-t 		- Hostnames (comma delimited)"
--mtarget 	- Match Target Sequence Number"
--noactivate 	- Don't activate configuration
--noversion 	- Do not create a new version
--path 		- Add path(s) to Match Target (Comma delimited)

"""+bcolors.UNDERLINE+bcolors.WARNING+"""Examples:"""+bcolors.ENDC+"""

python swapi.py appsec Integration -N asomarri -V4 -t swapi.akamai.io --mtarget 3 --emails asomarri@akamai.com
python swapi.py appsec Integration -N asomarri -V4 -t www.techjam4.io,www.techjam.io2 --mtarget 1  --noactivate
python swapi.py appsec Integration -N asomarri -V4 -t www.techjam.io1,jira.konanow.io --mtarget 1  --emails asomarri@akamai.com --noversion
python swapi.py appsec Integration -N asomarri -V4 -t www.techjam.io1,jira.konanow.io --mtarget 1  --noactivate --noversion"""
		elif retrieveobj == 'add' or retrieveobj == 'remove' or retrieveobj == 'new':
			print bcolors.UNDERLINE+bcolors.WARNING+"""Available Options"""+bcolors.ENDC+"""

-N 		- Configuration Name
-V 		- Configuration Version
-t 		- Hostnames (comma delimited)"
--mtarget 	- Match Target Sequence Number"
--policyId 	- Define policy to add Custom Rule
--ruleId 	- Custom Rules"
--action 	- Set action (default: alert)

"""+bcolors.UNDERLINE+bcolors.WARNING+"""Examples:"""+bcolors.ENDC+"""

HOSTNAMES

Selected Hostnames
python swapi.py appsec add -t ghost4.akamai.io -N gHost
python swapi.py appsec remove -t ghost4.akamai.io -N gHost

Match Targets
python swapi.py appsec add -t ghost4.akamai.io -N gHost --mtarget 1
python swapi.py appsec remove -t ghost4.akamai.io -N gHost --mtarget 1

--------------------------------------------------------------------

CUSTOM RULES

Shared Resources - Create/Remove
python swapi.py appsec new  -N asomarri --ruleId files/NoPass.json
python swapi.py appsec remove  -N asomarri --ruleId 635309

Security Configuration Policy
python swapi.py appsec add -N asomarri --ruleId 635273 --policyId SuMe_60356
python swapi.py appsec add -N asomarri --ruleId 635273 --policyId SuMe_60356 --action deny
python swapi.py appsec remove -N asomarri --ruleId 635273 --policyId SuMe_60356"""
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def addHostsSec(configId,propertyVersion,configHostnames):
		HostHeader = {"Content-Type": "application/json"}
		availableHostnames = []
		notFound = []
		found = []
		selectable = s.get(urljoin(baseurl, "/appsec/v1/configs/"+configId+"/versions/"+str(propertyVersion)+"/selectable-hostnames"),params=params)
		#print selectable.json()
		if retrieveobj == "add" or retrieveobj == "Integration":
			try:
				selectable.json()["availableSet"]
				for item in selectable.json()["availableSet"]:
					#print item["hostname"]
					availableHostnames.append(item["hostname"])
				for providedHostname in configHostnames:
					if providedHostname in availableHostnames:
						found.append(providedHostname)
					else:
						notFound.append(providedHostname)
			except:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Hostnames found in Available Set."+bcolors.ENDC
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		#print availableHostnames
		#print found
		#print notFound
		#print configHostnames
		getHosts = s.get(urljoin(baseurl, "/appsec/v1/configs/"+configId+"/versions/"+str(propertyVersion)+"/selected-hostnames"),params=params)
		#print getHosts.json()
		#print getHosts.status_code
		if getHosts.status_code == 200:
			currentHosts = getHosts.json()["hostnameList"]
			if retrieveobj == "add" or retrieveobj == "Integration":
				for item in found:
					currentHosts.append({"hostname":item})
			else:
				for rmhost in configHostnames:
					for item in currentHosts:
						#print item["hostname"]
						if item["hostname"] == rmhost:
							currentHosts.remove(item)
			#print currentHosts
			hostnamejson = {"hostnameList":currentHosts}
			#print hostnamejson
			putHosts = s.put(urljoin(baseurl, "/appsec/v1/configs/"+configId+"/versions/"+str(propertyVersion)+"/selected-hostnames"), headers=HostHeader,json=hostnamejson,params=params)
			if putHosts.status_code == 200:
				if retrieveobj == "Integration":
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Hostnames added successfully to Selected Hostnames."+bcolors.ENDC
					if notFound:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" The following hostnames were not found in Available Hosts:"+bcolors.ENDC
						print bcolors.TURQUO+"[APPSEC] "+bcolors.ENDC+','.join(notFound)
					return
				elif retrieveobj == "add":
					if found:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Hostnames added successfully to Selected Hostnames."+bcolors.ENDC
					if notFound:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" The following hostnames were not found in Available Hosts: \n"+bcolors.ENDC
						print bcolors.TURQUO+"[APPSEC] "+bcolors.ENDC+','.join(notFound)
				else:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Hostnames removed successfully from Selected Hostnames."+bcolors.ENDC
			else:
				json_data = putHosts.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			#print result.content
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if retrieveobj == 'msc':
		result = s.get(urljoin(baseurl, '/appsec/v1/configs'),params=params)
		if result.status_code == 200:
			if automation:
				for item in result.json()['configurations']:
					print item["id"]
				sys.exit()
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['configurations']:
					#print item
					Hostnameheader = ['Name', 'Config ID', 'Production Hostnames', 'Latest', 'Production', 'Staging']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([25,10,66,10,10,10])
					HostnameTable.set_cols_align(['c','c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m','m'])
					try:
						item["productionHostnames"]
						hostnames = item["productionHostnames"]
					except:
						hostnames = None
					try:
						item["productionVersion"]
						production = item["productionVersion"]
					except:
						production = None
					try:
						item["stagingVersion"]
						staging = item["stagingVersion"]
					except:
						staging = None
					try:
						item["name"]
						name = item["name"]
					except:
						name = "WAF Security File"
					Hostnamerow = [name,item["id"],hostnames,item["latestVersion"],production,staging]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
				try:
					HostTable
					print HostTable
				except:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Multi Security Configuration was found."+bcolors.ENDC
		else:
			if automation or respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if retrieveobj == 'custom':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if policyId:
				#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Policy ID: --policyId SuMe_60356\n\n"+bcolors.ENDC
				#print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				#sys.exit()
			if not propertyVersion:
				Version = findAppsecVersion(configId,respjson)
				if Version["Production"] != None:
					propertyVersion = str(Version["Production"])
					if not respjson and not automation:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using active PROD version: "+propertyVersion+bcolors.ENDC
				else:
					propertyVersion = str(Version["Latest"])
					if not respjson and not automation:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
			url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/security-policies/'+policyId+'/custom-rules'
			result = s.get(urljoin(baseurl, url),params=params)
			if result.status_code == 200:
				if automation:
					for rule in result.json():
						print rule['ruleId']
					sys.exit()
				if respjson:
					json_data = result.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					#print colorful_json
					print result.content
					sys.exit()
				else:
					CustomRuleTable = tt.Texttable()
					CustomRuleheader = ['name','id','Action','Policy']
					CustomRuleTable.header(CustomRuleheader)
					CustomRuleTable.set_cols_width([50,10,10,15])
					CustomRuleTable.set_cols_align(['c','c','c','c'])
					CustomRuleTable.set_cols_valign(['m','m','m','m'])
					for item in result.json():
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						Customrow = [item["name"],item['ruleId'],item["action"],policyId]
						CustomRuleTable.add_row(Customrow)
					CustomTable = CustomRuleTable.draw()
					print CustomTable
					print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
			else:
				if automation or respjson:
					print result.content
					sys.exit()
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not ruleId:
			url = '/appsec/v1/configs/'+configId+'/custom-rules'
			result = s.get(urljoin(baseurl, url),params=params)
			#print result.status_code
			#print result.json()
			if result.status_code == 200:
				if automation:
					for rule in result.json()['customRules']:
						print rule['id']
					sys.exit()
				if respjson:
					json_data = result.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					#print colorful_json
					print result.content
					sys.exit()
				else:
					CustomRuleTable = tt.Texttable()
					CustomRuleheader = ['name','id','Status','Version', 'Link']
					CustomRuleTable.header(CustomRuleheader)
					CustomRuleTable.set_cols_width([50,20,20,10,50])
					CustomRuleTable.set_cols_align(['c','c','c','c','c'])
					CustomRuleTable.set_cols_valign(['m','m','m','m','m'])
					for item in result.json()['customRules']:
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						Customrow = [item["name"],item['id'],item["status"],item['version'],item['link']]
						CustomRuleTable.add_row(Customrow)
					CustomTable = CustomRuleTable.draw()
					print CustomTable
			else:
				if automation or respjson:
					print result.content
					sys.exit()
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
				print result.content
		else:
			url = '/appsec/v1/configs/'+configId+'/custom-rules/'+ruleId
			result = s.get(urljoin(baseurl, url),params=params)
			if result.status_code == 200:
				#print result.status_code
				#print result.content
				if respjson:
					json_data = result.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					#print colorful_json
					print result.content
					sys.exit()
				else:
					CustomRuleTable = tt.Texttable()
					CustomRuleheader = ['name','id','Rule Activated','Version', 'Tag']
					CustomRuleTable.header(CustomRuleheader)
					CustomRuleTable.set_cols_width([20,20,20,10,50])
					CustomRuleTable.set_cols_align(['c','c','c','c','c'])
					CustomRuleTable.set_cols_valign(['m','m','m','m','m'])
					try:
						result.json()['tag']
						tag = result.json()['tag']
					except:
						tag = None
					Customrow = [result.json()["name"],result.json()['id'],str(result.json()["ruleActivated"]),result.json()['version'],tag]
					CustomRuleTable.add_row(Customrow)
					CustomTable = CustomRuleTable.draw()
					print CustomTable
					print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+"Conditions:"+bcolors.ENDC
					ConditionTable = tt.Texttable()
					Conditionheader = ['Type', 'Name','Positive Match','Value Wildcard','Value Case', 'Value']
					ConditionTable.header(Conditionheader)
					ConditionTable.set_cols_width([28,15,15,15,10,50])
					ConditionTable.set_cols_align(['c','c','c','c','c','c'])
					ConditionTable.set_cols_valign(['m','m','m','m','m','m'])
					try:
						result.json()['conditions']
						for item in result.json()['conditions']:
							try:
								item['value']
								value = item['value']
							except:
								value = None
							try:
								item["name"]
								name = item["name"]
							except:
								name = None
							try:
								item["valueWildcard"]
								valueWildcard = str(item["valueWildcard"])
							except:
								valueWildcard = None
							try:
								item["valueCase"]
								valueCase = str(item["valueCase"])
							except:
								valueCase = None
							Customrow = [item["type"],name,str(item['positiveMatch']),valueWildcard,valueCase,value]
							ConditionTable.add_row(Customrow)
						CondTable = ConditionTable.draw()
						print CondTable
					except:
						print bcolors.WHITE+"SWaPI has no access to Advanced Metadata unless using the export feature. "+bcolors.ENDC
			else:
				if automation or respjson:
					print result.content
					sys.exit()
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC] "+bcolors.WARNING+result.json()['title']
				print bcolors.TURQUO+"[APPSEC] "+bcolors.WARNING+result.json()['detail']
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'add' or retrieveobj == 'remove' or retrieveobj == 'new' or retrieveobj == 'activate':
		if retrieveobj == 'activate':
			if propertyName:
				configId = findConfigID(propertyName)
			else:
				if not configId:
					actionMenu()
			if not notes:
				actionMenu()
			if not propertyVersion:
				actionMenu()
			if not emails:
				actionMenu()
			if "," in emails:
				emails = emails.split(",")
			else:
				emails = emails.split("\n")
			#print emails
			if cdn == 'staging':
				cdn = "STAGING"
			else:
				cdn = "PRODUCTION"
			appsecActivation(configId,notes,propertyVersion,emails,cdn)
		if host:
			if propertyName:
				configId = findConfigID(propertyName)
			else:
				if not configId:
					actionMenu()
			if not propertyVersion:
				Version = findAppsecVersion(configId,respjson)
				propertyVersion = str(Version["Latest"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
			if "," in host:
				configHostnames = host.split(",")
			else:
				configHostnames = host.split("\n")
			try:
				path
				if "," in path:
					configPaths = path.split(",")
				else:
					configPaths = path.split("\n")
			except:
				configPaths = None
			#print configHostnames
			if seq:
				addMatchTargets(configId,propertyVersion,configHostnames,seq,configPaths)
			addHostsSec(configId,propertyVersion,configHostnames)
		elif ruleId:
			if propertyName:
				configId = findConfigID(propertyName)
			else:
				if not configId:
					actionMenu()
			if not propertyVersion:
				Version = findAppsecVersion(configId,respjson)
				propertyVersion = str(Version["Latest"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
			if retrieveobj == 'new':
				NewCustom(configId,ruleId)
			elif retrieveobj == 'remove':
				if policyId:
					appsec_actions = 'none'
					AddCustom(configId,propertyVersion,ruleId,policyId,appsec_actions)
				else:
					DeleteCustom(configId,ruleId)
			elif retrieveobj == 'add':
				if policyId:
					AddCustom(configId,propertyVersion,ruleId,policyId,appsec_actions)
		else:
			actionMenu()
	elif retrieveobj == 'Integration':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				actionMenu()
		if not host:
			actionMenu()
		if not seq and not policyId and not cloneFrom:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Do you want to clone a policy and create a new match target or modify existing? Use: "+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" --from - Clone Policy"+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" --policyId - New Policy Name"+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" --mtarget - Use existing match target, index/sequence # of match target\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if prefix:
			if len(prefix) != 4:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Prefix must be 4 characters long: --prefix FGCS\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if cloneFrom:
			if not policyId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" What's the name of your new policy? Use: --policyId 'My New Policy'\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if policyId:
			if not cloneFrom:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Which policy do you want to clone? Use: --from inmp_3422\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyVersion:
			Version = findAppsecVersion(configId,respjson)
			if Version["Production"] != None:
				propertyVersion = Version["Production"]
			elif Version["Staging"] != None:
				propertyVersion = Version["Staging"]
			else:
				propertyVersion = Version["Latest"]
		if not noactivate:
			if not emails:
				actionMenu()
			if "," in emails:
				emails = emails.split(",")
			else:
				emails = emails.split("\n")
		#print emails
		print bcolors.TURQUO+"\t\t-- Integration Module --"+bcolors.ENDC
		print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+AccountSwitch+bcolors.ENDC
		#print propertyVersion
		if "," in host:
			configHostnames = host.split(",")
		else:
			configHostnames = host.split("\n")
		try:
			path
			defaultFile = 'NO_MATCH'
			if "," in path:
				configPaths = path.split(",")
			else:
				configPaths = path.split("\n")
		except:
			configPaths = None
		#print configHostnames
		if not noversion:
			newPropertyVersion = newVersionAppsec(configId,propertyVersion)
		else:
			newPropertyVersion = propertyVersion
		#print newPropertyVersion
		addHostsSec(configId,newPropertyVersion,configHostnames)
		if cloneFrom:
			bypass = grabBypassLists(configId,propertyVersion,cloneFrom)
			newPolicy = SecClone(configId,newPropertyVersion,policyId,cloneFrom,respjson,prefix)
		if seq:
			addMatchTargets(configId,newPropertyVersion,configHostnames,seq,configPaths)
		else:
			createMatchTarget(configId,newPropertyVersion,newPolicy,configHostnames,configPaths,bypass,defaultFile,negativePath,negativeFile)
		if not noactivate:
			if not notes:
				notes = "Onboarding hostnames: "+host
			initcdn = "STAGING"
			appsecActivation(configId,notes,newPropertyVersion,emails,initcdn)
			if cdn == 'prod':
				cdn = "PRODUCTION"
				appsecActivation(configId,notes,newPropertyVersion,emails,cdn)
		print bcolors.ENDC+bcolors.TURQUO+"\t\t--Integration Complete--"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'newVersion':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				actionMenu()
		if not propertyVersion:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a config version: -V 4\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		newVersionAppsec(configId,propertyVersion)
	elif retrieveobj == 'hostPR':
		if not propertyName:
			print bcolors.WARNING+"You need to specify a filename using the following option: -N onboardingHostnames.txt\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not seq:
			print bcolors.WARNING+"You need to specify a match target sequence number: --mtarget 1\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		# Parse hostname file
		filename = propertyName
		try:
			outputfile = open(filename, 'r')
		except IOError:
			print bcolors.WARNING+"Couldn't find that file. Ar you sure this file exists?"+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		filelines = open(filename, 'r').readlines()
		readfile = []
		initialreadfile = []
		#	readfile = open(filename, 'r').readlines()
		for i in range (0,len(filelines)):
			if filelines[i].rstrip():
				initialreadfile.insert(i,filelines[i].strip())
		if not configId:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration ID: --configId 18117\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print configId
		if not propertyVersion:
			Version = findAppsecVersion(configId,respjson)
			url = '/appsec/v1/export/configs/'+configId+'/versions/'+str(Version['Latest'])
		else:
			url = '/appsec/v1/export/configs/'+configId+'/versions/'+str(propertyVersion)
		#print initialreadfile
		#print Version
		#print url
		result = s.get(urljoin(baseurl, url),params=params)
		#print result.status_code
		hostPRTable = tt.Texttable()
		hostPRheader = ['Hostname', 'Selected', 'Match Target']
		hostPRTable.header(hostPRheader)
		hostPRTable.set_cols_width([70,20,20])
		hostPRTable.set_cols_align(['c','c','c'])
		hostPRTable.set_cols_valign(['m','m','m'])
		matchTargetFound = False
		if result.status_code == 200:
			selectedHosts = result.json()['selectedHosts']
			for targets in result.json()['matchTargets']['websiteTargets']:
				if targets['sequence'] == seq:
					matchTargetFound = True
					try:
						matchTargets = targets['hostnames']
					except:
						matchTargets = ['All']
				else:
					pass
			if matchTargetFound == False:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Match Target Sequence number was not found.\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			#print selectedHosts
			#print matchTargets
			for hostname in initialreadfile:
				selectedFound = False
				targetFound = False
				if hostname in selectedHosts:#propertyName.decode('utf-8').strip():
					selectedFound = True
				if matchTargets[0] == 'All':
					targetFound = True
				else:
					if hostname in matchTargets:#propertyName.decode('utf-8').strip():
						targetFound = True
				hostPRrow = [hostname,str(selectedFound),str(targetFound)]
				hostPRTable.add_row(hostPRrow)
			PeerReviewTable = hostPRTable.draw()
			print PeerReviewTable
		else:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'latest':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		#print configId
		Version = findAppsecVersion(configId,respjson)
		if respjson:
			print json.dumps(Version)
			sys.exit()
		print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Latest Version: "+str(Version["Latest"])+bcolors.ENDC
		print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Production: "+str(Version["Production"])+bcolors.ENDC
		print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Staging: "+str(Version["Staging"])+"\n\n"+bcolors.ENDC
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'versions':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyVersion:
			url = '/appsec/v1/configs/'+configId+'/versions'
		else:
			url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)
		result = s.get(urljoin(baseurl, url),params=params)
		#print "StatusCode: "+str(result.status_code)
		#print result.json()
		if result.status_code == 200:
			#pprint.pprint(result.json())
			if automation:
				if propertyVersion:
					print result.json()['version']
				else:
					for version in result.json()['versionList']:
						print version['version']
				sys.exit()
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print result.json()
				if not propertyVersion:
					print bcolors.WARNING+"\nVersion List:"+bcolors.ENDC
					VersionTable = tt.Texttable()
					Versionheader = ['Version','Production', 'Staging','Based On']
					VersionTable.header(Versionheader)
					VersionTable.set_cols_width([10,40,40,10])
					VersionTable.set_cols_align(['c','c','c','c'])
					VersionTable.set_cols_valign(['m','m','m','m'])
					HostnameTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					Hostnameheader = ['Name','Config ID', 'Active Production', 'Active Staging']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([20,10,20,20])
					HostnameTable.set_cols_align(['c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m'])
					try:
						result.json()["productionActiveVersion"]
						production = result.json()["productionActiveVersion"]
					except:
						production = None
					try:
						result.json()["stagingActiveVersion"]
						staging = result.json()["stagingActiveVersion"]
					except:
						staging = None
					Hostnamerow = [result.json()["configName"],result.json()["configId"],production,staging]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
					for item in result.json()["versionList"]:
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						#print item
						try:
							item["basedOn"]
							basedon = item["basedOn"]
						except:
							basedon = None
						try:
							item['production']['time']
							prodtime = item['production']['time']
						except:
							prodtime = "Never Activated"
						try:
							item['staging']['time']
							stagingtime = item['staging']['time']
						except:
							stagingtime = "Never Activated"
						Versionrow = [item['version'],item['production']['status']+'\nTime: '+prodtime,item['staging']['status']+'\nTime: '+stagingtime,basedon]
						VersionTable.add_row(Versionrow)
					VTable = VersionTable.draw()
				else:
					VersionTable = tt.Texttable()
					Versionheader = ['Config Name','Version','Production', 'Staging', 'Create Date', 'Created By' ,'Based On','Activation Notes']
					VersionTable.header(Versionheader)
					VersionTable.set_cols_width([20,8,25,25,20,25,8,40])
					VersionTable.set_cols_align(['c','c','c','c','c','c','c','c'])
					VersionTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
					try:
						result.json()["basedOn"]
						basedon = result.json()["basedOn"]
					except:
						basedon = None
					try:
						result.json()['production']['time']
						prodtime = result.json()['production']['time']
					except:
						prodtime = "Never Activated"
					try:
						result.json()['staging']['time']
						stagingtime = result.json()['staging']['time']
					except:
						stagingtime = "Never Activated"
					try:
						result.json()['versionNotes']
						notes = result.json()['versionNotes']
					except:
						notes = "No Activation Notes"
					Versionrow = [result.json()['configName'],result.json()['version'],result.json()['production']['status']+'\nTime: '+prodtime,result.json()['staging']['status']+'\nTime: '+stagingtime, result.json()['createDate'], result.json()['createdBy'],basedon,notes]
					VersionTable.add_row(Versionrow)
					VTable = VersionTable.draw()
				print VTable
				if not propertyVersion:
					print bcolors.WARNING+"\nActive Versions:"+bcolors.ENDC
					print HostTable
		else:
			if automation or respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		#parsed = json.loads(result.json())
		#print json.dumps(parsed, indent=4, sort_keys=True)
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'protected':
		try:
			result = s.get(urljoin(baseurl, '/papi/v1/groups/'),params=params)
			#print result.content
			if result.status_code == 200:
				print bcolors.TURQUO+"[APPSEC] "+bcolors.WARNING+"Account: "+result.json()['accountName']+bcolors.ENDC
				AcctName = result.json()['accountName']
		except:
			AcctName = AccountSwitch
		url = '/appsec/v1/configs'
		#print url
		resultMSC = s.get(urljoin(baseurl, url),params=params)
		#print resultMSC.content
		prodProtectedHostnames = []
		prodMSCs = []
		prodNames = []
		prodVersions = []
		allMSCHostnames = []
		allAvailableHostnames = []
		allNotProtected = []
		wildcards = []
		if resultMSC.status_code == 200:
			for item in resultMSC.json()['configurations']:
				#print item
				try:
					item['productionVersion']
					prodMSCs.append(item['id'])
					prodVersions.append(item['productionVersion'])
					prodNames.append(item['name'])
					for protected in item['productionHostnames']:
						if '*' in protected:
							wildcards.append(protected.replace('*',''))
						prodProtectedHostnames.append(protected)
				except:
					try:
						item['name']
					except:
						prodNames.append('WAF Security File')
		else:
			if automation or respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(resultMSC.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = resultMSC.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
			#parsed = json.loads(result.json())
			#print json.dumps(parsed, indent=4, sort_keys=True)
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print wildcards
		#print len(wildcards)
		for i in range(0,len(prodMSCs)):
			url = '/appsec/v1/export/configs/'+str(prodMSCs[i])+'/versions/'+str(prodVersions[i])
			resultExport = s.get(urljoin(baseurl, url),params=params)
			if resultExport.status_code == 200:
				#print resultExport.json()
				try:
					resultExport.json()['selectableHosts']
					for selectable in resultExport.json()['selectableHosts']:
						if not selectable in allAvailableHostnames:
							allAvailableHostnames.append(selectable)
					file = 'files/'+str(prodNames[i])+' V'+str(prodVersions[i])+'.html'
					#print file
					html_output = """<!DOCTYPE html>
	<html>
	<head>
	<title>
		SWaPI - Protected Hosts Report
	</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	<style type="text/css">
	body, html {
		margin: 0;
		font: 400 15px/1.8 "Lato", sans-serif;
		color: #777;
		background-color:#EAECEE;
		}
		#Division
		{
			margin-top:30px;
			width:100%;
			padding:20px;
			border-radius:10px;
			border:10px solid #EE872A;
		}
		h1
		{
			color: #EE872A;
			font-family: verdana;
			font-size: 300%;
			text-align:center;
		}
		h3
		{
			color: #2E86C1;
			font-family: verdana;
			font-size: 18px;
			text-align:center;
		}
		table, th, td
		{
			border: 1px solid black;
			padding: 5px;
			text-align: left;
		}
		}
		#p01
		{
			color: black;
		}
		#td01
		{
			color: black;
			font-family: verdana;
			font-size: 20px;
			text-align:center;
		}
		.caption {
			position: absolute;
			left: 0;
			top: 50%;
			width: 100%;
			text-align: center;
			color: #000;
		}

		.caption span.border {
			background-color: #111;
			color: #fff;
			padding: 18px;
			font-size: 25px;
			letter-spacing: 10px;
		}
		.bargraph {
			list-style: none;
			padding-top: 20px;
			width:97%;
		}
		ul.bargraph li {
			height: 35px;
			color: white;
			text-align: left;
			font-style: italic;
			font-weight:bolder;
			font-size: 14px;
			line-height: 35px;
			padding: 0px 20px;
			margin-bottom: 5px;
		}
		ul.bargraph li.green {
			background: #27AE60;
		}

		ul.bargraph li.warning {
			background: #F1C40F;
		}

		ul.bargraph li.orange {
			background: #F39C12;
		}

		ul.bargraph li.brown {
			background: #E67E22;
		}

		ul.bargraph li.fail {
			background: #C0392B;
		}
	</style>
	</head>
	<body>
	<div class="w3-bar w3-black">
		<a href="https://ac.akamai.com/" target="_blank" class="w3-bar-item w3-button">Aloha</a>
		<a href="https://git.source.akamai.com/projects/GSS/repos/swapi/browse" target="_blank" class="w3-bar-item w3-button">GIT</a>
		<a href="https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/08/swapi-devops-takeover" target="_blank" class="w3-bar-item w3-button">Blog</a>
		<a href="https://community.akamai.com/" target="_blank" class="w3-bar-item w3-button">Community</a>
		<span class="w3-bar-item">SWaPI</span>
	</div>
	<div style='position:relative; border:1px solid #EAECEE; margin-top:5px;'>
		<img style='position:absolute; top:0; right:25px;' width='100px' height='40px' alt='' src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfwAAAEHCAYAAABLB/TJAAAACXBIWXMAABcSAAAXEgFnn9JSAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAHXpJREFUeNrs3T9yG8e2x/G2y+kt4aVOOApvRLwVEFoB4RUQCm4sqOrmgvNXZTh2QHAFF1qBwBVcMHJoMLnpI+otQG+OeEaGKQAz092n59/3U4WibFEYYP79+vT09Hz3+fNnBwAA+u17VgEAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAAACHwAAEPgAAIDABwCAwAcAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAAACHwAAEPgAABD4AACAwAcAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAAACHwAAAh8AABD4AACAwAcAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAAACHwAAAh8AABD4AACAwAcAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAEDgAwAAAh8AABD4AACAwAcAAAQ+AAAg8AEAAIEPAAAIfAAACHwAANB3P7AKhuPH337P8h+HLzF58WtXL/77IX9t89fiP//4+461CAAEPtoV7hLkY31lR4K8qkt9ZUcaBwAAAh+JA36qgTwOCPdztqxlACDwkT7gpeIuQv7aaDGP+Wstr//84+8b1joAEPhIG/Iz99zNbhnyqzzkqeoBgMBHwqCfadBbVfJ7DfklIQ8ABD7Shvwo/zHXav7CsJpfuOcu+yfWOgAQ+EgX9JmG8I3hYu7d8212G9Y4ABD46F/Q37nna/MEPQAQ+KCiBwAQ+IgV9MU1+g+Gi5FZ8uYEPQCAwG8m7GXE/dLZDcbba0W/ZG0DAAj89EGf5T9WzmYmvMKdVvVPRt9h4v6ci196KcYHf33ue90f/HmnL/mMchvglrsEAMDWd58/f2YtpAl76b5f5K9XRouQW+xmMbvvD+bjL35eGK6ifRH++Uu+w4ZGAAAQ+FT1BlX9i+l6J4aNk6oeDsJ/zd4EAAR+W8N+qmFvFZx7rerXAZ+xCPmZs5uuN9Z3Leb1J/wBgMBvTdjLgLl3xtXv1PcZ9doYkZC/7uDqfdSG1Mr3+wMAgY/QoJeBbBvjavkuD7qZ52eTfyfjCS56ssrlcsaC4AcAAj9l2MvAtrVxmL7Nw23lEfRzfb3q6eon+AGAwE8S9imu10/rjMIfSNAfC/45I/wBgMC3CPtZ/uPWcBES9pM6j65NMLlPmzHxEAAQ+NHDXqrnXwwX8aBh/1Tx82TO/jbArrjXan/LqgAwdN+zCoLCftWysF/kP/4g7L+S9bDRRhkAUOHDO+wtn3BXOeyp6iv56J7nLODaPgAqfHQy7OVa/ZawL3Wt1f6YVQGACh9Vwn7mbAfo1Ql768l9+qj2AEgAIPAJe4swysrCXm+3W1PVB6k9nwEAdBld+tXDfuLS3HpXFvaZe57Jj7APc6sNOACgwsfXkB1ryFpOXvOmbFKdRJ8jJrk8cdiAkT8XXemZvl4aJ/5+VPoACHx87T6XkGp0utwWh/2j+/M59vJ6qjMbYMl3nugf5edIGwMWDQJCHwCBT+D/LuFl+iz7sgfhtCzsvz6j3j0/p/6pgW1ShP9EX6GNAAbyASDwBx72i/zHB+PwPHvdviVhL/ewF8+if2rptpL1NNWXz5MKJfTHPHwHAIE/vLCXyvGT4SJKA6bhsJfGyLLNIX9mvWUa/LOa4f+Qf1fu0wdA4A8o7KXLeGcctGevGycaO3CsESKVfG8eM6vhP9fwr7I9f82/O1PxAiDwBxL4EnrXhov4mIfKtCTsN86va9o36KWaX/Z56lm9DW9RoRH1JtbAQwAg8NsbChLE/zIO16zkur1U/jcJvu4ggt4j+OXOgzHz7gMg8PsbBCm68n/Kg2R95jNYP253sEF/IviXJ7Y3XfsACPweB0DTXfkyYOzfxl9TRtzPGY3+l0aeVPvHnknwmvUEgMDv34l/4hoclZ9gkJ4sf3audyHy+szc8Zn0/qIt18p1+69erP/SORIAgMDvXuDvnO2I+J/z8FicWb7lk+9MngWvoT4+eEmjxXeSIrluvtNGz5efqRsD2uiS7XBDlQ+AwO9n2FtfN3/MQyNroHchalV/cH/7RF8p5ge410bAOlUD4MW1/ff5cpecKgAQ+N0P+0YH6hl25cvEOdPQ6lTHFcw06C8a3lzSgJHQN5/1T7+3LGeXL2fCqQJA1/3AKvgyKYtl2N+XVNhzgyC9c88D87wC8aCSt/hsIWQ7XetLHm8r33NlUfnLvPoa+hmHCAAqfKr7Kk5O4qLB+kfk5Xl3QeulBanmbzq2KeX6/4In3gHAad9T3ZtX9+eqz0Xk5b31CXsJen0q4KcOhr240Ip/p9ffAQBU+K2p7icu3kA9r8e76meQRsdVzzavVPzzVLcgAkAXDPkavnV1/5Couq8d9nopYdHRar5qxf+v/HvKCP8Zt9UBwLADf2b8/suSyjpGVe0T9nMN+zqNHRnxLwMAiwbMTl+F7bEBgjrobXTwv4r/Hh382fIBQbKOZfDdglvrAAzdILv09TrvreEiyu67X0Wqrv+7athr+K4qBOy9BvuXCXDqXibw3B7FaPjDSXxi3x0g32vKA3EAEPjDCvyNs71ufXJWvYgj899WHZVeUtVL9S7XujdteiTswSx+E33F6AnYa+hvOPQBEPj9D/tYgXvO6zNz5seYQrdS2OvARPm9lw8E+ugSTF4TebvJdylm+Zu6sPEXzJ4HgMAfQOBbzln/JUxLnoj3FBhWlR7oogG5OaiMZeT6UkN+14PtGDoDIA/GATAoQxy0NzV+/3PPup8Fhv1DjZDK3PNAO6nml33rxtaxBXKpYq7hP69Z+d/k/84R+gCo8PtZ3U+c8SNw8wAZnVm+NAaufd9bQpxBZ6XbeKaVf9UxGgzmAzAIQ5tpz7qaO1fdjwLC3hFKlSv/lT7s5rV7fqbAvuSfXJ3bbgBA4HfTpKnAd2GXEn5lZHnt4N9pd32Wv34uCf4rvVUSAAj8rtPrvNZPftsYBP6XB8Owq3oH/5PeIlkW/DeEPgACvx+sB+t9LOly9+3On9GVnyz4b3j4DgACn8D3ru51sKCPO7ryzYJfenzujvzKrfYGAQCB3zU6YO7SeDHngtkn8KUCnbOLmgV/cY3/jXuebfDQWvcZACDwO2Zi/P77kjnnfZa/oCs/SfDLlMJS0b93f3bzy1iPBWsHAIHfPdZdtJuSv687b/8jU78mD35Z35l7nqhIvKNrHwCBT4X/0snq3jM0qC6bCf0nnRb5J8clFQAEPhV+zQq/7rIfqz4FD2bBv9Zqn14WAL3R+7n09el4r4wXc+76fUZ1381qv2S7AgAV/sCq+8eSwXUTqnsAAIHf/cDflfx9ndu7CHsAAIHvKTN+/03J39e5/59rxgAAAr+lgR/rXvk77rsHABD4/qy79M/dkjep8T48ohUAQOAHeNWBz/iot4IBAEDg16W35JmK9HAbwh4AQOAHyDryOQl8AICpH1gFQfYx3oNH4AJAPf/3P6+loJu8KOzWf/vnH0yYReCbiLFjEfYAUD3oZSC23MJ87KFkH/K/f8x/LvLgX7G2hhX4XXja2XrgB+9CDtIEi3rITwDjFn6H9/nnYv4FoNqxNst/3Jb8mjze+jb/3Ul+bM1Ya3/q+zX8UQc+42bAB2+WKOzFpeF7TwL+Ld2PQLywP3ST/xuq/AEFftvJ9fvdgL//oiffw7vnIK9ANhwGQGnYS/Hm0xMmoT9lDRL4VPfNV/c3DSzT4j1953q45xAAKpkHHGdcMiPwW2HI3blNVPeZwXtO2P6AuVnAv73QgX4EPqug0UAf5Am/iere0Nhw/wAGT7vzLxpsmBP4KFfhYTg7qvvOhDOBD3T3uB2xGvsf+G14+tz+TINgcCf8hqt7i4P+yne/YIIQoDPncQK/A7Yt/gyPVPfdDny5z5fqHrAVqWHM8ebo0g9VpatpV/P/U903u71Svd+Gwweo7CHw33O8EfjBqtwmsmM1taK6b1sDgooDqC7k1rq7v/3zDy4LDCDw2xC2G1qcX7u/mx6Zn1HhA92j8+L7zFux72GhQeAfk2IWux9/+31CJdeZ6v4i1hvprUK+0/U+UnEAtcmMeXW79uf5sbZj1Q2jwi9aeE02OuTE/jjknUyr+6sIb9Wm9Uh3PpC2ypdz6aRipS/n/Tc8MW94gW99cq1y4t9Q3Qe7i7EeI864NQn4t0PfHwDv0M9fcuy9zV8fj/yK9AC8z18Zz6n41g8D+I67SNXlKVVu9ZId72aIO1jE6l4aDbNE24sKH2h38EvlvtJzjBzTI7ruCfwi8C1VqfSG3NKMUt3LwZwf2G36Xt4VPpUHELfqd0zOUwld+uGysl/QwYMPQ9u5Ilf3jQf1wfeSbe775K7B7QcAqPD7EvgXP/72+6jCvPlS1V0ObP+KVt0frMMPLfheg+rOPzKj4OjMOti+rLa61KNx8F2zg8b84XfaxrrD4mBZY12nTwf7x66JLmod4zKq2EjeuW97UHd0rRP4jZHqOg/kfUBFVjUAyk5qq/z1juq+0ereuTjX8JPcf5+vw3X+4zpgWQ/5yXdcc7tN9QQ/1terCPtC8cd7DQhZB2uf4MzfS44jn/Ew9zrY61jAzfQ7X1b8DI/6HVZ1GjN1l5X//r5YV77rq8LnKba3NG4uIr2v/HjUxkuxrXee77UNKJRe0/gYXoVftNAtB+5Nyk7k8qCcvOHx6CLeCz6w6r4N1XlZxROtws9PdPPAsN9X/Zx6iWKuYWTZML7SlwT2bb5cufNiUXMb+6773ZEG6cLzvHCh3+Emfx9pxMzOfYeAZb3SfUBey/x9lvlygo4rHeA20+1teS660Jd89l90PS08ent8w35P2H9rKFPrbozfv2qIrCKFRtur+6lRdd+W7nDv71blQSBaef0S2iipUhHmy1roen1nHPbHSGhu888wqxFWviG1Ld5Dewk+RdpHr/Q7ZMc+r/bSxFiWbJsPUvHqevA9Lre6b100cMx8kkZLjc9r3rAm8Ptb4VuqumOuBrK+lxHe45vqPlKXZhbYmAnpIbiv8P5yMl8Hfse3ZQ0LDSNpCH9oIOhfBtmthlGshvXRRr+u242Lf4vsq5fH9sGyriMv69Jn/9Cg/ZdrvofxnTa4nPX2Jt6p8M1OWj/+9nvpzqmj9e/6vKK1WotxUlkYfcTQz2Z9EloFfsa7stnFDsLoqkW7zqpC5RpS8e2c7cDZq6IxeLB+LZc1q3FMyv7QpvFDNxWrdwKfwK9PR9Bb3w5V9WQ019Dva7UfI6jPXbvfN/z9QkKnrOoOvW4vg/SqBMHate+OEamSZ0br/l73y8tE+8YqwbLmFcN+4do56de8yWONwO+/daKDvbTxkb9m+at3gZ+out9G+JwhlYPJLXkRrttXGqSnjYqrlu5CU6N1P0pU4Y60cr1OsKzLY+MGjuxTH1q6ra9LPnvIeA0eTkXgmwf+tdyPP/D9KUZ1/zHB6NqQ7RR91LCe3EIbgKWD9HQ5ixbvP1dnPnvm/McaXHbsGKgqK/n7ZZtPFiXd+kxdTeD7k9vinP3T1iZD3ZEiVvfLFn/HkO27KfnOIaH0tsrof/fcjRprgN79wSvFZZYuHFszl7b3ZFKyr8b6LA8H2zrmOXRktL03RPtxPwzs+0qVb9m1N03Qk9Dn6v6+wn26mwgnsonnSSHkJLQ901AKucZ6V+MRoPPA9fare55sZnui92Cm+4F3o0Iq+RM9IeMOHANtmmMjdFtLuMt9/+sT22nqwsdFjM+cL6nwCfxOBD7VfbONBktRRw3rNdaQHo2qg/SKE3RIdf/TqZO/0MsJS50Z7VPL1v3QjkdpfIWMI7gr269kX9DbOnfO5rZO78Y1D6c6bUjX8KVbX3YEy259uT1vNsD9KFV1H4vvNfxoVcfBdXvfk2XlmfQiNEZ/Phf2R0623sfYmfEbsbqn5Q6Zn/LXm3xZ38lL/izf0cW/NCFV8lt9///Sl/z5faRl7Qy29WPVRqQ28taxjomDYyNzPJyKCr9DVf5qQNVErCk6FyEnCevgDhw1/HBkQF3odftJzZHIk4Bl1d2fdy5i93bg2InD8D06Ba42UjY6K96/Iyxrr8s6FobFsjb655DqeGewrReRPkMVTwYNa6p7Av+bE61l4Mto/Uwn2el72Mca9V2num/qdpuQk+jL6l4ahSHX7asO0nt5YvbZJ32efuZbje8NAkDInR+lVa+sU53zPaQ3Ya+NsW2FZa0D94PtmWPk3vM96wZmyLZ5sj7WMPDA16fnhR7UZWau/dejY4g16jv1uspS9AocOwlpd+Uq4L3qDNI7DJhJihVbdm+458k6ZN3vXfmEPjEtajTGQoqCk/ea5/9/3vJj6Wujx/JYw7e+H+j3Xhm//6zvK1Cr+xgnlrrX7mNU+D7dzSGBefj91gGNpMqD9BpkcbIOec9lwklYJIRT3VbalmDzvSx17lq76cOpCPzhVfkS+JaD9y4GMHivkeq+wQPaO3SKz6wPMPGeuMd14170qIGvDcuQsQ51A3iUal92YQ9yajzYAsdW7E68p+nDqYbuhwF/dwl9y2kn566ng/carO5jfodx1caDnoRC7i3/HOEjT6wqVf1+oxoNCtlm2xOfJyQEtpEbEPce6yykcVF3xHpI4G88t3Wmyx1XbNxsdVvvIm/rjUGDsZFzCYHfDUsXd+axb04ceZU/0VsBqe7jVEQx1ankmr4H/G3Mno2DSXJkIJtP9+kHfZ+P7rnL/HAfj90daxEqzqK69GhchPQabWp8r5muR++5GPL3eNBtvYp0XJzanycG7wk11Gv4xRP0rK+3Lfq23lpS3afuumsy8L0G6Z2q7vRRqf/rnh/UEzpwVSZ3+VQ8qtWoOzZlxZeycZE5w3vN5TiVJ+XlLznP3brnuwFCGunS83H74ln2Fg0WBuwR+KZVvuU84FdS5VPdt7IxVGe7NBX40Qbp6XwJW2fzqNRbvZ7bqorPo0GZMmzMlqXbQn7ng4vfg3mjDQlpsHjPS1HSsPDxmOChW5035C79L1V+HshLZ3stf+F68lCdiNX9lwFoAYN+ssRfvanHyU4ibbeVs38mujRMQsYYbFJXwR0O/M2ZbT3Tit56W29jf/7AQYBU9wR+5Srf8lq+VPnTvHHRh4fqxFpPr1zzz+mu1GiINMubr1FgiKYK+xiNk9gD9nwCIGV1GT3cEoW908p+brBtCHxjQ+/SL67lW09Usez6etJq60OPNn3VXoImr98vArfZPFHYFyHg28W7TzgK3KJh5xM2UQc36viJ24T75pXB+mKEPoGfJPSlCrJ86ILcl7/o+GpaDHT3aDLwb3xnrtN/90tH1vHGYN3XDeFkgW80uHHVlQPKYoY9npBH4NdlXeXPZY79Dlf3Nz3b3lVPLpOGP+dsAA20bYoq2LBht0m4rGPVvewjlx3Z1vcnzjFBD6civqrhGv6fVf4mD+Q7w2CT69bStT/t4OrpY3VfOhYh8CQUraEoM/TVucc7YgNNTqRPRwJtEhrIZYHZwIxrKavL2I2LGMenzDy60wbF04vPOtKfryy2dYSGNdfvCXzvKn/q7AbwXXdtAF9Pq/sUJ+a74pY6fSradUDDZObqjQMJDQCZUGdeNhDtYAKf0EsHsQfsbTz28ZTVZbRw0ycvhjRKH3Rbbyqsp+LR368ib+vovR44ji79v1b5T87+wTerPPRHHVoti75u7woDtWKdmFcRGqJ1hPQi/SyPkq0y6lx6HfRhMb+GBE6iKXqtGnYp7wY4NrgxZFtL2E+q9lDkv7eOcH60GKG/cSDwPUN/rRWOlVeuIwNsBl7dRwsCPVGGTPB0UcxmV7ER41uBye1lPg28XYz11GAIJ1tW4N0Am8iNu2nd6YB1X3YB+9cu9jbgCXkEfqiZs52B77ojT9Nb9Hw7l/W0eJ+cj1RNqar8kEBZGq1Hn8Dsyj3xdavLaI2LwMbdR5+Z6SxuXwx8OBVPyCPwg6v8J2c/uG6Zh/64retgINX9uOT7x5zlLTTwLyuebKOfkKtUijGX2fV74hM2LprY1hbL5Po9gd946MvB9bPhIr507bf4ev5y4LtA1EFjGgyhtw8tUlaQNRqG3reEnbh+nCzIunQ3wJHv1kTBMIt5XFgcayDwfUN/4Wy7jC7bGKxaYV0PYBNniSuZ0G19dW4iHh01HzKC2uc7h3ynNjwhL+X1+6B7zY9cbw8pFkYe54V5wOfnCXktwG155aZ6ErGa2OImr/K3eeOiTcG/iPQ+b6xmwMpPPjsXfo98ljgIZMDTbYRtMzP4zF/eO1+vmyoDuTS8loENw64P2Ku7b8duRIbMgzCT5yxUvSShg0ZDbr8817vl+z32PCGPwI9d5T/pALuNs7s//5d8Gbs23J+v1X2MCVXujae7jBH4zugktD1R4Tzl6zd0cqcvjyc1OtFJo3YrE/2cCc5MgyvGfBXHrt9nkavg1CHcit6ECmTbbfThSuszvQBjbWBexN7WB+ebVA0uAp9VUCn0tzJhTv7HT4aLkev5E1lWT6r7RQc27fjEScjyxLx24YMhZ4br98Klm4N/04JQjHlPvGXjwiLcJPTf6csaA/ZagGv41UNfDri3hov40uJucr79DlX3RYUfY53HPgmd/d56H/Nj4Oeea5d6l50KzC7fE29W4ffgXvNN6mMNBH5o6K8ShP66wZH7Xarud4bvHRIEVU7M6wj7yTTxOjnlIfJ6ShnCKRsXmYt/r3nqh8Z4N1TPNFgmqbYBCHzf0P/VcBGXWuknDf2OVfexv3fqqiPGAM3FkZOqBP4+4er76Py7xE+tp67eE99EIzJl4D0GNCgtnpD36DFeg8BnFXiFvtyectez0O9SdW99sguZ5a30JKTBHFqdnZpud5Vo/e8DeyqODdjr8j3xlss61bhYJTw/zAMaY9uE6wQEvknoz/pS6Xe0uo/Vuh9VqPgtQiBGlT870eCyrvL3WrHGrpC7fE988saFHmspppYNvYx56pyQ6lgDgR+t0re8pl+EfkZ1b2Yc8SRUp7ET+kAdcfWygaJBNDEMfenanWj3ue+6OtUT0ssJd4pt5du4KrkbQMZyWF3Ll33obb78lYs8fXJD24DAZxUEh/4qQehvrebd127hzl27N1xWkpOQBl6MeRfmR967COOY1Z+c/GWq6bG8v3a/X0ReTykrvmTLsuw1Omjgxb7EeKfbenXQsIjdYJm08Pgn8FEp9H8yrKqKW/YmBu895OpeZLEC3+MktIrw+a+PTbcroZy/ZH95oydv331TGg3vZT3Jo3MPKnOLnpCu3BPfqtn8ZJvkL2m4v3bPlxl9K/4H/fev5f2KdRr4NLvNiUZQ5nhCXnLfff78mbUQiVbha2c7A9xbbWAAtehJ9vB17iT9xHPGO7+9pVEzKmlwbHVbUzET+PAI/ZGG/pXhYu500CAAAAR+w8Evo7Atp6yU7rdpHvw71jYAoAzX8I3oCH7L6/rFYL4paxsAQIXffKWfpIs/f83lyX6scQAAgd9s8EvFv3B2j9iV+6Nn+pAfAAAI/AZDP3PPt2JZVvsfNfip9gEABH7DwS/X3WVQn9XtezJuYJGH/pK1DQAg8JsNfbm2P9eXVTe/jOSf080PACDwmw/+zD1f278xXMy9VvwEPwAQ+CD4AQAEPgh+AACBj+jBX1zjnzm7wX2P2rhYM6ofAAh8NB/+Uw3+a6NFyKh+mRxoRdUPAAQ+2lH1z/R1abSYx4Pw52lpAEDgo+Hwz/IfUvlPDCv/IvwXdPkDAIGPdjQAJhr+8oo9k590+Y95Mh8AEPhoZwNgrK8sQiPgpzzw16xZACDw0f5GwEgbAMVPd/DfBWkcHN4VILfwbfKwX7AGAYDABwAALfY9qwAAAAIfAAAQ+AAAgMAHAAAEPgAAIPABAACBDwAACHwAAEDgAwBA4AMAAAIfAAAQ+AAAgMAHAAAEPgAAIPABAACBDwAACHwAAAh8AABA4AMAAAIfAAAQ+AAAgMAHAAAEPgAAIPABAACBDwAAgQ8AAAh8AABA4AMAAAIfAAAQ+AAAgMAHAAAEPgAAIPABAACBDwAAgQ8AAAh8AABA4AMAAAIfAAAQ+AAAgMAHAAAEPgAAIPABACDwAQAAgQ8AAAh8AABA4AMAAAIfAAAQ+AAAgMAHAAAEPgAABD4AACDwAQBA5/2/AAMA3d5mD7esMz8AAAAASUVORK5CYII='/>
	</div>
	<p><b>
		<h1 style="color:#2E86C1"><b>Protected Endpoint Report </b></h1>
	</b></p>
	<div id="Division">
		<h2>General Information</h2>
		<table style="width:30%">
			<tr>
				<th>
					<h3>Configuration Info</h3>
				</th>
			</tr>
		<table style="width:30%">"""
					html_output_append = '\n\t\t\t\t<tr>\n\t\t\t\t\t<th>Configuration Name</th>\n\t\t\t\t\t<td>'+resultExport.json()['configName']+'</td>\n\t\t\t\t</tr>'
					html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th>Configuration ID</th>\n\t\t\t\t\t<td>'+str(resultExport.json()['configId'])+'</td>\n\t\t\t\t</tr>'
					html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th>Version</th>\n\t\t\t\t\t<td>'+str(resultExport.json()['version'])+'</td>\n\t\t\t\t</tr>'
					html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th>Based On</th>\n\t\t\t\t\t<td>'+str(resultExport.json()['basedOn'])+'</td>\n\t\t\t\t</tr>'
					html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th>Create Date</th>\n\t\t\t\t\t<td>'+resultExport.json()['createDate']+'</td>\n\t\t\t\t</tr>'
					html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th>Created By</th>\n\t\t\t\t\t<td>'+resultExport.json()['createdBy']+'</td>\n\t\t\t\t</tr>\n\t\t\t</table>\n\t\t\t</table>\n\t\t\t<br></br>'
					html_output = html_output+html_output_append
					matchAllhostnames = False
					selectedHosts = resultExport.json()['selectedHosts']
					selectableHosts = resultExport.json()['selectableHosts']
					matchTargets = resultExport.json()['matchTargets']['websiteTargets']
					allHostnames = selectedHosts + selectableHosts
					protectedHostnames = []
					allHostnamePolicy = []
					#print bcolors.TURQUO+"---------------------------- All Hostnames ----------------------------\n"+bcolors.ENDC
					#for host in allHostnames:
					#	print host
					#print bcolors.TURQUO+"\n---------------------------- All Hostnames ----------------------------"+bcolors.ENDC
					#print bcolors.TURQUO+"\n\n---------------------------- Match Target ----------------------------"+bcolors.ENDC
					for item in matchTargets:
						#print item
						#print bcolors.WHITE+"\nChecking Policy: "+item["securityPolicy"]['policyId']+bcolors.ENDC
						try:
							item['hostnames']
							html_output_append = '\n\t\t\t<table style="width:100%">\n\t\t\t\t<tr>\n\t\t\t\t\t<th><h3>Match Target Sequence #'+str(item['sequence'])+'</h3></th>\n\t\t\t\t</tr>\n\t\t\t<table style="width:100%">'
							html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th style="color:blue">Policy ID</th>\n\t\t\t\t\t<td>'+str(item["securityPolicy"]['policyId'])+'</td>\n\t\t\t\t</tr>'
							html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th style="color:blue">Protected Endpoints</th>\n\t\t\t\t\t<td>'+' '.join(item['hostnames'])+'</td>\n\t\t\t\t</tr>'
							html_output_append = html_output_append+'\n\t\t\t</table>\n\t\t\t</table>\n\t\t\t<br>'
							html_output = html_output+html_output_append
							#actionarray = []
							#ruleidarray = []
							#ruleSetVersion = []
							#ruleCondition = []
							#print bcolors.WHITE+"Hostnames Protected by Policy: "+bcolors.ENDC
							for host in item['hostnames']:
								#print host
								protectedHostnames.append(host)
						except:
							html_output_append = '\n\t\t\t<table style="width:100%">\n\t\t\t\t<tr>\n\t\t\t\t\t<th><h3>Match Target Sequence'+str(item['sequence'])+'</h3></th>\n\t\t\t\t</tr>\n\t\t\t<table style="width:100%">'
							html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th style="color:blue">Policy ID</th>\n\t\t\t\t\t<td>'+str(item["securityPolicy"]['policyId'])+'</td>\n\t\t\t\t</tr>'
							html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th style="color:blue">Protected Endpoints</th>\n\t\t\t\t\t<td>All Hostnames</td>\n\t\t\t\t</tr>'
							html_output_append = html_output_append+'\n\t\t\t</table>\n\t\t\t</table>\n\t\t\t<br>'
							html_output = html_output+html_output_append
							matchAllhostnames = True
							for selhost in selectedHosts:
								protectedHostnames.append(selhost)
							allHostnamePolicy.append(item["securityPolicy"]['policyId'])
							#print bcolors.WARNING+"Match Target is protecting ALL hostnames."+bcolors.ENDC
					#print bcolors.TURQUO+"\n---------------------------- Match Target ----------------------------"+bcolors.ENDC
					html_output_append = html_output_append+'\n\t\t</div>'
					html_output = html_output+html_output_append
					html_output_append = """
	<div id="Division">
		<h2>Summary</h2>
		<table style="width:100%">
			<tr>
				<th>
					<h3>Available Hostnames</h3>
				</th>
			</tr>
		<table style="width:100%">"""
					html_output = html_output+html_output_append
					html_output_append = '\n\t\t\t\t<tr>\n\t\t\t\t\t<td>'+' '.join(allHostnames)+'</td>\n\t\t\t\t</tr>'
					html_output_append = html_output_append+'\n\t\t\t</table>\n\t\t\t</table>'
					html_output = html_output+html_output_append
					#print bcolors.TURQUO+"\n\n---------------------------- Summary ----------------------------"+bcolors.ENDC
					if not matchAllhostnames:
						html_output_append = """
		<table style="width:100%">
			<tr>
				<th>
					<h3>Protected Hostnames</h3>
				</th>
			</tr>
		<table style="width:100%">"""
						html_output = html_output+html_output_append
						html_output_append = '\n\t\t\t\t<tr>\n\t\t\t\t\t<td>'+' '.join(protectedHostnames)+'</td>\n\t\t\t\t</tr>'
						html_output_append = html_output_append+'\n\t\t\t</table>\n\t\t\t</table>'
						html_output = html_output+html_output_append
						#print bcolors.TURQUO+bcolors.UNDERLINE+"\nProtected Hostnames"+bcolors.ENDC
						for host in protectedHostnames:
							#print host
							if host in allHostnames:
								allHostnames.remove(host)
						html_output_append = """
		<table style="width:100%">
			<tr>
				<th>
					<h3>UnProtected Hostnames</h3>
				</th>
			</tr>
		<table style="width:100%">"""
						html_output = html_output+html_output_append
						html_output_append = '\n\t\t\t\t<tr>\n\t\t\t\t\t<td>'+' '.join(allHostnames)+'</td>\n\t\t\t\t</tr>'
						html_output_append = html_output_append+'\n\t\t\t</table>\n\t\t\t</table>'
						html_output = html_output+html_output_append
						#print bcolors.TURQUO+bcolors.UNDERLINE+"\nUnProtected Hostnames"+bcolors.ENDC
						#for host in allHostnames:
							#print host
					else:
						html_output_append = """
		<table style="width:100%">
			<tr>
				<th>
					<h3>Protected Hostnames</h3>
				</th>
			</tr>
		<table style="width:100%">"""
						html_output = html_output+html_output_append
						html_output_append = '\n\t\t\t\t<tr>\n\t\t\t\t\t<th style="color:blue">Policy Name</th>\n\t\t\t\t\t<td>'+' '.join(allHostnamePolicy)+'</td>\n\t\t\t\t</tr>'
						html_output_append = html_output_append+'\n\t\t\t\t<tr>\n\t\t\t\t\t<th style="color:blue">Selected Hostnames</th>\n\t\t\t\t\t<td>'+' '.join(selectedHosts)+'</td>\n\t\t\t\t</tr>'
						html_output_append = html_output_append+'\n\t\t\t</table>\n\t\t\t</table>'
						html_output = html_output+html_output_append
						#print bcolors.TURQUO+"\nThe following policies had ALL hostnames set up in Match Target:"+bcolors.ENDC
						#for policy in allHostnamePolicy:
							#print policy
						#print bcolors.TURQUO+"\nSelected Hosts:"+bcolors.ENDC
						#for host in selectedHosts:
							#print host
					#print bcolors.TURQUO+"\n---------------------------- Summary ----------------------------"+bcolors.ENDC
					html_output_append = '\n\t\t</div>'
					html_output = html_output+html_output_append
					final_output = """\n\t</body>
	</html>"""
					html_output = html_output+final_output
					f = open(file,'w')
					f.write(html_output)
					f.close()
					print bcolors.TURQUO+"-----------------------------------------------------------------"+bcolors.ENDC
					print bcolors.WHITE+"\nConfiguration Name: "+resultExport.json()['configName']+bcolors.ENDC
					print bcolors.WHITE+'Protected Hostname Report Generated: '+file+bcolors.ENDC
					print bcolors.TURQUO+"\n-----------------------------------------------------------------"+bcolors.ENDC
				except:
					pass
			else:
				if automation or respjson:
					print result.content
					sys.exit()
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(resultExport.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
				json_data = resultExport.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
		#print "Available:\n"
		#print allAvailableHostnames
		print bcolors.WARNING+"\n\n[-] Overall Results [-]"+bcolors.ENDC
		print bcolors.TURQUO+"\n----------------------------- Protected Hostnames -----------------------------\n"+bcolors.ENDC
		for protected in  prodProtectedHostnames:
			print protected
		print bcolors.TURQUO+"\n----------------------------- Protected Hostnames -----------------------------"+bcolors.ENDC
		for host in allAvailableHostnames:
			if not host in prodProtectedHostnames:
				wildcardFound = False
				for wildcardhost in wildcards:
					if wildcardhost in host:
						wildcardFound = True
				if wildcardFound == False:
					allNotProtected.append(host)
		print bcolors.TURQUO+"\n\n----------------------------- UnProtected Hostnames -----------------------------\n"+bcolors.ENDC
		for notprotected in  allNotProtected:
			print notprotected
		print bcolors.TURQUO+"\n----------------------------- UnProtected Hostnames -----------------------------"+bcolors.ENDC
		overallFile = 'files/'+AcctName+'.html'
		html_output = """<!DOCTYPE html>
	<html>
	<head>
	<title>
		SWaPI - Overall Results
	</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	<style type="text/css">
	body, html {
		margin: 0;
		font: 400 15px/1.8 "Lato", sans-serif;
		color: #777;
		background-color:#EAECEE;
		}
		#Division
		{
			margin-top:30px;
			width:100%;
			padding:20px;
			border-radius:10px;
			border:10px solid #EE872A;
		}
		h1
		{
			color: #EE872A;
			font-family: verdana;
			font-size: 300%;
			text-align:center;
		}
		h3
		{
			color: #2E86C1;
			font-family: verdana;
			font-size: 18px;
			text-align:center;
		}
		table, th, td
		{
			border: 1px solid black;
			padding: 5px;
			text-align: left;
		}
		}
		#p01
		{
			color: black;
		}
		#td01
		{
			color: black;
			font-family: verdana;
			font-size: 20px;
			text-align:center;
		}
		.caption {
			position: absolute;
			left: 0;
			top: 50%;
			width: 100%;
			text-align: center;
			color: #000;
		}

		.caption span.border {
			background-color: #111;
			color: #fff;
			padding: 18px;
			font-size: 25px;
			letter-spacing: 10px;
		}
		.bargraph {
			list-style: none;
			padding-top: 20px;
			width:97%;
		}
		ul.bargraph li {
			height: 35px;
			color: white;
			text-align: left;
			font-style: italic;
			font-weight:bolder;
			font-size: 14px;
			line-height: 35px;
			padding: 0px 20px;
			margin-bottom: 5px;
		}
		ul.bargraph li.green {
			background: #27AE60;
		}

		ul.bargraph li.warning {
			background: #F1C40F;
		}

		ul.bargraph li.orange {
			background: #F39C12;
		}

		ul.bargraph li.brown {
			background: #E67E22;
		}

		ul.bargraph li.fail {
			background: #C0392B;
		}
	</style>
	</head>
	<body>
	<div class="w3-bar w3-black">
		<a href="https://ac.akamai.com/" target="_blank" class="w3-bar-item w3-button">Aloha</a>
		<a href="https://git.source.akamai.com/projects/GSS/repos/swapi/browse" target="_blank" class="w3-bar-item w3-button">GIT</a>
		<a href="https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/08/swapi-devops-takeover" target="_blank" class="w3-bar-item w3-button">Blog</a>
		<a href="https://community.akamai.com/" target="_blank" class="w3-bar-item w3-button">Community</a>
		<span class="w3-bar-item">SWaPI</span>
	</div>
	<div style='position:relative; border:1px solid #EAECEE; margin-top:5px;'>
		<img style='position:absolute; top:0; right:25px;' width='100px' height='40px' alt='' src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfwAAAEHCAYAAABLB/TJAAAACXBIWXMAABcSAAAXEgFnn9JSAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAHXpJREFUeNrs3T9yG8e2x/G2y+kt4aVOOApvRLwVEFoB4RUQCm4sqOrmgvNXZTh2QHAFF1qBwBVcMHJoMLnpI+otQG+OeEaGKQAz092n59/3U4WibFEYYP79+vT09Hz3+fNnBwAA+u17VgEAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAAACHwAAEPgAAIDABwCAwAcAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAAACHwAAEPgAABD4AACAwAcAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAAACHwAAAh8AABD4AACAwAcAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAAACHwAAAh8AABD4AACAwAcAAAQ+AAAg8AEAAIEPAAAIfAAAQOADAEDgAwAAAh8AABD4AACAwAcAAAQ+AAAg8AEAAIEPAAAIfAAACHwAANB3P7AKhuPH337P8h+HLzF58WtXL/77IX9t89fiP//4+461CAAEPtoV7hLkY31lR4K8qkt9ZUcaBwAAAh+JA36qgTwOCPdztqxlACDwkT7gpeIuQv7aaDGP+Wstr//84+8b1joAEPhIG/Iz99zNbhnyqzzkqeoBgMBHwqCfadBbVfJ7DfklIQ8ABD7Shvwo/zHXav7CsJpfuOcu+yfWOgAQ+EgX9JmG8I3hYu7d8212G9Y4ABD46F/Q37nna/MEPQAQ+KCiBwAQ+IgV9MU1+g+Gi5FZ8uYEPQCAwG8m7GXE/dLZDcbba0W/ZG0DAAj89EGf5T9WzmYmvMKdVvVPRt9h4v6ci196KcYHf33ue90f/HmnL/mMchvglrsEAMDWd58/f2YtpAl76b5f5K9XRouQW+xmMbvvD+bjL35eGK6ifRH++Uu+w4ZGAAAQ+FT1BlX9i+l6J4aNk6oeDsJ/zd4EAAR+W8N+qmFvFZx7rerXAZ+xCPmZs5uuN9Z3Leb1J/wBgMBvTdjLgLl3xtXv1PcZ9doYkZC/7uDqfdSG1Mr3+wMAgY/QoJeBbBvjavkuD7qZ52eTfyfjCS56ssrlcsaC4AcAAj9l2MvAtrVxmL7Nw23lEfRzfb3q6eon+AGAwE8S9imu10/rjMIfSNAfC/45I/wBgMC3CPtZ/uPWcBES9pM6j65NMLlPmzHxEAAQ+NHDXqrnXwwX8aBh/1Tx82TO/jbArrjXan/LqgAwdN+zCoLCftWysF/kP/4g7L+S9bDRRhkAUOHDO+wtn3BXOeyp6iv56J7nLODaPgAqfHQy7OVa/ZawL3Wt1f6YVQGACh9Vwn7mbAfo1Ql768l9+qj2AEgAIPAJe4swysrCXm+3W1PVB6k9nwEAdBld+tXDfuLS3HpXFvaZe57Jj7APc6sNOACgwsfXkB1ryFpOXvOmbFKdRJ8jJrk8cdiAkT8XXemZvl4aJ/5+VPoACHx87T6XkGp0utwWh/2j+/M59vJ6qjMbYMl3nugf5edIGwMWDQJCHwCBT+D/LuFl+iz7sgfhtCzsvz6j3j0/p/6pgW1ShP9EX6GNAAbyASDwBx72i/zHB+PwPHvdviVhL/ewF8+if2rptpL1NNWXz5MKJfTHPHwHAIE/vLCXyvGT4SJKA6bhsJfGyLLNIX9mvWUa/LOa4f+Qf1fu0wdA4A8o7KXLeGcctGevGycaO3CsESKVfG8eM6vhP9fwr7I9f82/O1PxAiDwBxL4EnrXhov4mIfKtCTsN86va9o36KWaX/Z56lm9DW9RoRH1JtbAQwAg8NsbChLE/zIO16zkur1U/jcJvu4ggt4j+OXOgzHz7gMg8PsbBCm68n/Kg2R95jNYP253sEF/IviXJ7Y3XfsACPweB0DTXfkyYOzfxl9TRtzPGY3+l0aeVPvHnknwmvUEgMDv34l/4hoclZ9gkJ4sf3audyHy+szc8Zn0/qIt18p1+69erP/SORIAgMDvXuDvnO2I+J/z8FicWb7lk+9MngWvoT4+eEmjxXeSIrluvtNGz5efqRsD2uiS7XBDlQ+AwO9n2FtfN3/MQyNroHchalV/cH/7RF8p5ge410bAOlUD4MW1/ff5cpecKgAQ+N0P+0YH6hl25cvEOdPQ6lTHFcw06C8a3lzSgJHQN5/1T7+3LGeXL2fCqQJA1/3AKvgyKYtl2N+XVNhzgyC9c88D87wC8aCSt/hsIWQ7XetLHm8r33NlUfnLvPoa+hmHCAAqfKr7Kk5O4qLB+kfk5Xl3QeulBanmbzq2KeX6/4In3gHAad9T3ZtX9+eqz0Xk5b31CXsJen0q4KcOhr240Ip/p9ffAQBU+K2p7icu3kA9r8e76meQRsdVzzavVPzzVLcgAkAXDPkavnV1/5Couq8d9nopYdHRar5qxf+v/HvKCP8Zt9UBwLADf2b8/suSyjpGVe0T9nMN+zqNHRnxLwMAiwbMTl+F7bEBgjrobXTwv4r/Hh382fIBQbKOZfDdglvrAAzdILv09TrvreEiyu67X0Wqrv+7athr+K4qBOy9BvuXCXDqXibw3B7FaPjDSXxi3x0g32vKA3EAEPjDCvyNs71ufXJWvYgj899WHZVeUtVL9S7XujdteiTswSx+E33F6AnYa+hvOPQBEPj9D/tYgXvO6zNz5seYQrdS2OvARPm9lw8E+ugSTF4TebvJdylm+Zu6sPEXzJ4HgMAfQOBbzln/JUxLnoj3FBhWlR7oogG5OaiMZeT6UkN+14PtGDoDIA/GATAoQxy0NzV+/3PPup8Fhv1DjZDK3PNAO6nml33rxtaxBXKpYq7hP69Z+d/k/84R+gCo8PtZ3U+c8SNw8wAZnVm+NAaufd9bQpxBZ6XbeKaVf9UxGgzmAzAIQ5tpz7qaO1fdjwLC3hFKlSv/lT7s5rV7fqbAvuSfXJ3bbgBA4HfTpKnAd2GXEn5lZHnt4N9pd32Wv34uCf4rvVUSAAj8rtPrvNZPftsYBP6XB8Owq3oH/5PeIlkW/DeEPgACvx+sB+t9LOly9+3On9GVnyz4b3j4DgACn8D3ru51sKCPO7ryzYJfenzujvzKrfYGAQCB3zU6YO7SeDHngtkn8KUCnbOLmgV/cY3/jXuebfDQWvcZACDwO2Zi/P77kjnnfZa/oCs/SfDLlMJS0b93f3bzy1iPBWsHAIHfPdZdtJuSv687b/8jU78mD35Z35l7nqhIvKNrHwCBT4X/0snq3jM0qC6bCf0nnRb5J8clFQAEPhV+zQq/7rIfqz4FD2bBv9Zqn14WAL3R+7n09el4r4wXc+76fUZ1381qv2S7AgAV/sCq+8eSwXUTqnsAAIHf/cDflfx9ndu7CHsAAIHvKTN+/03J39e5/59rxgAAAr+lgR/rXvk77rsHABD4/qy79M/dkjep8T48ohUAQOAHeNWBz/iot4IBAEDg16W35JmK9HAbwh4AQOAHyDryOQl8AICpH1gFQfYx3oNH4AJAPf/3P6+loJu8KOzWf/vnH0yYReCbiLFjEfYAUD3oZSC23MJ87KFkH/K/f8x/LvLgX7G2hhX4XXja2XrgB+9CDtIEi3rITwDjFn6H9/nnYv4FoNqxNst/3Jb8mjze+jb/3Ul+bM1Ya3/q+zX8UQc+42bAB2+WKOzFpeF7TwL+Ld2PQLywP3ST/xuq/AEFftvJ9fvdgL//oiffw7vnIK9ANhwGQGnYS/Hm0xMmoT9lDRL4VPfNV/c3DSzT4j1953q45xAAKpkHHGdcMiPwW2HI3blNVPeZwXtO2P6AuVnAv73QgX4EPqug0UAf5Am/iere0Nhw/wAGT7vzLxpsmBP4KFfhYTg7qvvOhDOBD3T3uB2xGvsf+G14+tz+TINgcCf8hqt7i4P+yne/YIIQoDPncQK/A7Yt/gyPVPfdDny5z5fqHrAVqWHM8ebo0g9VpatpV/P/U903u71Svd+Gwweo7CHw33O8EfjBqtwmsmM1taK6b1sDgooDqC7k1rq7v/3zDy4LDCDw2xC2G1qcX7u/mx6Zn1HhA92j8+L7zFux72GhQeAfk2IWux9/+31CJdeZ6v4i1hvprUK+0/U+UnEAtcmMeXW79uf5sbZj1Q2jwi9aeE02OuTE/jjknUyr+6sIb9Wm9Uh3PpC2ypdz6aRipS/n/Tc8MW94gW99cq1y4t9Q3Qe7i7EeI864NQn4t0PfHwDv0M9fcuy9zV8fj/yK9AC8z18Zz6n41g8D+I67SNXlKVVu9ZId72aIO1jE6l4aDbNE24sKH2h38EvlvtJzjBzTI7ruCfwi8C1VqfSG3NKMUt3LwZwf2G36Xt4VPpUHELfqd0zOUwld+uGysl/QwYMPQ9u5Ilf3jQf1wfeSbe775K7B7QcAqPD7EvgXP/72+6jCvPlS1V0ObP+KVt0frMMPLfheg+rOPzKj4OjMOti+rLa61KNx8F2zg8b84XfaxrrD4mBZY12nTwf7x66JLmod4zKq2EjeuW97UHd0rRP4jZHqOg/kfUBFVjUAyk5qq/z1juq+0ereuTjX8JPcf5+vw3X+4zpgWQ/5yXdcc7tN9QQ/1terCPtC8cd7DQhZB2uf4MzfS44jn/Ew9zrY61jAzfQ7X1b8DI/6HVZ1GjN1l5X//r5YV77rq8LnKba3NG4uIr2v/HjUxkuxrXee77UNKJRe0/gYXoVftNAtB+5Nyk7k8qCcvOHx6CLeCz6w6r4N1XlZxROtws9PdPPAsN9X/Zx6iWKuYWTZML7SlwT2bb5cufNiUXMb+6773ZEG6cLzvHCh3+Emfx9pxMzOfYeAZb3SfUBey/x9lvlygo4rHeA20+1teS660Jd89l90PS08ent8w35P2H9rKFPrbozfv2qIrCKFRtur+6lRdd+W7nDv71blQSBaef0S2iipUhHmy1roen1nHPbHSGhu888wqxFWviG1Ld5Dewk+RdpHr/Q7ZMc+r/bSxFiWbJsPUvHqevA9Lre6b100cMx8kkZLjc9r3rAm8Ptb4VuqumOuBrK+lxHe45vqPlKXZhbYmAnpIbiv8P5yMl8Hfse3ZQ0LDSNpCH9oIOhfBtmthlGshvXRRr+u242Lf4vsq5fH9sGyriMv69Jn/9Cg/ZdrvofxnTa4nPX2Jt6p8M1OWj/+9nvpzqmj9e/6vKK1WotxUlkYfcTQz2Z9EloFfsa7stnFDsLoqkW7zqpC5RpS8e2c7cDZq6IxeLB+LZc1q3FMyv7QpvFDNxWrdwKfwK9PR9Bb3w5V9WQ019Dva7UfI6jPXbvfN/z9QkKnrOoOvW4vg/SqBMHate+OEamSZ0br/l73y8tE+8YqwbLmFcN+4do56de8yWONwO+/daKDvbTxkb9m+at3gZ+out9G+JwhlYPJLXkRrttXGqSnjYqrlu5CU6N1P0pU4Y60cr1OsKzLY+MGjuxTH1q6ra9LPnvIeA0eTkXgmwf+tdyPP/D9KUZ1/zHB6NqQ7RR91LCe3EIbgKWD9HQ5ixbvP1dnPnvm/McaXHbsGKgqK/n7ZZtPFiXd+kxdTeD7k9vinP3T1iZD3ZEiVvfLFn/HkO27KfnOIaH0tsrof/fcjRprgN79wSvFZZYuHFszl7b3ZFKyr8b6LA8H2zrmOXRktL03RPtxPwzs+0qVb9m1N03Qk9Dn6v6+wn26mwgnsonnSSHkJLQ901AKucZ6V+MRoPPA9fare55sZnui92Cm+4F3o0Iq+RM9IeMOHANtmmMjdFtLuMt9/+sT22nqwsdFjM+cL6nwCfxOBD7VfbONBktRRw3rNdaQHo2qg/SKE3RIdf/TqZO/0MsJS50Z7VPL1v3QjkdpfIWMI7gr269kX9DbOnfO5rZO78Y1D6c6bUjX8KVbX3YEy259uT1vNsD9KFV1H4vvNfxoVcfBdXvfk2XlmfQiNEZ/Phf2R0623sfYmfEbsbqn5Q6Zn/LXm3xZ38lL/izf0cW/NCFV8lt9///Sl/z5faRl7Qy29WPVRqQ28taxjomDYyNzPJyKCr9DVf5qQNVErCk6FyEnCevgDhw1/HBkQF3odftJzZHIk4Bl1d2fdy5i93bg2InD8D06Ba42UjY6K96/Iyxrr8s6FobFsjb655DqeGewrReRPkMVTwYNa6p7Av+bE61l4Mto/Uwn2el72Mca9V2num/qdpuQk+jL6l4ahSHX7asO0nt5YvbZJ32efuZbje8NAkDInR+lVa+sU53zPaQ3Ya+NsW2FZa0D94PtmWPk3vM96wZmyLZ5sj7WMPDA16fnhR7UZWau/dejY4g16jv1uspS9AocOwlpd+Uq4L3qDNI7DJhJihVbdm+458k6ZN3vXfmEPjEtajTGQoqCk/ea5/9/3vJj6Wujx/JYw7e+H+j3Xhm//6zvK1Cr+xgnlrrX7mNU+D7dzSGBefj91gGNpMqD9BpkcbIOec9lwklYJIRT3VbalmDzvSx17lq76cOpCPzhVfkS+JaD9y4GMHivkeq+wQPaO3SKz6wPMPGeuMd14170qIGvDcuQsQ51A3iUal92YQ9yajzYAsdW7E68p+nDqYbuhwF/dwl9y2kn566ng/carO5jfodx1caDnoRC7i3/HOEjT6wqVf1+oxoNCtlm2xOfJyQEtpEbEPce6yykcVF3xHpI4G88t3Wmyx1XbNxsdVvvIm/rjUGDsZFzCYHfDUsXd+axb04ceZU/0VsBqe7jVEQx1ankmr4H/G3Mno2DSXJkIJtP9+kHfZ+P7rnL/HAfj90daxEqzqK69GhchPQabWp8r5muR++5GPL3eNBtvYp0XJzanycG7wk11Gv4xRP0rK+3Lfq23lpS3afuumsy8L0G6Z2q7vRRqf/rnh/UEzpwVSZ3+VQ8qtWoOzZlxZeycZE5w3vN5TiVJ+XlLznP3brnuwFCGunS83H74ln2Fg0WBuwR+KZVvuU84FdS5VPdt7IxVGe7NBX40Qbp6XwJW2fzqNRbvZ7bqorPo0GZMmzMlqXbQn7ng4vfg3mjDQlpsHjPS1HSsPDxmOChW5035C79L1V+HshLZ3stf+F68lCdiNX9lwFoAYN+ssRfvanHyU4ibbeVs38mujRMQsYYbFJXwR0O/M2ZbT3Tit56W29jf/7AQYBU9wR+5Srf8lq+VPnTvHHRh4fqxFpPr1zzz+mu1GiINMubr1FgiKYK+xiNk9gD9nwCIGV1GT3cEoW908p+brBtCHxjQ+/SL67lW09Usez6etJq60OPNn3VXoImr98vArfZPFHYFyHg28W7TzgK3KJh5xM2UQc36viJ24T75pXB+mKEPoGfJPSlCrJ86ILcl7/o+GpaDHT3aDLwb3xnrtN/90tH1vHGYN3XDeFkgW80uHHVlQPKYoY9npBH4NdlXeXPZY79Dlf3Nz3b3lVPLpOGP+dsAA20bYoq2LBht0m4rGPVvewjlx3Z1vcnzjFBD6civqrhGv6fVf4mD+Q7w2CT69bStT/t4OrpY3VfOhYh8CQUraEoM/TVucc7YgNNTqRPRwJtEhrIZYHZwIxrKavL2I2LGMenzDy60wbF04vPOtKfryy2dYSGNdfvCXzvKn/q7AbwXXdtAF9Pq/sUJ+a74pY6fSradUDDZObqjQMJDQCZUGdeNhDtYAKf0EsHsQfsbTz28ZTVZbRw0ycvhjRKH3Rbbyqsp+LR368ib+vovR44ji79v1b5T87+wTerPPRHHVoti75u7woDtWKdmFcRGqJ1hPQi/SyPkq0y6lx6HfRhMb+GBE6iKXqtGnYp7wY4NrgxZFtL2E+q9lDkv7eOcH60GKG/cSDwPUN/rRWOlVeuIwNsBl7dRwsCPVGGTPB0UcxmV7ER41uBye1lPg28XYz11GAIJ1tW4N0Am8iNu2nd6YB1X3YB+9cu9jbgCXkEfqiZs52B77ojT9Nb9Hw7l/W0eJ+cj1RNqar8kEBZGq1Hn8Dsyj3xdavLaI2LwMbdR5+Z6SxuXwx8OBVPyCPwg6v8J2c/uG6Zh/64retgINX9uOT7x5zlLTTwLyuebKOfkKtUijGX2fV74hM2LprY1hbL5Po9gd946MvB9bPhIr507bf4ev5y4LtA1EFjGgyhtw8tUlaQNRqG3reEnbh+nCzIunQ3wJHv1kTBMIt5XFgcayDwfUN/4Wy7jC7bGKxaYV0PYBNniSuZ0G19dW4iHh01HzKC2uc7h3ynNjwhL+X1+6B7zY9cbw8pFkYe54V5wOfnCXktwG155aZ6ErGa2OImr/K3eeOiTcG/iPQ+b6xmwMpPPjsXfo98ljgIZMDTbYRtMzP4zF/eO1+vmyoDuTS8loENw64P2Ku7b8duRIbMgzCT5yxUvSShg0ZDbr8817vl+z32PCGPwI9d5T/pALuNs7s//5d8Gbs23J+v1X2MCVXujae7jBH4zugktD1R4Tzl6zd0cqcvjyc1OtFJo3YrE/2cCc5MgyvGfBXHrt9nkavg1CHcit6ECmTbbfThSuszvQBjbWBexN7WB+ebVA0uAp9VUCn0tzJhTv7HT4aLkev5E1lWT6r7RQc27fjEScjyxLx24YMhZ4br98Klm4N/04JQjHlPvGXjwiLcJPTf6csaA/ZagGv41UNfDri3hov40uJucr79DlX3RYUfY53HPgmd/d56H/Nj4Oeea5d6l50KzC7fE29W4ffgXvNN6mMNBH5o6K8ShP66wZH7Xarud4bvHRIEVU7M6wj7yTTxOjnlIfJ6ShnCKRsXmYt/r3nqh8Z4N1TPNFgmqbYBCHzf0P/VcBGXWuknDf2OVfexv3fqqiPGAM3FkZOqBP4+4er76Py7xE+tp67eE99EIzJl4D0GNCgtnpD36DFeg8BnFXiFvtyectez0O9SdW99sguZ5a30JKTBHFqdnZpud5Vo/e8DeyqODdjr8j3xlss61bhYJTw/zAMaY9uE6wQEvknoz/pS6Xe0uo/Vuh9VqPgtQiBGlT870eCyrvL3WrHGrpC7fE988saFHmspppYNvYx56pyQ6lgDgR+t0re8pl+EfkZ1b2Yc8SRUp7ET+kAdcfWygaJBNDEMfenanWj3ue+6OtUT0ssJd4pt5du4KrkbQMZyWF3Ll33obb78lYs8fXJD24DAZxUEh/4qQehvrebd127hzl27N1xWkpOQBl6MeRfmR967COOY1Z+c/GWq6bG8v3a/X0ReTykrvmTLsuw1Omjgxb7EeKfbenXQsIjdYJm08Pgn8FEp9H8yrKqKW/YmBu895OpeZLEC3+MktIrw+a+PTbcroZy/ZH95oydv331TGg3vZT3Jo3MPKnOLnpCu3BPfqtn8ZJvkL2m4v3bPlxl9K/4H/fev5f2KdRr4NLvNiUZQ5nhCXnLfff78mbUQiVbha2c7A9xbbWAAtehJ9vB17iT9xHPGO7+9pVEzKmlwbHVbUzET+PAI/ZGG/pXhYu500CAAAAR+w8Evo7Atp6yU7rdpHvw71jYAoAzX8I3oCH7L6/rFYL4paxsAQIXffKWfpIs/f83lyX6scQAAgd9s8EvFv3B2j9iV+6Nn+pAfAAAI/AZDP3PPt2JZVvsfNfip9gEABH7DwS/X3WVQn9XtezJuYJGH/pK1DQAg8JsNfbm2P9eXVTe/jOSf080PACDwmw/+zD1f278xXMy9VvwEPwAQ+CD4AQAEPgh+AACBj+jBX1zjnzm7wX2P2rhYM6ofAAh8NB/+Uw3+a6NFyKh+mRxoRdUPAAQ+2lH1z/R1abSYx4Pw52lpAEDgo+Hwz/IfUvlPDCv/IvwXdPkDAIGPdjQAJhr+8oo9k590+Y95Mh8AEPhoZwNgrK8sQiPgpzzw16xZACDw0f5GwEgbAMVPd/DfBWkcHN4VILfwbfKwX7AGAYDABwAALfY9qwAAAAIfAAAQ+AAAgMAHAAAEPgAAIPABAACBDwAACHwAAEDgAwBA4AMAAAIfAAAQ+AAAgMAHAAAEPgAAIPABAACBDwAACHwAAAh8AABA4AMAAAIfAAAQ+AAAgMAHAAAEPgAAIPABAACBDwAAgQ8AAAh8AABA4AMAAAIfAAAQ+AAAgMAHAAAEPgAAIPABAACBDwAAgQ8AAAh8AABA4AMAAAIfAAAQ+AAAgMAHAAAEPgAAIPABACDwAQAAgQ8AAAh8AABA4AMAAAIfAAAQ+AAAgMAHAAAEPgAABD4AACDwAQBA5/2/AAMA3d5mD7esMz8AAAAASUVORK5CYII='/>
	</div>
	<p><b>
		<h1 style="color:#2E86C1"><b>Protected Hostname Report </b></h1>
	</b></p>
	<div id="Division">
		<h2>Overall Results</h2>
		<table style="width:100%">
			<tr>
				<th>
					<h3>Protected Hostnames</h3>
				</th>
			</tr>
		<table style="width:100%">"""
		html_output = html_output+html_output_append
		html_output_append = '\n\t\t\t\t<tr>\n\t\t\t\t\t<td>'+' '.join(prodProtectedHostnames)+'</td>\n\t\t\t\t</tr>'
		html_output_append = html_output_append+'\n\t\t\t</table>\n\t\t\t</table><br>'
		html_output = html_output+html_output_append
		html_output_append = """
		<table style="width:100%">
			<tr>
				<th>
					<h3>UnProtected Hostnames</h3>
				</th>
			</tr>
		<table style="width:100%">"""
		html_output = html_output+html_output_append
		html_output_append = '\n\t\t\t\t<tr>\n\t\t\t\t\t<td>'+' '.join(allNotProtected)+'</td>\n\t\t\t\t</tr>'
		html_output_append = html_output_append+'\n\t\t\t</table>\n\t\t\t</table>'
		html_output = html_output+html_output_append
		html_output_append = '\n\t\t</div>'
		html_output = html_output+html_output_append
		final_output = """\n\t</body>
	</html>"""
		html_output = html_output+final_output
		f = open(overallFile,'w')
		f.write(html_output)
		f.close()
		print bcolors.TURQUO+"\n-----------------------------------------------------------------"+bcolors.ENDC
		print bcolors.WHITE+'\nOverall Results Report generated: '+overallFile+bcolors.ENDC
		print bcolors.TURQUO+"\n-----------------------------------------------------------------"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'ruleaudit':
		if not ruleId:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.WARNING+" You need to specify a ruleId to audit: --ruleId 3000014\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if ',' in AccountSwitch:
			AccountSwitch = AccountSwitch.split(',')
		else:
			AccountSwitch = AccountSwitch.split(',')
		#print AccountSwitch
		workbook = xlsxwriter.Workbook('files/'+AccountSwitch[0]+'-ruleAudit-'+ruleId+'-'+cdn+'.xlsx')
		worksheet = workbook.add_worksheet()
		if cdn == 'prod':
			header = ['Account','Account ID','Configuration ID','Configuration Name','PROD  Version','Policy Name','Policy ID',ruleId,'Ruleset Version ID']
		else:
			header = ['Account','Account ID','Configuration ID','Configuration Name','Staging  Version','Policy Name','Policy ID',ruleId,'Ruleset Version ID']
		row = 0
		# Add a bold format to use to highlight cells.
		header_format = workbook.add_format()
		header_format.set_bold()
		header_format.set_font_color('white')
		header_format.set_center_across()
		header_format.set_bg_color('black')
		header_format.set_font_size(12)
		for i in range(0,len(header)):
			worksheet.set_column(i, 50)
			worksheet.write(row,i, header[i],header_format)
		row += 1
		with open('files/'+AccountSwitch[0]+'-'+ruleId+'-'+cdn+'-SecurityAudit.csv', 'wb') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			if cdn == 'prod':
				header = ['Account','Account ID','Configuration ID','Configuration Name','PROD  Version','Policy Name','Policy ID',ruleId,'Ruleset Version ID']
			else:
				header = ['Account','Account ID','Configuration ID','Configuration Name','Staging  Version','Policy Name','Policy ID',ruleId,'Ruleset Version ID']
			wr.writerow(header)
			for account in AccountSwitch:
				#print account
				filename = '.map'
				readfile = open(filename, 'r')
				contents = readfile.readlines()
				for item in contents:
					if "[" and "]" in item:
						accountCheck = item[1:-2]
						if accountCheck == account:
							AccountSwitchKey = contents[contents.index(item)+1].strip()
							print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name "+account+" found and mapped to Account "+contents[contents.index(item)+1].strip()+bcolors.ENDC
				#print AccountSwitch
				try:
					AccountSwitchKey
				except:
					 AccountSwitchKey = account
				params = {'accountSwitchKey':AccountSwitchKey}
				msc = s.get(urljoin(baseurl, '/appsec/v1/configs'),params=params)
				#print msc.json()['configurations']
				if msc.status_code == 200:
					if len(AccountSwitch) > 1:
						print bcolors.TURQUO+'\n------------------------------ Separator ------------------------------\n'+bcolors.ENDC
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name: "+account+bcolors.ENDC
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Account: "+AccountSwitchKey+bcolors.ENDC
					for item in msc.json()['configurations']:
						if cdn == 'prod':
							try:
								item['productionVersion']
								configversion = item['productionVersion']
							except:
								pass
						else:
							try:
								item['stagingVersion']
								configversion = item['stagingVersion']
							except:
								pass
						try:
							configversion
							url = '/appsec/v1/export/configs/'+str(item["id"])+'/versions/'+str(configversion)
							result = s.get(urljoin(baseurl, url),params=params)
							if result.status_code == 200:
								print bcolors.TURQUO+'[APPSEC]'+bcolors.WARNING+' Retrieving information from Security Config: '+bcolors.WHITE+result.json()['configName']+bcolors.ENDC
								configName = result.json()['configName']
								for policy in result.json()['securityPolicies']:
									ruleAction = 'Not Enabled'
									for ruleinfo in policy['webApplicationFirewall']['ruleActions']:
										if str(ruleinfo['id']) == ruleId:
											ruleAction = ruleinfo['action']
											rulesetVersionId = ruleinfo['rulesetVersionId']
									mylist = [account,AccountSwitchKey,result.json()['configId'],result.json()['configName'],configversion,policy['name'],policy['id'],ruleAction,rulesetVersionId]
									#print mylist
									wr.writerow(mylist)
									row_format = workbook.add_format()
									row_format.set_center_across()
									row_format.set_font_size(12)
									row_format.set_border()
									for i in range(0,len(mylist)):
										worksheet.write(row,i, mylist[i],row_format)
									row += 1
							else:
								pass
						except:
							pass
						configversion = None
					if len(AccountSwitch) > 1:
						print bcolors.TURQUO+'\n------------------------------ Separator ------------------------------\n'+bcolors.ENDC
				else:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(msc.status_code)+bcolors.ENDC
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request for account: "+account+bcolors.ENDC
					print msc.content
		print bcolors.TURQUO+'\n------------------------------------------------------------------------------------------------------------------------'
		print bcolors.TURQUO+'[APPSEC]'+bcolors.ENDC+' CSV report generated. Filename: files/'+AccountSwitch[0]+'-'+ruleId+'-'+cdn+'-SecurityAudit.csv'
		print bcolors.TURQUO+'------------------------------------------------------------------------------------------------------------------------'
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		workbook.close()
		sys.exit()
	elif retrieveobj == 'audit':
		arrayWriter = []
		if ',' in AccountSwitch:
			AccountSwitch = AccountSwitch.split(',')
		else:
			AccountSwitch = AccountSwitch.split(',')
		#print AccountSwitch
		with open('files/'+AccountSwitch[0]+'-SecurityAudit.csv', 'wb') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			header = ['Account','Account ID','Configuration ID','Configuration Name','PROD  Version','Staging  Version','Policy Name','Policy ID','Ruleset Version','Ruleset Release Date','Hosts - FOUND','Hosts - Not Found','File Paths','Application Layer Controls','Rate Controls','Network Controls','Slow POST','API Protections','Reputation Controls','BOTMAN Controls','SQL','XSS','IN','OUT','HTTP','PHP','CMDi','Trojan','RFI','DDOS','WAF Bypass','Rate Control Bypass','IP Blacklists','GEO Blacklists','Blocked GEOs','IP Whitelists','Slow POST']
			#header = ['Account','Account ID','Configuration ID','Configuration Name','PROD  Version','Policy Name','Policy ID','Ruleset Version','Ruleset Release Date','Hosts - FOUND','Hosts - Not Found','File Paths','Application Layer Controls','Rate Controls','Network Controls','Slow POST','API Protections','Reputation Controls','BOTMAN Controls','SQL','XSS','CMDi','HTTP','RFI','PHP','Trojan','DDOS','IN','OUT', 'WAF Bypass List','Rate Control Bypass List','IP Blacklists','GEO Blacklists','Blocked Countries','IP Whitelists','Slow POST']
			#wr.writerow(header)
			rateControlMultiplier = 0
			for account in AccountSwitch:
				#print account
				filename = '.map'
				readfile = open(filename, 'r')
				contents = readfile.readlines()
				for item in contents:
					if "[" and "]" in item:
						accountCheck = item[1:-2]
						if accountCheck == account:
							AccountSwitchKey = contents[contents.index(item)+1].strip()
							#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name "+account+" found and mapped to Account "+contents[contents.index(item)+1].strip()+bcolors.ENDC
				#print AccountSwitch
				try:
					AccountSwitchKey
					key = AccountSwitchKey
					AccountSwitchKey = None
				except:
					 key = account
				params = {'accountSwitchKey':key}
				msc = s.get(urljoin(baseurl, '/appsec/v1/configs'),params=params)
				if msc.status_code == 200:
					if len(AccountSwitch) > 1:
						print bcolors.TURQUO+'\n------------------------------ Separator ------------------------------\n'+bcolors.ENDC
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name: "+account+bcolors.ENDC
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Account: "+key+bcolors.ENDC
					for item in msc.json()['configurations']:
						try:
							item['productionVersion']
							stagingVersion = 'None'
							try:
								item['stagingVersion']
								stagingVersion = item['stagingVersion']
							except:
								pass
							url = '/appsec/v1/export/configs/'+str(item["id"])+'/versions/'+str(item['productionVersion'])
							result = s.get(urljoin(baseurl, url),params=params)
							if result.status_code == 200:
								print bcolors.TURQUO+'[APPSEC]'+bcolors.WARNING+' Retrieving information from Security Config: '+bcolors.WHITE+result.json()['configName']+bcolors.ENDC
								configName = result.json()['configName']
								ratecontrols = {}
								reputationControls = {}
								rulesets = {}
								rateBypassLists = []
								try:
									result.json()['rulesets']
									for ruleset in result.json()['rulesets']:
										rulesets.update({ruleset['rulesetVersionId']:ruleset['releaseDate']})
								except:
									pass
								try:
									result.json()['ratePolicies']
									for rcconfig in result.json()['ratePolicies']:
										if rcconfig['used'] == True:
											header.append(rcconfig['name'].encode('utf-8').strip())
											ratecontrols.update({rcconfig['id']:rcconfig['name']})
											try:
												rcconfig['additionalMatchOptions']
												for addMO in rcconfig['additionalMatchOptions']:
													if addMO['type'] == 'NetworkListCondition':
														for rclist in  addMO['values']:
															rateBypassLists.append(rclist)
															rateBypassLists = list(set(rateBypassLists))
											except:
												pass
								except:
									pass
								try:
									result.json()['reputationProfiles']
									for repProfile in result.json()['reputationProfiles']:
										if repProfile['enabled'] == True:
											#header.append(repProfile['name'])
											reputationControls.update({repProfile['id']:repProfile['name']})
								except:
									pass
								for policy in result.json()['securityPolicies']:
									try:
										policy['securityControls']['applyReputationControls']
										applyReputationControls = policy['securityControls']['applyReputationControls']
									except:
										applyReputationControls = None
									try:
										policy['securityControls']['applyApiConstraints']
										applyApiConstraints = policy['securityControls']['applyApiConstraints']
									except:
										applyApiConstraints = None
									try:
										policy['securityControls']['applyBotmanControls']
										applyBotmanControls = policy['securityControls']['applyBotmanControls']
									except:
										applyBotmanControls = None
									prodhosts = 'No Hostnames'
									mtpath = 'No Path'
									wilcardHostnames = []
									for host in result.json()['selectedHosts']:
										if '*' in host:
											wilcardHostnames.append(host.replace('*',''))
									try:
										result.json()['matchTargets']['websiteTargets']
										for mtpolicy in result.json()['matchTargets']['websiteTargets']:
											bypassNL = []
											try:
												mtpolicy['bypassNetworkLists']
												for bypass in mtpolicy['bypassNetworkLists']:
													bypassNL.append(bypass['name'])
											except:
												pass
											if policy['id'] == mtpolicy['securityPolicy']['policyId']:
												try:
													mtpolicy['hostnames']
													mtargetarray = []
													mtargetnotFound = []
													for mhost in mtpolicy['hostnames']:
														hostFound = False
														if mhost in result.json()['selectedHosts']:
															mtargetarray.append(mhost)
															hostFound = True
														else:
															for wildcardhost in wilcardHostnames:
																if wildcardhost in mhost:
																	hostFound = True
																	mtargetarray.append(mhost)
														if hostFound == False:
															mtargetnotFound.append(mhost)
													#print mtargetarray
													#print mtpolicy['hostnames']
													#prodhosts = ','.join(mtpolicy['hostnames'])
													prodhosts = ','.join(mtargetarray)
													notfoundHosts = ','.join(mtargetnotFound)
													mtpath = ','.join(mtpolicy['filePaths'])
												except:
													prodhosts = ','.join(result.json()['selectedHosts'])
													notfoundHosts = []
									except:
										pass
									try:
										result.json()['matchTargets']['apiTargets']
										for apipolicy in result.json()['matchTargets']['apiTargets']:
											bypassNL = []
											try:
												apipolicy['bypassNetworkLists']
												for bypass in apipolicy['bypassNetworkLists']:
													bypassNL.append(bypass['name'])
											except:
												pass
											if policy['id'] == apipolicy['securityPolicy']['policyId']:
												prodhosts = apipolicy['apis'][0]['name']
												notfoundHosts = []
									except:
										pass
									#print 'Checkpoint: Creating Array'
									#print policy['name']
									#print policy['id']
									#print bypassNL
									try:
										policy['webApplicationFirewall']['attackGroupActions'][0]['rulesetVersionId']
										foundRuleset = policy['webApplicationFirewall']['attackGroupActions'][0]['rulesetVersionId']
									except:
										foundRuleset = 'None'
									try:
										rulesets[policy['webApplicationFirewall']['attackGroupActions'][0]['rulesetVersionId']]
										foundRuleSetVersion = rulesets[policy['webApplicationFirewall']['attackGroupActions'][0]['rulesetVersionId']]
									except:
										foundRuleSetVersion = 'None'
									#print applyBotmanControls
									#print policy['webApplicationFirewall']['attackGroupActions'][0]['rulesetVersionId']
									#print rulesets[policy['webApplicationFirewall']['attackGroupActions'][0]['rulesetVersionId']]
									#print prodhosts
									#print mtpath
									#print policy['securityControls']['applyApplicationLayerControls']
									#print policy['securityControls']['applyRateControls']
									#print policy['securityControls']['applyNetworkLayerControls']
									#print policy['securityControls']['applySlowPostControls']
									#print applyApiConstraints
									#print applyReputationControls
									#mylist =  [account,AccountSwitchKey,result.json()['configId'],result.json()['configName'],result.json()['version'],stagingVersion,policy['name'].encode('utf-8').strip(),policy['id'],foundRuleset,foundRuleSetVersion,prodhosts,notfoundHosts,mtpath,policy['securityControls']['applyApplicationLayerControls'],policy['securityControls']['applyRateControls'],policy['securityControls']['applyNetworkLayerControls'],policy['securityControls']['applySlowPostControls'],applyApiConstraints,applyReputationControls,applyBotmanControls]
									#mylist =  [account,AccountSwitchKey,result.json()['configId'],result.json()['configName'],result.json()['version'],policy['name'].encode('utf-8').strip(),policy['id'],foundRuleset,foundRuleSetVersion,prodhosts,notfoundHosts,mtpath,policy['securityControls']['applyApplicationLayerControls'],policy['securityControls']['applyRateControls'],policy['securityControls']['applyNetworkLayerControls'],policy['securityControls']['applySlowPostControls'],applyApiConstraints,applyReputationControls,applyBotmanControls]
									#print mylist
									#print 'Checkpoint: Completed Array'
									mylist =  [account,key,result.json()['configId'],result.json()['configName'],result.json()['version'],stagingVersion,policy['name'].encode('utf-8').strip(),policy['id'],foundRuleset,foundRuleSetVersion,prodhosts,notfoundHosts,mtpath,policy['securityControls']['applyApplicationLayerControls'],policy['securityControls']['applyRateControls'],policy['securityControls']['applyNetworkLayerControls'],policy['securityControls']['applySlowPostControls'],applyApiConstraints,applyReputationControls,applyBotmanControls]
									SQL = 'Not Enabled'
									XSS = 'Not Enabled'
									IN = 'Not Enabled'
									OUT = 'Not Enabled'
									HTTP = 'Not Enabled'
									PHP = 'Not Enabled'
									CMD = 'Not Enabled'
									TROJAN = 'Not Enabled'
									RFI = 'Not Enabled'
									DDOS = 'Not Enabled'
									#print 'Checkpoint: Start Risk Groups'
									try:
										policy['webApplicationFirewall']['attackGroupActions']
										for action in policy['webApplicationFirewall']['attackGroupActions']:
											if action['group'].strip() == 'SQL':
												SQL = action['action']
											elif action['group'].strip() == 'XSS':
												XSS = action['action']
											elif action['group'].strip() == 'XSS':
												XSS = action['action']
											elif action['group'].strip() == 'IN':
												IN = action['action']
											elif action['group'].strip() == 'OUT':
												OUT = action['action']
											elif action['group'].strip() == 'HTTP':
												HTTP = action['action']
											elif action['group'].strip() == 'PHP':
												PHP = action['action']
											elif action['group'].strip() == 'CMD':
												CMD = action['action']
											elif action['group'].strip() == 'TROJAN':
												TROJAN = action['action']
											elif action['group'].strip() == 'RFI':
												RFI = action['action']
											elif action['group'].strip() == 'DDOS':
												DDOS = action['action']
									except:
										pass
									RiskGroupArray = [SQL,XSS,IN,OUT,HTTP,PHP,CMD,TROJAN,RFI,DDOS]
									#print policy['id']
									#print RiskGroupArray
									for riskgroup in RiskGroupArray:
										mylist.append(riskgroup)
									try:
										mylist.append(','.join(bypassNL))
									except:
										mylist.append('None')
									try:
										mylist.append(','.join(rateBypassLists))
									except:
										mylist.append('None')
									#print 'Checkpoint: END Risk Groups'
									#print mylist
									IPBlacklist = 'Not Used'
									GEOBlacklist = 'Not Used'
									IPWhitelist = 'Not Used'
									geoItemArray = 'None'
									try:
										policy['ipGeoFirewall']['ipControls']['allowedIPNetworkLists']['networkList']
										IPWhitelist = ','.join(policy['ipGeoFirewall']['ipControls']['allowedIPNetworkLists']['networkList'])
									except:
										pass
									try:
										policy['ipGeoFirewall']['ipControls']['blockedIPNetworkLists']['networkList']
										IPBlacklist = ','.join(policy['ipGeoFirewall']['ipControls']['blockedIPNetworkLists']['networkList'])
									except:
										pass
									try:
										policy['ipGeoFirewall']['geoControls']['blockedIPNetworkLists']['networkList']
										GEOBlacklist = ','.join(policy['ipGeoFirewall']['geoControls']['blockedIPNetworkLists']['networkList'])
										payloadAppend = {"listType":"GEO","includeElements":True,"extended":"true"}
										params.update(payloadAppend)
										headers = {"Accept":"application/json"}
										listArray = []
										for netId in policy['ipGeoFirewall']['geoControls']['blockedIPNetworkLists']['networkList']:
											neturl = '/network-list/v2/network-lists/'+netId
											#print payload
											netdata = s.get(urljoin(baseurl, neturl), headers=headers, params=params)
											if netdata.status_code == 200:
												for value in netdata.json()['list']:
													listArray.append(value)
										geoItemArray = ','.join(listArray)
									except:
										pass
									mylist.append(IPBlacklist)
									mylist.append(GEOBlacklist)
									mylist.append(geoItemArray)
									mylist.append(IPWhitelist)
									try:
										policy['slowPost']
										mylist.append(policy['slowPost']['action'])
									except:
										mylist.append('Not Enabled')
									try:
										policy['ratePolicyActions']
										if rateControlMultiplier != 0:
											for i in range(rateControlMultiplier):
												mylist.append('')
										inpolicyRC = {}
										for rcconfig in policy['ratePolicyActions']:
											inpolicyRC.update({rcconfig['id']:rcconfig['ipv4Action']})
											#header.append(ratecontrols[rcconfig['id']].encode('utf-8').strip())
											#if rcconfig['id'] in ratecontrols:
											#	mylist.append(rcconfig['ipv4Action'])
											#else:
											#	mylist.append('Not Used')
											#mylist.append(ratecontrols[ratecontrol['id']])
											#mylist.append(rcconfig['ipv4Action'])
										#print ratecontrols
										#print inpolicyRC
										for id,sharedrc in ratecontrols.iteritems():
											#print id
											#print sharedrc
											#print inpolicyRC
											if id in inpolicyRC:
												mylist.append(inpolicyRC[id].encode('utf-8').strip())
											else:
												mylist.append('Not Used')
									except:
										pass
									#
									# Client Reputation Section
									#
									try:
										policy['clientReputation']['reputationProfileActions']
									except:
										pass
									#print mylist
									arrayWriter.append(mylist)
									#wr.writerow(mylist)
								rateControlMultiplier = len(ratecontrols) + rateControlMultiplier
							else:
								print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
								print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
								print result.content
						except:
							pass
					if len(AccountSwitch) > 1:
						print bcolors.TURQUO+'\n------------------------------ Separator ------------------------------\n'+bcolors.ENDC
				elif msc.status_code == 401:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" NOT Authorized: "+str(msc.status_code)+bcolors.ENDC
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Are you sure you using the right account? "+bcolors.ENDC
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Account Name: "+account+bcolors.ENDC
					#print msc.content
				else:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(msc.status_code)+bcolors.ENDC
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request for account: "+account+bcolors.ENDC
					print msc.content
			arrayWriter.insert(0, header)
			#for line in arrayWriter:
				#print line
				#wr.writerow(line)
			wr.writerows(arrayWriter)
		if os.stat('files/'+AccountSwitch[0]+'-SecurityAudit.csv').st_size != '447':
			print bcolors.TURQUO+'\n------------------------------------------------------------------------------------------------------------------------'
			print bcolors.TURQUO+'[APPSEC]'+bcolors.ENDC+' CSV report generated. Filename: files/'+AccountSwitch[0]+'-SecurityAudit.csv'
			print bcolors.TURQUO+'------------------------------------------------------------------------------------------------------------------------'
		else:
			pass
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'peerReview':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		Version = findAppsecVersion(configId,respjson)
		prodVersion = str(Version["Production"])
		print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Found Production version: "+prodVersion+bcolors.ENDC
		stagingVersion = str(Version["Staging"])
		print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Found Staging version: "+stagingVersion+bcolors.ENDC
		url = '/appsec/v1/export/configs/'+configId+'/versions/'+str(stagingVersion)
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			stagingName = result.json()['configName'].replace(" ","")+"-V"+str(stagingVersion)+".json"
			print stagingName
			AppsecExport(result.json()['configName'].replace(" ",""),stagingVersion,result.json(),respjson)
		url = '/appsec/v1/export/configs/'+configId+'/versions/'+str(prodVersion)
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			prodName = result.json()['configName'].replace(" ","")+"-V"+str(prodVersion)+".json"
			print prodName
			AppsecExport(result.json()['configName'].replace(" ",""),prodVersion,result.json(),respjson)
		print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" ColorDiff\n"+bcolors.ENDC
		print bcolors.WARNING+"\t\t\tSTAGING\t\t\t\t\t\t\t     PRODUCTION\n\n"+bcolors.ENDC
		bashCommand = "colordiff files/"+stagingName+" files/"+prodName+" -yd --suppress-common-lines -W 170"
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()
		print output
		sort1 = "cat files/"+stagingName+" | jq 'walk(if type == \"array\" then sort else . end)' > files/sorted-"+stagingName
		sort2 = "cat files/"+prodName+" | jq 'walk(if type == \"array\" then sort else . end)' > files/sorted-"+prodName
		print sort1
		print sort2
		process2 = subprocess.Popen(sort1, shell=True)
		#output2, error = process2.communicate()
		process3 = subprocess.Popen(sort2, shell=True)
		#output3, error = process3.communicate()
		sortedbashCommand = "colordiff files/sorted-"+stagingName+" files/sorted-"+prodName+" -yd --suppress-common-lines -W 170"
		print sortedbashCommand
		process4 = subprocess.Popen(sortedbashCommand.split(), stdout=subprocess.PIPE)
		output4, error = process4.communicate()
		print output4
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'configPR':
		if generate:
			if propertyName:
				configId = findConfigID(propertyName)
			else:
				if not configId:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
					print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
			if not propertyVersion:
				Version = findAppsecVersion(configId,respjson)
				if Version["Production"] != None:
					propertyVersion = str(Version["Production"])
					if not respjson and not automation:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using active PROD version: "+propertyVersion+bcolors.ENDC
				else:
					propertyVersion = str(Version["Latest"])
					if not respjson and not automation:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
			if propertyName:
				noSpaceName = propertyName.replace(" ", "")
				filename = 'files/'+noSpaceName+'-exclusions'+'-V'+str(propertyVersion)+'.xlsx'
			else:
				filename = 'files/'+configId+'-exclusions'+'-V'+str(propertyVersion)+'.xlsx'
			url = '/appsec/v1/export/configs/'+configId+'/versions/'+str(propertyVersion)
			result = s.get(urljoin(baseurl, url),params=params)
			workbook = xlsxwriter.Workbook(filename)
			ruleSheet = workbook.add_worksheet('Rule Exclusions')
			ruleEvalSheet = workbook.add_worksheet('Rule Eval Exclusions')
			wafSheet = workbook.add_worksheet('WAF Controls')
			wafEvalSheet = workbook.add_worksheet('WAF Eval Controls')
			rateSheet = workbook.add_worksheet('Rate Controls')
			repSheet = workbook.add_worksheet('Client Reputation')
			customSheet = workbook.add_worksheet('Custom Rules')
			ruleHeader = ['Policy Name','Policy ID','Rule ID','Positive Match','Selector','Action','Recommended Action','Approved','','Name','Condition','Exclusion','Format Example','Supported']
			customHeader = ['Policy Name','Policy ID','Rule ID','Name','Version','Action','Recommendation','Approved']
			wafHeader = ['Policy Name','Policy ID','Control','Current','Recommendation','Ruleset Version','Ruleset Release Date','Approved']
			riskGroups = ['SQL','XSS','CMD','RFI','HTTP','PHP','TROJAN','DDOS','IN','OUT']
			repProfiles = ['Web Scrapers (Low Threat)','Web Scrapers (High Threat)','Web Attackers (Low Threat)','Web Attackers (High Threat)','DoS Attackers (Low Threat)','DoS Attackers (High Threat)','Scanning Tools (Low Threat)','Scanning Tools (High Threat)']
			rateHeader = ['Policy Name','Policy ID','Rate Control ID','Rate Control Name','Request Type','Client Identifier','Use XFF','Hostnames','Paths','File Extensions','Request Methods','Request Headers','ASNumber','User-Agent','Response Codes','Network List','Current','Recommendation','Burst/Rate','Average/Period','Approved']
			repHeader = ['Policy Name','Policy ID','Profile ID','Profile','Current','Recommendation','Threshold','Approved']
			infoExc = ['Disabling Rule','Cookie Name','Query/Body Parameter Name','Any Header/Cookie/Param Value','Prefix','Header Name','JSON PAIRS','XML PAIRS']
			infoCon = ['IPs','Hosts','Paths','Extensions','Methods']
			info2Exc = ['Set "Recommended Action" column to "not used"','REQUEST_COOKIES:sub‌scribed_services','ARGS:Body','ANY_VALUE:ps','PREFIX:mp_','REQUEST_HEADERS:User-Agent','JSON_PAIRS:SendTo','XML_PAIRS:StatusUpdate']
			info2Con = ['IP:127.0.0.1','HOST:swapi.akamai.io','PATH:/api/v*','EXT:txt','METHOD:POST']
			row = 0
			# Add a bold format to use to highlight cells.
			table_format = workbook.add_format()
			table_format.set_center_across()
			table_format.set_align('center')
			table_format.set_align('vcenter')
			table_format.set_font_size(12)
			table_format.set_border()
			header_format = workbook.add_format()
			header_format.set_bold()
			header_format.set_center_across()
			header_format.set_align('center')
			header_format.set_align('vcenter')
			header_format.set_font_size(12)
			header_format.set_border()
			for i in range(0,len(rateHeader)):
				rateSheet.set_column(i, 50)
				rateSheet.write(row,i, rateHeader[i],header_format)
			for i in range(0,len(customHeader)):
				customSheet.set_column(i, 50)
				customSheet.write(row,i, customHeader[i],header_format)
			for i in range(0,len(repHeader)):
				repSheet.set_column(i, 50)
				repSheet.write(row,i, repHeader[i],header_format)
			for i in range(0,len(ruleHeader)):
				ruleSheet.set_column(i, 50)
				ruleEvalSheet.set_column(i, 50)
				ruleSheet.write(row,i, ruleHeader[i],header_format)
				ruleEvalSheet.write(row,i, ruleHeader[i],header_format)
			for i in range(0,len(wafHeader)):
				wafSheet.set_column(i, 50)
				wafEvalSheet.set_column(i, 50)
				wafSheet.write(row,i, wafHeader[i],header_format)
				wafEvalSheet.write(row,i, wafHeader[i],header_format)
			row = 1
			col = 9
			for i in range(0,len(infoExc)):
				if infoExc[i] == 'Disabling Rule':
					array = [infoExc[i],'','',info2Exc[i],'Yes']
				else:
					array = [infoExc[i],'','X',info2Exc[i],'Yes']
				for x in range(0,len(array)):
					#print row,col,array[x],x
					ruleSheet.set_column(x, 50)
					ruleSheet.write(row,col,array[x],table_format)
					ruleEvalSheet.set_column(x, 50)
					ruleEvalSheet.write(row,col,array[x],table_format)
					col += 1
				row += 1
				col = 9
			for i in range(0,len(infoCon)):
				array = [infoCon[i],'X','',info2Con[i],'Yes']
				for x in range(0,len(array)):
					#print row,col,array[x],x
					ruleSheet.set_column(x, 50)
					ruleSheet.write(row,col,array[x],table_format)
					ruleEvalSheet.set_column(x, 50)
					ruleEvalSheet.write(row,col,array[x],table_format)
					col += 1
				row += 1
				col = 9
			row = 1
			# ['Policy Name','Policy ID','Control','Current','Recommendation','Ruleset Version','Approved']
			if result.status_code == 200:
				wcrow = 1
				rcrow = 1
				crrow = 1
				rerow = 1
				curow = 1
				revrow = 1
				wevrow = 1
				if propertyName:
					print bcolors.TURQUO+"[APPSEC] "+bcolors.WARNING+"Property Name: "+bcolors.ENDC+propertyName
					print bcolors.TURQUO+"[APPSEC] "+bcolors.WARNING+"Configuration ID: "+bcolors.ENDC+str(configId)
				else:
					print bcolors.TURQUO+"[APPSEC] "+bcolors.WARNING+"Configuration ID: "+bcolors.ENDC+str(configId)
				print bcolors.TURQUO+"[APPSEC] "+bcolors.WARNING+"Property Version: "+bcolors.ENDC+str(propertyVersion)
				print bcolors.TURQUO+"[APPSEC] "+bcolors.WHITE+"Starting Information Gathering "+bcolors.ENDC
				for policy in result.json()['securityPolicies']:
					print bcolors.TURQUO+"[APPSEC] "+bcolors.WARNING+"Gathering information from policy: "+bcolors.ENDC+policy['name']
					# ['Policy Name','Policy ID','Rule ID','Selector','Approved','','Name','Condition','Exclusion','Format Example','Supported']
					try:
						for rule in policy['webApplicationFirewall']['evaluation']['ruleActions']:
							try:
								for value in rule['exception']['headerCookieOrParamValues']:
									array = [policy['name'],policy['id'],rule['id'],'','ANY_VALUE:'+value,rule['action'],rule['action'],'yes']
									for i in range(0,len(array)):
										ruleEvalSheet.set_column(i, 50)
										ruleEvalSheet.write(revrow,i, array[i],table_format)
									revrow += 1
							except:
								pass
							try:
								for excName in rule['exception']['specificHeaderCookieOrParamNames']:
									for value in excName['names']:
										array = [policy['name'],policy['id'],rule['id'],'',excName['selector']+':'+value,rule['action'],rule['action'],'yes']
										for i in range(0,len(array)):
											ruleEvalSheet.set_column(i, 50)
											ruleEvalSheet.write(revrow,i, array[i],table_format)
										revrow += 1
							except:
								pass
							try:
								rule['exception']['specificHeaderCookieOrParamPrefix']
								array = [policy['name'],policy['id'],rule['id'],'','PREFIX:'+rule['exception']['specificHeaderCookieOrParamPrefix']['prefix'],rule['action'],rule['action'],'yes']
								#print array
								for i in range(0,len(array)):
									ruleEvalSheet.set_column(i, 50)
									ruleEvalSheet.write(revrow,i, array[i],table_format)
								revrow += 1
							except:
								pass
							try:
								for condRule in rule['conditions']:
									if condRule['type'] == 'ipMatch':
										for IP in condRule['ips']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'IP:'+IP,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleEvalSheet.set_column(i, 50)
												ruleEvalSheet.write(revrow,i, array[i],table_format)
											revrow += 1
									elif condRule['type'] == 'hostMatch':
										for host in condRule['hosts']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'HOST:'+host,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleEvalSheet.set_column(i, 50)
												ruleEvalSheet.write(revrow,i, array[i],table_format)
											revrow += 1
									elif condRule['type'] == 'extensionMatch':
										for ext in condRule['extensions']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'EXT:'+ext,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleEvalSheet.set_column(i, 50)
												ruleEvalSheet.write(revrow,i, array[i],table_format)
											revrow += 1
									elif condRule['type'] == 'requestMethodMatch':
										for method in condRule['methods']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'METHOD:'+method,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleEvalSheet.set_column(i, 50)
												ruleEvalSheet.write(revrow,i, array[i],table_format)
											revrow += 1
									elif condRule['type'] == 'pathMatch':
										for path in condRule['paths']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'PATH:'+path,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleEvalSheet.set_column(i, 50)
												ruleEvalSheet.write(revrow,i, array[i],table_format)
											revrow += 1
							except:
								pass
					except:
						pass
					try:
						for rule in policy['webApplicationFirewall']['ruleActions']:
							try:
								for value in rule['exception']['headerCookieOrParamValues']:
									array = [policy['name'],policy['id'],rule['id'],'','ANY_VALUE:'+value,rule['action'],rule['action'],'yes']
									for i in range(0,len(array)):
										ruleSheet.set_column(i, 50)
										ruleSheet.write(rerow,i, array[i],table_format)
									rerow += 1
							except:
								pass
							try:
								for excName in rule['exception']['specificHeaderCookieOrParamNames']:
									for value in excName['names']:
										array = [policy['name'],policy['id'],rule['id'],'',excName['selector']+':'+value,rule['action'],rule['action'],'yes']
										for i in range(0,len(array)):
											ruleSheet.set_column(i, 50)
											ruleSheet.write(rerow,i, array[i],table_format)
										rerow += 1
							except:
								pass
							try:
								rule['exception']['specificHeaderCookieOrParamPrefix']
								array = [policy['name'],policy['id'],rule['id'],'','PREFIX:'+rule['exception']['specificHeaderCookieOrParamPrefix']['prefix'],rule['action'],rule['action'],'yes']
								#print array
								for i in range(0,len(array)):
									ruleSheet.set_column(i, 50)
									ruleSheet.write(rerow,i, array[i],table_format)
								rerow += 1
							except:
								pass
							try:
								for condRule in rule['conditions']:
									if condRule['type'] == 'ipMatch':
										for IP in condRule['ips']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'IP:'+IP,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleSheet.set_column(i, 50)
												ruleSheet.write(rerow,i, array[i],table_format)
											rerow += 1
									elif condRule['type'] == 'hostMatch':
										for host in condRule['hosts']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'HOST:'+host,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleSheet.set_column(i, 50)
												ruleSheet.write(rerow,i, array[i],table_format)
											rerow += 1
									elif condRule['type'] == 'extensionMatch':
										for ext in condRule['extensions']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'EXT:'+ext,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleSheet.set_column(i, 50)
												ruleSheet.write(rerow,i, array[i],table_format)
											rerow += 1
									elif condRule['type'] == 'requestMethodMatch':
										for method in condRule['methods']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'METHOD:'+method,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleSheet.set_column(i, 50)
												ruleSheet.write(rerow,i, array[i],table_format)
											rerow += 1
									elif condRule['type'] == 'pathMatch':
										for path in condRule['paths']:
											array = [policy['name'],policy['id'],rule['id'],str(condRule['positiveMatch']),'PATH:'+path,rule['action'],rule['action'],'yes']
											#print array
											for i in range(0,len(array)):
												ruleSheet.set_column(i, 50)
												ruleSheet.write(rerow,i, array[i],table_format)
											rerow += 1
							except:
								pass
					except:
						pass
					try:
						for rule in policy['customRuleActions']:
							#print rule
							# ['Policy Name','Policy ID','Rule ID','Name','Description','Version','Action','Recommendation','Approved']
							for customRule in result.json()['customRules']:
								if customRule['id'] == rule['id']:
									#print customRule['id'],rule['id']
									array = [policy['name'],policy['id'],rule['id'],customRule['name'],customRule['version'],rule['action'],rule['action'],'yes']
									#print array
									for i in range(0,len(array)):
										customSheet.set_column(i, 50)
										customSheet.write(curow,i, array[i],table_format)
									curow += 1
									break
					except:
						pass
					try:
						for group in policy['webApplicationFirewall']['attackGroupActions']:
							for ruleSet in result.json()['rulesets']:
								if ruleSet['rulesetVersionId'] == group['rulesetVersionId']:
									array = [policy['name'],policy['id'],group['group'],group['action'],group['action'],group['rulesetVersionId'],ruleSet['releaseDate'],'yes']
									#print array
									for i in range(0,len(array)):
										wafSheet.set_column(i, 50)
										wafSheet.write(wcrow,i, array[i],table_format)
									wcrow += 1
					except:
						pass
					try:
						for group in policy['webApplicationFirewall']['evaluation']['attackGroupActions']:
							for ruleSet in result.json()['rulesets']:
								if ruleSet['rulesetVersionId'] == policy['webApplicationFirewall']['evaluation']['rulesetVersionId']:
									array = [policy['name'],policy['id'],group['group'],group['action'],group['action'],policy['webApplicationFirewall']['evaluation']['rulesetVersionId'],ruleSet['releaseDate'],'yes']
									#print array
									for i in range(0,len(array)):
										wafEvalSheet.set_column(i, 50)
										wafEvalSheet.write(wevrow,i, array[i],table_format)
									wevrow += 1
					except:
						pass
					try:
						for rateC in policy['ratePolicyActions']:
							for rateFinder in result.json()['ratePolicies']:
								if rateFinder['id'] == rateC['id']:
									try:
										rateFinder['additionalMatchOptions']
										NLs = ''
										ReqHed = ''
										ReqMet = ''
										ResCodes = ''
										UserAgent = ''
										ASNumber = ''
										for matchOption in rateFinder['additionalMatchOptions']:
											if matchOption['type'] == 'NetworkListCondition':
												if matchOption['positiveMatch'] == False:
													NLs = 'Negative Match: '+','.join(matchOption['values'])
												else:
													NLs = 'Positive Match: '+','.join(matchOption['values'])
											elif matchOption['type'] == 'RequestMethodCondition':
												if matchOption['positiveMatch'] == False:
													ReqMet = 'Negative Match: '+','.join(matchOption['values'])
												else:
													ReqMet = 'Positive Match: '+','.join(matchOption['values'])
											elif matchOption['type'] == 'RequestHeaderCondition':
												if matchOption['positiveMatch'] == False:
													ReqHed = 'Negative Match: '+','.join(matchOption['values'])
												else:
													ReqHed = 'Positive Match: '+','.join(matchOption['values'])
											elif matchOption['type'] == 'UserAgentCondition':
												if matchOption['positiveMatch'] == False:
													UserAgent = 'Negative Match: '+','.join(matchOption['values'])
												else:
													UserAgent = 'Positive Match: '+','.join(matchOption['values'])
											elif matchOption['type'] == 'AsNumberCondition':
												if matchOption['positiveMatch'] == False:
													ASNumber = 'Negative Match: '+','.join(matchOption['values'])
												else:
													ASNumber = 'Positive Match: '+','.join(matchOption['values'])
											elif matchOption['type'] == 'ResponseStatusCondition':
												if matchOption['positiveMatch'] == False:
													ResCodes = 'Negative Match: '+','.join(matchOption['values'])
												else:
													ResCodes = 'Positive Match: '+','.join(matchOption['values'])
									except:
										NLs = ''
										ReqHed = ''
										ReqMet = ''
										ResCodes = ''
										UserAgent = ''
										ASNumber = ''
									try:
										rateFinder['path']
										if rateFinder['path']['positiveMatch'] == False:
											path = 'Negative Match: '+','.join(rateFinder['path']['values'])
										else:
											path = 'Positive Match: '+','.join(rateFinder['path']['values'])
									except:
										path = ''
									try:
										rateFinder['fileExtensions']
										if rateFinder['fileExtensions']['positiveMatch'] == False:
											fileExtensions = 'Negative Match: '+','.join(rateFinder['fileExtensions']['values'])
										else:
											fileExtensions = 'Positive Match: '+','.join(rateFinder['fileExtensions']['values'])
									except:
										fileExtensions = ''
									try:
										rateFinder['hostnames']
										hostnames = ','.join(rateFinder['hostnames'])
									except:
										hostnames = ''
									xff = str(rateFinder['useXForwardForHeaders'])
									requestType = rateFinder['requestType']
									clientIdentifier = rateFinder['clientIdentifier']
# ['Policy Name','Policy ID','Rate Control ID','Rate Control Name','Request Type','Client Identifier','Use XFF','Hostnames','Paths','File Extensions','Request Methods','Request Headers','ASNumber','User-Agent','Response Codes','Network List','Current','Recommendation','Burst/Rate','Average/Period','Approved']
									array = [policy['name'],policy['id'],rateC['id'],rateFinder['name'],requestType,clientIdentifier,xff,hostnames,path,fileExtensions,ReqMet,ReqHed,ASNumber,UserAgent,ResCodes,NLs,rateC['ipv4Action'],rateC['ipv4Action'],rateFinder['burstThreshold'],rateFinder['averageThreshold'],'yes']
									#print array
									for i in range(0,len(array)):
										rateSheet.set_column(i, 50)
										rateSheet.write(rcrow,i, array[i],table_format)
									rcrow += 1
					except:
						pass
					try:
						policy['slowPost']
						array = [policy['name'],policy['id'],'NA','Slow POST Protection','','','','','','','','','','','','',policy['slowPost']['action'],policy['slowPost']['action'],policy['slowPost']['slowRateThreshold']['rate'],policy['slowPost']['slowRateThreshold']['period'],'yes']
						#print array
						for i in range(0,len(array)):
							rateSheet.set_column(i, 50)
							rateSheet.write(rcrow,i, array[i],table_format)
						rcrow += 1
					except:
						pass
					try:
						for clientRep in policy['clientReputation']['reputationProfileActions']:
							# ['Policy Name','Policy ID','Profile ID','Profile','Current','Recommendation','Threshold','Approved']
							for crFinder in result.json()['reputationProfiles']:
								if crFinder['id'] == clientRep['id']:
									array = [policy['name'],policy['id'],clientRep['id'],crFinder['name'],clientRep['action'],clientRep['action'],crFinder['threshold'],'yes']
									#print array
									for i in range(0,len(array)):
										repSheet.set_column(i, 50)
										repSheet.write(crrow,i, array[i],table_format)
									crrow += 1
					except:
						pass
				workbook.close()
				print bcolors.TURQUO+"[APPSEC] "+bcolors.WHITE+"Completed successfully! "+bcolors.ENDC
				print bcolors.TURQUO+'\n------------------------------------------------------------------------------------------------------------------------'
				print bcolors.TURQUO+'[APPSEC]'+bcolors.WARNING+' Excel report generated. File location: '+bcolors.WHITE+filename+bcolors.ENDC
				print bcolors.TURQUO+'------------------------------------------------------------------------------------------------------------------------'
			else:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(msc.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request for account: "+account+bcolors.ENDC
				print result.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			if not PRd:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify an PR exclusion file: --PR files/ibmccExclusions.txt\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if propertyName:
				configId = findConfigID(propertyName)
			else:
				if not configId:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
					print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
			if not propertyVersion:
				Version = findAppsecVersion(configId,respjson)
				if Version["Production"] != None:
					propertyVersion = str(Version["Production"])
					if not respjson and not automation:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using active PROD version: "+bcolors.ENDC+propertyVersion
				else:
					propertyVersion = str(Version["Latest"])
					if not respjson and not automation:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+bcolors.ENDC+propertyVersion
			url = '/appsec/v1/export/configs/'+configId+'/versions/'+str(propertyVersion)
			try:
				exclusionsSheet = pd.read_excel(PRd, sheet_name='Rule Exclusions')
			except:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Unable to read file. Are you sure it exists?\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			startTime = datetime.datetime.now()
			exclusionsSheet = pd.read_excel(PRd, sheet_name='Rule Exclusions')
			#print exclusionsSheet.shape[0]
			policyIDColumn = exclusionsSheet['Policy ID']
			ruleIDColumn = exclusionsSheet['Rule ID']
			selectorsColumn = exclusionsSheet['Selector']
			positiveMColumn = exclusionsSheet['Positive Match']
			actionsColumn = exclusionsSheet['Action']
			recommendedColumn = exclusionsSheet['Recommended Action']
			approvedColumn = exclusionsSheet['Approved']
			ruleEvalSheet = pd.read_excel(PRd, sheet_name='Rule Eval Exclusions')
			#print exclusionsSheet.shape[0]
			policyIDREvColumn = ruleEvalSheet['Policy ID']
			ruleIDEvColumn = ruleEvalSheet['Rule ID']
			selectorsEvColumn = ruleEvalSheet['Selector']
			positiveMEvColumn = ruleEvalSheet['Positive Match']
			actionsEvColumn = ruleEvalSheet['Action']
			recommendedEvColumn = ruleEvalSheet['Recommended Action']
			approvedREvColumn = ruleEvalSheet['Approved']
			customSheet = pd.read_excel(PRd, sheet_name='Custom Rules')
			#print customSheet.shape[0]
			policyCuIDColumn = customSheet['Policy ID']
			ruleIDCuColumn = customSheet['Rule ID']
			recommendationCuColumn = customSheet['Recommendation']
			approvedCuColumn = customSheet['Approved']
			wafEvalSheet = pd.read_excel(PRd, sheet_name='WAF Eval Controls')
			#print riskGroupSheet.shape[0]
			policyIDEvColumn = wafEvalSheet['Policy ID']
			evControlColumn = wafEvalSheet['Control']
			recommendationRVEvColumn = wafEvalSheet['Ruleset Version']
			recommendationEvColumn = wafEvalSheet['Recommendation']
			approvedEvColumn = wafEvalSheet['Approved']
			riskGroupSheet = pd.read_excel(PRd, sheet_name='WAF Controls')
			#print riskGroupSheet.shape[0]
			policyIDRGColumn = riskGroupSheet['Policy ID']
			rgControlColumn = riskGroupSheet['Control']
			recommendationRVColumn = riskGroupSheet['Ruleset Version']
			recommendationRGColumn = riskGroupSheet['Recommendation']
			approvedRGColumn = riskGroupSheet['Approved']
			rateControlSheet = pd.read_excel(PRd, sheet_name='Rate Controls')
			#print rateControlSheet.shape[0]
			policyIDRCColumn = rateControlSheet['Policy ID']
			rcControlColumn = rateControlSheet['Rate Control Name']
			rcControlIDColumn = rateControlSheet['Rate Control ID']
			rcReqTypeColumn = rateControlSheet['Request Type']
			rcClientIDColumn = rateControlSheet['Client Identifier']
			rcUseXFFColumn = rateControlSheet['Use XFF']
			rcHostsColumn = rateControlSheet['Hostnames']
			rcPathsColumn = rateControlSheet['Paths']
			rcFEColumn = rateControlSheet['File Extensions']
			rcRMColumn = rateControlSheet['Request Methods']
			rcRHColumn = rateControlSheet['Request Headers']
			rcASNColumn = rateControlSheet['ASNumber']
			rcUAColumn = rateControlSheet['User-Agent']
			rcRCColumn = rateControlSheet['Response Codes']
			rcNLColumn = rateControlSheet['Network List']
			currentRCColumn = rateControlSheet['Current']
			recommendationRCColumn = rateControlSheet['Recommendation']
			burstColumn = rateControlSheet['Burst/Rate']
			averageColumn = rateControlSheet['Average/Period']
			approvedRCColumn = rateControlSheet['Approved']
			clientReputationSheet = pd.read_excel(PRd, sheet_name='Client Reputation')
			#print clientReputationSheet.shape[0]
			policyIDCRColumn = clientReputationSheet['Policy ID']
			profileCRColumn = clientReputationSheet['Profile']
			recommendationCRColumn = clientReputationSheet['Recommendation']
			thresholdColumn = clientReputationSheet['Threshold']
			approvedCRColumn = clientReputationSheet['Approved']
			#print url
			#print params
			result = s.get(urljoin(baseurl, url),params=params)
			if result.status_code == 200:
				if result.json()['securityPolicies']:
					APPROVED = True
					RiskGroupTable = tt.Texttable()
					RiskGroupHeader = ['Policy ID','Risk Group','Current Action','Recommended','Ruleset','Correct']
					RiskGroupTable.header(RiskGroupHeader)
					RiskGroupTable.set_cols_width([20,20,20,20,20,20])
					RiskGroupTable.set_cols_align(['c','c','c','c','c','c'])
					RiskGroupTable.set_cols_valign(['m','m','m','m','m','m'])
					wafEvalTable = tt.Texttable()
					wafEvalHeader = ['Policy ID','Risk Group','Current Action','Recommended','Ruleset','Correct']
					wafEvalTable.header(wafEvalHeader)
					wafEvalTable.set_cols_width([20,20,20,20,20,20])
					wafEvalTable.set_cols_align(['c','c','c','c','c','c'])
					wafEvalTable.set_cols_valign(['m','m','m','m','m','m'])
					customRuleTable = tt.Texttable()
					customRuleHeader = ['Policy Name','Policy ID','Rule ID','Name','Version','Action','Recommendation','Correct']
					customRuleTable.header(customRuleHeader)
					customRuleTable.set_cols_width([30,15,15,66,10,10,15,10])
					customRuleTable.set_cols_align(['c','c','c','c','c','c','c','c'])
					customRuleTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
					RateControlTable = tt.Texttable()
					RateControlHeader = ['Policy ID','Rate Control ID','Rate Control Name','Current Action','Recommended','Average/Period','Average Recommended','Burst/Rate','Burst Recommended','Correct']
					RateControlTable.header(RateControlHeader)
					RateControlTable.set_cols_width([15,17,36,15,15,15,17,11,17,7])
					RateControlTable.set_cols_align(['c','c','c','c','c','c','c','c','c','c'])
					RateControlTable.set_cols_valign(['m','m','m','m','m','m','m','m','m','m'])
					ClientRepTable = tt.Texttable()
					ClientRepHeader = ['Policy ID','Profile','Current','Recommendation','Current Threshold','Recommendation','Correct']
					ClientRepTable.header(ClientRepHeader)
					ClientRepTable.set_cols_width([25,49,20,20,20,20,20])
					ClientRepTable.set_cols_align(['c','c','c','c','c','c','c'])
					ClientRepTable.set_cols_valign(['m','m','m','m','m','m','m'])
					exclusionsTable = tt.Texttable()
					exclusionsHeader = ['Policy ID','Rule','Positive Match','Found','Not Found','Action','Recommended Action','Correct']
					exclusionsTable.header(exclusionsHeader)
					exclusionsTable.set_cols_width([15,14,8,48,48,15,15,8])
					exclusionsTable.set_cols_align(['c','c','c','c','c','c','c','c'])
					exclusionsTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
					ruleEvalTable = tt.Texttable()
					ruleEvalHeader = ['Policy ID','Rule','Positive Match','Found','Not Found','Action','Recommended Action','Correct']
					ruleEvalTable.header(ruleEvalHeader)
					ruleEvalTable.set_cols_width([15,14,8,48,48,15,15,8])
					ruleEvalTable.set_cols_align(['c','c','c','c','c','c','c','c'])
					ruleEvalTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
					for i in range (0,wafEvalSheet.shape[0]):
						if approvedEvColumn[i] == 'No':
							#print 'NOT APPROVED'
							pass
						else:
							#print 'APPROVED'
							#print policy['id'],policyIDRGColumn[i]
							for policy in result.json()['securityPolicies']: 	# 1 Deep
								if policy['id'] == policyIDEvColumn[i]:
									try:
										for riskGroup in policy['webApplicationFirewall']['evaluation']['attackGroupActions']:
											#print str(rgControlColumn[i]),str(riskGroup['group'])
											if str(evControlColumn[i]) == str(riskGroup['group']):
												#print str(recommendationEvColumn[i]),str(riskGroup['action'])
												if str(recommendationEvColumn[i]) == str(riskGroup['action']):
													correct = u'\u2713'
												else:
													correct = 'X'
													APPROVED = False
												if str(recommendationRVEvColumn[i]) == str(policy['webApplicationFirewall']['evaluation']['rulesetVersionId']):
													if correct != 'X':
														correct = u'\u2713'
												else:
													correct = 'X'
													APPROVED = False
												#print str(riskGroup['action'])
												tableEvArray = [policyIDEvColumn[i],evControlColumn[i],str(riskGroup['action']),recommendationEvColumn[i],str(policy['webApplicationFirewall']['evaluation']['rulesetVersionId']),correct]
												wafEvalTable.add_row(tableEvArray)
												break
									except:
										#print policy['webApplicationFirewall']['evaluation']['attackGroupActions']
										correct = 'X'
										APPROVED = False
										tableEvArray = [policyIDEvColumn[i],evControlColumn[i],'',recommendationEvColumn[i],'',correct]
										wafEvalTable.add_row(tableEvArray)
					#print policyIDColumn[i],ruleIDColumn[i],selectorsColumn[i],approvedColumn[i]
					EvalTable = wafEvalTable.draw()
					print bcolors.TURQUO+"\nKRS Evaluation Mode:"+bcolors.ENDC
					print EvalTable
					for i in range (0,riskGroupSheet.shape[0]):
						if approvedRGColumn[i] == 'No':
							#print 'NOT APPROVED'
							pass
						else:
							#print 'APPROVED'
							#print policy['id'],policyIDRGColumn[i]
							for policy in result.json()['securityPolicies']: 	# 1 Deep
								if policy['id'] == policyIDRGColumn[i]:
									for riskGroup in policy['webApplicationFirewall']['attackGroupActions']:
										#print str(rgControlColumn[i]),str(riskGroup['group'])
										if str(rgControlColumn[i]) == str(riskGroup['group']):
											#print str(recommendationRGColumn[i]),str(riskGroup['action'])
											if str(recommendationRGColumn[i]) == str(riskGroup['action']):
												correct = u'\u2713'
											else:
												correct = 'X'
												APPROVED = False
											if str(recommendationRVColumn[i]) == str(riskGroup['rulesetVersionId']):
												if correct != 'X':
													correct = u'\u2713'
											else:
												correct = 'X'
												APPROVED = False
											tableRGArray = [policyIDRGColumn[i],rgControlColumn[i],str(riskGroup['action']),recommendationRGColumn[i],str(riskGroup['rulesetVersionId']),correct]
											RiskGroupTable.add_row(tableRGArray)
											break
					#print policyIDColumn[i],ruleIDColumn[i],selectorsColumn[i],approvedColumn[i]
					WAFTable = RiskGroupTable.draw()
					print bcolors.TURQUO+"\nWAF Controls:"+bcolors.ENDC
					print WAFTable
					for i in range (0,ruleEvalSheet.shape[0]):
						if str(approvedREvColumn[i]) == 'No':
							#print 'NOT APPROVED'
							pass
						else:
							#print 'APPROVED'
							#print ruleIDColumn[i]
							notFound = False
							found = []
							notfound = []
							for policy in result.json()['securityPolicies']:
								#print policy['id'],policyIDColumn[i]
								#print str(int(ruleIDColumn[i]))
								#print recommendedColumn[i]
								if str(policy['id']) == policyIDREvColumn[i]:
									try:
										for rules in policy['webApplicationFirewall']['evaluation']['ruleActions']:
											#print str(int(ruleIDColumn[i])),str(rules['id'])
											#print selectorsColumn[i]
											if str(int(ruleIDEvColumn[i])) == str(rules['id']):
												notFound = True
												correct = u'\u2713'
												if str(rules['action']) == recommendedEvColumn[i]:
													correct = u'\u2713'
												else:
													correct = 'X'
													APPROVED = False
												#print selectorsColumn[i]
												positiveMatch = 'PASSED'
												if str(selectorsEvColumn[i]) == 'nan':
													pass
												elif 'IP:' in selectorsEvColumn[i]:
													foundAlready = False
													allIPs = selectorsEvColumn[i].split(':')[1].split('\n')
													#print 'PATHS: ',allPaths
													try:
														for ruleExc in rules['conditions']:
															if ruleExc['type'] == 'ipMatch':
																for exception in allIPs:
																	#print ruleExc['paths']
																	if exception in ruleExc['ips']:
																		found.append('IP:'+exception)
																		if positiveMEvColumn[i] != ruleExc['positiveMatch']:
																			positiveMatch = 'FAILED'
																			correct = 'X'
																			APPROVED = False
																		foundAlready = True
														if foundAlready == False:
															notfound.append('IP:'+allIPs)
															correct = 'X'
															APPROVED = False
													except:
														notfound = allIPs
														correct = 'X'
														APPROVED = False
												elif 'ANY_VALUE' in selectorsEvColumn[i]:
													exception = selectorsEvColumn[i].split(':')[1].strip()
													#print 'PATHS: ',allPaths
													try:
														rules['exception']['headerCookieOrParamValues']
														if exception in rules['exception']['headerCookieOrParamValues']:
																found.append('ANY_VALUE:'+exception)
														else:
															#print 'ARGS:'+exception
															notfound.append('ANY_VALUE:'+exception)
															correct = 'X'
															APPROVED = False
													except:
														notfound = allARGS
														correct = 'X'
														APPROVED = False
												elif 'ARGS' in selectorsEvColumn[i]:
													allARGS = selectorsEvColumn[i].split(':')[1].split('\n')
													#print 'PATHS: ',allPaths
													try:
														for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
															if ruleExc['selector'] == 'ARGS':
																for exception in allARGS:
																	#print ruleExc['names']
																	if exception.strip() in ruleExc['names']:
																		found.append('ARGS:'+exception)
																	else:
																		notfound.append('ARGS:'+exception)
																		correct = 'X'
																		APPROVED = False
													except:
														notfound = allARGS
														correct = 'X'
														APPROVED = False
												elif 'JSON_PAIRS' in selectorsEvColumn[i]:
													allJSON = selectorsEvColumn[i].split(':')[1].split('\n')
													try:
														for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
															if ruleExc['selector'] == 'JSON_PAIRS':
																for exception in allJSON:
																	#print ruleExc['names']
																	if exception.strip() in ruleExc['names']:
																		found.append('JSON_PAIRS:'+exception)
																	else:
																		notfound.append('JSON_PAIRS:'+exception)
																		correct = 'X'
																		APPROVED = False
													except:
														notfound = allJSON
														correct = 'X'
														APPROVED = False
												elif 'XML_PAIRS' in selectorsEvColumn[i]:
													allXML = selectorsEvColumn[i].split(':')[1].split('\n')
													try:
														for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
															if ruleExc['selector'] == 'XML_PAIRS':
																for exception in allXML:
																	#print ruleExc['names']
																	if exception.strip() in ruleExc['names']:
																		found.append('XML_PAIRS:'+exception)
																	else:
																		notfound.append('XML_PAIRS:'+exception)
																		correct = 'X'
																		APPROVED = False
													except:
														notfound = allXML
														correct = 'X'
														APPROVED = False
												elif 'REQUEST_HEADERS' in selectorsEvColumn[i]:
													allHeaders = selectorsEvColumn[i].split(':')[1].split('\n')
													try:
														for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
															if ruleExc['selector'] == 'REQUEST_HEADERS':
																for exception in allHeaders:
																	#print ruleExc['names']
																	if exception.strip() in ruleExc['names']:
																		found.append('REQUEST_HEADERS:'+exception)
																	else:
																		notfound.append('REQUEST_HEADERS:'+exception)
																		correct = 'X'
																		APPROVED = False
													except:
														notfound = allHeaders
														correct = 'X'
														APPROVED = False
												elif 'PREFIX' in selectorsEvColumn[i]:
													allPrefix = selectorsEvColumn[i].split(':')[1].split('\n')
													try:
														for exception in allPrefix:
															#print ruleExc['prefix']
															if exception == rules['exception']['specificHeaderCookieOrParamPrefix']['prefix']:
																found.append('PREFIX:'+exception)
															else:
																notfound.append('PREFIX:'+exception)
																correct = 'X'
																APPROVED = False
													except:
														notfound = allPrefix
														correct = 'X'
														APPROVED = False
												elif 'PATH' in selectorsEvColumn[i]:
													allPaths = selectorsEvColumn[i].split(':')[1].split('\n')
													foundAlready = False
													try:
														for ruleExc in rules['conditions']:
															if ruleExc['type'] == 'pathMatch':
																for exception in allPaths:
																	#print ruleExc['paths']
																	if exception in ruleExc['paths']:
																		found.append('PATHS:'+exception)
																		if positiveMEvColumn[i] != ruleExc['positiveMatch']:
																			positiveMatch = 'FAILED'
																			correct = 'X'
																			APPROVED = False
																		foundAlready = True
														if foundAlready == False:
															notfound.append('PATHS:'+exception)
															correct = 'X'
															APPROVED = False
													except:
														notfound = allPaths
														correct = 'X'
														APPROVED = False
												elif 'HOST' in selectorsEvColumn[i]:
													allHosts = selectorsEvColumn[i].split(':')[1].split('\n')
													foundAlready = False
													try:
														for ruleExc in rules['conditions']:
															if ruleExc['type'] == 'hostMatch':
																for exception in allHosts:
																	#print ruleExc['hosts']
																	if exception in ruleExc['hosts']:
																		found.append('HOST:'+exception)
																		if positiveMEvColumn[i] != ruleExc['positiveMatch']:
																			positiveMatch = 'FAILED'
																			correct = 'X'
																			APPROVED = False
																		foundAlready = True
														if foundAlready == False:
															notfound.append('HOST:'+exception)
															correct = 'X'
															APPROVED = False
													except:
														notfound = allHosts
														correct = 'X'
														APPROVED = False
												elif 'EXT' in selectorsEvColumn[i]:
													allExt = selectorsEvColumn[i].split(':')[1].split('\n')
													foundAlready = False
													try:
														for ruleExc in rules['conditions']:
															if ruleExc['type'] == 'extensionMatch':
																for exception in allExt:
																	#print ruleExc['paths']
																	if exception in ruleExc['extensions']:
																		found.append('EXT:'+exception)
																		if positiveMEvColumn[i] != ruleExc['positiveMatch']:
																			positiveMatch = 'FAILED'
																			correct = 'X'
																			APPROVED = False
																		foundAlready = True
														if foundAlready == False:
															notfound.append('EXT:'+exception)
															correct = 'X'
															APPROVED = False
													except:
														notfound = allExt
														correct = 'X'
														APPROVED = False
												elif 'METHOD' in selectorsEvColumn[i]:
													allMeth = selectorsEvColumn[i].split(':')[1].split('\n')
													foundAlready = False
													try:
														for ruleExc in rules['conditions']:
															if ruleExc['type'] == 'requestMethodMatch':
																for exception in allMeth:
																	#print ruleExc['paths']
																	if exception in ruleExc['methods']:
																		found.append('METHOD:'+exception)
																		if positiveMEvColumn[i] != ruleExc['positiveMatch']:
																			positiveMatch = 'FAILED'
																			correct = 'X'
																			APPROVED = False
																		foundAlready = True
														if foundAlready == False:
															notfound.append('METHOD:'+exception)
															correct = 'X'
															APPROVED = False
													except:
														notfound = allMeth
														correct = 'X'
														APPROVED = False
												elif 'REQUEST_COOKIES' in selectorsEvColumn[i]:
													allCookies = selectorsEvColumn[i].split(':')[1].split('\n')
													try:
														for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
															if ruleExc['selector'] == 'REQUEST_COOKIES':
																for exception in allCookies:
																	#print ruleExc['names']
																	if exception in ruleExc['names']:
																		found.append('REQUEST_COOKIES:'+exception)
																	else:
																		notfound.append('REQUEST_COOKIES:'+exception)
																		correct = 'X'
																		APPROVED = False
													except:
														notfound = allCookies
														correct = 'X'
														APPROVED = False

												ruleEvalArray = [policyIDREvColumn[i],ruleIDEvColumn[i],positiveMatch,','.join(found),','.join(notfound),rules['action'],recommendedEvColumn[i],correct]
												#print tableArray
												ruleEvalTable.add_row(ruleEvalArray)
										if notFound == False:
											#print recommendedColumn[i]
											#print ruleIDColumn[i]
											#print policyIDColumn[i]
											if recommendedEvColumn[i] == 'not used':
												ruleEvalArray = [policyIDREvColumn[i],ruleIDEvColumn[i],positiveMatch,','.join(found),','.join(notfound),'not used',recommendedEvColumn[i],correct]
												#print tableArray
												ruleEvalTable.add_row(ruleEvalArray)
									except:
										correct = 'X'
										APPROVED = False
										ruleEvalArray = [policyIDREvColumn[i],ruleIDEvColumn[i],positiveMatch,'',selectorsEvColumn[i],'',recommendedEvColumn[i],correct]
										#print tableArray
										ruleEvalTable.add_row(ruleEvalArray)
							else:
								pass
					ruleEvTable = ruleEvalTable.draw()
					print bcolors.TURQUO+"\nExclusions/Conditions KRS Evaluation Mode:"+bcolors.ENDC
					print ruleEvTable
					for i in range (0,exclusionsSheet.shape[0]):
						if str(approvedColumn[i]) == 'No':
							#print 'NOT APPROVED'
							pass
						else:
							#print 'APPROVED'
							#print ruleIDColumn[i]
							notFound = False
							found = []
							notfound = []
							for policy in result.json()['securityPolicies']:
								#print policy['id'],policyIDColumn[i]
								#print str(int(ruleIDColumn[i]))
								#print recommendedColumn[i]
								if str(policy['id']) == policyIDColumn[i]:
									for rules in policy['webApplicationFirewall']['ruleActions']:
										#print str(int(ruleIDColumn[i])),str(rules['id'])
										#print selectorsColumn[i]
										if str(int(ruleIDColumn[i])) == str(rules['id']):
											notFound = True
											correct = u'\u2713'
											if str(rules['action']) == recommendedColumn[i]:
												correct = u'\u2713'
											else:
												correct = 'X'
												APPROVED = False
											#print selectorsColumn[i]
											positiveMatch = 'PASSED'
											if str(selectorsColumn[i]) == 'nan':
												pass
											elif 'IP:' in selectorsColumn[i]:
												foundAlready = False
												allIPs = selectorsColumn[i].split(':')[1].split('\n')
												#print 'PATHS: ',allPaths
												try:
													for ruleExc in rules['conditions']:
														if ruleExc['type'] == 'ipMatch':
															for exception in allIPs:
																#print ruleExc['paths']
																if exception in ruleExc['ips']:
																	found.append('IP:'+exception)
																	if positiveMColumn[i] != ruleExc['positiveMatch']:
																		positiveMatch = 'FAILED'
																		correct = 'X'
																		APPROVED = False
																	foundAlready = True
													if foundAlready == False:
														notfound.append('IP:'+exception)
														correct = 'X'
														APPROVED = False
												except:
													notfound = allIPs
													correct = 'X'
													APPROVED = False
											elif 'ANY_VALUE' in selectorsColumn[i]:
												exception = selectorsColumn[i].split(':')[1].strip()
												#print 'PATHS: ',allPaths
												try:
													rules['exception']['headerCookieOrParamValues']
													if exception in rules['exception']['headerCookieOrParamValues']:
															found.append('ANY_VALUE:'+exception)
													else:
														#print 'ARGS:'+exception
														notfound.append('ANY_VALUE:'+exception)
														correct = 'X'
														APPROVED = False
												except:
													notfound = allARGS
													correct = 'X'
													APPROVED = False
											elif 'ARGS' in selectorsColumn[i]:
												allARGS = selectorsColumn[i].split(':')[1].split('\n')
												#print 'PATHS: ',allPaths
												try:
													for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
														if ruleExc['selector'] == 'ARGS':
															for exception in allARGS:
																#print ruleExc['names']
																if exception.strip() in ruleExc['names']:
																	found.append('ARGS:'+exception)
																else:
																	notfound.append('ARGS:'+exception)
																	correct = 'X'
																	APPROVED = False
												except:
													notfound = allARGS
													correct = 'X'
													APPROVED = False
											elif 'JSON_PAIRS' in selectorsColumn[i]:
												allJSON = selectorsColumn[i].split(':')[1].split('\n')
												try:
													for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
														if ruleExc['selector'] == 'JSON_PAIRS':
															for exception in allJSON:
																#print ruleExc['names']
																if exception.strip() in ruleExc['names']:
																	found.append('JSON_PAIRS:'+exception)
																else:
																	notfound.append('JSON_PAIRS:'+exception)
																	correct = 'X'
																	APPROVED = False
												except:
													notfound = allJSON
													correct = 'X'
													APPROVED = False
											elif 'XML_PAIRS' in selectorsColumn[i]:
												allXML = selectorsColumn[i].split(':')[1].split('\n')
												try:
													for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
														if ruleExc['selector'] == 'XML_PAIRS':
															for exception in allXML:
																#print ruleExc['names']
																if exception.strip() in ruleExc['names']:
																	found.append('XML_PAIRS:'+exception)
																else:
																	notfound.append('XML_PAIRS:'+exception)
																	correct = 'X'
																	APPROVED = False
												except:
													notfound = allXML
													correct = 'X'
													APPROVED = False
											elif 'REQUEST_HEADERS' in selectorsColumn[i]:
												allHeaders = selectorsColumn[i].split(':')[1].split('\n')
												try:
													for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
														if ruleExc['selector'] == 'REQUEST_HEADERS':
															for exception in allHeaders:
																#print ruleExc['names']
																if exception.strip() in ruleExc['names']:
																	found.append('REQUEST_HEADERS:'+exception)
																else:
																	notfound.append('REQUEST_HEADERS:'+exception)
																	correct = 'X'
																	APPROVED = False
												except:
													notfound = allHeaders
													correct = 'X'
													APPROVED = False
											elif 'PREFIX' in selectorsColumn[i]:
												allPrefix = selectorsColumn[i].split(':')[1].split('\n')
												try:
													for exception in allPrefix:
														#print ruleExc['prefix']
														if exception == rules['exception']['specificHeaderCookieOrParamPrefix']['prefix']:
															found.append('PREFIX:'+exception)
														else:
															notfound.append('PREFIX:'+exception)
															correct = 'X'
															APPROVED = False
												except:
													notfound = allPrefix
													correct = 'X'
													APPROVED = False
											elif 'PATH' in selectorsColumn[i]:
												allPaths = selectorsColumn[i].split(':')[1].split('\n')
												foundAlready = False
												try:
													for ruleExc in rules['conditions']:
														if ruleExc['type'] == 'pathMatch':
															for exception in allPaths:
																#print ruleExc['paths']
																if exception in ruleExc['paths']:
																	found.append('PATHS:'+exception)
																	if positiveMColumn[i] != ruleExc['positiveMatch']:
																		positiveMatch = 'FAILED'
																		correct = 'X'
																		APPROVED = False
																	foundAlready = True
													if foundAlready == False:
														notfound.append('PATHS:'+exception)
														correct = 'X'
														APPROVED = False
												except:
													notfound = allPaths
													correct = 'X'
													APPROVED = False
											elif 'HOST' in selectorsColumn[i]:
												allHosts = selectorsColumn[i].split(':')[1].split('\n')
												foundAlready = False
												try:
													for ruleExc in rules['conditions']:
														if ruleExc['type'] == 'hostMatch':
															for exception in allHosts:
																#print ruleExc['hosts']
																if exception in ruleExc['hosts']:
																	found.append('HOST:'+exception)
																	if positiveMColumn[i] != ruleExc['positiveMatch']:
																		positiveMatch = 'FAILED'
																		correct = 'X'
																		APPROVED = False
																	foundAlready = True
													if foundAlready == False:
														notfound.append('HOST:'+exception)
														correct = 'X'
														APPROVED = False
												except:
													notfound = allHosts
													correct = 'X'
													APPROVED = False
											elif 'EXT' in selectorsColumn[i]:
												allExt = selectorsColumn[i].split(':')[1].split('\n')
												foundAlready = False
												try:
													for ruleExc in rules['conditions']:
														if ruleExc['type'] == 'extensionMatch':
															for exception in allExt:
																#print ruleExc['paths']
																if exception in ruleExc['extensions']:
																	found.append('EXT:'+exception)
																	if positiveMColumn[i] != ruleExc['positiveMatch']:
																		positiveMatch = 'FAILED'
																		correct = 'X'
																		APPROVED = False
																	foundAlready = True
													if foundAlready == False:
														notfound.append('EXT:'+exception)
														correct = 'X'
														APPROVED = False
												except:
													notfound = allExt
													correct = 'X'
													APPROVED = False
											elif 'METHOD' in selectorsColumn[i]:
												allMeth = selectorsColumn[i].split(':')[1].split('\n')
												foundAlready = False
												try:
													for ruleExc in rules['conditions']:
														if ruleExc['type'] == 'requestMethodMatch':
															for exception in allMeth:
																#print ruleExc['paths']
																if exception in ruleExc['methods']:
																	found.append('METHOD:'+exception)
																	if positiveMColumn[i] != ruleExc['positiveMatch']:
																		positiveMatch = 'FAILED'
																		correct = 'X'
																		APPROVED = False
																	foundAlready = True
													if foundAlready == False:
														notfound.append('METHOD:'+exception)
														correct = 'X'
														APPROVED = False
												except:
													notfound = allMeth
													correct = 'X'
													APPROVED = False
											elif 'REQUEST_COOKIES' in selectorsColumn[i]:
												allCookies = selectorsColumn[i].split(':')[1].split('\n')
												try:
													for ruleExc in rules['exception']['specificHeaderCookieOrParamNames']:
														if ruleExc['selector'] == 'REQUEST_COOKIES':
															for exception in allCookies:
																#print ruleExc['names']
																if exception in ruleExc['names']:
																	found.append('REQUEST_COOKIES:'+exception)
																else:
																	notfound.append('REQUEST_COOKIES:'+exception)
																	correct = 'X'
																	APPROVED = False
												except:
													notfound = allCookies
													correct = 'X'
													APPROVED = False

											tableArray = [policyIDColumn[i],ruleIDColumn[i],positiveMatch,','.join(found),','.join(notfound),rules['action'],recommendedColumn[i],correct]
											#print tableArray
											exclusionsTable.add_row(tableArray)
									if notFound == False:
										#print recommendedColumn[i]
										#print ruleIDColumn[i]
										#print policyIDColumn[i]
										if recommendedColumn[i] == 'not used':
											breaktableArray = [policyIDColumn[i],ruleIDColumn[i],positiveMatch,','.join(found),','.join(notfound),'not used',recommendedColumn[i],correct]
											#print tableArray
											exclusionsTable.add_row(breaktableArray)
							else:
								pass
					FinalTable = exclusionsTable.draw()
					print bcolors.TURQUO+"\nExclusions/Conditions:"+bcolors.ENDC
					print FinalTable
					for i in range (0,rateControlSheet.shape[0]):
						#print i
						#print approvedRCColumn
						if approvedRCColumn[i] == 'No':
							#print 'NOT APPROVED'
							pass
						else:
							#print 'APPROVED'
							#print ruleIDColumn[i]
							#print str(rcControlIDColumn[i])
							if str(rcControlIDColumn[i]) != 'nan':
								for rateArray in result.json()['ratePolicies']:
									#print policy['id'],policyIDColumn[i]
									'''
									rcReqTypeColumn = rateControlSheet['Request Type']
									rcClientIDColumn = rateControlSheet['Client Identifier']
									rcUseXFFColumn = rateControlSheet['Use XFF']
									rcHostsColumn = rateControlSheet['Hostnames']
									rcPathsColumn = rateControlSheet['Paths']
									rcFEColumn = rateControlSheet['File Extensions']
									rcRMColumn = rateControlSheet['Request Methods']
									rcRHColumn = rateControlSheet['Request Headers']
									rcASNColumn = rateControlSheet['ASNumber']
									rcUAColumn = rateControlSheet['User-Agent']
									rcRCColumn = rateControlSheet['Response Codes']
									rcNLColumn = rateControlSheet['Network List']
									'''
									if rateArray['id'] == rcControlIDColumn[i]:
										correct = u'\u2713'
										if rateArray['averageThreshold'] != averageColumn[i]:
											correct = 'X'
											APPROVED = False
										if rateArray['burstThreshold'] != burstColumn[i]:
											correct = 'X'
											APPROVED = False
										if rateArray['requestType'] != rcReqTypeColumn[i]:
											correct = 'X'
											APPROVED = False
										if rateArray['clientIdentifier'] != rcClientIDColumn[i]:
											correct = 'X'
											APPROVED = False
										if rateArray['useXForwardForHeaders'] != rcUseXFFColumn[i]:
											correct = 'X'
											APPROVED = False
										if str(rcHostsColumn[i]) != 'nan':
											try:
												rateArray['hostnames']
												if ','.join(rateArray['hostnames']) != str(rcHostsColumn[i]):
													correct = 'X'
													APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										if str(rcPathsColumn[i]) != 'nan':
											try:
												rateArray['path']
												if rateArray['path']['positiveMatch'] == False:
													if 'Negative Match: '+','.join(rateArray['path']['values']) != rcPathsColumn[i]:
														correct = 'X'
														APPROVED = False
												elif 'Positive Match: '+','.join(rateArray['path']['values']) != rcPathsColumn[i]:
													correct = 'X'
													APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										if str(rcFEColumn[i]) != 'nan':
											try:
												rateArray['fileExtensions']
												if rateArray['fileExtensions']['positiveMatch'] == False:
													if 'Negative Match: '+','.join(rateArray['fileExtensions']['values']) != rcFEColumn[i]:
														correct = 'X'
														APPROVED = False
												elif 'Positive Match: '+','.join(rateArray['fileExtensions']['values']) != rcFEColumn[i]:
													correct = 'X'
													APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										if str(rcRMColumn[i]) != 'nan':
											try:
												rateArray['additionalMatchOptions']
												for addCon in rateArray['additionalMatchOptions']:
													if addCon['type'] == 'RequestMethodCondition':
														if addCon['positiveMatch'] == False:
															if 'Negative Match: '+','.join(addCon['values']) != rcRMColumn[i]:
																correct = 'X'
																APPROVED = False
														elif 'Positive Match: '+','.join(addCon['values']) != rcRMColumn[i]:
															correct = 'X'
															APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										if str(rcRHColumn[i]) != 'nan':
											try:
												rateArray['additionalMatchOptions']
												for addCon in rateArray['additionalMatchOptions']:
													if addCon['type'] == 'RequestHeaderCondition':
														if addCon['positiveMatch'] == False:
															if 'Negative Match: '+','.join(addCon['values']) != rcRHColumn[i]:
																correct = 'X'
																APPROVED = False
														elif 'Positive Match: '+','.join(addCon['values']) != rcRHColumn[i]:
															correct = 'X'
															APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										if str(rcASNColumn[i]) != 'nan':
											try:
												rateArray['additionalMatchOptions']
												for addCon in rateArray['additionalMatchOptions']:
													if addCon['type'] == 'AsNumberCondition':
														if addCon['positiveMatch'] == False:
															if 'Negative Match: '+','.join(addCon['values']) != rcASNColumn[i]:
																correct = 'X'
																APPROVED = False
														elif 'Positive Match: '+','.join(addCon['values']) != rcASNColumn[i]:
															correct = 'X'
															APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										if str(rcUAColumn[i]) != 'nan':
											try:
												rateArray['additionalMatchOptions']
												for addCon in rateArray['additionalMatchOptions']:
													if addCon['type'] == 'UserAgentCondition':
														if addCon['positiveMatch'] == False:
															if 'Negative Match: '+','.join(addCon['values']) != rcUAColumn[i]:
																correct = 'X'
																APPROVED = False
														elif 'Positive Match: '+','.join(addCon['values']) != rcUAColumn[i]:
															correct = 'X'
															APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										if str(rcRCColumn[i]) != 'nan':
											try:
												rateArray['additionalMatchOptions']
												for addCon in rateArray['additionalMatchOptions']:
													if addCon['type'] == 'ResponseStatusCondition':
														if addCon['positiveMatch'] == False:
															if 'Negative Match: '+','.join(addCon['values']) != rcRCColumn[i]:
																correct = 'X'
																APPROVED = False
														elif 'Positive Match: '+','.join(addCon['values']) != rcRCColumn[i]:
															correct = 'X'
															APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										if str(rcNLColumn[i]) != 'nan':
											try:
												rateArray['additionalMatchOptions']
												for addCon in rateArray['additionalMatchOptions']:
													if addCon['type'] == 'NetworkListCondition':
														if addCon['positiveMatch'] == False:
															if 'Negative Match: '+','.join(addCon['values']) != rcNLColumn[i]:
																correct = 'X'
																APPROVED = False
														elif 'Positive Match: '+','.join(addCon['values']) != rcNLColumn[i]:
															correct = 'X'
															APPROVED = False
											except:
												correct = 'X'
												APPROVED = False
										else:
											pass
										for policy in result.json()['securityPolicies']:
											if policy['id'] == policyIDRCColumn[i]:
												for rateP in policy['ratePolicyActions']:
													if rateP['id'] == rateArray['id']:
														if rateP['ipv4Action'] != recommendationRCColumn[i]:
															correct = 'X'
														tableRCArray = [policyIDRCColumn[i],rcControlIDColumn[i],rateArray['name'],rateP['ipv4Action'],recommendationRCColumn[i],rateArray['averageThreshold'],averageColumn[i],rateArray['burstThreshold'],burstColumn[i],correct]
														RateControlTable.add_row(tableRCArray)
													else:
														pass
										break
									else:
										pass
							else:
								for policy in result.json()['securityPolicies']:
									if policy['id'] == policyIDRCColumn[i]:
										correct = u'\u2713'
										if policy['slowPost']['action'] != recommendationRCColumn[i]:
											correct = 'X'
										if policy['slowPost']['slowRateThreshold']['rate'] != burstColumn[i]:
											correct = 'X'
										if policy['slowPost']['slowRateThreshold']['period'] != averageColumn[i]:
											correct = 'X'
										tableRCArray = [policyIDRCColumn[i],'NA',rcControlColumn[i],policy['slowPost']['action'],recommendationRCColumn[i],policy['slowPost']['slowRateThreshold']['period'],averageColumn[i],policy['slowPost']['slowRateThreshold']['rate'],burstColumn[i],correct]
										RateControlTable.add_row(tableRCArray)
								pass

					FinalTable = RateControlTable.draw()
					print bcolors.TURQUO+"\nRate Control Table:"+bcolors.ENDC
					print FinalTable
					for i in range (0,clientReputationSheet.shape[0]):
						#print i
						#print approvedRCColumn
						if approvedCRColumn[i] == 'No':
							#print 'NOT APPROVED'
							pass
						else:
							#print 'APPROVED'
							#print ruleIDColumn[i]
							'''
							policyIDCRColumn = clientReputationSheet['Policy ID']
							profileCRColumn = clientReputationSheet['Profile']
							recommendationCRColumn = clientReputationSheet['Recommendation']
							thresholdColumn = clientReputationSheet['Threshold']
							approvedCRColumn = clientReputationSheet['Approved']
							ClientRepHeader = ['Policy ID','Profile','Current','Recommendation','Current Threshold','Recommendation','Correct']
							'''
							#print str(rcControlIDColumn[i])
							try:
								result.json()['reputationProfiles']
								for clientRepArray in result.json()['reputationProfiles']:
									#print policy['id'],policyIDColumn[i]
									if clientRepArray['name'] == profileCRColumn[i]:
										correct = u'\u2713'
										if clientRepArray['threshold'] != thresholdColumn[i]:
											correct = 'X'
										for policy in result.json()['securityPolicies']:
											if policy['id'] == policyIDCRColumn[i]:
												for clientCR in policy['clientReputation']['reputationProfileActions']:
													if clientCR['id'] == clientRepArray['id']:
														if clientCR['action'] != recommendationCRColumn[i]:
															correct = 'X'
														tableCRArray = [policyIDCRColumn[i],profileCRColumn[i],clientCR['action'],recommendationCRColumn[i],clientRepArray['threshold'],thresholdColumn[i],correct]
														ClientRepTable.add_row(tableCRArray)
													else:
														pass
										break
									else:
										pass

							except:
								pass
					try:
						result.json()['reputationProfiles']
						FinalTable = ClientRepTable.draw()
						print bcolors.TURQUO+"\nClient Reputation Table Table:"+bcolors.ENDC
						print FinalTable
					except:
						pass
					for i in range (0,customSheet.shape[0]):
						if approvedCuColumn[i] == 'No':
							#print 'NOT APPROVED'
							pass
						else:
							#print 'APPROVED'
							#print policy['id'],policyIDRGColumn[i]
							# ['Policy Name','Policy ID','Rule ID','Name','Version','Action','Recommendation','Correct']
							notFound = False
							for policy in result.json()['securityPolicies']: 	# 1 Deep
								if policy['id'] == policyCuIDColumn[i]:
									for rule in policy['customRuleActions']:
										#print str(rgControlColumn[i]),str(riskGroup['group'])
										if str(ruleIDCuColumn[i]) == str(rule['id']):
											#print str(recommendationRGColumn[i]),str(riskGroup['action'])
											notFound = True
											if str(recommendationCuColumn[i]) == str(rule['action']):
												correct = u'\u2713'
											else:
												correct = 'X'
												APPROVED = False
											for customInfo in result.json()['customRules']:
												if str(customInfo['id']) == str(rule['id']):
													tableRGArray = [policy['name'],policyCuIDColumn[i],ruleIDCuColumn[i],customInfo['name'],customInfo['version'],rule['action'],recommendationCuColumn[i],correct]
													customRuleTable.add_row(tableRGArray)
													break
									if notFound == False:
										correct = 'X'
										APPROVED = False
										tableRGArray = [policy['name'],policyCuIDColumn[i],ruleIDCuColumn[i],'','','not used',recommendationCuColumn[i],correct]
										customRuleTable.add_row(tableRGArray)
					#print policyIDColumn[i],ruleIDColumn[i],selectorsColumn[i],approvedColumn[i]
					CustomTable = customRuleTable.draw()
					print bcolors.TURQUO+"\nCustom Rules:"+bcolors.ENDC
					print CustomTable
					if APPROVED == True:
						print bcolors.TURQUO+'\n\n[STATUS] '+bcolors.WARNING+'APPROVED: '+bcolors.ENDC+'YES'
					else:
						print bcolors.TURQUO+'\n\n[STATUS] '+bcolors.WARNING+'NOT APPROVED: '+bcolors.FAIL+'Peer Review Failed.'+bcolors.ENDC
						print bcolors.TURQUO+'[STATUS] '+bcolors.WARNING+'NOT APPROVED: '+bcolors.FAIL+'Please check your changes.'+bcolors.ENDC
			else:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
				print result.content
		endTime = datetime.datetime.now()
		totalTime = endTime - startTime
		#print minutes,secs
		seconds = totalTime.total_seconds()
		hours = seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60
		print bcolors.TURQUO+'[OVERALL] '+bcolors.WARNING+'Completion Time: '+bcolors.ENDC+'{} minutes, {} seconds'.format(int(minutes), round(seconds,2))
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'export':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyVersion:
			Version = findAppsecVersion(configId,respjson)
			if Version["Production"] != None:
				propertyVersion = str(Version["Production"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using active PROD version: "+propertyVersion+bcolors.ENDC
			else:
				propertyVersion = str(Version["Latest"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
		url = '/appsec/v1/export/configs/'+configId+'/versions/'+str(propertyVersion)
		#print url
		#print params
		result = s.get(urljoin(baseurl, url),params=params)
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				#print bcolors.TURQUO+"\n\n-----------------------------------------------------------------"+bcolors.ENDC
				AppsecExport(result.json()['configName'],propertyVersion,result.json(),respjson)
				sys.exit()
			else:
				if rateControls:
					RCTable = tt.Texttable()
					RCheader = ['ID','Name','Request Type','RC Type', 'Identifier', 'Burst', 'Average', 'Used' ,'Description']
					RCTable.header(RCheader)
					RCTable.set_cols_width([8,30,15,8,12,8,8,8,55])
					RCTable.set_cols_align(['c','c','c','c','c','c','c','c','c'])
					RCTable.set_cols_valign(['m','m','m','m','m','m','m','m','m'])
					try:
						result.json()["ratePolicies"]
						for item in result.json()["ratePolicies"]:
							try:
								item["description"]
								description = item["description"]
							except:
								description = None
							RCrow = [item['id'],item['name'],item['requestType'],item["type"],item["clientIdentifier"], item["burstThreshold"], item["averageThreshold"], str(item["used"]),description]
							RCTable.add_row(RCrow)
							#try:
							#	item["additionalMatchOptions"]
							#	tablelength = len(item["additionalMatchOptions"])
							#except:
							#	tablelength = 0
							#Matchheader = []
							#MatchRow = []
							#try:
							#	item["fileExtensions"]
							#	Matchheader.append(fileExtensions)
							#	MatchRow.append(item["fileExtensions"]["values"])
							#	tablelength = tablelength + 1
							#except:
							#	pass
							#try:
							#	item["additionalMatchOptions"]
							#	for match in item["additionalMatchOptions"]:
							#		Matchheader.append(match["type"])
							#		MatchRow.append(match["values"])
							#except:
							#	pass
							#cols = [35] * tablelength
							#align = ['c'] * tablelength
							#valign = ['m'] * tablelength
							#MatchTable = tt.Texttable()
							#MatchTable.header(Matchheader)
							#MatchTable.set_cols_width(cols)
							#MatchTable.set_cols_align(align)
							#MatchTable.set_cols_valign(valign)
							#MatchTable.add_row(MatchRow)
							#print "Conditions:"
							#print MatchConditionTable
						#MatchConditionTable = MatchTable.draw()
						RateControlTable = RCTable.draw()
						print bcolors.TURQUO+"\nRate Controls:"+bcolors.ENDC
						print RateControlTable
					except:
						pass
					print bcolors.TURQUO+"\n\n-----------------------------------------------------------------"+bcolors.ENDC
				elif wafrules:
					wafRuleSet = result.json()['rulesets']
					for item in result.json()["securityPolicies"]:
						try:
							item['webApplicationFirewall']
							print bcolors.WHITE+"\nPolicy: "+item["name"]+bcolors.ENDC
							#actionarray = []
							#ruleidarray = []
							#ruleSetVersion = []
							#ruleCondition = []
							RuleTable = tt.Texttable()
							Ruleheader = ['ID','Action','Exceptions']
							RuleTable.header(Ruleheader)
							RuleTable.set_cols_width([15,15,15])
							RuleTable.set_cols_align(['c','c','c'])
							RuleTable.set_cols_valign(['m','m','m'])
							for rule in item['webApplicationFirewall']['ruleActions']:
								#actionarray.append(rule['action'])
								#ruleidarray.append(rule['id'])
								#ruleSetVersion.append(rule['rulesetVersionId'])
								try:
									rule['conditions']
									RuleRow = [rule['id'],rule['action'],'Yes']
								except:
									RuleRow = [rule['id'],rule['action'],'No']
								RuleTable.add_row(RuleRow)
							currentRules = RuleTable.draw()
							#print bcolors.WHITE+"WAF Rules:"+bcolors.ENDC
							print currentRules
						except:
							pass
					print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
				elif exceptions:
					arrayWriter = []
					with open('files/'+AccountSwitch+'-Exceptions.csv', 'wb') as myfile:
						wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
						header = ['Account ID','Configuration ID','Configuration Name','PROD  Version','Policy Name','Policy ID','Rule','Action','Exception','Condition']
						wr.writerow(header)
						for item in result.json()["securityPolicies"]:
							try:
								item['webApplicationFirewall']['ruleActions']
								if not ruleId:
									print bcolors.TURQUO+"\nPolicy ID: "+item["id"]+bcolors.ENDC
									print bcolors.TURQUO+"Policy Name: "+item["name"]+bcolors.ENDC
								#actionarray = []
								#ruleidarray = []
								#ruleSetVersion = []
								#ruleCondition = []
								ExceptionTable = tt.Texttable()
								Exceptionheader = ['Rule ID', 'Exceptions','Conditions']
								ExceptionTable.header(Exceptionheader)
								ExceptionTable.set_cols_width([25,65,65])
								ExceptionTable.set_cols_align(['c','c','c'])
								ExceptionTable.set_cols_valign(['m','m','m'])
								for rule in item['webApplicationFirewall']['ruleActions']:
									#print AccountSwitch
									#print result.json()['configId']
									#print result.json()['configName']
									#print result.json()['version']
									#print item['name']
									#print item['id']
									#print rule['id']
									if ruleId:
										#print ruleId
										#print rule['id']
										if str(rule['id']) == ruleId:
											print bcolors.TURQUO+"\n\n-----------------------------------------------------------------"+bcolors.ENDC
											print bcolors.TURQUO+"\nPolicy ID: "+item["id"]+bcolors.ENDC
											print bcolors.TURQUO+"Policy Name: "+item["name"]+bcolors.ENDC
											conditions = []
											exceptions = []
											#mylist =  [AccountSwitchKey,result.json()['configId'],result.json()['configName'],result.json()['version'],item['name'].encode('utf-8').strip(),item['id'],]
											try:
												rule['conditions']
												conditions.append(rule['conditions'])
											except:
												pass
											try:
												rule['exception']
												exception.append(rule['exception'])
											except:
												pass
											if conditions:
												if exceptions:
													RuleRow = [rule['id'],conditions]
													ExceptionTable.add_row(RuleRow)
													ExcRules = ExceptionTable.draw()
													print ExcRules
											else:
												print bcolors.WARNING+"\nNo Exceptions or Conditions found."+bcolors.ENDC
											print bcolors.TURQUO+"\n\n-----------------------------------------------------------------"+bcolors.ENDC
											continue
									else:
										conditions = []
										exceptions = []
										#print rule
										try:
											rule['conditions']
											#print rule['conditions']
											#mylist =  [AccountSwitch,result.json()['configId'],result.json()['configName'],result.json()['version'],item['name'].encode('utf-8').strip(),item['id'],rule['id'],rule['action'],"None",rule['conditions']]
											Condition = rule['conditions']
											conditions.append(rule['conditions'])
											#print rule['conditions']
										except:
											Condition = None
										#print 'Finished Conditions'
										try:
											rule['exception']
											#print rule['exception']
											#mylist =  [AccountSwitch,result.json()['configId'],result.json()['configName'],result.json()['version'],item['name'].encode('utf-8').strip(),item['id'],rule['id'],rule['action'],rule['exception'],"None"]
											Exception = rule['exception']
											exceptions.append(rule['exception'])
											try:
												rule['exception']['specificHeaderCookieOrParamNames']['names']
												excArray = []
												#print 'Rule HeaderCookieParam Names:',rule['id']
												#print 'Selector:',rule['exception']['specificHeaderCookieOrParamNames']['selector']
												for value in rule['exception']['specificHeaderCookieOrParamNames']['names']:
													excArray.append(value)
												#print ','.join(excArray)
												#print '\n'
											except:
												pass
											try:
												rule['exception']['specificHeaderCookieOrParamPrefix']['prefix']
												#print 'Rule Prefix:',rule['id']
												#print 'Selector:',rule['exception']['specificHeaderCookieOrParamPrefix']['selector']
												#print 'Value:',rule['exception']['specificHeaderCookieOrParamPrefix']['prefix']
												#print '\n'
											except:
												pass
											try:
												rule['exception']['headerCookieOrParamValues']
												excArray = []
												#print 'Rule HeaderCookieParam Values:',rule['id']
												for value in rule['exception']['headerCookieOrParamValues']:
													excArray.append(value)
												#print ','.join(excArray)
												#print '\n'
											except:
												pass
										except:
											Exception = None
										mylist =  [AccountSwitch,result.json()['configId'],result.json()['configName'],result.json()['version'],item['name'].encode('utf-8').strip(),item['id'],rule['id'],rule['action'],Exception,Condition]
										#print 'Finished Exceptions'
										#print str(Exception)
										#print str(Condition)
										if Exception != None or Condition != None:
											RuleRow = [rule['id'],Exception,Condition]
											ExceptionTable.add_row(RuleRow)
										else:
											#print 'No Conditions/Exceptions'
											mylist =  [AccountSwitch,result.json()['configId'],result.json()['configName'],result.json()['version'],item['name'].encode('utf-8').strip(),item['id'],rule['id'],rule['action'],"None","None"]
										#print mylist
										arrayWriter.append(mylist)
										#if conditions:
										#	RuleRow = [rule['id'],conditions]
										#	ExceptionTable.add_row(RuleRow)
										#else:
										#	pass
										#print "Finished Successfully"
								if not ruleId:
									ExcRules = ExceptionTable.draw()
									print bcolors.WHITE+"WAF Rules:"+bcolors.ENDC
									print ExcRules
							except:
								pass
						wr.writerows(arrayWriter)
					try:
						os.stat('files/'+AccountSwitch+'-Exceptions.csv')
						print bcolors.TURQUO+'\n------------------------------------------------------------------------------------------------------------------------'
						print bcolors.TURQUO+'[APPSEC]'+bcolors.ENDC+' CSV report generated. Filename: files/'+AccountSwitch+'-Exceptions.csv'
						print bcolors.TURQUO+'------------------------------------------------------------------------------------------------------------------------'
					except:
						pass
					print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
				elif customRules:
					for item in result.json()["securityPolicies"]:
						try:
							item['customRuleActions']
							if not ruleId:
								print bcolors.TURQUO+"\nPolicy ID: "+item["id"]+bcolors.ENDC
								print bcolors.TURQUO+"Policy Name: "+item["name"]+bcolors.ENDC
							#actionarray = []
							#ruleidarray = []
							#ruleSetVersion = []
							#ruleCondition = []
							RuleTable = tt.Texttable()
							Ruleheader = ['ID','Action']
							RuleTable.header(Ruleheader)
							RuleTable.set_cols_width([25,25])
							RuleTable.set_cols_align(['c','c'])
							RuleTable.set_cols_valign(['m','m'])
							for rule in item['customRuleActions']:
								#actionarray.append(rule['action'])
								#ruleidarray.append(rule['id'])
								#ruleSetVersion.append(rule['rulesetVersionId'])
								if ruleId:
									#print ruleId
									#print rule['id']
									if str(rule['id']) == ruleId:
										print bcolors.TURQUO+"\nPolicy ID: "+item["id"]+bcolors.ENDC
										print bcolors.TURQUO+"Policy Name: "+item["name"]+bcolors.ENDC
										RuleRow = [rule['id'],rule['action']]
										RuleTable.add_row(RuleRow)
										currentRules = RuleTable.draw()
										print currentRules
										continue
								else:
									RuleRow = [rule['id'],rule['action']]
									RuleTable.add_row(RuleRow)
							if not ruleId:
								currentRules = RuleTable.draw()
								#print bcolors.WHITE+"WAF Rules:"+bcolors.ENDC
								print currentRules
						except:
							pass
					print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
				else:
					print bcolors.TURQUO+"\nSecurity Policies:"+bcolors.ENDC
					for item in result.json()["securityPolicies"]:
						#print bcolors.TURQUO+"----------- Start -----------"+bcolors.ENDC
						GTTable = tt.Texttable()
						GTheader = ['ID','Name']
						GTTable.header(GTheader)
						GTTable.set_cols_width([12,36])
						GTTable.set_cols_align(['c','c'])
						GTTable.set_cols_valign(['m','m'])
						SPTable = tt.Texttable()
						SPheader = ['API','KRS Ruleset', 'Rate Controls', 'Network Lists', 'Client Rep' ,'Slow POST']
						SPTable.header(SPheader)
						SPTable.set_cols_width([13,13,13,13,13,13])
						SPTable.set_cols_align(['c','c','c','c','c','c'])
						SPTable.set_cols_valign(['m','m','m','m','m','m'])
						RGTable = tt.Texttable()
						RGTable.set_deco(tt.Texttable.BORDER)
						#RGTable.set_cols_width([16,16,16,16,16,16,16,16,16,16])
						#RGTable.set_cols_align(['c','c','c','c','c','c','c','c','c','c'])
						#RGTable.set_cols_valign(['m','m','m','m','m','m','m','m','m','m'])
						RGheader = []
						RGrow = []
						try:
							item['securityControls']['applyReputationControls']
							applyReputationControls = str(item['securityControls']['applyReputationControls'])
						except:
							applyReputationControls = None
						GTRow = [item['id'],item['name']]
						try:
							str(item['securityControls']['applyApiConstraints'])
							apiConstraints = str(item['securityControls']['applyApiConstraints'])
						except:
							apiConstraints = 'Not Enabled'
						SProw = [apiConstraints,str(item['securityControls']['applyApplicationLayerControls']),str(item['securityControls']['applyRateControls']), str(item['securityControls']['applyNetworkLayerControls']), applyReputationControls,str(item['securityControls']['applySlowPostControls'])]
						SPTable.add_row(SProw)
						GTTable.add_row(GTRow)
						try:
							item['webApplicationFirewall']
							tablelength = len(item['webApplicationFirewall']['attackGroupActions'])
							for riskG in item['webApplicationFirewall']['attackGroupActions']:
								#print riskG
								RGheader.append(riskG['group'])
								RGrow.append(riskG['action'])
							RGTable.header(RGheader)
							cols = [10] * tablelength
							align = ['c'] * tablelength
							valign = ['m'] * tablelength
							RGTable.set_cols_width(cols)
							RGTable.set_cols_align(align)
							RGTable.set_cols_valign(valign)
							RGTable.add_row(RGrow)
						except:
							pass
						try:
							item['webApplicationFirewall']['ruleActions']
							RGTable.set_cols_width([18,18,18,18,18,18,18,18])
							RGTable.set_cols_align(['c','c','c','c','c','c','c','c'])
							RGTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
							print item['webApplicationFirewall']['ruleActions'][0]
							if '100000' in str(item['webApplicationFirewall']['ruleActions'][0]):
								for aag in item['webApplicationFirewall']['ruleActions']:
									if aag['id'] == 1000001:
										RGheader.append('SQLi')
									elif aag['id'] == 1000002:
										RGheader.append('XSS')
									elif aag['id'] == 1000003:
										RGheader.append('LFI')
									elif aag['id'] == 1000004:
										RGheader.append('RFI')
									elif aag['id'] == 1000005:
										RGheader.append('CMDi')
									elif aag['id'] == 1000006:
										RGheader.append('Attack Tools')
									elif aag['id'] == 1000007:
										RGheader.append('Protocol Attacks')
									elif aag['id'] == 1000008:
										RGheader.append('Platform Attacks')
									RGrow.append(aag['action'])
								RGTable.header(RGheader)
								RGTable.add_row(RGrow)
							else:
								pass
						except:
							pass
						try:
							item['ratePolicyActions']
							RateCTable = tt.Texttable()
							RateCTable.set_deco(tt.Texttable.BORDER)
							RateCTable.set_cols_width([12,12,12])
							RateCTable.set_cols_align(['c','c','c'])
							RateCTable.set_cols_valign(['m','m','m'])
							RateCheader = ['ID','IPv4', 'IPv6']
							RateCTable.header(RateCheader)
							for value in item['ratePolicyActions']:
								RateCrow = [value['id'],str(value['ipv4Action']),str(value['ipv6Action'])]
								RateCTable.add_row(RateCrow)
						except:
							pass
						IPGEOTable = tt.Texttable()
						IPGEOTable.set_deco(tt.Texttable.BORDER)
						IPGEOTable.set_cols_width([48,48,48])
						IPGEOTable.set_cols_align(['c','c','c'])
						IPGEOTable.set_cols_valign(['m','m','m'])
						IPGEOheader = ['GEO Blacklist','IP Blacklist', 'IP Exceptions']
						IPGEOTable.header(IPGEOheader)
						try:
							item['ipGeoFirewall']['geoControls']['blockedIPNetworkLists']['networkList']
							GEO = item['ipGeoFirewall']['geoControls']['blockedIPNetworkLists']['networkList']
						except:
							GEO = None
						try:
							item['ipGeoFirewall']['ipControls']['blockedIPNetworkLists']['networkList']
							IP = item['ipGeoFirewall']['ipControls']['blockedIPNetworkLists']['networkList']
						except:
							IP = None
						try:
							item['ipGeoFirewall']['ipControls']['allowedIPNetworkLists']['networkList']
							Allowed = item['ipGeoFirewall']['ipControls']['allowedIPNetworkLists']['networkList']
						except:
							Allowed = None
						IPGEOrow = [GEO,IP,Allowed]
						IPGEOTable.add_row(IPGEOrow)
						try:
							item['slowPost']
							SlowPTable = tt.Texttable()
							SlowPTable.set_deco(tt.Texttable.BORDER)
							SlowPTable.set_cols_width([20,20,20])
							SlowPTable.set_cols_align(['c','c','c'])
							SlowPTable.set_cols_valign(['m','m','m'])
							SlowPheader = ['Action','Period', 'Rate']
							SlowPTable.header(SlowPheader)
							SlowProw = [item['slowPost']['action'],item['slowPost']['slowRateThreshold']['period'],item['slowPost']['slowRateThreshold']['rate']]
							SlowPTable.add_row(SlowProw)
						except:
							pass
						BasicInfo = GTTable.draw()
						print bcolors.WARNING+""
						print BasicInfo
						print ""+bcolors.ENDC
						#print bcolors.TURQUO+"\nID: "+item['id']+bcolors.ENDC
						#print bcolors.TURQUO+"Name: "+item['name']+"\n"+bcolors.ENDC
						EnabledControls = SPTable.draw()
						print bcolors.WHITE+"Enabled Controls:"+bcolors.ENDC
						print EnabledControls
						try:
							item['webApplicationFirewall']
							RiskGroup = RGTable.draw()
							print bcolors.WHITE+"Risk Group Information:"+bcolors.ENDC
							print RiskGroup
						except:
							pass
						try:
							item['ratePolicyActions']
							RCGroup = RateCTable.draw()
							print bcolors.WHITE+"Rate Control Information:"+bcolors.ENDC
							print RCGroup
						except:
							pass
						IPGEOControls = IPGEOTable.draw()
						print bcolors.WHITE+"Network Lists:"+bcolors.ENDC
						print IPGEOControls
						try:
							item['slowPost']
							SlowPOSTControls = SlowPTable.draw()
							print bcolors.WHITE+"Slow POST:"+bcolors.ENDC
							print SlowPOSTControls
						except:
							pass
						print bcolors.TURQUO+"\n\n-----------------------------------------------------------------"+bcolors.ENDC
				manifest = json.loads(result.text, object_pairs_hook=OrderedDict)
				AppsecExport(result.json()['configName'],propertyVersion,manifest,respjson)
		else:
			if automation or respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print result.content
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
		#AppsecExport(result.json()['configName'],propertyVersion,result.json(),respjson)
	elif retrieveobj == 'hostnames' or retrieveobj == 'selected' or retrieveobj == 'available':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyVersion:
			Version = findAppsecVersion(configId,respjson)
			if Version["Production"] != None:
				propertyVersion = str(Version["Production"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using active PROD version: "+propertyVersion+bcolors.ENDC
			else:
				propertyVersion = str(Version["Latest"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
		url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/selectable-hostnames'
		result1 = s.get(urljoin(baseurl, url),params=params)
		#url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/selected-hostnames'
		#result2 = s.get(urljoin(baseurl, url))
		availableSet = []
		selectedSet = []
		#print result1.content
		#hostnameList = []
		if result1.status_code == 200:
			if automation:
				if retrieveobj == 'selected':
					for hostname in result1.json()['selectedSet']:
						print hostname['hostname']
					sys.exit()
				elif retrieveobj == 'available':
					for hostname in result1.json()['availableSet']:
						print hostname['hostname']
					sys.exit()
				else:
					print result1.content
				sys.exit()
			elif respjson:
				json_data = result1.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				if retrieveobj == 'selected':
					print json.dumps(result1.json()['selectedSet'])
				elif retrieveobj == 'available':
					print json.dumps(result1.json()['availableSet'])
				else:
					print result1.content
				sys.exit()
			else:
				try:
					result1.json()["availableSet"]
					for item in result1.json()["availableSet"]:
						availableSet.append(item["hostname"])
				except:
					pass
				try:
					result1.json()["selectedSet"]
					for item in result1.json()["selectedSet"]:
						selectedSet.append(item["hostname"])
				except:
					pass
				#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result1.status_code)+bcolors.ENDC
				#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Configuration ID: "+str(result1.json()["configId"])+bcolors.ENDC
				#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Available Hostnames:"+bcolors.ENDC
				#print availableSet
				#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Selected Hostnames:"+bcolors.ENDC
				#print selectedSet
				if retrieveobj == 'selected':
					selected = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					selectedheader = ['Selected']
					selected.header(selectedheader)
					selected.set_cols_width([150])
					selected.set_cols_align(['c'])
					selected.set_cols_valign(['m'])
					selectedrow = [selectedSet]
					selected.add_row(selectedrow)
					SelectedTable = selected.draw()
					print SelectedTable
				elif retrieveobj == 'available':
					available = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					availableheader = ['Available']
					available.header(availableheader)
					available.set_cols_width([150])
					available.set_cols_align(['c'])
					available.set_cols_valign(['m'])
					availablerow = [availableSet]
					available.add_row(availablerow)
					AvailableTable = available.draw()
					print AvailableTable
				else:
					HostnameTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					Hostnameheader = ['Config ID','Available', 'Selected']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([10,65,65])
					HostnameTable.set_cols_align(['c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m'])
					Hostnamerow = [result1.json()["configId"],availableSet,selectedSet]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
					print HostTable
		else:
			if automation or respjson:
				print result1.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result1.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print result1.content
		#pprint.pprint(result1.json())
		#if result2.status_code == 200:
		#	print bcolors.WARNING+"\n\n[AppSec] StatusCode: "+str(result2.status_code)+bcolors.ENDC
		#	print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Selected Hostnames:"+bcolors.ENDC
		#	for item in result2.json()["hostnameList"]:
		#		hostnameList.append(item["hostname"])
			#pprint.pprint(result2.json())
		#	print hostnameList
		#else:
		#	print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result2.status_code)+bcolors.ENDC
		#	print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
		#	print result2.json()
		#parsed = json.loads(result.json())
		#print json.dumps(parsed, indent=4, sort_keys=True)
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'rate':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyVersion:
			Version = findAppsecVersion(configId,respjson)
			if Version["Production"] != None:
				propertyVersion = str(Version["Production"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using active PROD version: "+propertyVersion+bcolors.ENDC
			else:
				propertyVersion = str(Version["Latest"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
		url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/rate'
		result = s.get(urljoin(baseurl, url),params=params)
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Configuration ID: "+str(result.json()["configId"])+bcolors.ENDC
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Version: "+str(result.json()["version"])+bcolors.ENDC
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Policies:"+bcolors.ENDC
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
				print result.content
		else:
			if automation or respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print result.content
		#print result.json()
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'clone':
		if prefix:
			if len(prefix) != 4:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Prefix must be 4 characters long: --prefix FGCS\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyVersion:
			Version = findAppsecVersion(configId,respjson)
			propertyVersion = str(Version["Latest"])
			if not respjson and not automation:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
		if not policyId:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a new policy name with the following option: --policyId newPolicy \n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		elif not cloneFrom:
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify which policy to clone: --from clonePolicy \n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			SecClone(configId,propertyVersion,policyId,cloneFrom,respjson,prefix)
	elif retrieveobj == 'policies':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyVersion:
			Version = findAppsecVersion(configId,respjson)
			if Version["Production"] != None:
				propertyVersion = str(Version["Production"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using active PROD version: "+propertyVersion+bcolors.ENDC
			else:
				propertyVersion = str(Version["Latest"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
		url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/security-policies'
		result = s.get(urljoin(baseurl, url),params=params)
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Configuration ID: "+str(result.json()["configId"])+bcolors.ENDC
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Version: "+str(result.json()["version"])+bcolors.ENDC
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Policies:"+bcolors.ENDC
		if result.status_code == 200:
			if automation:
				for policy in result.json()['policies']:
					print policy['policyId']
				sys.exit()
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				PolicyTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				Policyheader = ['ID','Policy Name']
				PolicyTable.header(Policyheader)
				PolicyTable.set_cols_width([15,60])
				PolicyTable.set_cols_align(['c','c'])
				PolicyTable.set_cols_valign(['m','m'])
				for policyItem in result.json()["policies"]:
					Policyrow = [policyItem['policyId'],policyItem['policyName']]
					PolicyTable.add_row(Policyrow)
				PolicyTableDraw = PolicyTable.draw()
				print PolicyTableDraw
				'''
				for i in range(0,len(result.json()["policies"])):
					print bcolors.WARNING+str(i)+". "+result.json()["policies"][i]["policyName"]+bcolors.ENDC
					#print bcolors.WARNING+"Policy Name: "+bcolors.ENDC+result.json()["policies"][i]["policyName"]
					#print bcolors.WARNING+"Policy ID: "+bcolors.ENDC+result.json()["policies"][i]["policyId"]
					policyId = result.json()["policies"][i]["policyId"]
					url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/match-targets'
					query = {"policyId":policyId,"includeChildObjectName":True}
					result2 = s.get(urljoin(baseurl, url),params=query)
					if result2.status_code == 200:
						for item in result2.json()["matchTargets"]["apiTargets"]:
							print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" API Match Targets: "+bcolors.ENDC
							#print result2.json()["matchTargets"]["apiTargets"]
							HostnameTable = tt.Texttable()
							#HostnameTable.set_deco(tt.Texttable.HEADER)
							Hostnameheader = ['#','Target ID','API Definition', 'API ID', 'WAF Bypass Lists']
							HostnameTable.header(Hostnameheader)
							HostnameTable.set_cols_width([3,10,40,15,71])
							HostnameTable.set_cols_align(['c','c','c','c','c'])
							HostnameTable.set_cols_valign(['m','m','m','m','m'])
							try:
								item["bypassNetworkLists"]
								bypassNetworkLists = []
								for nlId in item["bypassNetworkLists"]:
									bypassNetworkLists.append(nlId["name"])
							except:
								bypassNetworkLists = None
							Hostnamerow = [item["sequence"],item["targetId"],item["apis"][0]["name"],item["apis"][0]["id"],bypassNetworkLists]
							#Hostnamerow = [item["sequence"],hostnames,item["filePaths"]]
							HostnameTable.add_row(Hostnamerow)
							HostTable = HostnameTable.draw()
							tab = tt.Texttable()
							tab.set_deco(tt.Texttable.VLINES)
							header = ['Policy ID', 'Rate Control', 'NL', 'BOTMAN', 'Slow POST', 'Kona Ruleset', 'Client Rep', 'API Definition']
							tab.header(header)
							tab.set_cols_width([17,17,17,17,17,17,17,17])
							tab.set_cols_align(['c','c','c','c','c','c','c','c'])
							tab.set_cols_valign(['m','m','m','m','m','m','m','m'])
							try:
								item["effectiveSecurityControls"]["applyBotmanControls"]
								applyBotmanControls = str(item["effectiveSecurityControls"]["applyBotmanControls"])
							except:
								applyBotmanControls = None
							try:
								item["effectiveSecurityControls"]["applyApiConstraints"]
								applyApiConstraints = str(item["effectiveSecurityControls"]["applyApiConstraints"])
							except:
								applyApiConstraints = None
							try:
								item["effectiveSecurityControls"]["applyReputationControls"]
								applyReputationControls = str(item["effectiveSecurityControls"]["applyReputationControls"])
							except:
								applyReputationControls = None
							row = [item["securityPolicy"]["policyId"],str(item["effectiveSecurityControls"]["applyRateControls"]),str(item["effectiveSecurityControls"]["applyNetworkLayerControls"]),applyBotmanControls,str(item["effectiveSecurityControls"]["applySlowPostControls"]),str(item["effectiveSecurityControls"]["applyApplicationLayerControls"]),applyReputationControls,applyApiConstraints]
							tab.add_row(row)
							URLTable = tab.draw()
							print HostTable
							print URLTable,"\n\n"
						#print bcolors.WARNING+"Web Match Targets: "+bcolors.ENDC
						for item in result2.json()["matchTargets"]["websiteTargets"]:
							print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Website Match Targets: "+bcolors.ENDC
							#print item["hostnames"]
							#print item
							#print bcolors.WARNING+"File Paths: "+bcolors.ENDC
							#print item["filePaths"]
							HostnameTable = tt.Texttable()
							#HostnameTable.set_deco(tt.Texttable.HEADER)
							Hostnameheader = ['#','Target ID','Hostnames', 'File Paths', 'WAF Bypass Lists']
							HostnameTable.header(Hostnameheader)
							HostnameTable.set_cols_width([3,10,70,18,38])
							HostnameTable.set_cols_align(['c','c','c','c','c'])
							HostnameTable.set_cols_valign(['m','m','m','m','m'])
							try:
								item["bypassNetworkLists"]
								bypassNetworkLists = []
								for nlId in item["bypassNetworkLists"]:
									bypassNetworkLists.append(nlId["name"])
							except:
								bypassNetworkLists = None
							try:
								item["hostnames"]
								hostnames = str(item["hostnames"])
							except:
								hostnames = None
							Hostnamerow = [item["sequence"],item["targetId"],hostnames,item["filePaths"],bypassNetworkLists]
							#Hostnamerow = [item["sequence"],hostnames,item["filePaths"]]
							HostnameTable.add_row(Hostnamerow)
							HostTable = HostnameTable.draw()
							tab = tt.Texttable()
							tab.set_deco(tt.Texttable.VLINES)
							header = ['Policy Name', 'Policy ID', 'Rate Control', 'NL', 'BOTMAN', 'Slow POST', 'Kona Ruleset', 'Client Rep', 'API Definition']
							tab.header(header)
							tab.set_cols_width([30,13,15,8,8,11,15,13,17])
							tab.set_cols_align(['c','c','c','c','c','c','c','c','c'])
							tab.set_cols_valign(['m','m','m','m','m','m','m','m','m'])
							try:
								item["effectiveSecurityControls"]["applyBotmanControls"]
								applyBotmanControls = str(item["effectiveSecurityControls"]["applyBotmanControls"])
							except:
								applyBotmanControls = None
							try:
								item["effectiveSecurityControls"]["applyApiConstraints"]
								applyApiConstraints = str(item["effectiveSecurityControls"]["applyApiConstraints"])
							except:
								applyApiConstraints = None
							try:
								item["effectiveSecurityControls"]["applyReputationControls"]
								applyReputationControls = str(item["effectiveSecurityControls"]["applyReputationControls"])
							except:
								applyReputationControls = None
							row = [result.json()["policies"][i]["policyName"], result.json()["policies"][i]["policyId"],str(item["effectiveSecurityControls"]["applyRateControls"]),str(item["effectiveSecurityControls"]["applyNetworkLayerControls"]),applyBotmanControls,str(item["effectiveSecurityControls"]["applySlowPostControls"]),str(item["effectiveSecurityControls"]["applyApplicationLayerControls"]),applyReputationControls,applyApiConstraints]
							tab.add_row(row)
							URLTable = tab.draw()
							print HostTable
							print URLTable,"\n\n"
					else:
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result2.status_code)+bcolors.ENDC
						print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
						print result2.content
					'''
		else:
			if automation or respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			print result.content
		#print result.json()
		#pprint.pprint(result.json())
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'targets':
		if propertyName:
			configId = findConfigID(propertyName)
		else:
			if not configId:
				print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" You need to specify a Configuration Name or ID: -N asomarri / --configId 18117\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyVersion:
			Version = findAppsecVersion(configId,respjson)
			if Version["Production"] != None:
				propertyVersion = str(Version["Production"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using active PROD version: "+propertyVersion+bcolors.ENDC
			else:
				propertyVersion = str(Version["Latest"])
				if not respjson and not automation:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" No Property Version provided. Using latest version: "+propertyVersion+bcolors.ENDC
		if policyId:
			params.update({"policyId":policyId,"includeChildObjectName":True})
		else:
			params.update({"includeChildObjectName":True})
		#print query
		url = '/appsec/v1/configs/'+configId+'/versions/'+str(propertyVersion)+'/match-targets'
		result = s.get(urljoin(baseurl, url),params=params)
		#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
		#print result.json()
		if result.status_code == 200:
			if automation:
				for item in result.json()["matchTargets"]["websiteTargets"]:
					print item["targetId"]
				for item in result.json()["matchTargets"]["apiTargets"]:
					print item["targetId"]
				sys.exit()
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Configuration Version: "+str(propertyVersion)+bcolors.ENDC
				for item in result.json()["matchTargets"]["websiteTargets"]:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" Website Match Targets: "+bcolors.ENDC
					#print item["hostnames"]
					#print item
					#print bcolors.WARNING+"File Paths: "+bcolors.ENDC
					#print item["filePaths"]
					HostnameTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					Hostnameheader = ['#','Target ID','Hostnames', 'File Paths', 'WAF Bypass Lists']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([3,10,70,35,38])
					HostnameTable.set_cols_align(['c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m'])
					try:
						item["bypassNetworkLists"]
						bypassNetworkLists = []
						for nlId in item["bypassNetworkLists"]:
							bypassNetworkLists.append(nlId["name"])
					except:
						bypassNetworkLists = None
					try:
						item["hostnames"]
						hostnames = str(item["hostnames"])
					except:
						hostnames = 'ALL Hostnames'
					if item['defaultFile'] == 'RECURSIVE_MATCH':
						filePaths = 'Match on all requests that end in a trailing slash'
					elif item['defaultFile'] == 'BASE_MATCH':
						filePaths = 'Match only requests for top-level hostnames ending in a trailing slash'
					else:
						filePaths = str(item["filePaths"])
					Hostnamerow = [item["sequence"],item["targetId"],hostnames,filePaths,bypassNetworkLists]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
					IDBypass = tt.Texttable()
					#IDBypass.set_deco(tt.Texttable.VLINES)
					IDBypassheader = ['Target ID', 'WAF Bypass List']
					IDBypass.header(IDBypassheader)
					IDBypass.set_cols_width([15,100])
					IDBypass.set_cols_align(['c','c'])
					IDBypass.set_cols_valign(['m','m'])
					IDBypassrow = [item["targetId"],bypassNetworkLists]
					IDBypass.add_row(IDBypassrow)
					BypassTable = IDBypass.draw()
					tab = tt.Texttable()
					tab.set_deco(tt.Texttable.VLINES)
					header = ['Policy ID', 'Rate Controls', 'NL', 'BOTMAN', 'SlowPOST', 'Kona Ruleset', 'ClientRep', 'API Definition']
					tab.header(header)
					tab.set_cols_width([19,19,19,19,19,19,19,19])
					tab.set_cols_align(['c','c','c','c','c','c','c','c'])
					tab.set_cols_valign(['m','m','m','m','m','m','m','m'])
					try:
						item["effectiveSecurityControls"]["applyBotmanControls"]
						applyBotmanControls = str(item["effectiveSecurityControls"]["applyBotmanControls"])
					except:
						applyBotmanControls = None
					try:
						item["effectiveSecurityControls"]["applyApiConstraints"]
						applyApiConstraints = str(item["effectiveSecurityControls"]["applyApiConstraints"])
					except:
						applyApiConstraints = None
					try:
						item["effectiveSecurityControls"]["applyReputationControls"]
						applyReputationControls = str(item["effectiveSecurityControls"]["applyReputationControls"])
					except:
						applyReputationControls = None
					row = [item['securityPolicy']['policyId'], str(item["effectiveSecurityControls"]["applyRateControls"]),str(item["effectiveSecurityControls"]["applyNetworkLayerControls"]),applyBotmanControls,str(item["effectiveSecurityControls"]["applySlowPostControls"]),str(item["effectiveSecurityControls"]["applyApplicationLayerControls"]),applyReputationControls,applyApiConstraints]
					tab.add_row(row)
					URLTable = tab.draw()
					print HostTable
					#print BypassTable
					print URLTable,"\n\n"
				for item in result.json()["matchTargets"]["apiTargets"]:
					print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" API Match Targets: "+bcolors.ENDC
					#print result2.json()["matchTargets"]["apiTargets"]
					HostnameTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					Hostnameheader = ['#','Target ID','API Definition', 'API ID', 'WAF Bypass Lists']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([3,10,40,15,71])
					HostnameTable.set_cols_align(['c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m'])
					try:
						item["bypassNetworkLists"]
						bypassNetworkLists = []
						for nlId in item["bypassNetworkLists"]:
							bypassNetworkLists.append(nlId["name"])
					except:
						bypassNetworkLists = None
					Hostnamerow = [item["sequence"],item["targetId"],item["apis"][0]["name"],item["apis"][0]["id"],bypassNetworkLists]
					#Hostnamerow = [item["sequence"],hostnames,item["filePaths"]]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
					tab = tt.Texttable()
					tab.set_deco(tt.Texttable.VLINES)
					header = ['Policy ID', 'Rate Control', 'NL', 'BOTMAN', 'Slow POST', 'Kona Ruleset', 'Client Rep', 'API Definition']
					tab.header(header)
					tab.set_cols_width([17,17,17,17,17,17,17,17])
					tab.set_cols_align(['c','c','c','c','c','c','c','c'])
					tab.set_cols_valign(['m','m','m','m','m','m','m','m'])
					try:
						item["effectiveSecurityControls"]["applyBotmanControls"]
						applyBotmanControls = str(item["effectiveSecurityControls"]["applyBotmanControls"])
					except:
						applyBotmanControls = None
					try:
						item["effectiveSecurityControls"]["applyApiConstraints"]
						applyApiConstraints = str(item["effectiveSecurityControls"]["applyApiConstraints"])
					except:
						applyApiConstraints = None
					try:
						item["effectiveSecurityControls"]["applyReputationControls"]
						applyReputationControls = str(item["effectiveSecurityControls"]["applyReputationControls"])
					except:
						applyReputationControls = None
					row = [item["securityPolicy"]["policyId"],str(item["effectiveSecurityControls"]["applyRateControls"]),str(item["effectiveSecurityControls"]["applyNetworkLayerControls"]),applyBotmanControls,str(item["effectiveSecurityControls"]["applySlowPostControls"]),str(item["effectiveSecurityControls"]["applyApplicationLayerControls"]),applyReputationControls,applyApiConstraints]
					tab.add_row(row)
					URLTable = tab.draw()
					print HostTable
					print URLTable,"\n\n"
				#print bcolors.WARNING+"Web Match Targets: "+bcolors.ENDC
		else:
			if automation or respjson:
				print result.content
				sys.exit()
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(result.status_code)+bcolors.ENDC
			print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print bcolors.WHITE+"This module allows you to use Application Security API to view/modify/activate Security Configurations\n"+bcolors.ENDC
		print bcolors.WARNING+"APPSEC Retrieve Information:\n"+bcolors.ENDC
		print "msc 		- List Multi Security Configuration"
		print "versions 	- List all Versions for a specific Security Configuration"
		print "hostnames 	- List all hostnames for a specific Security Configuration"
		print "available 	- List Available for a specific Security Configuration"
		print "selected 	- List Selected hostnames for a specific Security Configuration"
		print "policies 	- List all Security Policies for a specific Security Configuration"
		print "targets 	- List Match Targets for a specific Security Configuration"
		print "custom 		- List Custom Rules"
		print "export 		- AppSec Export Feature"
		print bcolors.WARNING+"\nAPPSEC Actions:\n"+bcolors.ENDC
		print "newVersion 	- Create a new configuration version"
		print "add 		- Add hostnames or custom rules to a Security Configuration"
		print "remove 		- Remove hostnames or custom rules from a Security Configuration"
		print "activate 	- Activate Security Configuration to Staging or Production"
		print "new 		- Create and add a new custom rule in Shared Resources"
		print bcolors.WARNING+"\nSWaPI Automations:\n"+bcolors.ENDC
		print "Integration 	- Automates the process of onboarding new hostnames into WAF"
		print "hostPR 		- Check configuration hostnames against a list to make sure no hostname was missed - Useful for Peer Reviews"
		print "protected 	- Generates a 'Protected Hostname' report"
		print "audit 		- Generates an Audit CSV report, which is a snapshot of your current configuration"
		print "ruleaudit 	- Generates a Rule Audit CSV report for a specific rule"
		print bcolors.WARNING+"\nAvailable Options:\n"+bcolors.ENDC
		print "-N 		- Specify a Security Configuration using its Name"
		print "--config 	- Specify a Security Configuration using its ID"
		print "--json	 	- Provide raw JSON response"
		print "--auto 		- Used for automation. Keep output simple and concise"
		print "--ruleId 	- Used to display information about a specific custom rule or to an apply action to a specific custom rule"
		print "--policyId 	- Get information about a specific policy ID"
		print "--exceptions 	- Used with the export command. It will provide information about Exceptions and Conditions in all Security Policies"
		print "--rate 		- Used with the export command. Show all rate controls in Shared Resources"
		print "--custom 	- Used with the export command. Show custom rule information from each Security Policy"
		print "--rules 	- Used with the export command. Show all rules enabled in each Security Policy"
		print bcolors.TURQUO+"\nMain Blog: https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/09/swapi-application-security-main"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()





def PAPI(automation,AccountSwitch,stagingPush,srto,origin,host,retrieveobj,contractId,groupId,propertyId,propertyName,edgeId,propertyVersion,edge,latest,emails,notes,cdn,PRd,cemails,rules,cloneFrom,copyHostnames,ipVersion,ruleFormat,productId,cpcode,creds,respjson):
	if not respjson and not automation:
		print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	home = expanduser("~")
	#print creds
	#print os.getenv("USER")
	#print os.getenv("SUDO_USER")
	#print os.getenv("HOME")
	filename = home+'/.edgerc'
	#print filename
	try:
		outputfile = open(filename, 'r')
	except IOError:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Unable to open "EdgeRC" file. Does this file exists in your user directory? Location: '+home+bcolors.ENDC+bcolors.ENDC
		print bcolors.WHITE+'\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	edgerc = EdgeRc(filename)
	section = creds
	try:
		baseurl = 'https://%s' % edgerc.get(section, 'host')
	except:
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' SWaPI was unable to find any valid section in your EdgeRC file called: '+section+bcolors.ENDC
		print bcolors.TURQUO+'[Error]'+bcolors.WARNING+' Please check your EdgeRC file and fix.'+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	if AccountSwitch:
		filename = '.map'
		readfile = open(filename, 'r')
		contents = readfile.readlines()
		for item in contents:
			if "[" and "]" in item:
				accountCheck = item[1:-2]
				if accountCheck == AccountSwitch:
					AccountSwitch = contents[contents.index(item)+1].strip()
					if not respjson and not automation and retrieveobj != 'Integration':
						print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" Friendly Name found and mapped to Account: "+contents[contents.index(item)+1].strip()+bcolors.ENDC
	params = {'accountSwitchKey':AccountSwitch}
	def CreateANewEdge(productId,contractId,groupId,prefix,ipVersion):
		params.update({"contractId":contractId,"groupId":groupId,"options":"mapDetails"})
		CNEheaders = {"Content-Type":"application/json","PAPI-Use-Prefixes":"false"}
		prefix = prefix[:-1]
		CNEjson = {"productId":productId,"domainPrefix":prefix,"domainSuffix":"edgesuite.net","secure":False,"ipVersionBehavior":ipVersion}
		#print CNEjson
		CNEresult = s.post(urljoin(baseurl, "/papi/v1/edgehostnames/"),headers=CNEheaders,params=params,json=CNEjson)
		#print CNEresult.json()
		#print edge
		if CNEresult.status_code == 400:
			if retrieveobj == "Integration":
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"EdgeHostname is already created. Continuing with process."+bcolors.ENDC
				return edge
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"EdgeHostname is already created."+bcolors.ENDC
		elif CNEresult.status_code == 201:
			if retrieveobj == "Integration":
				#edgeIdLink = CNEresult.json()["edgeHostnameLink"]
				#print edgeIdLink
				# /papi/v1/edgehostnames/ehn_2697875?options=mapDetails&groupId=grp_109027&contractId=ctr_F-MRTALC
				PollId = CNEresult.json()["edgeHostnameLink"].split("?")[0].split("/")[4]
				#print PollId
				PollHeader = {"PAPI-Use-Prefixes": "false"}
				PollResult = s.get(urljoin(baseurl, "/papi/v1/edgehostnames/"+PollId),headers=PollHeader,params=CNEquery)
				#print PollResult.content
				Poll = PollResult.status_code
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Creating new EdgeHostname. This might take some time."+bcolors.ENDC
				while Poll == 404:
					PollResult = s.get(urljoin(baseurl, "/papi/v1/edgehostnames/"+PollId),headers=PollHeader,params=params)
					try:
						Poll = PollResult.status_code
					except:
						pass
				edgeId = CNEresult.json()["edgeHostnameLink"].split("?")[0].split("/")[4]
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"New EdgeHostname created successfully."+bcolors.ENDC
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"EdgeId: "+CNEresult.json()["edgeHostnameLink"].split("?")[0].split("/")[4]+bcolors.ENDC
				#print edgeId
				return edgeId
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"New EdgeHostname created successfully."+bcolors.ENDC
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"EdgeId: "+CNEresult.json()["edgeHostnameLink"].split("?")[0].split("/")[4]+bcolors.ENDC
			#print CNEresult.status_code
			#print CNEresult.content
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"There was a problem creating your EdgeHostname."+bcolors.ENDC
			print CNEresult.status_code
			print CNEresult.content
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def CreateANewProperty(propertyName,contractId,groupId,productId):
		params.update({"contractId":contractId,"groupId":groupId})
		CNjson = {"productId":productId,"propertyName":propertyName}
		CNheaders = {"Content-Type":"application/json","PAPI-Use-Prefixes":"false"}
		CNresult = s.post(urljoin(baseurl, "/papi/v1/properties/"),json=CNjson,headers=CNheaders,params=params)
		if CNresult.status_code == 201:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'New Configuration has been created: '+propertyName+bcolors.ENDC
			if retrieveobj == "Integration":
				#print CNresult.status_code
				#print CNresult.content
				return
			elif host:
				propertyId = CNresult.json()['propertyLink'].split('?')[0].split('/')[4]
				return propertyId
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'There was a problem creating your configuration.'+bcolors.ENDC
			print CNresult.status_code
			print CNresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	def CloneAProperty(propertyName,contractId,groupId,productId,propertyId,propertyVersion,eTag,copyHostnames):
		params.update({"contractId":contractId,"groupId":groupId})
		FromInfo = {"propertyId":propertyId,"version":propertyVersion,"cloneFromVersionEtag":eTag,"copyHostnames":copyHostnames}
		CPjson = {"productId":productId,"propertyName":propertyName,"cloneFrom":FromInfo}
		CPheaders = {"Content-Type":"application/json","PAPI-Use-Prefixes":"false"}
		CPresult = s.post(urljoin(baseurl, "/papi/v1/properties/"),json=CPjson,headers=CPheaders,params=params)
		if CPresult.status_code == 201:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'Configuration Cloned Successfully. '+propertyName+bcolors.ENDC
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'PropertyID: '+CPresult.json()['propertyLink'].split('?')[0].split('/')[4]+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'There was a problem creating your configuration.'+bcolors.ENDC
			print CNresult.status_code
			print CNresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	def Search(edgeHostname,propertyName,host,propertyVersion):
		Sheaders = {'Content-Type':'application/json',"PAPI-Use-Prefixes":"false"}
		#print propertyName
		if edgeHostname:
			Sbody = {"edgeHostname":edge}
		elif propertyName:
			Sbody = {"propertyName":propertyName}
		elif host:
			Sbody = {"hostname":host}
		else:
			print "You need to specify either a target '-t', an EdgeHostname '-E' or a Property Name '-N'.\n\n"
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print params
		result = s.post(urljoin(baseurl, '/papi/v1/search/find-by-value'),headers=Sheaders,json=Sbody,params=params)
		#print "StatusCode: "+str(result.status_code)
		#print result.content
		#print propertyName
		#print result.json()["versions"]["items"]
		if result.status_code == 200 or result.status_code ==201:
			if result.json()["versions"]["items"]:
				if retrieveobj == "Integration":
					if ExistingConfig == "FALSE":
						print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+" A configuration has been found with that name. Please make sure you use a NEW configuration name: "+propertyName+"\n\n"+bcolors.ENDC
						print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
						sys.exit()
				StagingVersion = None
				ProductionVersion = None
				contractId = "ctr_"+result.json()["versions"]["items"][0]["contractId"]
				groupId = "grp_"+result.json()["versions"]["items"][0]["groupId"]
				propertyId = "prp_"+result.json()["versions"]["items"][0]["propertyId"]
				accountId = "act_"+result.json()["versions"]["items"][0]["accountId"]
				currentVersion = result.json()["versions"]["items"][0]["propertyVersion"]
				#for i in range(0,len(result.json()["versions"]["items"])):
				#	if result.json()["versions"]["items"][i]["productionStatus"] == "ACTIVE":
				#		ProductionVersion = result.json()["versions"]["items"][i]["propertyVersion"]
				#	if result.json()["versions"]["items"][i]["stagingStatus"] == "ACTIVE":
				#		StagingVersion = result.json()["versions"]["items"][i]["propertyVersion"]
					#if result.json()["versions"]["items"][i]["propertyName"] == propertyName:
					#contractId = result.json()["versions"]["items"][i]["contractId"]
					#groupId = result.json()["versions"]["items"][i]["groupId"]
					#propertyId = result.json()["versions"]["items"][i]["propertyId"]
					#accountId = result.json()["versions"]["items"][i]["propertyId"]
					#productionStatus = result.json()["versions"]["items"][i]["productionStatus"]
					#stagingStatus = result.json()["versions"]["items"][i]["stagingStatus"]
					#propertyVersion = result.json()["versions"]["items"][i]["propertyVersion"]
			else:
				if retrieveobj == "Integration":
					if ExistingConfig == "FALSE":
						return
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"No Configuration has been found with that name.\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'There was a problem searching this account.'+bcolors.ENDC
			print result.status_code
			print result.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		Pheaders = {"PAPI-Use-Prefixes":"false"}
		PQuery = {"contractId":contractId,"groupId":groupId}
		LatestJson = s.get(urljoin(baseurl, "/papi/v1/properties/"+str(propertyId)+"/versions/latest"), headers=Pheaders,params=params)
		#print LatestJson.content
		latestVersion = LatestJson.json()["versions"]["items"][0]["propertyVersion"]
		#print latestVersion
		Latestresult = s.get(urljoin(baseurl, '/papi/v1/properties/'+propertyId+'/versions'),headers=Pheaders,params=params)
		Presult = s.get(urljoin(baseurl, '/papi/v1/properties/'+propertyId+'/versions'),headers=Pheaders,params=params)
		try:
			Presult.json()["versions"]["items"]
		except:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'No valid version was returned.'+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		for i in range(0,len(Presult.json()["versions"]["items"])):
			if Presult.json()["versions"]["items"][i]["productionStatus"] == "ACTIVE":
				ProductionVersion = Presult.json()["versions"]["items"][i]["propertyVersion"]
			if Presult.json()["versions"]["items"][i]["stagingStatus"] == "ACTIVE":
				StagingVersion = Presult.json()["versions"]["items"][i]["propertyVersion"]
		#print Presult.json()
		if retrieveobj == "delete":
				return contractId,groupId,propertyId
		if retrieveobj == "activate":
			if propertyVersion:
				return contractId,groupId,propertyId
		productId = Presult.json()["versions"]["items"][0]["productId"]
		if retrieveobj == "Integration":
			if ProductionVersion == None:
				propertyVersion = currentVersion
				eTag = getEtag(contractId,groupId,propertyId,str(propertyVersion))
			else:
				propertyVersion = ProductionVersion
				eTag = getEtag(contractId,groupId,propertyId,str(propertyVersion))
			#print contractId,groupId,propertyId,str(propertyVersion),eTag
			return propertyId,propertyVersion,eTag
		if retrieveobj == "cpcodes":
			return accountId,contractId,groupId,propertyId
		if retrieveobj == "create":
			return contractId,groupId,productId
		#if retrieveobj == "cpcodes":
		#	return accountId,contractId,groupId,propertyId
		if retrieveobj == "newVersion":
			if propertyVersion:
				eTag = getEtag(contractId,groupId,propertyId,str(propertyVersion))
				return contractId,groupId,propertyId,propertyVersion,eTag
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"No version has been provided. Using latest version: "+str(latestVersion)+bcolors.ENDC
				eTag = getEtag(contractId,groupId,propertyId,str(latestVersion))
				return contractId,groupId,propertyId,latestVersion,eTag
		if retrieveobj == "clone": #contractId,groupId,productId,propertyId,propertyVersion,eTag
			if propertyVersion:
				eTag = getEtag(contractId,groupId,propertyId,propertyVersion)
				return contractId,groupId,productId,propertyId,propertyVersion,eTag
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"No version has been provided. Using latest version: "+str(latestVersion)+bcolors.ENDC
				eTag = getEtag(contractId,groupId,propertyId,str(latestVersion))
				return contractId,groupId,productId,propertyId,latestVersion,eTag
		if retrieveobj == "poll":
			params.update({'contractId':contractId,'groupId':groupId})
			PollEdgeID = s.get(urljoin(baseurl, '/papi/v1/edgehostnames/'),params=params)
			#print PollEdgeID.status_code
			#print PollEdgeID.content
			for i in range(0,len(PollEdgeID.json()["edgeHostnames"]["items"])):
				edgeIDs.append(PollEdgeID.json()["edgeHostnames"]["items"][i]["edgeHostnameId"])
			#print edgeIDs
			if not edgeId:
				return(contractId,groupId,edgeIDs)
			else:
				return(contractId,groupId)
		if (retrieveobj == "add") or (retrieveobj == "remove") or (retrieveobj == "download") or (retrieveobj == "freeze") or (retrieveobj == "update") or (retrieveobj == 'activate'):
			if (retrieveobj == "freeze") or (retrieveobj == "update") or (retrieveobj == "download") or (retrieveobj == 'activate'):
				if propertyVersion: # contractId,groupId,propertyId,latest = Search(None,propertyName,None,propertyVersion)
					return contractId,groupId,propertyId,propertyVersion
				else:
					return contractId,groupId,propertyId,latestVersion
			eTag = getEtag(contractId,groupId,propertyId,str(latestVersion))
			configHostnames = getHostnames(contractId,groupId,propertyId,latestVersion)
			#/papi/v1/properties/{propertyId}/versions/latest{?activatedOn,contractId,groupId}
			return contractId,groupId,propertyId,latestVersion,eTag,configHostnames
		else:
			return accountId,contractId,groupId,propertyId
		sys.exit()
	def PollEdgeHostname(contractId,groupId,edgeId):
		#print contractId,groupId,edgeId
		#sys.exit()
		params.update({'contractId':contractId,'groupId':groupId})
		for edge in edgeId:
			#print edge
			PEresult = s.get(urljoin(baseurl, '/papi/v1/edgehostnames/'+edge),params=params)
			print PEresult.status_code
			print PEresult.content,"\n"
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def deleteConfiguration(contractId,groupId,propertyId):
		params.update({'contractId':contractId,'groupId':groupId})
		Dltresult = s.delete(urljoin(baseurl, '/papi/v1/properties/'+propertyId),params=params)
		if Dltresult.status_code == 200:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'Configuration has been deleted successfully.'+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'There was a problem deleting Configuration.'+bcolors.ENDC
			print CNresult.status_code
			print CNresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	def CreateANewVersion(contractId,groupId,propertyId,propertyVersion,eTag):
		params.update({'contractId':contractId,'groupId':groupId})
		CVjson = {'createFromVersion':propertyVersion,'createFromVersionEtag':eTag}
		CVheaders = {'Content-Type':'application/json',"PAPI-Use-Prefixes":"false"}
		CVresult = s.post(urljoin(baseurl, '/papi/v1/properties/'+propertyId+'/versions/'),json=CVjson,headers=CVheaders,params=params)
		if CVresult.status_code == 201:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'New configuration version has been created successfully: '+CVresult.json()["versionLink"].split("?")[0].split("/")[6]+bcolors.ENDC
			if retrieveobj == "Integration":
				return int(CVresult.json()["versionLink"].split("?")[0].split("/")[6])
			#print CVresult.status_code
			#print CVresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'There was a problem creating a new version.'+bcolors.ENDC
			print CNresult.status_code
			print CNresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	def AddHostnames(contractId,groupId,propertyId,propertyVersion,eTag,configHostnames):
		params.update({"contractId":contractId,"groupId":groupId,"validateHostnames":"false"})
		AHheaders = {'Content-Type':'application/json',"PAPI-Use-Prefixes":"false"}
		AHresult = s.put(urljoin(baseurl, '/papi/v1/properties/'+propertyId+"/versions/"+str(propertyVersion)+"/hostnames/"),json=configHostnames,headers=AHheaders,params=params)
		if AHresult.status_code == 200:
			if retrieveobj == "add" or retrieveobj == "Integration" or retrieveobj == "create":
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Hostnames added successfully."+bcolors.ENDC
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Hostnames removed successfully."+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"We encountered some issues adding hostnames to the Property."+bcolors.ENDC
			print bcolors.WARNING+str(AHresult.status_code)+bcolors.ENDC
			print bcolors.WARNING+AHresult.content+bcolors.ENDC
		if retrieveobj == "Integration" or retrieveobj == "create":
			return
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def DownloadRule(contractId,groupId,propertyId,propertyVersion):
		params.update({"contractId":contractId,"groupId":groupId,"validateRules":"false"})
		GetRule = s.get(urljoin(baseurl, "/papi/v1/properties/"+propertyId+"/versions/"+str(propertyVersion)+"/rules/"),params=params)
		#print GetRule.json()
		#print GetRule.status_code
		#print GetRule.json()
		jsonContent = GetRule.json()
		if retrieveobj == "Integration" or retrieveobj == "create":
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Downloading current configuration."+bcolors.ENDC
			return jsonContent
		filename = "files/"+propertyName+".json"
		f = open(filename,"w+")
		with f as outfile:
			json.dump(jsonContent, outfile, indent=4)
		f.close()
		print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"JSON File has been created:",filename+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def FreezeRule(contractId,groupId,propertyId,propertyVersion,ruleFormat):
		params.update({"contractId":contractId,"groupId":groupId})
		FRheaders = {"Content-Type":"application/vnd.akamai.papirules."+ruleFormat+"+json","PAPI-Use-Prefixes":"false"}
		GetRule = s.get(urljoin(baseurl, "/papi/v1/properties/"+propertyId+"/versions/"+str(propertyVersion)+"/rules/"),params=params)
		FreezeRule = s.put(urljoin(baseurl, "/papi/v1/properties/"+propertyId+"/versions/"+str(propertyVersion)+"/rules/"),headers=FRheaders,params=params,json=GetRule.json())
		#print GetRule.json()
		if FreezeRule.status_code == 200:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Action completed successfully"+bcolors.ENDC
		else:
			print bcolors.WARNING+FreezeRule.content+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def UpdateRule(contractId,groupId,propertyId,propertyVersion,rulesJson):
		params.update({"contractId":contractId,"groupId":groupId,"validateRules":False})
		GetRule = s.get(urljoin(baseurl, "/papi/v1/properties/"+propertyId+"/versions/"+str(propertyVersion)+"/rules/"),params=params)
		#print GetRule.content
		#ruleFormat = GetRule.json()["ruleFormat"]
		ruleFormat = "v2018-02-27"
		URheaders = {"Content-Type":"application/vnd.akamai.papirules."+ruleFormat+"+json","PAPI-Use-Prefixes":"false"}
		URresult = s.put(urljoin(baseurl, "/papi/v1/properties/"+propertyId+"/versions/"+str(propertyVersion)+"/rules/"),json=rulesJson,headers=URheaders,params=params)
		if URresult.status_code == 200:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Uploaded JSON file successfully."+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"There was a problem uploading your new configuration."+bcolors.ENDC
			print bcolors.WARNING+str(URresult.status_code)+bcolors.ENDC
			print bcolors.WARNING+URresult.content+bcolors.ENDC
		if retrieveobj == "Integration" or retrieveobj == "create":
			return
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def CreateCPCode(contractId,groupId,productId,CPCodeName):
		params.update({"contractId":contractId,"groupId":groupId})
		CCPheaders = {'Content-Type':'application/json',"PAPI-Use-Prefixes":"false"}
		CCPjson = {"productId":productId,"cpcodeName":CPCodeName}
		CCPresult = s.post(urljoin(baseurl, "/papi/v1/cpcodes/"),json=CCPjson,headers=CCPheaders,params=params)
		# "cpcodeLink" : "/papi/v1/cpcodes/cpc_634219?groupId=grp_109027&contractId=ctr_F-MRTALC"
		#print CCPresult.json()["cpcodeLink"].split("?")[0].split("/")[4].split("cpc_")
		#print CCPresult.content
		if CCPresult.status_code == 201:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"New CPCode created successfully: "+CCPresult.json()["cpcodeLink"].split("?")[0].split("/")[4].split("cpc_")[0]+bcolors.ENDC
			if retrieveobj == "Integration":
				CPCodeFinder = CCPresult.json()["cpcodeLink"].split("?")[0].split("/")[4].split("cpc_")[0]
				#print CPCodeFinder
				return CPCodeFinder
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+'There was a problem creating your configuration.'+bcolors.ENDC
			print CCPresult.status_code
			print CCPresult.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	def Activate(contractId,groupId,propertyId,propertyVersion,cdn,PRd,cemails,emails): #,notes,emails
		ACheaders = {"Content-Type":"application/json","PAPI-Use-Prefixes":"false"}
		params.update({"contractId":contractId,"groupId":groupId})
		#print emails
		if retrieveobj == "Integration":
			if ',' in emails:
				emails = emails.split(',')
			else:
				emails = emails.split('\n')
		#print emails
		body = {"propertyVersion":int(propertyVersion),"notifyEmails":emails,"acknowledgeAllWarnings":True,"useFastFallback":False}
		#print body
		if cdn == 'staging':
			ActNet = {"network": "STAGING"}
			body.update(ActNet)
		elif cdn == 'prod':
			complianceRecord = {"noncomplianceReason":"NONE","unitTested":True,"peerReviewedBy":PRd,"customerEmail":cemails}
			ActNet = {"network": "PRODUCTION","complianceRecord":complianceRecord}
			body.update(ActNet)
		#print body
		result = s.post(urljoin(baseurl, '/papi/v1/properties/'+propertyId+'/activations'),headers=ACheaders,json=body,params=params)
		if result.status_code == 201:
			if cdn == "staging":
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Activating Configuration in Akamai's Staging Platform."+bcolors.ENDC
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Activating Configuration in Akamai's Production Platform."+bcolors.ENDC
			if retrieveobj == "Integration":
				return result.json()
			else:
				print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		else:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"There was a problem activating your configuration."+bcolors.ENDC
			print "StatusCode: "+str(result.status_code)
			print result.content
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	def ModifyOriginAndCPCode(rulesjson,cpcode,origin,productId,srto):
		productId = productId.split("\n")
		if productId[0] == "prd_Site_Defender":
			CPCodeAppend = {unicode("name"):unicode("cpCode"),unicode("options"):{unicode("value"):{unicode("products"):[unicode("Site_Defender")],unicode("id"):int(cpcode)}}}
		else:
			CPCodeAppend = {unicode("name"):unicode("cpCode"),unicode("options"):{unicode("value"):{unicode("products"):[unicode("SPM")],unicode("id"):int(cpcode)}}}
		OriginAppend = {unicode("name"):unicode("origin"),unicode("options"):{unicode("cacheKeyHostname"):unicode("ORIGIN_HOSTNAME"),unicode("forwardHostHeader"):unicode("REQUEST_HOST_HEADER"),unicode("trueClientIpHeader"):unicode("True-Client-IP"),unicode("hostname"):unicode(origin),unicode("compress"):True,unicode("httpPort"):80,unicode("enableTrueClientIp"):True,unicode("trueClientIpClientSetting"):False,unicode("originType"):unicode("CUSTOMER")}}
		#print CPCodeAppend
		for i in range(0,len(rulesjson["rules"]["behaviors"])):
			if rulesjson["rules"]["behaviors"][i]["name"] == "cpCode":
				rulesjson["rules"]["behaviors"][i] = CPCodeAppend
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Added CPCode: "+str(cpcode)+bcolors.ENDC
				break
		for i in range(0,len(rulesjson["rules"]["behaviors"])):
			if rulesjson["rules"]["behaviors"][i]["name"] == "origin":
				rulesjson["rules"]["behaviors"][i] = OriginAppend
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Added CUSTOMER Origin: "+origin+bcolors.ENDC
				break
		for i in range(0,len(rulesjson["rules"]["behaviors"])):
			if rulesjson["rules"]["behaviors"][i]["name"] == "webApplicationFirewall":
				del[rulesjson["rules"]["behaviors"][i]]
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Removed WAF behavior."+bcolors.ENDC
				break
		for i in range(0,len(rulesjson["rules"]["children"][0]["behaviors"])):
			if rulesjson["rules"]["children"][0]["behaviors"][i]["name"] == "sureRoute":
				if srto == "None":
					del[rulesjson["rules"]["children"][0]["behaviors"][i]]
					print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Removed SureRoute behavior."+bcolors.ENDC
				else:
					rulesjson["rules"]["children"][0]["behaviors"][i]["options"]["testObjectUrl"] = srto
					rulesjson["rules"]["children"][0]["behaviors"][i]["options"].update({"enableCustomKey":False})
					print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Added SRTO successfully."+bcolors.ENDC
				break
		#print productId
		#print productId[0]
		if "SPM" in productId[0]:
			for i in range(0,len(rulesjson["rules"]["children"][0]["children"])):
				#print json["rules"]["children"][0]["children"][i]["name"]
				if rulesjson["rules"]["children"][0]["children"][i]["name"] == "JPEG Images":
					del[rulesjson["rules"]["children"][0]["children"][i]]
					print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Removed Adaptive Image Compression behavior."+bcolors.ENDC
					break
		#print "\n\n\n\n",json
		return rulesjson
	#def AdditionalOrigin(json,hostname,origin):
	#	for i in range(0,len(json["rules"]["behaviors"])):
	#		if json["rules"]["behaviors"][i]["name"] == "origin":
	#			currentOrigin = json["rules"]["behaviors"][i]["options"]["hostname"]
	#			break
	#	if currentOrigin == origin:
	#		ExistingOrigin = True
	#	else:
	#	sys.exit()
	def getPropertyId(contractId,groupId,propertyName):
		#print contractId,groupId,propertyName
		params.update({"contractId":contractId,"groupId":groupId})
		GPIresult = s.get(urljoin(baseurl, "/papi/v1/properties/"),params=params)
		for i in range(0,len(GPIresult.json()['properties']['items'])):
			#print resultIGP3.json()['properties']['items']
			if GPIresult.json()['properties']['items'][i]['propertyName'] == propertyName:
				propertyId = GPIresult.json()['properties']['items'][i]['propertyId']
		#print propertyId
		return propertyId
	def getHostnames(contractId,groupId,propertyId,propertyVersion):
		getHostHeader = {"PAPI-Use-Prefixes": "false"}
		params.update({"contractId":contractId,"groupId":groupId})
		getHosts = s.get(urljoin(baseurl, "/papi/v1/properties/"+propertyId+"/versions/"+str(propertyVersion)+"/hostnames"), headers=getHostHeader,params=params)
		configHostnames = getHosts.json()["hostnames"]["items"]
		return configHostnames
	def getEtag(contractId,groupId,propertyId,propertyVersion):
		params.update({"contractId":contractId,"groupId":groupId})
		GEresult = s.get(urljoin(baseurl, "/papi/v1/properties/"+propertyId+"/versions/"+propertyVersion),params=params)
		eTag = GEresult.json()["versions"]["items"][0]["etag"]
		return eTag
	def addInOrigins(rulesjson,origin,hosts,OriginsIndex):
		for i in range(0,len(rulesjson["rules"]["children"][OriginsIndex]["children"])):
			if origin == rulesjson["rules"]["children"][OriginsIndex]["children"][i]["behaviors"][0]["options"]["hostname"]:
				hostsCriteria = rulesjson["rules"]["children"][OriginsIndex]["children"][i]["criteria"][0]["options"]["values"]
				for item in hosts:
					hostsCriteria.append(item)
				#print hostsCriteria
				rulesjson["rules"]["children"][OriginsIndex]["children"][i]["criteria"][0]["options"]["values"] = hostsCriteria
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Provided Origin was found in Child Rule 'Origins'. Criteria Updated with hostnames accordingly."+bcolors.ENDC
		return rulesjson
	def AddNewOrigin(rulesjson,hosts,origin,OriginsIndex):
		if OriginsIndex == None:
			Origins = { "behaviors": [], "criteria": [], "criteriaMustSatisfy": "all", "name": "Origins", "children": [ { "behaviors": [ { "name": "origin", "options": { "cacheKeyHostname": "REQUEST_HOST_HEADER", "forwardHostHeader": "REQUEST_HOST_HEADER", "trueClientIpHeader": "True-Client-IP", "hostname": origin, "compress": True, "httpPort": 80, "enableTrueClientIp": True, "trueClientIpClientSetting": False, "originType": "CUSTOMER" } } ], "criteria": [ { "name": "hostname", "options": { "values": hosts, "matchOperator": "IS_ONE_OF" } } ], "criteriaMustSatisfy": "all", "name": origin, "children": [] } ] }
			rulesjson["rules"]["children"].append(Origins)
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"A new 'Origins' rule has been created."+bcolors.ENDC
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Child Rule with new Origin has been added to 'Origins'."+bcolors.ENDC
		else:
			Origins = { "behaviors": [ { "name": "origin", "options": { "cacheKeyHostname": "REQUEST_HOST_HEADER", "forwardHostHeader": "REQUEST_HOST_HEADER", "trueClientIpHeader": "True-Client-IP", "hostname": origin, "compress": True, "httpPort": 80, "enableTrueClientIp": True, "trueClientIpClientSetting": False, "originType": "CUSTOMER" } } ], "criteria": [ { "name": "hostname", "options": { "values": hosts, "matchOperator": "IS_ONE_OF" } } ], "criteriaMustSatisfy": "all", "name": origin, "children": [] }
			rulesjson["rules"]["children"][OriginsIndex]["children"].append(Origins)
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Child Rule with new Origin has been added to 'Origins'."+bcolors.ENDC
		return rulesjson
	def CurentOrigin(rulesjson):
		Origins = []
		OriginsIndex = None
		OriginsExist = False
		for i in range(0,len(rulesjson["rules"]["behaviors"])):
			if rulesjson["rules"]["behaviors"][i]["name"] == "origin":
				try:
					rulesjson["rules"]["behaviors"][i]["options"]["hostname"]
					defaultOrigin = rulesjson["rules"]["behaviors"][i]["options"]["hostname"]
				except KeyError:
					pass
				try:
					rulesjson["rules"]["behaviors"][i]["options"]["netStorage"]
					defaultOrigin = rulesjson["rules"]["behaviors"][i]["options"]["netStorage"]["downloadDomainName"]
				except KeyError:
					pass
		for i in range(0,len(rulesjson["rules"]["children"])):
			if rulesjson["rules"]["children"][i]["name"] == "Origins":
				OriginsIndex = i
				OriginsExist = True
		if OriginsExist == True:
			for i in range(0,len(rulesjson["rules"]["children"][OriginsIndex]["children"])):
				Origins.append(rulesjson["rules"]["children"][OriginsIndex]["children"][i]["behaviors"][0]["options"]["hostname"])
		#print defaultOrigin,Origins,OriginsExist,OriginsIndex
		return defaultOrigin,Origins,OriginsExist,OriginsIndex
	def BasePageRequest(hosts,edge,cdn):
		headers = {'X-Akamai-Debug': 'true', 'User-Agent': "Security Web API - SWaPI", 'Pragma': 'akamai-x-get-cache-key, akamai-x-get-true-cache-key, akamai-x-get-extracted-values, akamai-x-cache-remote-on, akamai-x-cache-on, akamai-x-check-cacheable, akamai-x-get-request-id, akamai-x-get-client-ip, akamai-x-get-nonces, akamai-xget-ssl-client-session-id, akamai-x-serial-no', 'X-Akamai-Meta-Trace': '1', 'X-Akamai-Request-Trace': 'all' } # , 'Cookie': 'Aka-Debug-Mdttrace=expires=1467070076~md5=7c593c6ecfecc473c86450fa8b5a5b89'
		platform = "mac"
		if "edgesuite" in edge:
			protocol = "http://"
		else:
			protocol = "https://"
		verify = False
		for host in hosts:
			DNSTOHOST(host,platform,cdn,edge)
			host = protocol+host
			#try:
			rs = requests.get(host, headers=headers, verify=verify)
			if rs.status_code in Bad_Codes:
				print bcolors.FAIL+"\n[PAPI] Base Page Request"+bcolors.ENDC
				print bcolors.FAIL+"[PAPI] Regression Test Result: FAILED."+bcolors.ENDC
				print bcolors.FAIL+"[PAPI] Host:",host+bcolors.ENDC
				print bcolors.FAIL+"[PAPI] StatusCode:",str(rs.status_code)+bcolors.ENDC
				print bcolors.FAIL+"[PAPI] Platform:",cdn+bcolors.ENDC
			else:
				print bcolors.WARNING+"\n[PAPI] Base Page Request"+bcolors.ENDC
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Regression Test Result: SUCCESS."+bcolors.ENDC
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Host:",host+bcolors.ENDC
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"StatusCode:",str(rs.status_code)+bcolors.ENDC
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Platform:",cdn+bcolors.ENDC
			#except:
			#	print bcolors.WARNING+"[RegressionTest] There was a problem processing request to host:",host
			#	print "[RegressionTest] You might want to check in a browser if it's working..."+bcolors.ENDC
		return
	def StagingRegressionTest(hostlist,edges,activationIdlist,contractIdlist,groupIdlist):
		cdn = "staging"
		for i in range(0,len(activationIdlist)):
			print bcolors.WHITE+'\n\n<!----------- Regression Test Module ----------->\n'+bcolors.ENDC
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Making sure Configuration is ACTIVE in Staging. This might take some time."+bcolors.ENDC
			path = activationIdlist[i].split("?")[0]
			#print path
			headers = {"PAPI-Use-Prefixes": "false"}
			params.update({"contractId":contractIdlist[i],"groupId":groupIdlist[i]})
			result = s.get(urljoin(baseurl, path), params=params,headers=headers)
			#print result.content
			status = result.json()["activations"]["items"][0]["status"]
			while status == "PENDING":
				PollResult = s.get(urljoin(baseurl, path), params=params,headers=headers)
				try:
					status = PollResult.json()["activations"]["items"][0]["status"]
				except:
					pass
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Configuration is active in Staging. Starting Staging Regression Test."+bcolors.ENDC
			BasePageRequest(hostlist[i],edges[i],cdn)
			print bcolors.WHITE+'\n\n<!----------- Regression Test Module ----------->'+bcolors.ENDC
		return
	def newIntegration(hosts,edge,cpcode,origin,contractId,groupId,productId,emails,PRd,cemails,ExistingEdge,ExistingCPCode,ExistingConfig,propertyId,propertyVersion,eTag,srto):
		#print hosts,edge,cpcode,origin,contractId,groupId,productId,emails,PRd,cemails,ExistingEdge,ExistingCPCode
		print bcolors.WHITE+'<!----------- ConfigCreator Module ----------->\n\n'+bcolors.ENDC
		#if ',' in hosts:
		#	hosts = hosts.split(",")
		#else:
		#	hosts = hosts.split("\n")
		# print emails
		# "edgeHostnameLink" : "/papi/v1/edgehostnames/ehn_2697366?options=mapDetails&groupId=grp_109027&contractId=ctr_F-MRTALC"
		# "cpcodeLink" : "/papi/v1/cpcodes/cpc_634219?groupId=grp_109027&contractId=ctr_F-MRTALC"
		if ExistingEdge == "FALSE":
			edgesplit = edge.split("edgesuite.net")
			prefix = edgesplit[0]
			#prefix = domainPrefix[:-1]
			ipVersion = "IPV4"
			edgeId = CreateANewEdge(productId,contractId,groupId,prefix,ipVersion)
		else:
			edgeId = edge
		if ExistingCPCode == "FALSE":
			cpcode = CreateCPCode(contractId,groupId,productId,propertyName)
		#print propertyName,contractId,groupId,productId
		if ExistingConfig == "FALSE":
			configHostnames = []
			CreateANewProperty(propertyName,contractId,groupId,productId)
			propertyId = getPropertyId(contractId,groupId,propertyName)
			eTag = getEtag(contractId,groupId,propertyId,propertyVersion)
			rulesjson = DownloadRule(contractId,groupId,propertyId,propertyVersion)
			modifiedrulesJson = ModifyOriginAndCPCode(rulesjson,cpcode,origin,productId,srto)
			UpdateRule(contractId,groupId,propertyId,propertyVersion,modifiedrulesJson)
		else:
			propertyVersion = CreateANewVersion(contractId,groupId,propertyId,propertyVersion,eTag)
			eTag = getEtag(contractId,groupId,propertyId,str(propertyVersion))
			configHostnames = getHostnames(contractId,groupId,propertyId,propertyVersion)
			rulesjson = DownloadRule(contractId,groupId,propertyId,propertyVersion)
			defaultOrigin,Origins,OriginsExist,OriginsIndex = CurentOrigin(rulesjson)
			if origin == defaultOrigin:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Same Origin found in Default Rule. No modification was done in ruleSet."+bcolors.ENDC
				pass
			elif origin in Origins:
				modifiedrulesJson = addInOrigins(rulesjson,origin,hosts,OriginsIndex)
				UpdateRule(contractId,groupId,propertyId,propertyVersion,modifiedrulesJson)
			else:
				modifiedrulesJson = AddNewOrigin(rulesjson,hosts,origin,OriginsIndex)
				UpdateRule(contractId,groupId,propertyId,propertyVersion,modifiedrulesJson)
				#pass
		#print propertyId
		#print eTag
		#print hosts
		for i in range(0,len(hosts)):
			addhosts = {"cnameType":"EDGE_HOSTNAME","cnameFrom":hosts[i],"cnameTo":edge}
			configHostnames.append(addhosts)
		#print configHostnames
		AddHostnames(contractId,groupId,propertyId,propertyVersion,eTag,configHostnames)
		cdn = "staging"
		actStagingLink = Activate(contractId,groupId,propertyId,propertyVersion,cdn,PRd,cemails,emails)
		cdn = "prod"
		actProdLink = Activate(contractId,groupId,propertyId,propertyVersion,cdn,PRd,cemails,emails)
		print bcolors.UNDERLINE+bcolors.WHITE+"\nConfiguration Summary:\n"+bcolors.ENDC
		print "Property Name:",propertyName
		print "Contract:",contractId
		print "Group:",groupId
		print "PropertyId:",propertyId
		print "CPCode:",cpcode
		print "Production Activation Link:",actProdLink["activationLink"]
		print "Staging Activation Link:",actStagingLink["activationLink"]
		print "EdgeId:",edgeId
		print "Hostnames:",hosts
		print "EdgeHostname:",edge
		print "Origin:",origin
		print "Customer Email:",cemails
		print "SA Email:",emails
		print "Peer Reviewer:",PRd
		print bcolors.WHITE+'\n\n<!----------- ConfigCreator Module ----------->\n\n'+bcolors.ENDC
		return actStagingLink["activationLink"]
		#sys.exit()
	if retrieveobj == "download":
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#contractId,groupId,propertyId,propertyVersion = InfoGathering()
		#print propertyVersion
		#if not propertyVersion:
		#	contractId,groupId,propertyId,propertyVersion = Search(None,propertyName,None,propertyVersion)
		#else:
		contractId,groupId,propertyId,propertyVersion = Search(None,propertyName,None,propertyVersion)
		#print contractId,groupId,propertyId,propertyVersion
		DownloadRule(contractId,groupId,propertyId,propertyVersion)
	elif retrieveobj == "Integration":
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify the an Integration Configuration file: -N KonaNowAPI\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#file_read = csv.reader('files/'+propertyName+".csv", dialect=csv.excel_tab)
		#spamreader = csv.reader(open('files/'+propertyName+".csv", 'rU'), dialect=csv.excel_tab)
		if not os.path.isfile("files/"+propertyName+".csv"):
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"This File does NOT exists: files/"+propertyName+".csv"'\n\n'+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		with open("files/"+propertyName+".csv", "rU") as file:
			fieldnames = ("Account","ContractId","GroupId","ProductId","Property Name","ExistingConfig","Hostnames","EdgeHostnames","Existing Edge","CPCodes","Existing CPCode","Origin","SA Email","PRr Email","Customer Email","SRTO")
			reader = csv.DictReader(file, fieldnames=fieldnames)
			#print reader
			configCounter = 0
			eTag = None
			hostlist = []
			edges = []
			activationIdlist = []
			contractIdlist = []
			groupIdlist = []
			for row in reader:
				if not row["Account"]:
					continue
				else:
					if configCounter == 0:
						configCounter = configCounter + 1
						pass
					else:
						contractId = row["ContractId"]
						groupId = row["GroupId"]
						productId = row["ProductId"]
						propertyName = row["Property Name"]
						ExistingConfig = row["ExistingConfig"]
						hosts = row["Hostnames"]
						edge = row["EdgeHostnames"]
						ExistingEdge = row["Existing Edge"]
						cpcode = row["CPCodes"]
						ExistingCPCode = row["Existing CPCode"]
						origin = row["Origin"]
						emails = row["SA Email"]
						PRd = row["PRr Email"]
						cemails = row["Customer Email"]
						srto = row["SRTO"]
						configCounter = configCounter + 1
						#print hosts,edge,cpcode,origin,contractId,groupId,productId,emails,PRd,cemails,ExistingEdge,ExistingCPCode
						#if action == "new":
						# propertyId,propertyVersion,eTag
						if ',' in hosts:
							hosts = hosts.split(",")
						else:
							hosts = hosts.split("\n")
						if ExistingConfig == "FALSE":
							Search(None,propertyName,None,propertyVersion)
							propertyVersion = "1"
							propertyId = None
							eTag = None
							activationId = newIntegration(hosts,edge,cpcode,origin,contractId,groupId,productId,emails,PRd,cemails,ExistingEdge,ExistingCPCode,ExistingConfig,propertyId,propertyVersion,eTag,srto)
						else:
							propertyId,propertyVersion,eTag = Search(None,propertyName,None,propertyVersion)
							activationId = newIntegration(hosts,edge,cpcode,origin,contractId,groupId,productId,emails,PRd,cemails,ExistingEdge,ExistingCPCode,ExistingConfig,propertyId,propertyVersion,eTag,srto)
					#	activationId = "/papi/v1/properties/416770/activations/5157970?groupId=33119&contractId=3-TWDH9B"
						hostlist.append(hosts)
						edges.append(edge)
						activationIdlist.append(activationId)
						contractIdlist.append(contractId)
						groupIdlist.append(groupId)
			#print hostlist
			#print edges
			#print activationIdlist
			#print contractIdlist
			#print groupIdlist
			#StagingRegressionTest(hostlist,edges,activationIdlist,contractIdlist,groupIdlist)
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == "poll":
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		edgeIDs = []
		if not edgeId:
			contractId,groupId,edgeIDs = Search(None,propertyName,None,propertyVersion)
		else:
			edgeIDs.append(edgeId)
			contractId,groupId = Search(None,propertyName,None,propertyVersion)
		PollEdgeHostname(contractId,groupId,edgeIDs)
		#else:
		#	print bcolors.WARNING+"Which object do you want to poll: edgehostnames\n\n"+bcolors.ENDC
		#print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		#sys.exit()
	elif retrieveobj == "freeze":
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#contractId,groupId,propertyId,propertyVersion = InfoGathering()
		contractId,groupId,propertyId,propertyVersion = Search(None,propertyName,None,propertyVersion)
		FreezeRule(contractId,groupId,propertyId,propertyVersion,ruleFormat)
	elif retrieveobj == "update":
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#contractId,groupId,propertyId,propertyVersion = InfoGathering()
		contractId,groupId,propertyId,propertyVersion = Search(None,propertyName,None,propertyVersion)
		#print contractId,groupId,propertyId,propertyVersion
		#print propertyName
		filename = "files/"+propertyName+".json"
		#print filename
		try:
			with open(filename) as json_data:
				rulesJson = json.load(json_data)
			#print(d)
			#rulesJson = open(filename, 'r').readlines()
		except:
			print bcolors.WARNING+"SWaPI was unable to find the json file in the files folder. It should have the same name as your configuration, with a .json extension.\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print rulesJson
		UpdateRule(contractId,groupId,propertyId,propertyVersion,rulesJson)
	elif retrieveobj == 'activate':
		if not emails:
			print bcolors.WARNING+"You need to specify the activation emails with: --emails asomarri@akamai.com\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if cdn == 'prod':
			if not cemails:
				print bcolors.WARNING+"You need to specify customer's emails with: --cemails customer@swapi.com\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if not PRd:
				print bcolors.WARNING+"You need to specify a PR'r with: --PRd atorresr@akamai.com\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if ',' in emails:
			emails = emails.split(',')
		else:
			emails = emails.split('\n')
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not cdn:
			print bcolors.WARNING+"You need to specify the Activation Platform: --cdn staging/prod\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not propertyVersion:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"LATEST version will be activated."+bcolors.ENDC
			#contractId,groupId,propertyId,latest = InfoGathering()
			contractId,groupId,propertyId,latest = Search(None,propertyName,None,propertyVersion)
			propertyVersion = latest
		else:
			#contractId,groupId,propertyId = InfoGathering()
			contractId,groupId,propertyId = Search(None,propertyName,None,propertyVersion)
		#print contractId,groupId,propertyId,propertyVersion,cdn,notes,emails
		Activate(contractId,groupId,propertyId,propertyVersion,cdn,PRd,cemails,emails)
	elif retrieveobj == 'newVersion':
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#contractId,groupId,propertyId,propertyVersion,eTag = InfoGathering()
		contractId,groupId,propertyId,propertyVersion,eTag = Search(None,propertyName,None,propertyVersion)
		#print contractId,groupId,propertyId,propertyVersion,eTag
		CreateANewVersion(contractId,groupId,propertyId,propertyVersion,eTag)
	elif retrieveobj == 'delete':
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#contractId,groupId,propertyId,propertyVersion,eTag = InfoGathering()
		contractId,groupId,propertyId = Search(None,propertyName,None,propertyVersion)
		#print contractId,groupId,propertyId,propertyVersion,eTag
		deleteConfiguration(contractId,groupId,propertyId)
	elif retrieveobj == 'clone':
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#contractId,groupId,productId,propertyId,propertyVersion,eTag = InfoGathering()
		if not cloneFrom:
			print bcolors.WARNING+"Please specify a configuration name to Clone From with the '--from' option.\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		contractId,groupId,productId,propertyId,propertyVersion,eTag = Search(None,cloneFrom,None,propertyVersion)
		#print contractId,groupId,productId,propertyId,propertyVersion,eTag
		CloneAProperty(propertyName,contractId,groupId,productId,propertyId,propertyVersion,eTag,copyHostnames)
	elif retrieveobj == 'create':
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if cpcode and not host:
			contractId,groupId,productId = Search(None,propertyName,None,propertyVersion)
			CreateCPCode(contractId,groupId,productId,cpcode)
		if edge and not host:
			contractId,groupId,productId = Search(None,propertyName,None,propertyVersion)
			edgesplit = edge.split("edgesuite.net")
			prefix = edgesplit[0]
			CreateANewEdge(productId,contractId,groupId,prefix,ipVersion)
		if not productId:
			if not cloneFrom:
				productId = 'Site_Defender'
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Product NOT specified. SWaPI's Default: Site_Defender"+bcolors.ENDC
		if cloneFrom:
			#contractId,groupId,productId = InfoGathering()
			contractId,groupId,productId = Search(None,cloneFrom,None,propertyVersion)
		#elif (contractId == None) and (groupId == None):
		#	contractId,groupId = InfoGathering()
		#	print bcolors.WARNING+"[ConfigCreate] Configuration will be created in Top Level Group"+bcolors.ENDC
		elif not contractId or not groupId:
			TLDGroup = s.get(urljoin(baseurl, '/papi/v1/groups/'))
			#print bcolors.WARNING+"You need to specify a contractId and a groupId: --contract ctr_F-MRTALC --group grp_109031"+bcolors.ENDC
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Group NOT specified, creating config in Top Level Group."+bcolors.ENDC
			#print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			for item in TLDGroup.json()['groups']['items']:
				try:
					item['parentGroupId']
					pass
				except:
					groupId = item['groupId']
					contractId = item['contractIds'][0]
			#print groupId
			#print contractId
		#print propertyName,contractId,groupId,productId
		if host:
			if not edge:
				print bcolors.WARNING+"You need to specify your EdgeHostname: -E swapi.akamai.io.edgesuite.net\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if not cpcode:
				print bcolors.WARNING+"You need to provide a CPCODE to add: --cpcode 740920\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if not edge:
				print bcolors.WARNING+"You need to provide an Origin: --origin origin-www.customer.com\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			if stagingPush:
				if not emails:
					print bcolors.WARNING+"You need to specify the activation emails with: --emails asomarri@akamai.com\n\n"+bcolors.ENDC
					print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
					sys.exit()
			configHostnames = []
			propertyId = CreateANewProperty(propertyName,contractId,groupId,productId)
			propertyVersion = '1'
			eTag = getEtag(contractId,groupId,str(propertyId),propertyVersion)
			if ',' in host:
				host = host.split(",")
			else:
				host = host.split("\n")
			for i in range(0,len(host)):
				addhosts = {"cnameType":"EDGE_HOSTNAME","cnameFrom":host[i],"cnameTo":edge}
				configHostnames.append(addhosts)
			#print configHostnames
			AddHostnames(contractId,groupId,str(propertyId),propertyVersion,eTag,configHostnames)
			rulesjson = DownloadRule(contractId,groupId,str(propertyId),propertyVersion)
			modifiedrulesJson = ModifyOriginAndCPCode(rulesjson,cpcode,origin,productId,srto)
			UpdateRule(contractId,groupId,str(propertyId),propertyVersion,modifiedrulesJson)
			if stagingPush:
				cdn = 'staging'
				if ',' in emails:
					emails = emails.split(',')
				else:
					emails = emails.split('\n')
				#print contractId,groupId,propertyId,propertyVersion,cdn,notes,emails
				Activate(contractId,groupId,str(propertyId),propertyVersion,cdn,PRd,cemails,emails)
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			CreateANewProperty(propertyName,contractId,groupId,productId)
		#contractId,groupId,productId = InfoGathering()
		#print propertyName
	elif (retrieveobj == 'add') or (retrieveobj == 'remove'):
		if not propertyName:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#contractId,groupId,propertyId,propertyVersion,eTag,configHostnames = InfoGathering()
		contractId,groupId,propertyId,propertyVersion,eTag,configHostnames = Search(None,propertyName,None,propertyVersion)
		#print contractId,groupId,propertyId,propertyVersion,eTag,configHostnames
		#sys.exit()
		if not host:
			print bcolors.WARNING+"You need to specify a hostname to add with the target option: -t mother-ship.metroid.akamaiu.com\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			if ',' in host:
				hosts = host.split(',')
			else:
				hosts = host.split('\n')
			hostsIndex = len(hosts)
		if retrieveobj == 'remove':
			for host in hosts:
				hostFound = False
				#print host
				for i in range(0,len(configHostnames)):
					#print configHostnames[i]
					if host in configHostnames[i]['cnameFrom']:
						DeleteIndex = i
						hostFound = True
					else:
						if i == (len(configHostnames)-1) and (hostFound == False):
							print bcolors.WARNING+"SWaPI was unable to find this hostname in the specified configuration:",host,"\n\n"+bcolors.ENDC
							print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
							sys.exit()
				del configHostnames[DeleteIndex]
			#print configHostnames
			AddHostnames(contractId,groupId,propertyId,propertyVersion,eTag,configHostnames)
		if not edge:
			print bcolors.WARNING+"You need to specify an EdgeHostname to associate your hostnames: -E metroid.akamaiu.com.edgesuite.net\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			if ',' in edge:
				edges = edge.split(',')
			else:
				edges = edge.split('\n')
			edgesIndex = len(edges)
		#print hosts
		#print edges
		if len(hosts) == 1:
			if len(edges) != 1:
				print bcolors.WARNING+"The number of EdgeHostnames does not match the number of hostnames.\n\n"+bcolors.ENDC+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			else:
				addhosts = {"cnameType":"EDGE_HOSTNAME","cnameFrom":hosts[0],"cnameTo":edges[0]}
			configHostnames.append(addhosts)
		else:
			if len(edges) == 1:
				for i in range(0,len(hosts)):
					addhosts = {"cnameType":"EDGE_HOSTNAME","cnameFrom":hosts[i],"cnameTo":edges[0]}
					configHostnames.append(addhosts)
			elif len(edges) != len(hosts):
				print bcolors.WARNING+"The number of EdgeHostnames does not match the number of hostnames.\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
			else:
				for i in range(0,len(hosts)):
					addhosts = {"cnameType":"EDGE_HOSTNAME","cnameFrom":hosts[i],"cnameTo":edges[i]}
					configHostnames.append(addhosts)
		#print configHostnames
		AddHostnames(contractId,groupId,propertyId,propertyVersion,eTag,configHostnames)
	elif retrieveobj == 'search':
		headers = {'Content-Type':'application/json',"PAPI-Use-Prefixes":"false"}
		if edge:
			body = {"edgeHostname":edge}
		elif propertyName:
			body = {"propertyName":propertyName}
		elif host:
			body = {"hostname":host}
		else:
			print bcolors.WARNING+"You need to specify either a target '-t', an EdgeHostname '-E' or a Property Name '--name'.\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		result = s.post(urljoin(baseurl, '/papi/v1/search/find-by-value'),headers=headers,json=body,params=params)
		#print "StatusCode: "+str(result.status_code)
		#print result.content
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Search Results: "+bcolors.ENDC
				SearchTable = tt.Texttable()
				if propertyName:
					Searchheader = ['Contract','Group','PropertyId','Property Name','Version','Production Status','Staging Status','Updated By User']
					SearchTable.header(Searchheader)
					SearchTable.set_cols_width([12,12,12,40,7,16,16,25])
					SearchTable.set_cols_align(['c','c','c','c','c','c','c','c'])
					SearchTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
					for item in result.json()['versions']['items']:
						#print item
						Searchrow = [item['contractId'],item['groupId'],item['propertyId'],item['propertyName'],str(item['propertyVersion']),item['productionStatus'],item['stagingStatus'],item['updatedByUser']]
						SearchTable.add_row(Searchrow)
				else:
					Searchheader = ['Contract','Group','PropertyId','Property Name','Version','Edge','Hostname']
					SearchTable.header(Searchheader)
					SearchTable.set_cols_width([12,12,12,40,7,45,45])
					SearchTable.set_cols_align(['c','c','c','c','c','c','c'])
					SearchTable.set_cols_valign(['m','m','m','m','m','m','m'])
					for item in result.json()['versions']['items']:
						#print item
						Searchrow = [item['contractId'],item['groupId'],item['propertyId'],item['propertyName'],str(item['propertyVersion']),item['edgeHostname'],item['hostname']]
						SearchTable.add_row(Searchrow)
				SRCHTable = SearchTable.draw()
				print SRCHTable
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'settings':
		result = s.get(urljoin(baseurl, '/papi/v1/client-settings'),params=params)
		print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
		#print result.content
		json_data = result.json()
		formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'build':
		result = s.get(urljoin(baseurl, '/papi/v1/build'),params=params)
		print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
		json_data = result.json()
		formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'formats':
		result = s.get(urljoin(baseurl, '/papi/v1/rule-formats'),params=params)
		print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
		#print result.content
		json_data = result.json()
		formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'locations':
		result = s.get(urljoin(baseurl, '/diagnostic-tools/v2/ghost-locations/available'),params=params)
		#print result.content
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['locations']:
					#print item
					Hostnameheader = ['ID', 'Location']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([50,50])
					HostnameTable.set_cols_align(['c','c'])
					HostnameTable.set_cols_valign(['m','m'])
					Hostnamerow = [item['id'],item['value']]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
				print HostTable
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == "entitlement":
		contracts = []
		groups = []
		CPCode_Product = []
		Contract_Product = []
		all_properties = []
		all_properties2 = []
		Config_CPCode = []
		Product_Dictionary = {}
		data = {}
		start_time = time.time()
		result = s.get(urljoin(baseurl, '/papi/v1/contracts'),params=params)
		if result.status_code == 200:
			data.update({"account_ID":result.json()['accountId']})
			for item in result.json()['contracts']['items']:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Querying Contract: "+item['contractId']+bcolors.ENDC
				params.update({'contractId':item['contractId']})
				contracts.append(item['contractId'])
				products = s.get(urljoin(baseurl, '/papi/v1/products'),params=params)
				if products.status_code == 200:
					data.update({"Products":products.json()["products"]["items"]})
					product_total = len(products.json()["products"]["items"])
					for product in products.json()['products']['items']:
						print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Found Product: "+product['productName']+bcolors.ENDC
						CPCode_Product.append(product['productName'])
				else:
					pass
				#ctr_prd = s.get(urljoin(baseurl, '/contract-api/v1/contracts/'+item['contractId'].lstrip('ctr_')+'/products/summaries'),params=params)
				#if ctr_prd.status_code == 200:
					#print ctr_prd.json()
				#	for prd_item in ctr_prd.json()['products']['marketing-products']:
				#		Contract_Product.append(prd_item['marketingProductName'])
				#	Contract_Product = list(set(Contract_Product))
				#	Product_Dictionary.update({ctr_prd.json()['products']['contractId']:Contract_Product})
				#else:
				#	print ctr_prd.json()
			contracts = list(set(contracts))
			data.update({"contracts":contracts})
		else:
			pass
		#print Contract_Product
		#for h in Product_Dictionary:
		#	print Product_Dictionary[h]
		apigroups = s.get(urljoin(baseurl, '/papi/v1/groups'),params=params)
		#print result.json()
		#Account_Name = result.json()["accountName"]
		#print bcolors.WARNING+"\n\nAccount Name: "+result.json()["accountName"]+bcolors.ENDC+"\n"
		#data.update({"Account_Name":Account_Name})
		for item in apigroups.json()['groups']['items']:
			Account_Name = apigroups.json()['accountName']
			#groups.append(item['groupId'])
			#print item['groupName']
			#print item['contractIds']
			#for contract in item['contractIds']:
				#contracts.append(contract)
		#print contracts
		#print groups
		#for contract in contracts:
			#for group in groups:
				#print group, contract
			try:
				item['contractIds']
				params.update({'contractId':item['contractIds'][0],'groupId':item['groupId']})
				#result = s.get(urljoin(baseurl, '/papi/v1/cpcodes'), params=params)
				#if result.status_code == 200:
					#print result.json()
					#for i in range(0,len(result.json()["cpcodes"]["items"])):
						#try:
							#result.json()["cpcodes"]["items"][i]["productIds"][0]
							#print result.json()["cpcodes"]["items"][i]["productIds"][0]
							#CPCode_Product.append(result.json()["cpcodes"]["items"][i]["productIds"][0])
						#except:
							#pass
				#else:
					#pass
				apiproperties = s.get(urljoin(baseurl, '/papi/v1/properties'), params=params)
				if apiproperties.status_code == 200:
					#print result.json()["properties"]["items"]
					PropertiesList = apiproperties.json()["properties"]["items"]
					for item in PropertiesList:
						print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Property: "+item["propertyName"]+bcolors.ENDC
						print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Latest Version Found: "+str(item["latestVersion"])+bcolors.ENDC
						params.update({"validateRules":"fast"})
						config = s.get(urljoin(baseurl, "/papi/v1/properties/"+item["propertyId"]+"/versions/"+str(item["latestVersion"])+"/rules"), params=params)
						if config.status_code == 200:
							for behavior in config.json()["rules"]["behaviors"]:
								if behavior["name"] == "cpCode":
									#print behavior["options"]
									url = '/papi/v1/cpcodes/'+str(behavior["options"]["value"]["id"])
									cpcode_request = s.get(urljoin(baseurl, url), params=params)
									try:
										cpcode_request.json()["cpcodes"]["items"][0]["productIds"][0]
										#print cpcode_request.json()["cpcodes"]["items"][0]["productIds"][0]
										Config_CPCode.append(cpcode_request.json()["cpcodes"]["items"][0]["productIds"][0].replace("prd_",""))
										print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Product found: "+cpcode_request.json()["cpcodes"]["items"][0]["productIds"][0]+bcolors.ENDC
										item["Product"] = cpcode_request.json()["cpcodes"]["items"][0]["productIds"][0]
										if len(PropertiesList) > 1:
											print bcolors.TURQUO+bcolors.BOLD+"\n------------------------Property Separator------------------------\n"+bcolors.ENDC
									except:
										print "\n"
										pass
									#try:
									#	behavior["options"]["value"]["products"][0]
									#	Config_CPCode.append(behavior["options"]["value"]["products"][0])
									#	print bcolors.WARNING+"[Property Main CPCode] "+bcolors.ENDC+"Product found: "+behavior["options"]["value"]["products"][0]+"\n"
									#	item["Product"] = behavior["options"]["value"]["products"][0]
										#print behavior["options"]["value"]["products"][0]
									#except:
									#	print "\n"
									#	pass
						else:
							#print result.json()
							pass
					#all_properties.append(result.json()["properties"]["items"])
					all_properties.append(PropertiesList)
				else:
					#print result.json()
					pass
			except:
				pass
		#print all_properties
		print Config_CPCode
		TotalTime = (time.time() - start_time)
		AverageTime = TotalTime/len(Config_CPCode)
		data.update({"Config_CPCode":Config_CPCode})
		CPCode_Product = list(set(CPCode_Product))
		#print len(CPCode_Product)
		found_Products = list(set(Config_CPCode))
		#print Config_CPCode
		#print CPCode_Product
		Usage = len(found_Products)
		Percentage_Use = {}
		Summary = {}
		Summary.update({"Account_Name":Account_Name})
		Summary.update({"Total":str(len(Config_CPCode))})
		print bcolors.WHITE+"\n\n[Summary] \n"+bcolors.ENDC
		print bcolors.WARNING+"Account Name: "+Account_Name+bcolors.ENDC
		print bcolors.WARNING+"Total Time: "+str(TotalTime)+bcolors.ENDC
		print bcolors.WARNING+"Total Amount of configurations: "+str(len(Config_CPCode))+bcolors.ENDC
		print bcolors.WARNING+"Average time per config: "+str(AverageTime)+bcolors.ENDC+"\n"
		for item in CPCode_Product:
			#print item
			#print item.lstrip( 'prd_' )
			amount = Config_CPCode.count(item.lstrip( 'prd_' ))
			percentage = ( 100.00 * amount ) / len(Config_CPCode)
			#print round(percentage,2)
			print bcolors.WARNING+"Product: "+item+bcolors.ENDC
			print bcolors.WARNING+"Total Configurations Found: "+str(amount)+bcolors.ENDC
			print bcolors.WARNING+"Usage Percentage: "+str(round(percentage,2)) + "%"+bcolors.ENDC+"\n"
			Summary.update({item:{"Total":str(amount),"Percentage":str(round(percentage,2))}})
			Percentage_Use.update({item:round(percentage,2)})
		data.update({"Percentage_Use":Percentage_Use})
		data.update({"Properties":all_properties})
		data.update({"Summary":Summary})
		#print Summary
		#print CPCode_Product
		#headers = {"PAPI-Use-Prefixes":"false"}
		#ctr_result = s.get(urljoin(baseurl, '/papi/v1/contracts'),headers=headers,params)
		#contracts = ctr_result.json()['contracts']['items']
		#print contracts
		#for contract in contracts:
			#print contract
		#	payload = {'contractId': contract['contractId']}
		#	result = s.get(urljoin(baseurl, '/papi/v1/products'), params=payload)
			#print result
		#	data.update({"Products":result.json()["products"]["items"]})
			#product_total = len(result.json()["products"]["items"])
		product_total = len(CPCode_Product)
		product_Utilization = (Usage * 100) / product_total
		data.update({"Product_Utilization":product_Utilization})
		data.update({"Product_Used":Usage})
		data.update({"Product_Total":product_total})
		print bcolors.TURQUO+"[Results] "+bcolors.WARNING+"Product Utilization: "+str(product_Utilization)+bcolors.ENDC
		print bcolors.TURQUO+"[Results] "+bcolors.WARNING+"Percentage Use: "+str(Percentage_Use)+"%"+bcolors.ENDC
		print bcolors.TURQUO+"[Results] "+bcolors.WARNING+"Product Utilization: "+str(product_Utilization)+bcolors.ENDC
		print bcolors.TURQUO+"[Results] "+bcolors.WARNING+"Products Used: "+str(Usage)+bcolors.ENDC
		print bcolors.TURQUO+"[Results] "+bcolors.WARNING+"Total Products: "+str(product_total)+bcolors.ENDC
		print CPCode_Product
		data.update({"CPCode_Product":CPCode_Product})
		print data
		sys.exit()
	elif retrieveobj == 'audit':
		if ',' in AccountSwitch:
			AccountSwitch = AccountSwitch.split(',')
		else:
			AccountSwitch = AccountSwitch.split(',')
		#print AccountSwitch
		with open('files/'+AccountSwitch[0]+'-DeliveryAudit.csv', 'wb') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			header = ['Account ID','Account Name','Contract','Group','Property Name','Property ID','PROD Version','Product','Hostnames','Default Origin','Default CPCode','Default CPCode Name','Tier Distribution','SiteShield']
			wr.writerow(header)
			for account in AccountSwitch:
				#print account
				filename = '.map'
				readfile = open(filename, 'r')
				contents = readfile.readlines()
				for item in contents:
					if "[" and "]" in item:
						accountCheck = item[1:-2]
						if accountCheck == account:
							AccountSwitchKey = contents[contents.index(item)+1].strip()
							#print bcolors.TURQUO+"[APPSEC]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name "+account+" found and mapped to Account "+contents[contents.index(item)+1].strip()+bcolors.ENDC
				#print AccountSwitch
				try:
					AccountSwitchKey
				except:
					 AccountSwitchKey = account
				params = {'accountSwitchKey':AccountSwitchKey}
				groupapi = s.get(urljoin(baseurl, '/papi/v1/groups/'),params=params)
				if groupapi.status_code == 200:
					if len(AccountSwitch) > 1:
						print bcolors.TURQUO+'\n------------------------------ Separator ------------------------------\n'+bcolors.ENDC
					print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WHITE+" Friendly Name: "+account+bcolors.ENDC
					print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WHITE+" Account: "+AccountSwitchKey+bcolors.ENDC
					for item in groupapi.json()['groups']['items']:
						try:
							item['contractIds']
							params.update({'contractId':item['contractIds'][0],'groupId':item['groupId']})
							propertyapi = s.get(urljoin(baseurl, '/papi/v1/properties/'),params=params)
							if propertyapi.status_code == 200:
								for pmconfig in propertyapi.json()['properties']['items']:
									if pmconfig['productionVersion'] != None:
										print bcolors.TURQUO+'[PAPI]'+bcolors.WARNING+' Retrieving information from Property Manager Config: '+bcolors.WHITE+pmconfig['propertyName']+bcolors.ENDC
										accountName = groupapi.json()['accountName']
										hostnames = []
										hostnamesapi = s.get(urljoin(baseurl, '/papi/v1/properties/'+pmconfig['propertyId']+'/versions/'+str(pmconfig['productionVersion'])+'/hostnames/'),params=params)
										if hostnamesapi.status_code == 200:
											#print hostnamesapi.json()
											for host in hostnamesapi.json()['hostnames']['items']:
												hostnames.append(host['cnameFrom'])
										else:
											pass
										ruleTreeapi = s.get(urljoin(baseurl, '/papi/v1/properties/'+pmconfig['propertyId']+'/versions/'+str(pmconfig['productionVersion'])+'/rules/'),params=params)
										if ruleTreeapi.status_code == 200:
											defaultOrigin = 'None'
											defaultCPCode = 'None'
											defaultCPCodeName = 'None'
											defaultProduct = 'None'
											TD = 'None'
											SS = 'None'
											for rulebehavior in ruleTreeapi.json()['rules']['behaviors']:
												if rulebehavior['name'] == 'origin':
													#print rulebehavior['options']['hostname']
													if rulebehavior['options']['originType'] == 'CUSTOMER':
														defaultOrigin = rulebehavior['options']['hostname']
													else:
														defaultOrigin = rulebehavior['options']['netStorage']['downloadDomainName']
												if rulebehavior['name'] == 'cpCode':
													#print rulebehavior['options']['value']['id']
													defaultCPCode = rulebehavior['options']['value']['id']
													try:
														rulebehavior['options']['value']['name']
														defaultCPCodeName = rulebehavior['options']['value']['name']
													except:
														pass
													try:
														rulebehavior['options']['value']['products'][0]
														defaultProduct = rulebehavior['options']['value']['products'][0]
													except:
														pass
												if rulebehavior['name'] == 'tieredDistribution':
													if rulebehavior['options'] == 'False':
														TD = 'Disabled'
													else:
														try:
															rulebehavior['options']['tieredDistributionMap']
															TD = rulebehavior['options']['tieredDistributionMap']
														except:
															TD = 'Default'
												if rulebehavior['name'] == 'siteShield':
													SS = rulebehavior['options']['ssmap']['value']
													#print rulebehavior['options']['value']['name']
													#print rulebehavior['options']['value']['products'][0]
											#print groupapi.json()['accountId']
											#print groupapi.json()['accountName']
											#print item['contractIds'][0]
											#print item['groupId']
											#print pmconfig['propertyName']
											#print pmconfig['propertyId']
											#print defaultProduct
											#print str(pmconfig['productionVersion'])
											#print hostnames
											#print defaultOrigin
											#print defaultCPCode
											#print defaultCPCodeName
											#print TD
											#print SS
											#print 'Finished Printing'
											mylist =  [groupapi.json()['accountId'],groupapi.json()['accountName'],item['contractIds'][0],item['groupId'],pmconfig['propertyName'],pmconfig['propertyId'],str(pmconfig['productionVersion']),defaultProduct,hostnames,defaultOrigin,defaultCPCode,defaultCPCodeName,TD,SS]
											#print mylist
											#mylist.append(riskgroup)
											#print mylist
											wr.writerow(mylist)
										elif ruleTreeapi.status_code == 403:
											print bcolors.TURQUO+"[PAPI]"+bcolors.WARNING+" Permission Denied to Property: "+pmconfig['propertyId']+bcolors.ENDC
											print ruleTreeapi.content
										else:
											#print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(ruleTreeapi.status_code)+bcolors.ENDC
											print bcolors.TURQUO+"[PAPI]"+bcolors.WARNING+" There was a problem processing your request: "+str(ruleTreeapi.status_code)+bcolors.ENDC
											print ruleTreeapi.content
									else:
										pass
							else:
								#print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(propertyapi.status_code)+bcolors.ENDC
								print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request: "+str(propertyapi.status_code)+bcolors.ENDC
								print propertyapi.content
						except:
							pass
					if len(AccountSwitch) > 1:
						print bcolors.TURQUO+'\n------------------------------ Separator ------------------------------\n'+bcolors.ENDC
				elif groupapi.status_code == 401:
					print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" NOT Authorized: "+str(groupapi.status_code)+bcolors.ENDC
					print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" Are you sure you using the right account? "+bcolors.ENDC
					print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" Account Name: "+account+bcolors.ENDC
					#print msc.content
				else:
					print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" StatusCode: "+str(groupapi.status_code)+bcolors.ENDC
					print bcolors.TURQUO+"[PAPI]"+bcolors.ENDC+bcolors.WARNING+" There was a problem processing your request for account: "+account+bcolors.ENDC
					print groupapi.content
		if os.stat('files/'+AccountSwitch[0]+'-DeliveryAudit.csv').st_size != '204':
			print bcolors.TURQUO+'\n------------------------------------------------------------------------------------------------------------------------'
			print bcolors.TURQUO+'[PAPI]'+bcolors.ENDC+' CSV report generated. Filename: files/'+AccountSwitch[0]+'-DeliveryAudit.csv'
			print bcolors.TURQUO+'------------------------------------------------------------------------------------------------------------------------'
		else:
			pass
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'groups':
		result = s.get(urljoin(baseurl, '/papi/v1/groups/'),params=params)
		#print result.content
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Account: "+result.json()['accountName']+bcolors.ENDC
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['groups']['items']:
					#print item
					Hostnameheader = ['Contract', 'Group ID', 'Group Name', 'Parent Group Id']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([20,20,60,20])
					HostnameTable.set_cols_align(['c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m'])
					try:
						item['parentGroupId']
						parentGroupId = item['parentGroupId']
					except:
						parentGroupId = "Parent"
					try:
						item['contractIds'][0]
						contract = item['contractIds'][0]
					except:
						contract = None
					Hostnamerow = [contract,item['groupId'],item['groupName'],parentGroupId]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
				print HostTable
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'properties':
		headers = {"PAPI-Use-Prefixes":"false"}
		if propertyName:
			accountId,contractId,groupId,propertyId = Search(None,propertyName,None,propertyVersion)
			params.update({'contractId':contractId,'groupId':groupId})
			url = '/papi/v1/properties/'+propertyId
			result = s.get(urljoin(baseurl, url), headers=headers, params=params)
			#print result.content
			if result.status_code == 200:
				if respjson:
					json_data = result.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					#print colorful_json
					print result.content
					sys.exit()
				else:
					#print result.json()['configurations']
					HostnameTable = tt.Texttable()
					#HostnameTable.set_deco(tt.Texttable.HEADER)
					for item in result.json()['properties']['items']:
						#print item
						Hostnameheader = ['Contract','Group','Property ID', 'Property Name', 'Asset ID', 'Latest Version', 'Production', 'Staging']
						HostnameTable.header(Hostnameheader)
						HostnameTable.set_cols_width([20,20,20,45,20,15,15,15])
						HostnameTable.set_cols_align(['c','c','c','c','c','c','c','c'])
						HostnameTable.set_cols_valign(['m','m','m','m','m','m','m','m'])
						try:
							item['productionVersion']
							productionVersion = item['productionVersion']
						except:
							productionVersion = None
						try:
							item['stagingVersion']
							stagingVersion = item['stagingVersion']
						except:
							stagingVersion = None
						Hostnamerow = [item['contractId'],item['groupId'],item['propertyId'],item['propertyName'],item['assetId'],item['latestVersion'],productionVersion,stagingVersion]
						HostnameTable.add_row(Hostnamerow)
						HostTable = HostnameTable.draw()
					try:
						print HostTable
					except:
						print bcolors.TURQUO+"[PAPI]"+bcolors.WARNING+" No Properties found in this group: "+groupId+bcolors.ENDC
			else:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			result = s.get(urljoin(baseurl, '/papi/v1/groups/'),params=params)
			#print result.content
			if result.status_code == 200:
				url = '/papi/v1/properties/'
				propertiesTable = tt.Texttable()
				propHeader = ['Contract','Group Name','Group ID','Property ID', 'Property Name', 'Asset ID', 'Latest Version', 'Production', 'Staging']
				propertiesTable.header(propHeader)
				propertiesTable.set_cols_width([15,25,15,15,50,12,12,12,12])
				propertiesTable.set_cols_align(['c','c','c','c','c','c','c','c','c'])
				propertiesTable.set_cols_valign(['m','m','m','m','m','m','m','m','m'])
				for item in result.json()['groups']['items']:
					#print itemtry:
					try:
						item['contractIds'][0]
						contract = item['contractIds'][0]
						groupName = item['groupName']
						params.update({'contractId':contract,'groupId':item['groupId']})
						result2 = s.get(urljoin(baseurl, url), headers=headers, params=params)
						if result2.status_code == 200:
							if respjson:
								json_data = result2.json()
								formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
								colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
								#print colorful_json
								print result2.content
							else:
								#HostnameTable.set_deco(tt.Texttable.HEADER)
								for item in result2.json()['properties']['items']:
									#print item
									if automation:
										print item['propertyName']
									else:
										try:
											item['productionVersion']
											productionVersion = item['productionVersion']
										except:
											productionVersion = None
										try:
											item['stagingVersion']
											stagingVersion = item['stagingVersion']
										except:
											stagingVersion = None
										propRow = [item['contractId'],groupName,item['groupId'],item['propertyId'],item['propertyName'],item['assetId'],item['latestVersion'],productionVersion,stagingVersion]
										propertiesTable.add_row(propRow)
							#except:
							#	print bcolors.TURQUO+"[PAPI]"+bcolors.WARNING+" No Properties found in this group: "+groupId+bcolors.ENDC
					except:
						pass
				if respjson or automation:
					sys.exit()
				HostTable = propertiesTable.draw()
				print HostTable
			else:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'contracts':
		result = s.get(urljoin(baseurl, '/papi/v1/contracts/'),params=params)
		#print result.content
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Account ID: "+result.json()['accountId']+bcolors.ENDC
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['contracts']['items']:
					#print item
					Hostnameheader = ['Contract', 'Contract Name']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([20,40])
					HostnameTable.set_cols_align(['c','c'])
					HostnameTable.set_cols_valign(['m','m'])
					Hostnamerow = [item['contractId'],item['contractTypeName']]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
				print HostTable
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'products':	# /papi/v1/products/{?contractId}
		result = s.get(urljoin(baseurl, '/papi/v1/contracts/'),params=params)
		#print result.content
		if result.status_code == 200:
			if not respjson:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Account ID: "+result.json()['accountId']+bcolors.ENDC
			for item in result.json()['contracts']['items']:
				#print item
				headers = {"PAPI-Use-Prefixes":"false"}
				params.update({'contractId':item['contractId']})
				result2 = s.get(urljoin(baseurl, '/papi/v1/products/'), headers=headers, params=params)
				#print result.content
				if result2.status_code == 200:
					if respjson:
						json_data = result2.json()
						formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
						colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
						#print colorful_json
						print result2.content
					else:
						print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Contract ID: "+result2.json()['contractId']+bcolors.ENDC
						#print result.json()['configurations']
						HostnameTable = tt.Texttable()
						#HostnameTable.set_deco(tt.Texttable.HEADER)
						for item in result2.json()['products']['items']:
							#print item
							Hostnameheader = ['Product ID', 'Product Name']
							HostnameTable.header(Hostnameheader)
							HostnameTable.set_cols_width([30,30])
							HostnameTable.set_cols_align(['c','c'])
							HostnameTable.set_cols_valign(['m','m'])
							Hostnamerow = [item['productId'],item['productName']]
							HostnameTable.add_row(Hostnamerow)
							HostTable = HostnameTable.draw()
						print HostTable
				else:
					json_data = result2.json()
					formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
					colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
					print colorful_json
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if retrieveobj not in ['patch','audit','entitlement','groups','contracts','products','versions','properties','ruleTree','hostnames','cpcodes','edgehostnames','locations','latest','settings','build','formats','create','delete','newVersion','add','remove','activate','Integration']:
		print bcolors.WHITE+"This module allows you to view/modify/create/activate Property Manager Configurations\n"+bcolors.ENDC
		print bcolors.WARNING+"PAPI Retrieve Information:\n"+bcolors.ENDC
		print "groups 		- List all ACGs (Access Control Groups)"
		print "contracts 	- List all Contracts"
		print "products 	- List all Products associated to a contract"
		print "versions 	- List all versions of a specified Property Manager Configuration"
		print "properties 	- List all Property Manager Configurations created under a specified ACG"
		print "ruleTree 	- Display JSON file for a specified Property Manager Configuration"
		print "hostnames 	- List all hostnames of associated to a Property Manager Configuration"
		print "cpcodes 	- List CPCodes associated to an ACG"
		print "edgehostnames 	- List Edgehostnames associated to an ACG"
		print "latest"
		print "locations"
		print "settings"
		print "build"
		print "formats"
		print bcolors.WARNING+"\nPAPI Actions:\n"+bcolors.ENDC
		print "create 		- You can use it to create new PM Configurations, CPCODES, Edge Hostnames"
		print "delete 		- Delete a PM Configuration. Only works if not active in either Staging or PROD"
		print "newVersion 	- You can use it to create new PM Configurations, CPCODES, Edge Hostnames"
		print "add 		- Add hostnames to a specific PM Configuration"
		print "remove 		- Remove hostnames from a specific PM Configuration"
		print "download 	- Download ruleTree into a JSON file"
		print "update 		- Update ruleTree with local JSON file"
		print "activate 	- Activate Configuration to Staging or Production"
		print bcolors.WARNING+"\nSWaPI Automations:\n"+bcolors.ENDC
		print "Integration 	- Automates the process of onboarding new hostnames into Property Manager"
		print "audit 		- Provide a Property Manager Audit for the selected account"
		print bcolors.TURQUO+"\nMain Blog: https://ac.akamai.com/people/asomarri@akamai.com/blog/2018/08/20/swapi-property-manager-papi-main"+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	if not propertyName:
		if not contractId:
			print bcolors.WARNING+"You need to specify a ContractId: --contract ctr_3-TWDH9B\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		if not groupId:
			if retrieveobj != 'products':
				print bcolors.WARNING+"You need to specify a GroupId: --group grp_33119\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		if not propertyId:
			if retrieveobj == "versions" or retrieveobj == "latest" or retrieveobj == "hostnames" or retrieveobj == 'ruleTree':
				print bcolors.WARNING+"You need to specify a propertyId: --propertyId prp_33119\n\n"+bcolors.ENDC
				print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
				sys.exit()
		#print bcolors.WARNING+"You need to specify a configuration Name: -N SuperMetroid\n\n"+bcolors.ENDC
		#print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		#sys.exit()
	else:
		accountId,contractId,groupId,propertyId = Search(None,propertyName,None,propertyVersion)
	if retrieveobj == 'cpcodes':
		params.update({"contractId":contractId,"groupId":groupId})
		headers = {"PAPI-Use-Prefixes":"false"}
		if cpcode:
			url = '/papi/v1/cpcodes/'+cpcode
		else:
			url = '/papi/v1/cpcodes/'
		result = s.get(urljoin(baseurl, url), headers=headers, params=params)
		#print result.content
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Contract ID: "+contractId+bcolors.ENDC
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Group ID: "+groupId+bcolors.ENDC
				if cpcode:
					print bcolors.WARNING+"CPCode: "+cpcode+bcolors.ENDC
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['cpcodes']['items']:
					#print item
					Hostnameheader = ['CPCode ID', 'CPCode Name', 'Create Date', 'Product ID']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([15,50,30,30])
					HostnameTable.set_cols_align(['c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m'])
					#print item['productIds']
					try:
						item['productIds'][0]
						product = item['productIds'][0]
					except:
						product = None
					Hostnamerow = [item['cpcodeId'],item['cpcodeName'],item['createdDate'],product]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
				print HostTable
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'ruleTree':
		headers = {"PAPI-Use-Prefixes":"false"}
		params.update({'contractId':contractId,'groupId':groupId})
		if not propertyVersion:
			url = '/papi/v1/properties/'+propertyId+'/versions/latest'
			ACpayloadIG = {'contractId':contractId,'groupId':groupId}
			ACResult = s.get(urljoin(baseurl, url), params=params)
			latest = ACResult.json()['versions']['items'][0]['propertyVersion']
			url = '/papi/v1/properties/'+propertyId+'/versions/'+str(latest)+'/rules/'
		else:
			url = '/papi/v1/properties/'+propertyId+'/versions/'+str(propertyVersion)+"/rules/"
		result = s.get(urljoin(baseurl, url), headers=headers, params=params)
		if respjson:
			print result.content
			sys.exit()
		print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
		json_data = result.json()
		formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'patch':
		headers = {"PAPI-Use-Prefixes":"false","Content-Type":"application/json-patch+json"}
		params.update({'contractId':contractId,'groupId':groupId})
		if not propertyVersion:
			url = '/papi/v1/properties/'+propertyId+'/versions/latest'
			ACpayloadIG = {'contractId':contractId,'groupId':groupId}
			ACResult = s.get(urljoin(baseurl, url), params=params)
			latest = ACResult.json()['versions']['items'][0]['propertyVersion']
			url = '/papi/v1/properties/'+propertyId+'/versions/'+str(latest)+'/rules'
		else:
			url = '/papi/v1/properties/'+propertyId+'/versions/'+str(propertyVersion)+"/rules"
		filename = "files/"+propertyName+"-patch.json"
		#print filename
		try:
			with open(filename) as json_data:
				patchJson = json.load(json_data)
			#print(d)
			#rulesJson = open(filename, 'r').readlines()
		except:
			print bcolors.WARNING+"SWaPI was unable to find the json file in the files folder. It should have the same name as your configurationName + '-patch', with a .json extension.\n\n"+bcolors.ENDC
			print bcolors.WHITE+'<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		#print patchJson
		#print url
		#print params
		#print headers
		result = s.patch(urljoin(baseurl, url), headers=headers, params=params, json=patchJson)
		if respjson:
			print result.content
			sys.exit()
		if result.status_code == 200:
			print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Patch Successful"+bcolors.ENDC
		else:
			print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'versions':
		headers = {"PAPI-Use-Prefixes":"false"}
		params.update({'contractId':contractId,'groupId':groupId})
		if propertyVersion:
			url = '/papi/v1/properties/'+propertyId+'/versions/'+str(propertyVersion)
		else:
			url = '/papi/v1/properties/'+propertyId+'/versions/'
		result = s.get(urljoin(baseurl, url), headers=headers, params=params)
		#print result.content
		if result.status_code == 200:
			activeVersion = {'Production':None,'Staging':None}
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Contract ID: "+result.json()['contractId']+bcolors.ENDC
				print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"Version List: "+bcolors.ENDC
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['versions']['items']:
					#print item
					Hostnameheader = ['Version', 'Production', 'Staging', 'Updated By User','Updated Date', 'Rule Format', 'Notes']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([10,15,15,30,20,13,50])
					HostnameTable.set_cols_align(['c','c','c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m','m','m'])
					try:
						item['note']
						note = item['note']
					except:
						note = None
					if item['productionStatus'] == 'ACTIVE':
						activeVersion.update({'Production':str(item['propertyVersion'])})
					if item['stagingStatus'] == 'ACTIVE':
						activeVersion.update({'Staging':str(item['propertyVersion'])})
					Hostnamerow = [item['propertyVersion'],item['productionStatus'],item['stagingStatus'],item['updatedByUser'],item['updatedDate'],item['ruleFormat'],note]
					HostnameTable.add_row(Hostnamerow)
				HostTable = HostnameTable.draw()
				print HostTable
				if not propertyVersion:
					print bcolors.WARNING+"Active Versions: "+bcolors.ENDC
					ActiveTable = tt.Texttable()
					Activeheader = ['Production Version', 'Staging Version']
					ActiveTable.header(Activeheader)
					ActiveTable.set_cols_width([20,20])
					ActiveTable.set_cols_align(['c','c'])
					ActiveTable.set_cols_valign(['m','m'])
					Activerow = [activeVersion['Production'],activeVersion['Staging']]
					ActiveTable.add_row(Activerow)
					ActTable = ActiveTable.draw()
					print ActTable
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'edgehostnames':
		headers = {"PAPI-Use-Prefixes":"false"}
		params.update({'contractId':contractId,'groupId':groupId,'options':'mapDetails'})
		if edge:
			url = '/papi/v1/edgehostnames/'+edge
		else:
			url = '/papi/v1/edgehostnames/'
		result = s.get(urljoin(baseurl, url), headers=headers, params=params)
		#print result.content
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['edgeHostnames']['items']:
					#print item
					Hostnameheader = ['Edge Hostname', 'ID', 'IP Version', 'Map Domain','Secure', 'Slot']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([65,9,15,35,10,10])
					HostnameTable.set_cols_align(['c','c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m','m'])
					try:
						item['mapDetails:slotNumber']
						slotNumber = item['mapDetails:slotNumber']
					except:
						slotNumber = None
					try:
						item['mapDetails:mapDomain']
						mapDomain = item['mapDetails:mapDomain']
					except:
						mapDomain = None
					Hostnamerow = [item['edgeHostnameDomain'],item['edgeHostnameId'],item['ipVersionBehavior'],mapDomain,str(item['secure']),slotNumber]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
				print HostTable
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'hostnames':
		headers = {"PAPI-Use-Prefixes":"false"}
		params.update({'contractId':contractId,'groupId':groupId,'options':'mapDetails'})
		if propertyVersion:
			url = '/papi/v1/properties/'+propertyId+'/versions/'+propertyVersion+'/hostnames/'
		else:
			url = '/papi/v1/properties/'+propertyId+'/versions/latest'
			ACpayloadIG = {'contractId':contractId,'groupId':groupId,'accountSwitchKey':AccountSwitch}
			ACResult = s.get(urljoin(baseurl, url), params=ACpayloadIG)
			latest = ACResult.json()['versions']['items'][0]['propertyVersion']
			url = '/papi/v1/properties/'+propertyId+'/versions/'+str(latest)+'/hostnames/'
		result = s.get(urljoin(baseurl, url), headers=headers, params=params)
		#print result.content
		if result.status_code == 200:
			if respjson:
				json_data = result.json()
				formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
				colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
				#print colorful_json
				print result.content
				sys.exit()
			else:
				#print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
				#print bcolors.WARNING+"Property Name: "+result.json()['propertyName']+bcolors.ENDC
				#print bcolors.WARNING+"Property ID: "+result.json()['propertyId']+bcolors.ENDC
				#print result.json()['configurations']
				HostnameTable = tt.Texttable()
				#HostnameTable.set_deco(tt.Texttable.HEADER)
				for item in result.json()['hostnames']['items']:
					#print item
					Hostnameheader = ['Property Name','Property ID','Hostnames', 'Edge Hostname', 'Edge ID']
					HostnameTable.header(Hostnameheader)
					HostnameTable.set_cols_width([25,15,70,50,15])
					HostnameTable.set_cols_align(['c','c','c','c','c'])
					HostnameTable.set_cols_valign(['m','m','m','m','m'])
					Hostnamerow = [result.json()['propertyName'],result.json()['propertyId'],item['cnameFrom'],item['cnameTo'],item['edgeHostnameId']]
					HostnameTable.add_row(Hostnamerow)
					HostTable = HostnameTable.draw()
				try:
					HostTable
					print HostTable
				except:
					print bcolors.TURQUO+"[PAPI] "+bcolors.WARNING+"No Hostnames were found. "+bcolors.ENDC
		else:
			json_data = result.json()
			formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
			colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
			print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	elif retrieveobj == 'latest':
		latestHeaders = {"PAPI-Use-Prefixes": "false"}
		params.update({'contractId':contractId,'groupId':groupId})
		#if cdn:
		#	if cdn == 'prod':
		#		activatedOn = {'activatedOn':'PRODUCTION'}
		#	else:
		#		activatedOn = {'activatedOn':'STAGING'}
		#	payload.update(activatedOn)
		url = '/papi/v1/properties/'+str(propertyId)+'/versions/latest'
		result = s.get(urljoin(baseurl, url), params=params,headers=latestHeaders)
		if respjson:
			print result.content
			sys.exit()
		print bcolors.WARNING+"StatusCode: "+str(result.status_code)+bcolors.ENDC
		#print result.content
		json_data = result.json()
		formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.Terminal256Formatter())
		print colorful_json
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		sys.exit()
	else:
		print "Did you choose a valid option?"
	print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC



def main():
	usage = "%prog -W|-R|-B subtype -t <target> [option] [option-argument] ... "
	parser = OptionParser(usage=usage, epilog='otherstuff', version=VERSION)
	class MyParser(OptionParser):
		def format_epilog(self, formatter):
			return self.epilog

	parser =MyParser(usage=usage, version=bcolors.WHITE+"\n\n-- whiteRabbit --\n\n"+bcolors.ENDC+bcolors.TURQUO+"  Version: "+VERSION+"\n\n"+bcolors.ENDC+bcolors.WHITE+"-- whiteRabbit --\n\n"+bcolors.ENDC, epilog=
"""

"""+bcolors.TURQUO+"""Examples:"""+bcolors.ENDC+"""

Identity Access Management
python swapi.py iam search -t 'nbc'
python swapi.py iam apiclient --userId ml5vvvu5oman7w4d

SWaPI's Mapping System
python swapi.py map -N nasdaq -A AANA-35EV8X
python swapi.py map search -N nasdaq
python swapi.py map delete -N nasdaq

Property Manager
python swapi.py papi create -N Megaman
python swapi.py papi search -N Megaman
python swapi.py papi ruleTree -N Megaman

Network Lists
python swapi.py NL create -N "WAF Bypass List" --listType IP --netlist 64.68.40.0/24,64.78.9.9
python swapi.py NL activate -N 'WAF Bypass List'
python swapi.py NL activate -N 'WAF Bypass List' --cdn prod

Application Security
python swapi.py appsec msc
python swapi.py appsec versions -N asomarri
python swapi.py appsec policies -N asomarri

""")
	#parser.add_option("-P", "--papi", metavar="PAPI", type="choice", action="store", dest="papi", choices=[ 'choices', 'help', 'retrieve', 'add', 'update', 'deactivate','activate', 'delete', 'create', 'poll', 'search', 'CCU', 'Integration','download','freeze','NL', 'CPS', 'SecMon', 'appsec', 'options', 'crawl','checkip', 'audit' ],
	#				help="Use this option if you would like to use the PAPI module. Example: python swapi.py create -N SuperMetroid -A new")
	#parser.add_option("-O","--object", type="choice", action="store", dest="retrieveobj", choices =[ 'hostnames' ,'products', 'groups', 'contracts','edgehostnames' ,'cpcodes', 'properties','versions', 'locations','formats','settings','build', 'latest', 'NL', 'certs', 'sps', 'SS', 'RP', 'DS', 'policies', 'targets', 'msc', 'custom', 'ruleTree','export', 'protected', 'hostPR'],
	#				help="Use this option when you want to retrieve information back about your Account. Options: 'hostnames' ,'products', 'groups', 'contracts','edgehostnames' ,'cpcodes', 'properties','versions', 'locations','formats','settings','build', 'latest', 'NL', 'certs', 'sps', 'SS', 'RP', 'DS', 'policies', 'targets', 'custom', 'ruleTree','export', 'protected', 'hostPR' ")
	parser.add_option("-N","--name", type='string', dest="propertyName",
					help="If you want to specify the property name: --name SuperMetroid")
	parser.add_option("-A","--account", metavar="AccountSwitch", dest="AccountSwitch",
					help="Leverage the account Switching capability. Format: -A 1-599K:1-2RBE")
	parser.add_option("-t", "--target", metavar="HOST", dest="host",
					help="Used to add hostnames into a config. Format: add -t www.asomarri.com")
	parser.add_option("--json", action="store_true", dest="respjson", default=False,
					help="Provide JSON Response Content back.")
	parser.add_option("--ref",nargs=1 , metavar="Ref#", type="string", dest="refId",
					help="To retrieve information about a Reference ID: --ref 9.6f64d440.1318965461.2f2b078")
	parser.add_option('--cdn' ,nargs=1 , metavar="CDN Platform", type="choice", dest="cdn", choices=['prod','staging'] , default="staging",
					help="Which Akamai's Platform are you testing on? Default: 'staging'. Format: sudo python swapi.py -W self -t http://www.att.com --cdn prod")
	parser.add_option("-E",nargs=1 , metavar="Edge Hostname", type="string", dest="edge",
					help="Used through several module to provide an EdgeHostname, edgeId or as IP identifier for Akamai Edge Servers. Format: -E www.asomarri.com.edgesuite.net")
	parser.add_option("--auto", action="store_true", dest="automation", default=False,
					help="If you want to display only relevant data for automation: --auto")
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Property Manager"+bcolors.ENDC,"\n")
	group.add_option("--origin", type='string', dest="origin",
					help="If you are creating a New Configuration, you can provide an Origin to configure: --origin origin-customer.akamai.io")
	parser.add_option("--stagingPush", action="store_true", dest="stagingPush", default=False,
					help="If you are creating a New Configuration, you can activate the configuration automatically to Staging: --stagingPush")
	group.add_option("--srto", type='string', dest="srto",
					help="If you are creating an ION Configuration, you can provide the SureRoute Test Object path: --srto /akamai/srto.html")
	group.add_option("--contract", type='string', dest="contractId",
					help="If you want to retrive any information that needs a contractId, you can specify: --contract ctr_F-E9CVKJ")
	group.add_option("--group", type='string', dest="groupId",
					help="If you want to retrive any information that needs a groupId, you can specify: --group grp_101401")
	group.add_option("--product", type='string', dest="productId",
					help="If you want to specify a specific product: --product prd_Site_Defender")
	group.add_option("--propertyId", type='string', dest="propertyId",
					help="If you want to retrive any information that needs a propertyId, you can specify: --property prp_373888")
	group.add_option("--cpcode", type='string', dest="cpcode",
					help="If you want to specify a cpcode: --cpcode 633420")
	group.add_option("--ruleFormat", type='choice', action="store", dest="ruleFormat",choices=["v2018-02-27","v2017-06-19","v2016-11-15","v2015-08-17","latest"], default="v2018-02-27",
					help="When you want to freeze a configuration to a specific ruleset: freeze -N SuperMetroid --ruleFormat v2018-02-27 (this is the default)")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Application Security"+bcolors.ENDC,"\n")
	group.add_option("--policyId", type='string', dest="policyId",
					help="Used by APPSEC to specify a Policy ID: --policyId aaa2_41395")
	group.add_option("--ruleId", type='string', dest="ruleId",
					help="Used by APPSEC to specify a Custom Rule ID: --ruleId 633725")
	group.add_option("--configId", type='string', dest="configId",
					help="Used by APPSEC to specify a Configuration ID: --configId 29969")
	group.add_option("--prefix", type='string', dest="prefix",
					help="Used by APPSEC Clone feature to specify a new policy prefix: --prefix NPCL")
	group.add_option("--rules", action="store_true", dest="rules", default=False,
					help="Used by APPSEC to export only WAF rules: --rules")
	group.add_option("--customRules", action="store_true", dest="customRules", default=False,
					help="Used by APPSEC to export only Custom Rules: --customRules")
	group.add_option("--exceptions", action="store_true", dest="exceptions", default=False,
					help="Used by APPSEC to export Exceptions and Conditions: --exceptions")
	group.add_option("--mtarget", metavar="SEQUENCE", type="int", dest="seq",
					help="Used by APPSEC to specify a match target sequence # to modify: --mtarget 1")
	group.add_option("--path", metavar="Path", type="string", dest="path",
					help="Used by APPSEC to add a path to the match target: --path /*")
	group.add_option("--actions", type="choice", action="store", default="alert", dest="appsec_actions",choices =[ "alert", "deny", "none"],
					help="Used by APPSEC to specify a WAF action. By default, it's set to Alert: --action deny")
	parser.add_option("--rateControls", action="store_true", dest="rateControls", default=False,
					help="Used by APPSEC to export Rate Control information back.")
	group.add_option("--negativeFile", action="store_true", dest="negativeFile", default=False,
					help="Used by APPSEC Match Target to specify a negative file extension match: --negativeFile")
	group.add_option("--negativePath", action="store_true", dest="negativePath", default=False,
					help="Used by APPSEC Match Target to specify a negative path match: --negativePath")
	group.add_option("--generate", action="store_true", dest="generate", default=False,
					help="Used by APPSEC Peer Review Module to generate an Exclusion Excel Sheet: --generate")
	group.add_option("--defaultFile", type='choice', action="store", dest="defaultFile",choices=["NO_MATCH","BASE_MATCH","RECURSIVE_MATCH"],default="BASE_MATCH",
					help="Used by APPSEC Match Target to specify a description of the rule to match on paths.  --defaultFile NO_MATCH. Default: BASE_MATCH")
	group.add_option("--bypass", type='string', dest="bypass",
					help="Used by APPSEC Match Target to specify a Bypass Network List ID: --bypass 1304427_AAXXBBLIST")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Activation"+bcolors.ENDC,"\n")
	group.add_option("--noactivate", action="store_true", dest="noactivate", default=False,
					help="If you want run the Integration module without activation: --noactivate")
	group.add_option("--noversion", action="store_true", dest="noversion", default=False,
					help="If you want to run the Integration module without creating a new version: --noversion")
	group.add_option("--notes", type='string', dest="notes",
					help="If you want to specify the configurations or activation notes: --notes 'Initial Configuration'")
	group.add_option("--emails", type='string', action='store', dest="emails",
					help="If you want to specify the notification emails, separate using a comma delimiter: --emails 'asomarri@akamai.com,swapi@akamai.com'")
	group.add_option("--cemails", type='string', action='store', dest="cemails",
					help="If you want to specify the notification emails, separate using a comma delimiter: --cemails 'customer@swapi.com,swapi@akamai.com'")
	group.add_option("--PR", type='string', action='store', dest="PRd",
					help="If you are activating a configuration in PROD, you must specify a PR'r email address: --PRd 'atorresr@akamai.com,swapi@akamai.com'")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Alerts"+bcolors.ENDC,"\n")
	group.add_option("--fname", type='string', dest="fname",
					help="Filter results to only include definitions that contain the specified field: --fname aca_cpcode")
	group.add_option("--fvalue", type="string", dest="fvalue",
					help="With fieldName specified, further filter results based on the field’s value. This matches either a scalar value or membership within an array: --fvalue 87525")
	group.add_option("--ids", type="string", dest="ids",
					help="Filter results to include a subset, repeating the parameter to specify more than one definitionId identifier: --ids s@123")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - SIEM"+bcolors.ENDC,"\n")
	group.add_option("--offset", type='string', dest="offset",
					help="Fetch only security events that have occurred from offset: --offset c0bc409010aa6928e57cd5a3000433b9")
	group.add_option("--limit", type="int", dest="limit",
					help="Maximum number of security events each fetch returns: --limit 10")
	group.add_option("--start", type="int", dest="start",
					help="The start of a specified time range, expressed in Unix epoch seconds: --start 1488816442")
	group.add_option("--end", type="int", dest="end",
					help="The end of a specified time range, expressed in Unix epoch seconds: --end 1488816784")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - IAM"+bcolors.ENDC,"\n")
	group.add_option("--userId", type='string', dest="userId",
					help="To view User's information with uiIdentityId: --userId 'B-F-MS1YIN'")
	group.add_option("--passwd", type='string', dest="passwd",
					help="To set User's password: --passwd mynewpassword")
	group.add_option("--sendEmail", action="store_true", dest="sendEmail", default=False,
					help="If you want send an email when resetting a User password: --sendEmail")
	group.add_option("--sqa", action="store_true", dest="sqa", default=False,
					help="Used when adding an API Client ID. When enabled API Client ID will be set for SQA environment: --sqa")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Case Management"+bcolors.ENDC,"\n")
	group.add_option("--category", type='string', dest="category",
					help="Used to view sub-categories of a Top Level Category: --category 'Security'")
	group.add_option("-d", type='string', dest="duration",
					help="Duration. Number of days to retrieve cases: -d 10")
	group.add_option("--description", type='string', dest="description",
					help="An extented  description of the problem: --description 'Getting Error Denied with Reference Number: #18.df1fc917.1548793365.68031bc'")
	group.add_option("--sev", type='string', dest="sev",
					help="Specifies the level of severity: --sev 1-Major Impact")
	group.add_option("--sub", type='string', dest="sub",
					help="Specifies sub category element: --sub Billing")
	group.add_option("--subject", type='string', dest="subject",
					help="Subject line that serves as title: --subject 'WAF 403 Forbidden'")
	group.add_option("--userDetail", type='string', dest="userDetail",
					help="Data about user on whose behalf the support ticket was created: --userDetail 'Security'")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - SiteShield"+bcolors.ENDC,"\n")
	group.add_option("--mapId", type='string', dest="mapId",
					help="To view information about a specific SiteShield map: --mapId 1523")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - PLX Analytics"+bcolors.ENDC,"\n")
	group.add_option("--attackId", type='string',default='None', dest="attack",
					help="If you want to perform a diff between two versions, use this option: --attackId 51278")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Fast DNS"+bcolors.ENDC,"\n")
	group.add_option("--zones", type='string', nargs=2, dest="zonesDiff",
					help="If you want to perform a diff between two versions, use this option: --zones versionID1 versionID2")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI General Options"+bcolors.ENDC,"\n")
#					help="Trigger Akamai's Average Rate Control") 'retrieve', 'modify', 'update', 'deactivate','activate', 'delete', 'formats', 'create'
	group.add_option("--edgeId", type='string', dest="edgeId",
					help="If you want to retrive information about a particular edgehostname, you can specify: --edgeId ehn_2436253")
	group.add_option("--creds", type='string', default="default", dest="creds",
					help="If you want to specify a set of credentials from your EdgeRC file: --creds entsec")
	group.add_option("--from", type='string', dest="cloneFrom",
					help="If you want to specify the property name: --from SuperMetroid")
	group.add_option("-V","--propertyVersion", type='string', dest="propertyVersion",
					help="If you want to specify the property version: --propertyVersion 1")
	group.add_option("--ruleTree", action="store_true", dest="ruleTree", default=False,
					help="If you want to get the PM configuration in a JSON format: -V5 --ruleTree")
	group.add_option("--latest", action="store_true", dest="latest", default=False,
					help="If you want to GET the latest version of a configuration, you can specify: --latest")
	group.add_option("--copyHosts", action="store_true", dest="copyHostnames", default=False,
					help="If you want to copy the hostnames when Cloning a configuration, use this option: --copyHosts")
	group.add_option("--ipVersion", type='choice', action="store", dest="ipVersion",choices=["IPV6_COMPLIANCE","IPV4"],default="IPV4",
					help="When creating a new EdgeHostname, you can specify if it's IPv6 Compliance. --ipVersion IPV6_COMPLIANCE. Default: IPV4")
	group.add_option("--reportId", type='string', dest="reportPackId",
					help="If you want to retrive information about a specific Report Pack ID: --reportId 100116")
	group.add_option("--platform", type="choice", action="store", dest="platform", choices =['mac', 'linux', 'windows'], default='mac',
					help="Use this option to set your hosts file location according to your OS. Default: mac")
	group.add_option("--extended", action="store_true", dest="extended", default=False,
					help="If you want to retrieve verbose data about Network Lists or Alerts, use this option: --extended")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Network Lists"+bcolors.ENDC,"\n")
	group.add_option("--type", type="choice", action="store", dest="listType", choices =[ 'website','api','primary','secondary',"IP", "GEO","user-active","user-closed","company-active","company-closed",'AKAMAICDN','A','AAAA','CNAME','ALIAS','MX','NS','PTR','SOA','SRV','TXT','DNSKEY','DS','NSEC','NSEC3','NSEC3PARAM','RRSIG'],
					help="If you want to retrieve GEO elements of a network list, use this option (by default IP): --listType GEO")
	group.add_option("--items", action="store_true", dest="includeElements", default=False,
					help="If you want to retrieve elements about Network Lists, use this option: --includeElements")
	group.add_option("--netId", type='string', dest="netId",
					help="If you want to specify a Network List ID: --netId 7054_FEOSERVERS")
	group.add_option("--netlist", type='string', dest="netlist",
					help="NOT USED ANYMORE - Use -t instead. Comma delimited list of IPs or GEOs that you want to add: -t 1.1.1.1,2.2.2.2,3.3.3.3")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - CPS"+bcolors.ENDC,"\n")
	group.add_option("--enroll", type='string', dest="enrollmentId",
					help="If you want to specify a Certificate Enrollment: --enroll 22135")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Contract API"+bcolors.ENDC,"\n")
	group.add_option("--depth", type="choice", action="store", dest="depth", choices =['TOP', 'ALL'], default='ALL',
					help="Returns a specific set of contracts. Select TOP to return only parent contracts or ALL to return both parent and child contracts: --depth TOP")
	group.add_option("--to", type='string', dest="to",
					help="The end date, in UTC: --to 2016-03-31")
	parser.add_option_group(group)
	group = OptionGroup(parser, bcolors.OKBLUE+"SWaPI - Finale - codeRain"+bcolors.ENDC,"\n")
	group.add_option("--base64", type='string', dest="unlockCodeBase64",
					help="If you want to unlock codeRain, provide correct base64 value: --base64 d2hpdGVSY9Y29kZVJhaW4=")
	parser.add_option_group(group)
	(options, args) = parser.parse_args()
	#print args
	try:
		os.stat("files")
	except:
		os.mkdir("files")
	try:
		open('.map', 'r')
	except:
		open('.map', 'w+')
	try:
		open('.apiclient', 'r')
	except:
		open('.apiclient', 'w+')
	try:
		args[0]
		apiModule = args[0].lower()
	except:
		if autoInstall == True:

			print bcolors.WARNING+"""

	%whiCall trans opt: received - """+str(datetime.datetime.now().time())+"""

		"""+bcolors.TURQUO+"""Trace program: """+bcolors.WHITE+"""swapi running"""+bcolors.ENDC+"""

	             wake up, Neo...
	    	"""+bcolors.TURQUO+"""%bld"""+bcolors.ENDC+"""the matrix has you"""+bcolors.TURQUO+"""%clr"""+bcolors.ENDC+"""
	         follow the white rabbit.
			"""+bcolors.BOLD+bcolors.BLINK+bcolors.WARNING+"""
	            KNOCK, KNOCK, Neo.
				"""+bcolors.ENDC+"""
			  """+bcolors.WHITE+"""
	                        (`.         ,-,
	                        ` `.    ,;' /
	                         `.  ,'/ .'
	                          `. X /.'
	                .-;--''--.._` ` (
	              .'            /   `
	             ,           ` '   Q '
	             ,         ,   `._    \-
	          ,.|         '     `-.;_'
	          :  . `  ;    `  ` --,.._;
	           ' `    ,   )   .'
	              `._ ,  '   /_
	                 ; ,''-,;' ``-
	                  ``-..__``--`

			"""+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			print bcolors.WARNING+"Use any of the following options for help and usage instructions:\n"+bcolors.ENDC
			print bcolors.OKGREEN+"python swapi.py --version	- Display SWaPI's current version"+bcolors.ENDC
			print bcolors.OKGREEN+"python swapi.py --help		- Options menu"+bcolors.ENDC
			print bcolors.OKGREEN+"python swapi.py help		- Command Examples Menu"+bcolors.ENDC
			print bcolors.OKGREEN+"python swapi.py modules		- List supported modules"+bcolors.ENDC
			print bcolors.OKGREEN+"python swapi.py whiteRabbit 	- Showcase SWaPI's logo (thanks to Metasploit)"+bcolors.ENDC
			print bcolors.TURQUO+'\n[GIT] '+bcolors.ENDC+'https://github.com/akamai-contrib/swapi'
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	try:
		args[1]
		apiObject = args[1]
	except:
		apiObject = None
	try:
		args[2]
		apiAction = args[2]
	except:
		apiAction = None
	if apiModule == 'modules':
		print """

	"""+bcolors.WHITE+"""---------- SWaPI Available Modules ----------"""+bcolors.ENDC+"""

	map 		- SWaPI's Mapping System
	appsec 		- Application Security API
	papi		- Property Manager API
	case		- Case Management API
	alerts		- Alerts API
	contract	- Contract API
	dns		- FastDNS API
	iam 		- Identity Access Management
	nl		- Network List API
	siem 		- SIEM API
	ss 		- SiteShield API
	crawl 		- Diagnostic API
	checkip 	- Diagnostic API
	cps/sps 	- CPS or SPS API
	plx 		- Prolexic Analytics API
	license 	- Show SWaPI's License information
	codeRain 	- Can you unblock this feature to have the coolest screen saver!!
	secmon 		- SecMon API to retrieve information (Incomplete & Deprecated)


	"""+bcolors.WHITE+"""---------- SWaPI Available Modules ----------"""+bcolors.ENDC+"""


		"""
		sys.exit()
	if apiModule == 'license':
		print bcolors.TURQUO+'\n\n\t\t\t*********[LICENSE]*********\n'+bcolors.ENDC
		print '''	Copyright 2019. Aurelio Somarriba Lucas

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

		http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.'''
		print bcolors.TURQUO+'\n\t\t\t*********[LICENSE]*********\n\n'+bcolors.ENDC
		sys.exit()
	if apiModule == 'coderain':		# Thank you and merits to https://github.com/devsnd/matrix-curses/blob/master/matrix-curses.py
		if options.unlockCodeBase64 == 'd2hpdGVSYWJiaXQ9Y29kZVJhaW4=':
			try:
				codeRain()
			except KeyboardInterrupt:
				curses.endwin()
				curses.curs_set(1)
				curses.reset_shell_mode()
				curses.echo()
				sys.exit()
		elif options.unlockCodeBase64 == None:
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			print bcolors.TURQUO+"[codeRain] "+bcolors.WARNING+"Use the --base64 option to provide unlock code. "+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
		else:
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			print bcolors.TURQUO+"[codeRain] "+bcolors.WARNING+"Base64 does not Match! Try again!"+bcolors.ENDC
			print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
			sys.exit()
	if apiModule == 'setup':
		setUp()
	if apiModule == 'gui':
		usedFonts = ['slant','cyberlarge','doom','acrobatic','brite','bubble','sblood','starwars','utopia','univers','epic','jazmine','mirror','roman','speed']
		font = random.choice(usedFonts)
		f = Figlet(font=font)
		print f.renderText('No GUI, Kellen')
		sys.exit()
	if apiModule == 'whiterabbit':		# Thank you Metasploit

		print bcolors.WARNING+"""

%whiCall trans opt: received - """+str(datetime.datetime.now().time())+"""

	"""+bcolors.TURQUO+"""Trace program: """+bcolors.WHITE+"""swapi running"""+bcolors.ENDC+"""

             wake up, Neo...
    	"""+bcolors.TURQUO+"""%bld"""+bcolors.ENDC+"""the matrix has you"""+bcolors.TURQUO+"""%clr"""+bcolors.ENDC+"""
         follow the white rabbit.
		"""+bcolors.BOLD+bcolors.BLINK+bcolors.WARNING+"""
            KNOCK, KNOCK, Neo.
			"""+bcolors.ENDC+"""
		  """+bcolors.WHITE+"""
                        (`.         ,-,
                        ` `.    ,;' /
                         `.  ,'/ .'
                          `. X /.'
                .-;--''--.._` ` (
              .'            /   `
             ,           ` '   Q '
             ,         ,   `._    \-
          ,.|         '     `-.;_'
          :  . `  ;    `  ` --,.._;
           ' `    ,   )   .'
              `._ ,  '   /_
                 ; ,''-,;' ``-
                  ``-..__``--`

		"""+bcolors.ENDC
		sys.exit()
	if apiModule == 'help':
		print """

"""+bcolors.WHITE+"""<!----------- SWaPI HELP -----------!>"""+bcolors.ENDC+"""

"""+bcolors.TURQUO+"""<Property Manager>"""+bcolors.ENDC+"""

"""+bcolors.WARNING+"""RETRIEVE"""+bcolors.ENDC+"""

python swapi.py papi groups
python swapi.py papi contracts
python swapi.py papi products -N SuperMetroid
python swapi.py papi cpcodes -N SuperMetroid
python swapi.py papi properties -N SuperMetroid
python swapi.py papi versions -N SuperMetroid
python swapi.py papi versions -N SuperMetroid -V5
python swapi.py papi ruleTree -N SuperMetroid -V5
python swapi.py papi hostnames -N SuperMetroid -V5
python swapi.py papi edgehostnames -N SuperMetroid
python swapi.py papi edgehostnames -N SuperMetroid -E ehn_32223
python swapi.py papi latest -N SuperMetroid
python swapi.py papi formats
python swapi.py papi locations
python swapi.py papi settings
python swapi.py papi builds

--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""AUTOMATIONS"""+bcolors.ENDC+"""

-Integration-
python swapi.py papi Integration -N SWaPI

NOTE: Fill CSV file and save in the files/ folder with the same name of the configuration you want.
NOTE: This will automatically activate NEW configuration in Staging and Production (normally on new configurations, customer is not CNAMEd).


-One-Liner-
python swapi.py papi create -N DevOpsPAPI -t devops-papi.akamai.io -E papidemo.akamai.io.edgesuite.net --origin origin-devops-papi.akamai.io --cpcode 743969 --stagingPush --emails asomarri@akamai.com


--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""ACTIONS"""+bcolors.ENDC+"""

-CREATE-

"""+bcolors.UNDERLINE+"""PROPERTY MANAGER"""+bcolors.ENDC+"""
New version from latest:
python swapi.py papi newVersion -N SuperMetroid

New version from specific version:
python swapi.py papi newVersion -N SuperMetroid -V4

New Configuration in main group:
python swapi.py papi create -N TDKS

Delete Configuration (only works if no configuration is active in either Staging or PROD):
python swapi.py papi delete -N TDKS

New Configuration in same group as "from" configuration (does NOT clone the configuration):
python swapi.py papi create -N MortalKombat --from SuperMetroid

"""+bcolors.UNDERLINE+"""EDGEHOSTNAMES (FF Only)"""+bcolors.ENDC+"""
python swapi.py papi create -N Megaman -E staging-megaman.akamaiu.com.edgesuite.net

POLL EdgeHostnames
python swapi.py papi poll -N Megaman -E 715426


"""+bcolors.UNDERLINE+"""CPCODES"""+bcolors.ENDC+"""
python swapi.py papi create -N IBMMain --cpcode 'IBM Main'


-CLONING COMMANDS-

Cloning a configuration (Clones latest version):
python swapi.py papi clone -N Megaman --from SuperMetroid

Cloning a specific version:
python swapi.py papi clone -N Megaman --from SuperMetroid -V4

Cloning a configuration, including hostnames:
python swapi.py papi clone -N Megaman --from SuperMetroid --copyHosts


-ACTIVATION COMMANDS-

python swapi.py papi activate -N SuperMetroid --emails asomarri@akamai.com (BY DEFAULT, SWaPI WILL ACTIVATE IN STAGING)
python swapi.py papi activate -N SuperMetroid --cdn prod --emails asomarri@akamai.com --cemails swapi@customer.com --PRd atorresr@akamai.com


-ADD/REMOVE HOSTNAMES-

python swapi.py papi add -N SuperMetroid -t mother-ship.metroid.akamaiu.com,maridia.metroid.akamaiu.com -E metroid.akamaiu.com.edgesuite.net
python swapi.py papi remove -N SuperMetroid -t mother-ship.metroid.akamaiu.com,maridia.metroid.akamaiu.com
NOTE: comma-delimited

-UPDATE COMMAND-

Updates a configuration by reading a json file:
python swapi.py papi update -N Megaman

NOTE: The JSON File must be in our files folder, with the SAME Configuration Name: files/Megaman.json


-DOWNLOAD COMMANDS-

Download Rule Configuration and create JSON file:
python swapi.py papi download -N Megaman

NOTE: New JSON File will be saved in: files/Megaman.json (propertyName.json)


-FREEZE COMMANDS-

Use this ONLY if on LATEST ruleset. Freezes to 'v2018-02-27' by default:
python swapi.py papi freeze -N Megaman


--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""Search"""+bcolors.ENDC+"""

python swapi.py papi search -N SuperMetroid
python swapi.py papi search -t www.streetfighter.com
python swapi.py papi search -E metroid.akamaiu.com.edgesuite.net

--------------------------------------------------------------------------------


"""+bcolors.TURQUO+"""<Identity Access Management>"""+bcolors.ENDC+"""

"""+bcolors.WARNING+"""RETRIEVE"""+bcolors.ENDC+"""

Add your API Client ID to your SWaPI script:
python swapi.py IAM apiclient --userId ml5vvvu5oman7w4d

Search Accounts and Account Switch Keys
python swapi.py IAM search -t 'ibm bluemix'

python swapi.py IAM groups
python swapi.py IAM properties
python swapi.py IAM properties --group 109031
python swapi.py IAM properties --propertyId 10505595 --group 109031
python swapi.py IAM users
python swapi.py IAM users --userId B-F-MS1YIN
python swapi.py IAM users --group 109027
python swapi.py IAM roles

--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""ACTIONS"""+bcolors.ENDC+"""
python swapi.py IAM create -N 'New Sub Group' --group 109027
python swapi.py IAM rename --group 109031 -N 'New Group Name'
python swapi.py IAM delete --group 109031
python swapi.py IAM reset --userId B-F-MS1YIN
python swapi.py IAM reset --userId B-F-MS1YIN --passwd mynewpassword
python swapi.py IAM unlock --userId B-F-MS1YIN
python swapi.py IAM lock --userId B-F-MS1YIN


--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""<Case Management>"""+bcolors.ENDC+"""

"""+bcolors.WARNING+"""RETRIEVE"""+bcolors.ENDC+"""

List Cases:
python swapi.py case list
python swapi.py case list -N F-CS-1388269

Information for cases
python swapi.py case categories
python swapi.py case sub --category Technical
python swapi.py case severities --category Technical

"""+bcolors.WARNING+"""ACTIONS"""+bcolors.ENDC+"""

python swapi.py case create -N files/newCase.json
python swapi.py case add -N F-CS-1388269 --notes 'This is a serious issue. Please escalate'
python swapi.py case close -N F-CS-1388269 --notes 'Issue Resolved. Closing case. '

--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""<Fast DNS>"""+bcolors.ENDC+"""

"""+bcolors.WARNING+"""RETRIEVE"""+bcolors.ENDC+"""

Main Menu
python swapi.py dns

Fast DNS Zones
python swapi.py dns zones

Records for a Zone
python swapi.py dns -N pcrichard.com records
python swapi.py dns -N pcrichard.com records --type A
python swapi.py dns -N pcrichard.com records --type SOA

Download Master Zone File
python swapi.py dns -N pcrichard.com download
python swapi.py dns -N pcrichard.com download -V 51bd2e3c-4069-41bb-a1b6-03aac5d78a5a

Zone version information
python swapi.py dns -N pcrichard.com versions

More information about Zone
python swapi.py dns -N pcrichard.com contracts
python swapi.py dns -N pcrichard.com groups
python swapi.py dns -N pcrichard.com edgehostnames
python swapi.py dns -N pcrichard.com algorithms
python swapi.py dns -N pcrichard.com types
python swapi.py dns -N pcrichard.com tsig

List Authoritative Name Servers
python swapi.py dns -N pcrichard.com authorities

Perform a DIFF between versions:
python swapi.py dns -N pcrichard.com diff --zones ea3ead19-dee8-49a6-9aad-fe8c31df23bf 51bd2e3c-4069-41bb-a1b6-03aac5d78a5a

"""+bcolors.WARNING+"""ACTIONS"""+bcolors.ENDC+"""



--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""<SWaPI - Diagnostics>"""+bcolors.ENDC+"""

Crawl logs using RefId
python swapi.py crawl --ref 18.27333217.1528594239.fa8602

Check IP - Verify it's an Akamai Edge Server
python swapi.py checkip -E 165.254.92.147



--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""<SWaPI - Mapping System>"""+bcolors.ENDC+"""

Map a friendly Name to an Account Switch Key
python swapi.py map -N nasdaq -A AANA-35EV8X

Delete an existing Map
python swapi.py map delete -N nasdaq

Search for names or accounts in your .map file
python swapi.py map search -N nasdaq
python swapi.py map search -A AANA-35EV8X


--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""<SWaPI - SIEM>"""+bcolors.ENDC+"""


SWaPI SIEM:
python swapi.py siem
python swapi.py siem --config 31026 --creds siem-entsec --start 1534784400


--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""<SWaPI - SiteShield>"""+bcolors.ENDC+"""

"""+bcolors.WARNING+"""RETRIEVE"""+bcolors.ENDC+"""

List SS Maps
python swapi.py SS
python swapi.py SS --mapId 31026

--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""ACTIONS"""+bcolors.ENDC+"""

Acknowledge an SS Map
python swapi.py SS --mapId 31026 ack


--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""<SWaPI - Network Lists>"""+bcolors.ENDC+"""

"""+bcolors.WARNING+"""RETRIEVE"""+bcolors.ENDC+"""

python swapi.py NL list
python swapi.py NL list --json
python swapi.py NL list --type IP
python swapi.py NL list --type GEO
python swapi.py NL list -N 'Image Manager Servers'
python swapi.py NL list -N 'rijohnso GEO Blacklist' --items

--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""ACTIONS"""+bcolors.ENDC+"""

-CREATE-
python swapi.py NL create -N "Test IP Block" --type IP -t 1.1.1.1,2.2.2.2,3.3.3.3
python swapi.py NL create -N "Test GEO Block" --type GEO -t cn,pt

-ADD/REMOVE-
"""+bcolors.WARNING+"""ADD/DELETE"""+bcolors.ENDC+"""
python swapi.py NL add -N 'WAF Bypass List' -t 64.16.23.0/24,64.10.10.10
python swapi.py NL remove -N 'WAF Bypass List' -t 64.10.10.10
python swapi.py NL remove -N 'WAF Bypass List' -t cr

-ACTIVATION-
"""+bcolors.WARNING+"""ACTIVATION"""+bcolors.ENDC+"""
python swapi.py NL activate -N 'WAF Bypass List'
python swapi.py NL activate -N 'WAF Bypass List' --cdn prod


--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""SEARCH"""+bcolors.ENDC+"""
python swapi.py NL search -t 1.1.1.1
python swapi.py NL search -t cn
python swapi.py NL search -t 1.1.1.1 --json
python swapi.py NL search -t 1.1.1.1


--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""SWaPI - Application Security"""+bcolors.ENDC+"""

"""+bcolors.WARNING+"""EXPORT"""+bcolors.ENDC+"""

python swapi.py appsec export -N asomarri
NOTE: This option downloads JSON file and creates a new file in the files/ folder

python swapi.py appsec export -N asomarri --json

Show All Rules enabled in FW Policy
python swapi.py appsec export -N asomarri --rules

Show Rate Control Information
python swapi.py appsec export -N asomarri --rate

Show Custom Rule information
python swapi.py appsec export -N asomarri --custom
python swapi.py appsec export -N asomarri --custom --ruleId 633858

Show Exceptions and Conditions created in KRS rules
python swapi.py appsec export -N asomarri --exceptions
python swapi.py appsec export -N asomarri --exceptions --ruleId 973300


--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""RETRIEVE"""+bcolors.ENDC+"""

List Multi-Security Configurations
python swapi.py appsec msc

List Active and Latest versions
python swapi.py appsec latest -N asomarri

List Versions
python swapi.py appsec versions -N asomarri
python swapi.py appsec versions -N asomarri -V5

List Hostnames
python swapi.py appsec hostnames -N asomarri

List Policies
python swapi.py appsec policies -N asomarri

List Match Targets
python swapi.py appsec targets -N asomarri
python swapi.py appsec targets -N asomarri --policyId SuMe_60356

List Custom Rules
python swapi.py appsec custom -N asomarri
python swapi.py appsec custom -N asomarri --ruleId 633731
python swapi.py appsec custom -N asomarri --policyId SuMe_60356

NOTE: You can add the "--json" option to change output view from Table to JSON.


--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""AUTOMATION/REPORTING"""+bcolors.ENDC+"""

-Integration-
python swapi.py appsec Integration -N asomarri -V3 -t tourian.akamaiu.io --mtarget 3 --emails asomarri@akamai.com
	- Creates a New Version of the Security configuration.
	- Adds hostnames to Selected Hostnames.
	- Adds hostnames to Match Target.
	- Activates configuration in Staging and Production.

python swapi.py appsec Integration -N asomarri -V3 -t www.techjam4.io,www.techjam.io2 --mtarget 1  --noactivate
	- Creates a New Version of the Security configuration.
	- Adds hostnames to Selected Hostnames.
	- Adds hostnames to Match Target.

python swapi.py appsec Integration -N asomarri -V3 -t www.techjam.io1,jira.konanow.io --mtarget 1  --noactivate --noversion
	- Adds hostnames to Selected Hostnames.
	- Adds hostnames to Match Target.


Generate Protected Endpoint report
python swapi.py appsec protected


Host Addition Peer Review
python swapi.py appsec hostPR -N files/onboardinghosts.txt


--------------------------------------------------------------------------------

"""+bcolors.WARNING+"""ACTIONS"""+bcolors.ENDC+"""

-CREATE-

Create a new Configuration version:
python swapi.py appsec newVersion -N asomarri -V5


-Add/REMOVE Hostnames-

Selected Hosts
python swapi.py appsec add -N asomarri -t sonic.tdks.io,dev-tools2.akamai.io
python swapi.py appsec remove -N asomarri -t sonic.tdks.io,dev-tools2.akamai.io


Match Targets
python swapi.py appsec add -N asomarri -t dev-tools.akamai.io --mtarget 1
python swapi.py appsec remove -N asomarri -t dev-tools.akamai.io --mtarget 1


-Add/REMOVE Custom Rules-

python swapi.py appsec new -N asomarri --ruleId files/NoPass.json
python swapi.py appsec remove -N asomarri --ruleId 635309
python swapi.py appsec add -N asomarri --ruleId 635273 --policyId SuMe_60356
python swapi.py appsec add -N asomarri --ruleId 635273 --policyId SuMe_60356 --action deny
python swapi.py appsec remove -N asomarri --ruleId 635273 --policyId SuMe_60356


-ACTIVATION-

Staging:
python swapi.py appsec activate -N asomarri -V7 --notes "Testing API" --emails asomarri@akamai.com

Production:
python swapi.py appsec activate -N asomarri -V7 --notes "Testing API" --emails asomarri@akamai.com --cdn prod

--------------------------------------------------------------------------------

"""+bcolors.TURQUO+"""<SWaPI - SPS/CPS>"""+bcolors.ENDC+"""


"""+bcolors.WARNING+"""RETRIEVE"""+bcolors.ENDC+"""
python swapi.py CPS certs
python swapi.py CPS certs -N konanow.edgesuite.net (CPS API)
python swapi.py CPS secureEdge --contract 3-TWDH9B --group 33119 (SPS API)


--------------------------------------------------------------------------------

"""+bcolors.WHITE+"""<!----------- SWaPI HELP -----------!>"""+bcolors.ENDC+"""

		"""
		sys.exit()
	if not options.respjson and not options.automation:
		print bcolors.BOLD+bcolors.WHITE+'\n\t\t\t            <> '+bcolors.ENDC+bcolors.BOLD+bcolors.UNDERLINE+bcolors.TURQUO+' SWaPI '+bcolors.ENDC+bcolors.BOLD+bcolors.WHITE+' <>'+bcolors.ENDC
		print(bcolors.WHITE+"""
			   ________    ________   _________"""+bcolors.ENDC+"""
			SW"""+bcolors.WHITE+"""|________|  |________|      |
			  |        |  |           ____|____
			                      """+bcolors.ENDC+"""Akamai For DevOps

			""")
	if apiModule == 'crawl' or apiModule == 'checkip':
		Diagnostic(options.automation,options.AccountSwitch,options.host,apiModule,options.edge,options.refId,options.cpcode,options.creds,options.respjson)
	elif apiModule == 'map':
		mapping(options.AccountSwitch,options.propertyName,apiObject)
	elif apiModule == 'audit':
		auditModule(options.automation,options.AccountSwitch,options.propertyName,options.creds)
	elif apiModule == 'contract':
		ContractsAPI(options.sqa,options.AccountSwitch,options.propertyName,options.creds,options.respjson,apiObject,options.contractId,options.depth,options.cloneFrom,options.to)
	elif apiModule == 'alerts':
		AlertsManagement(options.AccountSwitch,options.propertyName,options.creds,options.respjson,apiObject,options.fname,options.fvalue,options.ids,options.extended)
	elif apiModule == 'case':
		caseManagement(options.duration,options.AccountSwitch,options.propertyName,options.creds,options.respjson,apiObject,options.category,options.listType,options.notes)
	elif apiModule == 'plx':
		plxAnalytics(options.AccountSwitch,options.propertyName,options.creds,options.respjson,apiObject,options.host,options.contractId,options.groupId,options.start,options.end,options.attack)
	elif apiModule == 'dns':
		fastDNS(options.AccountSwitch,options.propertyName,options.creds,options.respjson,apiObject,options.listType,options.host,options.contractId,options.groupId,options.zonesDiff,options.propertyVersion)
	elif apiModule == 'secmon':
		SecMon(options.automation,options.AccountSwitch,apiObject,options.reportPackId,options.respjson,options.creds)
	elif apiModule == 'cps' or apiModule == 'sps':
		CPSandSPS(options.automation,options.AccountSwitch,apiObject,options.edge,options.creds,options.respjson,options.productId,options.contractId,options.groupId,options.enrollmentId,options.propertyName)
	elif apiModule == 'ss':
		SiteShield(options.automation,options.AccountSwitch,apiObject,options.mapId,options.creds,options.respjson)
	elif apiModule == 'siem':
		SIEMModule(options.automation,options.AccountSwitch,options.propertyName,options.creds,options.configId,options.offset,options.limit,options.start,options.end,options.respjson)
	elif apiModule == 'iam':
		IAMModule(options.sqa,options.automation,options.host,options.AccountSwitch,options.propertyName,options.creds,options.groupId,apiObject,options.respjson,options.propertyId,options.userId,options.sendEmail,options.passwd)
	elif apiModule == 'nl':
		NetworkListAPI(options.automation,options.AccountSwitch,options.host,apiObject,options.creds,options.propertyName,options.netId,options.listType,options.includeElements,options.extended,options.respjson,options.netlist,options.emails,options.cdn)
	elif apiModule == 'appsec':
		APPSEC_MAIN(options.generate,options.prefix,options.bypass,options.defaultFile,options.negativePath,options.negativeFile,options.path,options.automation,options.AccountSwitch,options.host,apiObject,options.propertyName,options.propertyVersion,options.emails,options.notes,options.cdn,options.PRd,options.cemails,options.cloneFrom,options.copyHostnames,options.ipVersion,options.creds,options.policyId,options.configId,options.ruleId,options.respjson,options.appsec_actions,options.seq,options.noactivate,options.noversion,options.rateControls,options.rules,options.customRules,options.exceptions)
	elif apiModule == 'papi':
		PAPI(options.automation,options.AccountSwitch,options.stagingPush,options.srto,options.origin,options.host,apiObject,options.contractId,options.groupId,options.propertyId,options.propertyName,options.edgeId,options.propertyVersion,options.edge,options.latest,options.emails,options.notes,options.cdn,options.PRd,options.cemails,options.ruleTree,options.cloneFrom,options.copyHostnames,options.ipVersion,options.ruleFormat,options.productId,options.cpcode,options.creds,options.respjson)
	else:
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
		print bcolors.TURQUO+"[SWaPI] "+bcolors.WARNING+"Not a valid module: "+apiModule+bcolors.ENDC
		print bcolors.WHITE+'\n\n<!----------- SWaPI -----------!>\n\n'+bcolors.ENDC
	sys.exit()

if __name__ == "__main__":
	main()
