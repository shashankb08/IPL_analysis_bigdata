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
  		elif (int(row[7])>0):
			
			batname=row[4]
			ballname=row[6]
			if (batname,ballname) in ref.keys():
				ref[(batname,ballname)]+=int(row[7])
			else:
				ref[(batname,ballname)]=int(row[7])

	file1.close()

key_max = max(ref.iteritems(), key=operator.itemgetter(1))[0]


end=time.time()


print 'Max: ',key_max
print ref[key_max]
print('time: ',end-start)

