import csv
import string
import random
t=["RCB","SRH"]
t1bat=['CH Gayle','V Kohli','AB de Villiers','SR Watson','SN Khan','KM Jadhav','STR Binny','AF Milne','YS Chahal','HV Patel','Parvez Rasool']
t2bat=['DA Warner','S Dhawan','MC Henriques','NV Ojha','DJ Hooda','EJG Morgan','A Ashish Reddy','KV Sharma','B Kumar','A Nehra','Mustafizur Rahman']
t1bowl=['AF Milne','SR Watson','AF Milne','Parvez Rasool','HV Patel','Parvez Rasool','HV Patel','YS Chahal','SR Watson','YS Chahal','AF Milne','YS Chahal','Parvez Rasool','YS Chahal','Parvez Rasool','SR Watson','HV Patel','AF Milne','HV Patel','SR Watson']
t2bowl=['A Nehra','B Kumar','Mustafizur','A Nehra','B Kumar','Mustafizur','MC Henriques','KV Sharma','MC Henriques','KV Sharma','MC Henriques','A Ashish Reddy','MC Henriques','KV Sharma','A Ashish Reddy','B Kumar','KV Sharma','Mustafizur','B Kumar','Mustafizur']
batsmen=['a','b']
batsmen[0]=t1bat[0]
batsmen[1]=t1bat[1]
meta={}
t1={}
t2={}
score=[0,0]
flag=0
wickets=[0,0]
out_prob={}
def out(x,o,b):
    if x[0] in out_prob.keys():
        out_prob[batsmen[0]]*=(1-float(meta[x][7]))
    else:
        out_prob[batsmen[0]]=1-float(meta[x][7])
    print("prob",out_prob[batsmen[0]],batsmen[0],x)
    if float(out_prob[batsmen[0]]) < 0.5:
        print("out")
        wickets[flag]+=1
        #print ("wicket",wickets[flag])
        if wickets[flag]==10:#all out
            
            return 1
        else:
            if flag==0:
                batsmen[0]=t1bat[wickets[flag]+1]
            else:
                batsmen[0]=t2bat[wickets[flag]+1]
    return 0

with open('/home/bsnova/Desktop/assignment/batc.csv') as File2:#bats men cluster (FORMAT: name,cluster)
    reader2 = csv.reader(File2)
    for row in reader2:
        t1[row[0]]=int(row[1])
File2.close()
with open('/home/bsnova/Desktop/assignment/bowlc.csv') as File3:#bowler men cluster (FORMAT: name,cluster)
    reader3 = csv.reader(File3)
    for row in reader3:
        t2[row[0]]=int(row[1])
File3.close()
#print (t2)
with open('/home/bsnova/Desktop/assignment/mstatf.csv') as csv_file:# probbility file(FORMAT: batsmen,bowler,cumu;ative prob of 0,.......,cumilative prob of 6, prob of wicket)
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        meta[(row[0],row[1])]=[row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]]
csv_file.close()
#print (meta)
for i in range(0,20):
    bowler=t2bowl[i]
    for j in range(0,6):
        x=(batsmen[0],bowler)
        #print (x)
        if x not in meta.keys() and batsmen[0] in t1.keys() and bowler not in t2.keys():
            x=(t1[batsmen[0]],bowler)
        elif x not in meta.keys() and bowler in t2.keys() and batsmen[0] not in t1.keys():
                x=(batsmen[0],t2[bowler])
        elif x not in meta.keys() and batsmen[0] in t1.keys() and bowler in t2.keys():
                x=(t1[batsmen[0]],t2[bowler])
        
        if x not in meta.keys():
            meta[x]=[random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()]

        r=out(x,i,j+1)
        if (r or (i==19 and j==5)):
            flag=1
            batsmen[0]=t2bat[0]
            batsmen[1]=t2bat[1]
            for m in range(0,20):
                    bowler=t1bowl[m]
                    for n in range(0,6):

                        x=(batsmen[0],bowler)
                        #print (x)
                        if x not in meta.keys() and batsmen[0] in t1.keys() and bowler not in t2.keys():
                            x=(t1[batsmen[0]],bowler)
                        elif x not in meta.keys() and bowler in t2.keys() and batsmen[0] not in t1.keys():
                                x=(batsmen[0],t2[bowler])
                        elif x not in meta.keys() and batsmen[0] in t1.keys() and bowler in t2.keys():
                                x=(t1[batsmen[0]],t2[bowler])
                        if x not in meta.keys():
                            meta[x]=[random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()]

                        r=out(x,m,n+1)
                        if (r or score[1]>score[0] or (m==19 and n==5)):
                            
                                print('team:', t[0])
                                print("Score\tWicket")
                                print(score[0],'\t',wickets[0])
                                print('team:', t[1])
                                print("Score\tWicket")
                                print(score[1],'\t',wickets[1])
                                if score[0]>score[1]:
                                    print (t[0]," won by :",(score[0]-score[1]))
                                elif score[0]<score[1]:
                                    print (t[1]," won by :",(score[1]-score[0]))
                                else:
                                    print ("Match Draw")
                                exit(0)
                            
                        else:
                            s=random.random()
                            if s>=float(meta[x][0]) and s<float(meta[x][1]):
                                pre=0
                            elif s>=float(meta[x][1]) and s<float(meta[x][2]):
                                pre=1
                            elif s>=float(meta[x][2]) and s<float(meta[x][3]):
                                pre=2
                            elif s>=float(meta[x][3]) and s<float(meta[x][4]):
                                pre=3
                            elif s>=float(meta[x][4]) and s<float(meta[x][5]):
                                pre=4
                            elif s>=float(meta[x][5]) and s<float(meta[x][6]):
                                pre=5
                            else:
                                pre=6
            
                            score[1]+=pre
                            print(m,n,pre,score[1],wickets[1])
                            #print ("s: ",s)
                            #print ("pre: ",pre)
                            #print ("score: ",score[0])
                            if pre%2!=0:
                                temp=batsmen[0]
                                batsmen[0]=batsmen[1]
                                batsmen[1]=temp
                    temp=batsmen[0]
                    batsmen[0]=batsmen[1]
                    batsmen[1]=temp

        else:
            s=random.random()
            if s>=float(meta[x][0]) and s<float(meta[x][1]):
                pre=0
            elif s>=float(meta[x][1]) and s<float(meta[x][2]):
                pre=1
            elif s>=float(meta[x][2]) and s<float(meta[x][3]):
                pre=2
            elif s>=float(meta[x][3]) and s<float(meta[x][4]):
                pre=3
            elif s>=float(meta[x][4]) and s<float(meta[x][5]):
                pre=4
            elif s>=float(meta[x][5]) and s<float(meta[x][6]):
                pre=5
            else:
                pre=6
            
            score[0]+=pre
            print(i,j,pre,score[0],wickets[0])
            #print ("s: ",s)
            #print ("pre: ",pre)
            #print ("score: ",score[0])
            if pre%2!=0:
                temp=batsmen[0]
                batsmen[0]=batsmen[1]
                batsmen[1]=temp
    temp=batsmen[0]
    batsmen[0]=batsmen[1]
    batsmen[1]=temp