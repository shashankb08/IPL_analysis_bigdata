import csv
import numpy as np
arr=[]
team1="Royal Challengers Bangalore"
team2="Kolkata Knight Riders"
t1=[]
t2=[]
with open('/home/bsnova/Desktop/assignment/match.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        t1.append(row[1])
File.close() 
def test(x):
    for r in arr:
        if x==r[0]:
            return True
batc=[]
bowlc=[]
with open('/home/bsnova/Desktop/assignment/batc.csv') as File2:
    reader2 = csv.reader(File2)
    for row in reader2:
        t1=[row[0],row[1]]
        batc.append(t1)
File2.close()
with open('/home/bsnova/Desktop/assignment/bowlc.csv') as File3:
    reader3 = csv.reader(File3)
    for row in reader3:
        t2=[row[0],row[1]]
        bowlc.append(t2)
File3.close()
with open('/home/bsnova/Desktop/assignment/ipl.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if row[0] in t1 and row[1] in t1:
            x=(row[0],row[1])
            if  test(x):
                d=[(index, rowss.index(x)) for index, rowss in enumerate(arr) if x in rowss]
                #print d
                #print arr
                c=d[0][0]
                #print c
                arr[c][int(row[2])+1]+=1
                if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                    arr[c][8]+=1
           
            else:
                temp=[x,0,0,0,0,0,0,0,0]
                temp[int(row[2])+1]+=1
                if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                    temp[8]+=1
                arr.append(temp)
        for k in range(0,6):
            for l in range(0,6):
                
#print (arr)   
csv_file.close()
arr1=[]
with open('/home/bsnova/Desktop/assignment/mstat.csv', 'w') as File1:
        writer = csv.writer(File1)
        for r in arr:
            z=r[1]+r[2]+r[3]+r[4]+r[5]+r[6]+r[7]
            #temp=[r[0][0],r[0][1],"runs",r[1]/z,r[2]/z,r[3]/z,r[4]/z,r[5]/z,r[6]/z,r[7]/z]
            temp=[r[0][0],r[0][1],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8]]
            print(temp,z)
            #print("\n")
            arr1.append(temp)
            writer.writerow(temp)
File1.close()