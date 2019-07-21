
import csv
import os
import glob
import time


start=time.time()
path = ('/home/bsnova/Desktop/assignment/*.csv')
files = glob.glob(path)

bowlers={}


for name in files:
	file1 = open(name)
	reader = csv.reader(file1)

	for row in reader:
	 	if row[0]=='info' and row[1]=='city':
			print ("1")
			if row[2] not in bowlers.keys():
				print ("2")		
				bowlers[row[2]]=row[3]

	file1.close()
 
print (bowlers)

