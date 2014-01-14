#!/usr/bin/python
##
# Simple report on logical used
# and physical used space.
# It should evolve more, just
# basic report for now.
##
# blake golliher
# blakegolliher@gmail.com
#
##

import json, urllib2, os, base64, getpass, sys

usage = """
Usage: ./getVaults.py manager name (or ip)
e.g ./getVaults.py dsnet.manager

Vault name: 			itms8
  logical space used: 		428.7 GB
  physical space used: 		428.7 GB
  estimated logical space used: 216.6 TB

Vault name: 			itms7
  logical space used: 		300.4 GB
  physical space used: 		300.4 GB
  estimated logical space used: 216.6 TB

EXAMPLE

"""

if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

manager = sys.argv[1]

colorred = "\033[01;31m{0}\033[00m"
colorgrn = "\033[1;36m{0}\033[00m"

def sizeof_fmt(num):
    for x in ['Bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

password = getpass.getpass()

request = urllib2.Request("https://" + manager + "/manager/api/json/1.0/listVaults.adm")
request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % ('admin',password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

data = json.load(result)

names = []
logusedspace = []
phyusedspace = []
estusedspace = []

for item in data['responseData']['vaults']:
        names.append(item['name'])
        logusedspace.append(item['usedLogicalSizeFromStorage'])
        phyusedspace.append(item['usedPhysicalSizeFromStorage'])
	estusedspace.append(item['estimateUsableTotalLogicalSizeFromStorage'])

for name,log,phy,est in zip(names, logusedspace, phyusedspace, estusedspace):
        print colorred.format("Vault name: 			") + name
        print colorgrn.format("  logical space used: 		") + sizeof_fmt(log)
        print colorgrn.format("  physical space used: 		") + sizeof_fmt(phy)
 	print colorgrn.format("  estimated logical space used:  ") + str(sizeof_fmt(est))
