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

EXAMPLE
Usage: ./getVaults.py manager name (or ip)
[blakegolliher@admin001 ~ ]$ ./getVaults.py dsnet.manager

Vault name: video01
  space used on disk: 		4.990 PB
  space used to the app :	2.772 PB

Vault name: music01
  space used on disk: 		19.383 GB
  space used to the app :	10.752 GB

....

"""

if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

manager = sys.argv[1]

def sizeof_fmt(num):
    for x in ['Bytes','KB','MB','GB','TB', 'PB']:
        if num < 1000.0:
            return "%3.3f %s" % (num, x)
        num /= 1000.0

request = urllib2.Request("https://" + manager + "/manager/api/json/1.0/listVaults.adm")
request.add_header('Accept', 'application/json')
result = urllib2.urlopen(request)

data = json.load(result)

names = []
phyusedspace = []
estusedspace = []

for item in data['responseData']['vaults']:
        names.append(item['name'])
        phyusedspace.append(item['usedPhysicalSizeFromStorage'])
        estusedspace.append(item['estimateUsableUsedLogicalSizeFromStorage'])

for name,phy,est in zip(names, phyusedspace, estusedspace):
        print "\nVault name: %s " % name
        print "  space used on disk: 		%s " % sizeof_fmt(phy)
        print "  space used to the app :	%s " % str(sizeof_fmt(est))
print "\n"
