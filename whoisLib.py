#! /usr/bin/python
#################################################
#                   whoisLib                    #
#################################################
# teekayzed                                     #
# teekayzed@users.noreply.github.com            #
#                                               #
# Features:                                     #
#   - Searches for preexisting PKL or CSV       #
#   - If not found, builds TLD&WHOIS pairings   #
#      and saves them in run directory          #
#   - If found it scrapes iana.org for any new  #
#      TLDs                                     #
#   - Performs WHOIS lookup of domains          #
#   - Performs RWHOIS lookup of IP addresses    #
#   - Will export "tld,whois" pairings to CSV   #
#################################################
#################################################
'''
#######################
#  TO DO LIST
#  
#  --Move main into respective functions
#  --Build out args and test
#  --Build out PKL and CSV check
#  --Build out updateTLD func and logic
#  --Build out getWhoisServer to check imported
#		CSV/PKL for existing, if not lookup
#		TLD and add its whois server to the
#		CSV/PKL. Set flag that it has been updated
#		in order to call export at end.
#  --Build out getWhois - perform whois lookup
#  --Build out TLDWhois Class - See notes below
#  --Build out getRWhois - perform IP lookup
#  --Build out dictToCSV
#  --Build out dictToPKL
#  --Tidy up documentation and comments
#
#		#####################
#		#
#		# Class for all info for a TLD
#		# Will include TLD suffix, WHOIS
#		# server, name servers, rWHOIS
#		# server, Sponsoring Org, admin
#		# contact info, and technical 
#		# contact info. 
#		#
#		# Pass a TLD suffix, and it will
#		# build the rest as possible
#		#
#		# follow defs:
#		#    __init__(self, suffix) - pass suffix and
#		#      then initialize all attributes
#		#    build* - one for each bit of info, called
#		#      from within init to fully initialize
#		#      attributes
#		#    getInfo - gets background info,
#		#      all contained in single string, maybe
#		#    getWhois - returns whois server
#		#    getRWhois - returns rwhois serveread
#		#    getNS - returns lsit of Name Servers
#		#
#		#####################
#
#######################
'''

#########
# IMPORTS
#########
import requests
import re

#########
# VARS
#########
programName="whoisLib.py"
programDescription="WHOIS utility module"
programVersion="1.0"

tldDB='https://www.iana.org/domains/root/db'
tldURIList = [] #Init list for list for all TLD URIs
whoisDictionary = {}

verbose=False
progress=0
##################################################
# FUNCTIONS
##################################################
#############
# GET ARGS
#############
def getArgs():
	parser = argparse.ArgumentParser(prog=programName, description=programDescription)
	parser.add_argument("-a","--arg",help="ARG HELP",required=False)


	return parser.parse_args()

	###############################################
	# OTHER NOTES 
	# 
	# For groups of args [in this case one of the two is required]:
	# group = parser.add_mutually_exclusive_group(required=True)
	# group.add_argument("-a1", "--arg1", help="ARG HELP")
	# group.add_argument("-a2", "--arg2", help="ARG HELP")
	#
	# To make a bool thats true:
	# parser.add_argument("-a","--arg",help="ARG HELP", action="store_true")
	#
	###############################################
#############
# END OF ARGS
#############


#############
# MAIN
#############
def main(args):
	r = requests.get(tldDB)
	regex = '<span class="domain tld">+<a href="\/\w*\/\w*\/\w*\/\w*\.\w*">'
	matches = re.findall(regex, r.text)

	# For each entry in the list of matches, trim off the
	# unncessary bits and slap 'em into the tldURIList list
	for match in matches:
		tldURIList.append(match[34:-2])

	# For every URI found on the main page, loop
	for uri in tldURIList:
		# Set each 'key' in dict to the '.*' value
		key = '.' + uri[17:-5]

		# Generate a full URI for each TLD and retrieve
		tldURI = 'https://www.iana.org' + uri

		r = requests.get(tldURI)

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
#############
# END OF MAIN
#############


#############
# checkForPKL
#############
def checkForPKL():
	print "checkforPKL"
#############
# END OF checkForPKL
#############


#############
# checkForCSV
#############
def checkForPKL():
	print "checkforPKL"
#############
# END OF checkForCSV
#############


#############
# updateTLD
#############
def updateTLD():
	print "updateTLD"
#############
# END OF updateTLD
#############


#############
# getWhoisServer
#############
def getWhoisServer(tldSuffix):
	print "getWhoisServer"
#############
# END OF getWhoisServer
#############


#############
# getWhois
#############
def getWhois(tld):
	print "getWhois"
#############
# END OF getWhois
#############


#############
# getRWhois
#############
def getRWhois(ip):
	print "getRWhois"
#############
# END OF getRWhois
#############


#############
# dictToCSV
#############
def dictToCSV(dictionary,filename):
	print "dictToCSV"
#############
# END OF dictToCSV
#############


#############
# dictToPKL
#############
def dictToPKL(dictionary,pklname):
	print "dictToPKL"
#############
# END OF dictToPKL
#############

##################################################
# END OF FUNCTIONS
##################################################


###########################
# PROG DECLARE
###########################
if __name__ == '__main__':
	args = getArgs()
	main(args)
