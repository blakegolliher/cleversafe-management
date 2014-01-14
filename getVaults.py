#!/usr/bin/python
##
#
# Simple report on logical used
# and physical used space.
# It should evolve more, just
# basic report for now.
##
# [blakegolliher@admin001 cleversafe-code]$ ./getVaults.py
# Password:
# Vault name: avault.
#   logical space used: 0 bytes.
#   physical space used: 0 bytes.
# Vault name: avault1.
#   logical space used: 0 bytes.
#   physical space used: 0 bytes.
# Vault name: avault2.
#   logical space used: 0 bytes.
#   physical space used: 0 bytes.
# Vault name: avault3.
#   logical space used: 0 bytes.
#   physical space used: 0 bytes.
# Vault name: avault4.
#   logical space used: 0 bytes.
#   physical space used: 0 bytes.
# Vault name: avault5.
#   logical space used: 0 bytes.
#   physical space used: 0 bytes.
# [blakegolliher@admin001 cleversafe-code]$
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

request = urllib2.Request("https://17.176.156.23/manager/api/json/1.0/listVaults.adm")
request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % ('admin',password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

data = json.load(result)

names = []
logusedspace = []
phyusedspace = []

for x in data['responseData']['vaults']:
        names.append(x['name'])
        logusedspace.append(x['usedLogicalSizeFromStorage'])
        phyusedspace.append(x['usedPhysicalSizeFromStorage'])

for name,log,phy in zip(names, logusedspace, phyusedspace):
        print colorred.format("Vault name: ") + name
        print colorgrn.format("  logical space used: ") + sizeof_fmt(log)
        print colorgrn.format("  physical space used: ") + sizeof_fmt(phy)
