import csv
import os
import glob
import time
import operator
start=time.time()
path = ('/home/bsnova/Desktop/assignment/*.csv')
files = glob.glob(path)
bowl={}
for name in files:
	file1 = open(name)
	reader = csv.reader(file1)
	for row in reader:
		if(row[0]=='info' or row[0]=='version'):
			reader.next()
		else:
			batname=row[4]
			ballname=row[6]			
			if (row[6],row[4]) in bowl.keys():     
				bowl[(row[6],row[4])]+=1
    			else:   
				bowl[(row[6],row[4])]=1

	file1.close()
 

key_max = max(bowl.iteritems(), key=operator.itemgetter(1))[0]
#list1=sorted(bowlers.items(),key=lambda x:x[1],reverse=True)


end= time.time();
print 'Max: ',key_max
print bowl[key_max]
print('time: ',end-start)

