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

import json, urllib2, os, base64, getpass

colorred = "\033[01;31m{0}\033[00m"
colorgrn = "\033[1;36m{0}\033[00m"

def sizeof_fmt(num):
    for x in ['Bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

password = getpass.getpass()

request = urllib2.Request("https://dsnet.manager/manager/api/json/1.0/listVaults.adm")
request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % ('admin',password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

data = json.load(result)

names = []
logusedspace = []
phyusedspace = []
estusedspace = []

for x in data['responseData']['vaults']:
        names.append(x['name'])
        logusedspace.append(x['usedLogicalSizeFromStorage'])
        phyusedspace.append(x['usedPhysicalSizeFromStorage'])
	estusedspace.append(x['estimateUsableTotalLogicalSizeFromStorage'])

for name,log,phy,est in zip(names, logusedspace, phyusedspace, estusedspace):
        print colorred.format("\nVault name: 			") + name
        print colorgrn.format("  logical space used: 		") + sizeof_fmt(log)
        print colorgrn.format("  physical space used: 		") + sizeof_fmt(phy)
	    print colorgrn.format("  estimated logical space used: ") + sizeof_fmt(est) + "\n"
