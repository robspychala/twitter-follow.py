#!/usr/bin/python

import re
import urllib2
from sets import Set
import twitter
import getopt
import sys

def follow():
	
	opts, args = getopt.getopt(sys.argv[1:], None, ['url=', 'username=', 'password='])

	url = None
	username = None
	password = None

	for o, v in opts:
		if o == "--url":
		    url = v
		elif o == "--username":
		    username = v
		elif o == "--password":
		    password = v
	
	if (not (url and username and password)):
		usage()
		exit(1)
		
	print "requesting url=" + url

	req = urllib2.Request(url)
	req.add_header('Referer', 'http://www.python.org/')
	f = urllib2.urlopen(req)

	users = Set()

	for line in f:
		m = re.search('\shref=\"http://twitter.com/(\w*)\".*', line)
		if (m and m.group(1) not in users):
			users.add(m.group(1))

	f.close()

	if (len(users) > 0):
		
		print "Great! Found " + str(len(users)) + " twitter users!"

		api = twitter.Api(username=username, password=password)

		for name in users:
	
			print "create friendship with: " + name
	
			try:
				api.CreateFriendship(name)
			except:
				print "error with: " + name
	else:
		print "Oops! No users found"
		
def usage():
	 
	print sys.argv[0] + " error"
	print "bad input command line parameters, follow.py needs --url=<where the list of user links is> --username=<your twitter> --password=<your twitter>"
	print
	
if __name__ == "__main__":
	follow()