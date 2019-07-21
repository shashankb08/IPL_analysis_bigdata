import csv 
import glob
import os



count=1
path = ('/home/bsnova/Desktop/assignment/ipl/*.csv')
files = glob.glob(path)


#Listing all the bowlers who took out respective batsmen and storing them in file
for name in files:
 file1 = open(name)
 reader = csv.reader(file1)
 
 for row in reader:
  if(row[0]=='info' or row[0]=='version'):
    reader.next()
  elif(row[9]=='caught' or row[9]=='bowled' or row[9]=='run out'):
	name=row[4]	
	if(row[4]=='V Kohli'):
	 count=count+1
	filename="%s.txt"%name   
	f=open(filename,'a')
	f.write(row[6]+"\n")  
	print ("batsmen:"+row[4]+"    bowler :"+row[6])
 	f.close()
 file1.close()
 
print count


#Finding the batsmen's weakness
path = ('/home/bsnova/Desktop/assignment/*.txt')
files = glob.glob(path)

for name in files:

 file2=open(name,"r+")

 wordcount={}

 for word in file2.read().splitlines():
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1
 maxs=-1
 for k,v in wordcount.items():
    if(v>maxs):
     maxs=v
     key =k
 file2.close()
 base=(os.path.basename(name))
 print "batsmen: "+os.path.splitext(base)[0],";\tweakness: ",key, "\tno of times wicket(s) taken: ",maxs




