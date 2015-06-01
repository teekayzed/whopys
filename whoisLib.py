import requests
import re



targetURL = 'https://www.iana.org/domains/root/db'

r = requests.get(targetURL)

regex = '<span class="domain tld">+<a href="\/\w*\/\w*\/\w*\/\w*\.\w*">'

matches = re.findall(regex, r.text)

# Create empty list
tldURIs = []
whoisDictionary = {}
# For each entry in the list of matches, trim off the
# unncessary bits and slap 'em into the tldURIs list
for match in matches:
	tldURIs.append(match[34:-2])



# Initialize the progress counter
progress=0

# For every URI found on the main page, loop
for uri in tldURIs:


	# Set each 'key' in dict to the '.*' value
	key = '.' + uri[17:-5]

	# Generate a full URI for each TLD and retrieve
	newURI = 'https://www.iana.org' + uri

	r = requests.get(newURI)

	# Find place in page for the WHOIS server and match
	regex = 'WHOIS Server:.*'
	
	matches = re.findall(regex, r.text)

	# If a match is found continue, or else the TLD
	# Does not have a WHOIS server and should be
	# ignored.
	if matches:
		# Entry will be the first, trim the first 18
		# Characters to remove the B.S.
		match = matches[0]
		match = match[18:]

		# Add entry to the dictionary of the '.*' for the key
		# and the WHOIS server for the match
		whoisDictionary[key] = match

		# The following is for progress notification
		print 'WHOIS server found for ' + key + ' at ' + match
		progress += 1
		if (progress % 50) == 0:
			print 'Number of domains found: ' + str(progress)

# Once completed print out the dictionary
print whoisDictionary




#####################
#
# Class for all info for a TLD
# Will include TLD suffix, WHOIS
# server, name servers, rWHOIS
# server, Sponsoring Org, admin
# contact info, and technical 
# contact info. 
#
# Pass a TLD suffix, and it will
# build the rest as possible
#
# follow defs:
#    __init__(self, suffix) - pass suffix and
#      then initialize all attributes
#    build* - one for each bit of info, called
#      from within init to fully initialize
#      attributes
#    getInfo - gets background info,
#      all contained in single string, maybe
#    getWhois - returns whois server
#    getRWhois - returns rwhois serveread
#    getNS - returns lsit of Name Servers
#
#####################
'''

def checkForPKL():

def updateTLD():

def getWhoisServer(tldSuffix):

def getWhois(tld):

def getRWhois(ip):

def dictToCSV(dictionary,filename):
	import csv
	with open(filename,'wb') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',', 
			quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for key, value in dictionary.iteritems():
			csvwriter.writerow(key,value)

def dictToPKL(dictionary,pklname):


'''