#!/usr/bin/python
##
#
# Quick pass at parsing Cleversafe
# access logs.  
#
# Blake Golliher - blakegolliher@gmail.com
#
##
import json

request_latency = []
timestamp_start = []
status = []
request_method = []

f = file('access.log', "r")
lines = f.readlines()
for line in lines:
        try:
            loadLines = json.loads(line)
            request_latency.append(loadLines['request_latency'])
            timestamp_start.append(loadLines['timestamp_start'])
	    status.append(loadLines['status'])
	    request_method.append(loadLines['request_method'])
        except ValueError:
            pass

print "\nAccessor Log Report"
for req,ts,st,rm in zip(request_latency,timestamp_start,status,request_method):
	print "Request is a %s at %s. It took %s ms and returned a %s " % (rm,ts,req,st)
