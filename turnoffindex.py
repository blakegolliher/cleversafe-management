#!/usr/bin/python
##
#
# simple tool to turn off
# indexing on all vaults
#
##
# blake golliher
# blakegolliher@gmail.com
#
##

import json, urllib2, os, base64, getpass, sys
import socket
import urllib

usage = """

EXAMPLE
Usage: ./turnoffindex.py manager name (or ip)

....

"""

if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

passwd = getpass.getpass()

manager = sys.argv[1]

def checkhost(hostname):
    contest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        contest.connect((hostname,443 ))
	      # is it reachable on port 443?
    	  # print "Port 443 reachable"
    except socket.error as e:
    	  print "Error on connect: %s" % e
	exit()
  contest.close()

checkhost(manager)

request = urllib2.Request("https://" + manager + "/manager/api/json/1.0/viewSystemConfiguration.adm")
request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % ('admin',passwd)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

data = json.load(result)

names = []
ids = []
indexlist = []

for item in data['responseData']['vaults']:
        names.append(item['name'])
        ids.append(item['id'])
	      indexlist.append(item['nameIndexEnabled'])

for name,id,index in zip(names,ids,indexlist):
        changeurl = urllib2.Request("https://" + manager + "/manager/api/json/1.0/editVault.adm")
        data = urllib.urlencode({"id":id,"nameIndexEnabled":"false"})
        changeurl.add_header('Accept', 'application/json')
        base64string = base64.encodestring('%s:%s' % ('admin',passwd)).replace('\n', '')
        changeurl.add_header("Authorization", "Basic %s" % base64string)
        changeresult = urllib2.urlopen(changeurl,data)
        print "Vault: %s\t\tID: %s\t\tIndex: %s" % (name, id, index)
