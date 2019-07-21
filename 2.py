import csv 
import glob
import os
import operator
import time
start = time.time()
path = ('/home/bsnova/Desktop/assignment/ipl/*.csv')
files = glob.glob(path)
ref={}
for name in files:
	file1=open(name)
	reader=csv.reader(file1)
	for row in reader:
  		if(row[0]=='info' or row[0]=='version'):
			reader.next()
  		elif(row[9]=='caught' or row[9]=='bowled' or row[9]=='run out' or row[9]=='lbw' or row[9]=="caught and bowled"):
			batname=row[4]
			ballname=row[6]
			if (batname,ballname) in ref.keys():
				ref[(batname,ballname)]+=1
			else:
				ref[(batname,ballname)]=1
	file1.close()

key_max = max(ref.iteritems(), key=operator.itemgetter(1))[0]


end=time.time()


print 'Max: ',key_max
print ref[key_max]
print('time: ',end-start)
