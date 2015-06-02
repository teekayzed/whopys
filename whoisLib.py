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
whoisLib.py 
.checks for PKL/CSV existence, if not notifies user and gives
    chance to cancel, then performs the full scrape of tld/whois pairings
  -u --update runs updateTLD to update and then export
  -w --whois  runs getWhoisServer to find tld passed, if not found, scrapes
         iana for the TLD, adds it to dict, then runs getWhois
  -i --ip  runs getRWhois
.then calls dictToCSV and dictToPKL to export dictionary
.then returns results of whatever was called, then exits

	

#######################
#  TO DO LIST
#  
#  XXMove main into respective functions
#  XXBuild out args and test
#  XXBuild out PKL and CSV check
#  --Build out updateTLD func and logic
#  --Build out getWhoisServer to check imported
#		CSV/PKL for existing, if not lookup
#		TLD and add its whois server to the
#		CSV/PKL. Set flag that it has been updated
#		in order to call export at end.
#  --Build out getWhois - perform whois lookup
#  --Build out TLDWhois Class - See notes below
#  --Build out getRWhois - perform IP lookup
#  XXBuild out dictToCSV
#  XXBuild out dictToPKL
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
import sys
import argparse
import os.path
import csv
import timeit
import pickle

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

##################################################
# FUNCTIONS
##################################################
#############
# GET ARGS
#############
def getArgs():
	parser = argparse.ArgumentParser(prog=programName, description=programDescription)
	parser.add_argument("-a","--arg",help="ARG HELP",required=False)
	parser.add_argument("-v","--verbose",help="Increase verbosity",action="store_true",required=False)
	parser.add_argument("-u","--update",help="Update TLD/Whois pairing",action="store_true",required=False)
	parser.add_argument("-w","--whois",help="Perform whois lookup",required=False)
	parser.add_argument("-i","--ip",help="Perform IP lookup",required=False)


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
	
	if args.verbose:
		startTime = timeit.default_timer()

	if checkForFile("tldwhois.pkl") == True:
		tldPKLExists = True
		if args.verbose:
			print "PKL file exists."
		#If it exists, import PKL to dictionary
	
	if checkForFile("tldwhois.csv") == True:
		tldCSVExists = True
		if args.verbose:
			print "CSV file exists."
		#If it exists, but not PKL, import CSV to dictionary
	
	if (not checkForFile("tldwhois.pkl")) and (not checkForFile("tldwhois.csv")):
		if args.verbose:
			print "Neither the PKL or CSV file exist. Full update is needed..."
		updateTLD()
		global whoisDictionary
		dictToPKL(whoisDictionary,"tldwhois.pkl")
		dictToCSV(whoisDictionary,"tldwhois.csv")
		#If neither exists. Notify user, and ask if want to create. Then update, export to PKL and CSV, then continue
	
	if (checkForFile("tldwhois.pkl") == True) and (checkForFile("tldwhois.csv") == False):
		#Import PKL. 
		if args.verbose:
			print "PKL exists... Importing..."
		whoisDictionary = pickle.load(open("tldwhois.pkl", "rb"))
		#Export to CSV.
		if args.verbose:
			print "CSV doesn't exist... Exporting the PKL to CSV..."
		dictToCSV(whoisDictionary,"tldwhois.csv")

	if (checkForFile("tldwhois.pkl") == False) and (checkForFile("tldwhois.csv") == True):
		
		#Import CSV. 
		if args.verbose:
			print "CSV exists... Importing..."
		reader = csv.reader(open('tldwhois.csv', 'rb'))
		whoisDictionary = dict(x for x in reader)
		#Export to PKL.
		if args.verbose:
			print "PKL doesn't exist... Exporting the CSV to PKL..."
		dictToPKL(whoisDictionary,"tldwhois.pkl")

	if (checkForFile("tldwhois.pkl") == True) and (checkForFile("tldwhois.csv") == True):
		#Both true, continue.
		if args.verbose:
			print "PKL and CSV exist. Continuing."

	if args.update:
		#go through entire process to create PKL and CSV files. Might have to clear existing. Who knows
		updateTLD()

	if args.whois:
		getWhois(getWhoisServer(args.whois))		

	if args.ip:
		getRWhois(ip)

	endTime = timeit.default_timer()
	if args.verbose:
		print endTime - startTime
	
	# Once completed print out the dictionary
	#print whoisDictionary
#############
# END OF MAIN
#############


#############
# checkForPKL
#############
def checkForFile(filename):
	if os.path.isfile(sys.path[0] + "/" + filename):
		return True
	else:
		return False
#############
# END OF checkForPKL
#############


#############
# updateTLD
#############
def updateTLD():
	global whoisDictionary
	if args.verbose:
		print "Fully updating TLD list..."


	r = requests.get(tldDB)
	regex = '<span class="domain tld">+<a href="\/\w*\/\w*\/\w*\/\w*\.\w*">'
	matches = re.findall(regex, r.text)

	# For each entry in the list of matches, trim off the
	# unncessary bits and slap 'em into the tldURIList list
	for match in matches:
		tldURIList.append(match[34:-2])

	# For every URI found on the main page, loop
	progress = 0
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
			
			
			progress += 1
			if args.verbose:
				print 'WHOIS server found for ' + key + ' at ' + match
				if (progress % 50) == 0:
					print 'Number of domains found: ' + str(progress)

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
	if args.verbose:
		print "Exporting dictionary to CSV..."
	writer = csv.writer(open(filename, 'wb'))
	for key, value in dictionary.items():
		writer.writerow([key, value])
#############
# END OF dictToCSV
#############


#############
# dictToPKL
#############
def dictToPKL(dictionary,pklname):
	if args.verbose:
		print "Exporting dictionary to PKL..."
	pickle.dump(dictionary,open(pklname,"wb"))
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
