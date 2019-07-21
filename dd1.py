import csv 
import glob
import os
import operator
import time
import random
import math

t1={}
with open('/home/bsnova/Desktop/assignment/batc.csv') as File2:
    reader2 = csv.reader(File2)
    for row in reader2:
        t1[row[0]]=[int(row[1]),float(row[2]),float(row[3])]
File2.close()

t2={}
with open('/home/bsnova/Desktop/assignment/bowlc.csv') as File3:
    reader3 = csv.reader(File3)
    for row in reader3:
        t2[row[0]]=[int(row[1]),float(row[2]),float(row[3])]
File3.close()


place={"Delhi Daredevils":"Delhi","Gujarat Lions":"Rajkot","Kings XI Punjab":"Chandigarh","Deccan Chargers":"Hyderabad","Kochi Tuskers Kerala":"Kochi","Pune Warriors":"Pune","Kolkata Knight Riders":"Kolkata","Mumbai Indians":"Mumbai","Rising Pune Supergiants":"Pune","Rising Pune Supergiant":"Pune","Royal Challengers Bangalore":"Bangalore","Sunrisers Hyderabad":"Hyderabad","Chennai Super Kings":"Chennai","Rajasthan Royals":"Jaipur"}

path = ('/home/bsnova/Desktop/assignment/ipl/*.csv')
files = glob.glob(path)
ref={}

for name in files:
	file1=open(name)
	reader=csv.reader(file1)
	prev=prev1=('a')
	for row in reader:
			
		if(row[0]=='info' and row[1]=='city'):
				city=row[2]

		if(row[0]!='info' and row[0]!='version'):
    			

			#print (row[3],place[row[3]])
			if place[row[3]]==city :
				i=1
			else:
				i=0
			if int(row[4] in t1.keys())==0:
				t1[row[4]]=[0,random.randint(30,70)+random.random(),random.randint(140,150)+random.random()]

			if int(row[6] in t2.keys())==0:
				t2[row[6]]=[0,random.randint(40,50)+random.random(),random.randint(8,9)+random.random()]

			x=t1[row[4]]
			z=t2[row[6]]
			
			tup=(x[1],x[2],i,z[1],z[2])
			if tup in ref.keys():
					temp=ref[tup]
					temp[0]+=int(row[7])
					if(row[9]=='caught' or row[9]=='bowled' or row[9]=='run out' or row[9]=='lbw' or row[9]=="caught and bowled"):
						temp[1]+=1
					temp[2]+=1
					ref[tup]=temp
			
			else:
					temp=[int(row[7]),0,1]
					if(row[9]=='caught' or row[9]=='bowled' or row[9]=='run out' or row[9]=='lbw' or row[9]=="caught and bowled"):
						temp[1]+=1
					ref[tup]=temp
		
		
	file1.close()



for  key, value in ref.items():
	print (key,value)
with open('/home/bsnova/Desktop/assignment/ph3stat11.csv', 'w') as File11:
        writer = csv.writer(File11)
        for key, value in ref.items():
            new_value=(value[0]/value[2])*6
            #new_value[1]=(value[1]/value[2])*(value[1]/value[2])*(value[1]/value[2])
            temp=[key[0],key[1],key[2],key[3],key[4],new_value]
            writer.writerow(temp)
File11.close()

with open('/home/bsnova/Desktop/assignment/ph3stat12.csv', 'w') as File12:
        writer = csv.writer(File12)
        for key, value in ref.items():
            
            #new_value[0]=(value[0]/value[2])*6
            new_value=(value[1]/value[2])*6
            temp=[key[0],key[1],key[2],key[3],key[4],new_value]
            writer.writerow(temp)
File12.close()
'''
for key, value in ref.items():
			new_value=[value[0]/value[2],value[1]/value[2],value[2],value[3]]
			temp1=[key[0],key[1],key[2],key[3],key[4],key[5],key[6],new_value[0],new_value[1]]
			writer.writerow(temp1)
			temp2=[key[2],key[3],key[0],key[1],key[4],key[5],key[6],new_value[0],new_value[1]]
			#writer.writerow(temp2)
		'''