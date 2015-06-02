import csv
testDict = {}
testDict['a']='1'
testDict['b']='2'
testDict['c']='3'
testDict['d']='4'

writer = csv.writer(open('testdict.csv', 'wb'))
for key, value in testDict.items():
   writer.writerow([key, value])