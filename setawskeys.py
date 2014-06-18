#!/usr/bin/python
##
#
# set aws keys per user 
#
##
# blake golliher
# blakegolliher@gmail.com
#
##

import json, urllib, urllib2, os, base64, getpass, sys, socket

usage = """

EXAMPLE
Usage: ./setawskey.py manager.dsnet.com user hereisthekey hereisthesecretcode

....

"""

if len(sys.argv)!=5:
    print (usage)
    sys.exit(0)

passwd = getpass.getpass()

manager = sys.argv[1]
sysname = sys.argv[2]
key = sys.argv[3]
secretkey = sys.argv[4]

def checkhost(hostname):
    contest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    	contest.connect((hostname,443 ))
	    # is it reachable on port 443?
    	# print "Port 443 reachable"
    except socket.error as e:
    	print "Error on %s, can not connect to port 443 : %s" % (hostname, e)
	exit()
    contest.close()

checkhost(manager)

request = urllib2.Request("https://" + manager + "/manager/api/json/1.0/listAccounts.adm")
namedata = urllib.urlencode({"name":sysname})
request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % ('admin',passwd)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request,namedata)

jsonresult = json.load(result)
for name in jsonresult['responseData']['accounts']:
	if name['name'] != sysname:
		pass
	else:
		id = name['id']
		# should print out access keys, possibly as a switch?
		# print 'Access keys are :'
		# print '\t%s' % name['accessKeys']
		# print name['id']
		# print 'found it!\n'
		request = urllib2.Request("https://" + manager + "/manager/api/json/1.0/importAccountAccessKey.adm")
		keydata = urllib.urlencode({"id":id,"accessKeyId":key,"secretAccessKey":secretkey})
		request.add_header('Accept', 'application/json')
		base64string = base64.encodestring('%s:%s' % ('admin',passwd)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)
		result = urllib2.urlopen(request,keydata)

		data = json.load(result)

		print data['responseHeader']['status'] 
		print '\n'
		# print data['responseHeader']
		sys.exit(0)

# curl -sku admin "https://manager.dsnet.com/manager/api/json/1.0/listAccounts.adm" | jq '.responseData.accounts[] | select (.name=="bgolliher") | .id'
