#!/usr/bin/python
##
# Simple report on logical used
# and physical used space.
# It should evolve more, just
# basic report for now.
#
# Assumes only one storage pool.
##
# blake golliher
# blakegolliher@gmail.com
#
##

import json, urllib2, os, base64, getpass, sys

usage = """
Usage: ./getVaults.py manager name (or ip)
e.g ./getVaults.py dsnet.manager

Pool name:			thepool
   Usable space: 		   5.25 PB

Vault name:			vault01
   logical space used:		   758.61 GB
   physical space used:		   758.61 GB
Vault name:			vault02
   logical space used:		   130.14 GB
   physical space used:		   130.14 GB

"""

if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

manager = sys.argv[1]

def readable_size(size):
    for unit in ['bytes','KB','MB','GB','TB']:
        if size < 1000.0 and size > -1000.0:
            return "%3.2f %s" % (size, unit)
        size /= 1000.0
    return "%3.2f %s" % (size, 'PB')

password = getpass.getpass()

request = urllib2.Request("https://" + manager + "/manager/api/json/1.0/listVaults.adm")
request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % ('admin',password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

data =   json.load(result)
pname =  data['responseData']['vaults'][0]['storagePools'][0]['storagePool']['name']
pusize = data['responseData']['vaults'][0]['storagePools'][0]['storagePool']['usableSize']

print '\nPool name:			%s ' % pname
print '   Usable space: 		   %s \n' % readable_size(pusize)

names = []
logusedspace = []
phyusedspace = []

for item in data['responseData']['vaults']:
        names.append(item['name'])
        logusedspace.append(item['usedLogicalSizeFromStorage'])
        phyusedspace.append(item['usedPhysicalSizeFromStorage'])

for name,log,phy in zip(names, logusedspace, phyusedspace):
        print 'Vault name:			%s ' % name
        print '   logical space used:		   %s ' % readable_size(log)
        print '   physical space used:		   %s ' % readable_size(phy)
