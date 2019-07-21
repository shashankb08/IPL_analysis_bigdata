import csv
import numpy as np
arr={}
t1={}
t2={}

with open('/home/bsnova/Desktop/assignment/batc.csv') as File2:
    reader2 = csv.reader(File2)
    for row in reader2:
        t1[row[0]]=int(row[1])
File2.close()
with open('/home/bsnova/Desktop/assignment/bowlc.csv') as File3:
    reader3 = csv.reader(File3)
    for row in reader3:
        t2[row[0]]=int(row[1])
File3.close()
with open('/home/bsnova/Desktop/assignment/ipl.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if row[0] in t1.keys():
            c1=t1[row[0]]
            if row[1] in t2.keys():
                
                c2=t2[row[1]]
                y=(c1,c2)
                if y in arr.keys():
                    arr[y][int(row[2])]+=1
                    if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                        arr[y][7]+=1
               
                else:
                    temp=[0,0,0,0,0,0,0,0]
                    temp[int(row[2])]+=1
                    if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                        temp[7]+=1
                    arr[y]=temp
            else:
                y=(c1,row[1])
                if y in arr.keys():
                    arr[y][int(row[2])]+=1
                    if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                        arr[y][7]+=1
               
                else:
                    temp=[0,0,0,0,0,0,0,0]
                    temp[int(row[2])]+=1
                    if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                        temp[7]+=1
                    arr[y]=temp
        if row[0] not in t1.keys():
            if row[1] in t2.keys():
                c2=t2[row[1]]
                y=(row[0],c2)
                if y in arr.keys():
                    arr[y][int(row[2])]+=1
                    if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                        arr[y][7]+=1
               
                else:
                    temp=[0,0,0,0,0,0,0,0]
                    temp[int(row[2])]+=1
                    if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                        temp[7]+=1
                    arr[y]=temp
        
        x=(row[0],row[1])
        if x in arr.keys():
            arr[x][int(row[2])]+=1
            if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                arr[x][7]+=1
               
        else:
            temp=[0,0,0,0,0,0,0,0]
            temp[int(row[2])]+=1
            if(row[3]=='caught' or row[3]=='bowled' or row[3]=='run out' or row[3]=='lbw' or row[3]=="caught and bowled"):
                temp[7]+=1
            arr[x]=temp
                  
csv_file.close()
with open('/home/bsnova/Desktop/assignment/mstatf.csv', 'w') as File1:
        writer = csv.writer(File1)
        for key, value in arr.items():
            z=value[0]+value[1]+value[2]+value[3]+value[4]+value[5]+value[6]
            new_value=[x / z for x in value]
            for i in range(1,7):
                new_value[i]+=new_value[i-1]
            print (key,new_value)
            temp=[key[0],key[1],new_value[0],new_value[1],new_value[2],new_value[3],new_value[4],new_value[5],new_value[6],new_value[7]]
            writer.writerow(temp)
File1.close()