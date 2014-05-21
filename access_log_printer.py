#!/usr/bin/python
##
# Cleversafe Access log parser
# summarizes access logs from
# Cleversafe accessors.
##
# Blake Golliher
# blakegolliher@gmail.com
##
import json,sys,numpy,os

usage = """

EXAMPLE
Usage: ./access_log_printer.py filename

    [bgolliher@storageadmin001 ~]$ python access_log_printer.py access.log-2014-05-18T231349255

    Accessor Log Report
    There were 636618 PUT and 0 GET and 0 DELETE calls (and 0 others)
    The avg latency per call was 38.46 seconds with a max of 682.00 seconds, and a min of 0.0000 seconds.
    Post Transfer time average was 0.04 miliseconds, the max was 342.00, and the min was 0.00.
    The size average was 2.5MB.  The max was 32.0MB, and the min was 116.0bytes.
"""

if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

tgtfile = sys.argv[1]

if ( not os.path.isfile(tgtfile)):
    print("Error: %s file not found" % tgtfile)
    print (usage)
    sys.exit(0)
else:
    print("Using %s ..." % tgtfile)


def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

request_latency = []
timestamp_start = []
status = []
request_method = []
sizes = []
puts = []
gets = []
deletes = []
others = []
post_transfer = []

f = file(tgtfile, "r")
lines = f.readlines()
for line in lines:
	try:
		loadLines = json.loads(line)
		request_latency.append(int(loadLines['request_latency']))
		post_transfer.append(int(loadLines['stat']['post_transfer']))
		timestamp_start.append(loadLines['timestamp_start'])
		status.append(loadLines['status'])
		request_method.append(loadLines['request_method'])
		sizes.append(int(loadLines['request_length']))
		if loadLines['request_method'] == 'PUT':
			puts.append(loadLines['request_method'])
		elif loadLines['request_method'] == 'GET':
			gets.append(loadLines['request_method'])
		elif loadLines['request_method'] == 'DELETE':
			deletes.append(loadLines['request_method'])
		else:
			others.append(loadLines['request_method'])
	except ValueError:
		pass

avg_lat = numpy.average(request_latency) / 1000
max_lat = numpy.max(request_latency) / 1000
min_lat = numpy.min(request_latency) / 1000
post_time_avg = numpy.average(post_transfer)
post_time_min = numpy.min(post_transfer)
post_time_max = numpy.max(post_transfer)
size_avg = numpy.average(sizes)
size_max = numpy.max(sizes)
size_min = numpy.min(sizes)

print "\nAccessor Log Report"
print "There were %s PUT and %s GET and %s DELETE calls (and %s others)" % (len(puts),len(gets),len(deletes),len(others))
print "The avg latency per call was %.2f seconds with a max of %.2f seconds, and a min of %.4f seconds." % (avg_lat,max_lat,min_lat)
print "Post Transfer time average was %.2f miliseconds, the max was %.2f, and the min was %.2f." % (post_time_avg,post_time_max,post_time_min)
print "The size average was %s.  The max was %s, and the min was %s." % (sizeof_fmt(size_avg),sizeof_fmt(size_max),sizeof_fmt(size_min))
