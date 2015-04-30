#!/usr/bin/env python
import sys, time, datetime, os, pwd, csv, random

def read_file(filename):
	with open(filename, 'r') as f:
		data = [row for row in csv.reader(f.read().splitlines())]
	return data

def makePairs(numbers_array):
	index = random.randint(0,len(numbers_array) - 1)
	first = numbers_array.pop(index)
	index = random.randint(0,len(numbers_array) - 1)
	second = numbers_array.pop(index)

	return (first, second)

def makeCallFile(numtocall, conference_id):
	# Get Arguments
	numArgs = len(sys.argv)
	# First argument Number to Call

	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S-%m-%d-%Y')

	#create temp and destination directories
	temp_dir = "/tmp/:"
	callfile = "call_" + st + ".call"
	startcallfile = temp_dir + callfile
	end_dir = "/var/spool/asterisk/outgoing/"
	endcallfile = end_dir + callfile

	#write file to disk
	scf = open(startcallfile,"w")
	scf.write("Channel: SIP/flowroute/" + str(numtocall) + "\n")
	scf.write("MaxRetries: 1\n")
	scf.write("RetryTime: 60\n")
	scf.write("WaitTime: 30\n")
	scf.write("Context: listen\n")
	scf.write("Extension: s\n")
	#if asteriskParams['variables']!="":
	scf.write("Set: CONFID=" + conference_id + " \n")

	scf.close()

	#change file permission
	os.chmod(startcallfile,0777)
	os.chown(startcallfile, pwd.getpwnam(os.environ['USER']).pw_uid, pwd.getpwnam(os.environ['USER']).pw_gid)

	#hour-minute-second-month-day-year (example: 02-10-00-09-27-2007)
	# if asteriskParams['touchtime'] != "":
	# 	ctime = time.mktime(datetime.datetime.strptime(asteriskParams['touchtime'], "%H:%M:%S-%m-%d-%Y").timetuple())
	# 	os.utime(startcallfile,ctime,ctime,) #change file time to future date

	#move file to /var/spool/asterisk/outgoing
	os.rename(startcallfile, endcallfile)

d = read_file('phone_numbers.csv')
numbers = []

for i in d:
	numbers.append(i[0])

while len(numbers) > 0:
	pair = makePairs(numbers)
	print pair[0], pair[1]
	confid = str(pair[0][-4:]) + str(pair[1][-4:])
	print confid
	makeCallFile(pair[0],confid)
	makeCallFile(pair[1],confid)