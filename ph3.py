from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark import SparkConf,SparkContext
from numpy import array
import random
import csv
import math

place={"Delhi Daredevils":"Delhi","Gujarat Lions":"Rajkot","Kings XI Punjab":"Chandigarh","Deccan Chargers":"Hyderabad","Kochi Tuskers Kerala":"Kochi","Pune Warriors":"Pune","Kolkata Knight Riders":"Kolkata","Mumbai Indians":"Mumbai","Rising Pune Supergiants":"Pune","Rising Pune Supergiant":"Pune","Royal Challengers Bangalore":"Bangalore","Sunrisers Hyderabad":"Hyderabad","Chennai Super Kings":"Chennai","Rajasthan Royals":"Jaipur"}




t=['Chandigarh','Kings XI Punjab','Sunrisers Hyderabad']

bat1=['KL Rahul','CH Gayle','MA Agarwal','KK Nair','AJ Finch','Yuvraj Singh','R Ashwin','AJ Tye', 'BB Sran', 'MM Sharma', 'Mujeeb Ur Rahman']
bowl2=['B Kumar','CJ Jordan','B Kumar','CJ Jordan','Rashid Khan','S Kaul','DJ Hooda','Rashid Khan','DJ Hooda','Shakib Al Hasan','S Kaul','Shakib Al Hasan','CJ Jordan','Rashid Khan','S Kaul','B Kumar','CJ Jordan','B Kumar','S Kaul','Rashid Khan']
bat2=['WP Saha','S Dhawan','KS Williamson','YK Pathan','MK Pandey','DJ Hooda','Shakib Al Hasan','CJ Jordan', 'B Kumar', 'Rashid Khan', 'S Kaul']
bowl1=['BB Sran','MM Sharma','BB Sran','AJ Tye','MM Sharma','BB Sran','R Ashwin','Mujeeb Ur Rahman','R Ashwin','Mujeeb Ur Rahman','AJ Tye','Mujeeb Ur Rahman','MM Sharma','R Ashwin','AJ Tye','Mujeeb Ur Rahman','AJ Tye','BB Sran','MM Sharma','R Ashwin']



#q=[]

batsmen=[bat1[0],bat1[1]]  #batsmen currently playing
wicket=[0,0]   #number of wickets fall in each team.
score=[0,0] #score of each team

outprob={}

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



#PySpark
conf=SparkConf().setMaster("local").setAppName("SparkDecisionTree")
sc=SparkContext(conf=conf)
def createLabeledPoints1(fields):
	return LabeledPoint(fields[5],array([fields[0],fields[1],fields[2],fields[3],fields[4]]))
def createLabeledPoints2(fields):
	return LabeledPoint(fields[5],array([fields[0],fields[1],fields[2],fields[3],fields[4]]))
rawData1= sc.textFile("/home/bsnova/Desktop/assignment/ph3stat11.csv")
rawData2= sc.textFile("/home/bsnova/Desktop/assignment/ph3stat12.csv")
csvData1= rawData1.map(lambda x:x.split(","))
csvData2= rawData2.map(lambda x:x.split(","))

trainingData1= csvData1.map(createLabeledPoints1)
trainingData2= csvData2.map(createLabeledPoints2)
model1=DecisionTree.trainClassifier(trainingData1,numClasses=50,categoricalFeaturesInfo={},impurity='gini',maxDepth=10)
model2=DecisionTree.trainRegressor(trainingData2,categoricalFeaturesInfo={},impurity='variance',maxDepth=10)



#Out function which return 1 on all out of the team, and check is a batsmen id ou and if so new batsmen is replaced in FIFO manner
def out(tup,flag,i):
   #prediction part
   arr2=[array(tup)]
   testData2=sc.parallelize(arr2)
   predictions2=model2.predict(testData2)
   results2=predictions2.collect()
   if batsmen[0] in outprob.keys():
      outprob[batsmen[0]]=outprob[batsmen[0]]*(1-(float(results2[0])))
   elif float(results2[0])!=0:
      outprob[batsmen[0]]=(1-float(results2[0]))
   else:
      outprob[batsmen[0]]=1
   print("\n\n\n")
   print("out_pro",outprob[batsmen[0]],float(results2[0]))
   print("\n\n\n")
   #q.append(float(results2[0]))
   #if int(math.ceil(results2[0]*10))%2==0 :  #making the matsmen  out if the predicted number is even
   if outprob[batsmen[0]]<0.7 :
      wicket[flag]+=1
      if wicket[flag]<10 : #if all out
            batsmen[0]=batsmen[1]
            if flag==0:
               batsmen[1]=bat1[wicket[flag]+1]
            else:
               batsmen[1]=bat2[wicket[flag]+1]
            return 0
      else:
         return 1
   else:
      return 0

#score computation
def comp(fl,i):
   bowl='bowler'
   if fl==0:
      bowl=bowl2[i]
   else:
      bowl=bowl1[i]

   if int(batsmen[0] in t1.keys())==0:
		t1[batsmen[0]]=[0,random.randint(30,70)+random.random(),random.randint(140,150)+random.random()]
   if int(bowl in t2.keys())==0:
		t2[bowl]=[0,random.randint(40,50)+random.random(),random.randint(8,9)+random.random()]
   x=t1[batsmen[0]]
   z=t2[bowl]
   if place[t[fl+1]]==t[0] :
		k=1
   else:
		k=0
   tup=(x[1],x[2],k,z[1],z[2])
   r=out(tup,fl,i)
   if r!=1: #if not all out
      arr1=[array(tup)]
      testData1=sc.parallelize(arr1)
      predictions1=model1.predict(testData1)
      results1=predictions1.collect()
      score[fl]=score[fl]+int(math.ceil(results1[0]))
   if r==1 or i==19 :
      return 1

def print_out():
   print ( "\n\n\n\n\n\n\n\n\n\n\n\n\n")
   #print (model2.toDebugString())
   #print ( "\n\n\n\n")
   print ("team1:",t[1])
   print (score[0],'/',wicket[0])
   print ("team2:",t[2])
   print (score[1],'/',wicket[1])
   #print (q)
   


#over itration
for  i in range(0,20):
   c=comp(0,i)
   if c==1:
      print_out()
      for j in range(0,20):
         v=comp(1,j)
         if v==1:
           print_out()
           exit(0)   

'''
   if int(batsmen[0] in t1.keys())==0:
		t1[batsmen[0]]=[0,random.randint(30,70)+random.random(),random.randint(140,150)+random.random()]
   #if int(batsmen[1] in t1.keys())==0:
	#		t1[batsmen[1]]=[0,random.randint(30,70)+random.random(),random.randint(140,150)+random.random()]  
   if int(bowl2[i] in t2.keys())==0:
		t2[bowl2[i]]=[0,random.randint(40,50)+random.random(),random.randint(8,9)+random.random()]
   x=t1[batsmen[0]]
   #y=t1[batsmen[1]]
   z=t2[bowl2[i]]
   if place[t[flag+1]]==t[0] :
		k=1
   else:
		k=0
   tup=(x[1],x[2],k,z[1],z[2])

   r=out(tup,flag,i)
   if r!=1: #if not all out
      arr1=[array(tup)]
      testData1=sc.parallelize(arr1)
      predictions1=model1.predict(testData1)
      results1=predictions1.collect()
      score[flag]=score[flag]+int(math.ceil(results1[0]))
   if ((r==1) or (i==19)): #if all out or 20 overs completed
      for  j in range(0,20): #team 2 batting
         flag=1
         if place[t[flag+1]]==t[0] :
		      k=1
         else:
		      k=0
         batsmen=[bat2[0],bat2[1]]
         if int(batsmen[1] in t1.keys())==0:
		      t1[batsmen[1]]=[0,random.randint(30,70)+random.random(),random.randint(140,150)+random.random()]
         #if int(batsmen[1] in t1.keys())==0:
			#   t1[batsmen[1]]=[0,random.randint(30,70)+random.random(),random.randint(140,150)+random.random()] 
         if int(bowl1[j] in t2.keys())==0:
		      t2[bowl1[j]]=[0,random.randint(40,50)+random.random(),random.randint(8,9)+random.random()]
         x=t1[batsmen[0]]
         #y=t1[batsmen[1]]
         z=t2[bowl1[j]]
         tup=(x[1],x[2],k,z[1],z[2])
         r=out(tup,flag,j)
         if r!=1:
            arr1=[array(tup)]
            testData1=sc.parallelize(arr1)
            predictions1=model1.predict(testData1)
            results1=predictions1.collect()
            score[flag]=score[flag]+int(math.ceil(results1[0]))
         print ("\n\n\n")
         print results1,j
         print ("\n\n\n")
         if r==1 or j==19:
            print ( "\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print ("team1:",t[1])
            print (score[0],'/',wicket[0])
            print ("team2:",t[2])
            print (score[1],'/',wicket[1])
            print (q)
            exit(0)
'''

'''
   if batsmen[0] in outprob.keys():
      outprob[batsmen[0]]=outprob[batsmen[0]]*(float(results2[0]))
   elif float(results2[0])!=0:
      outprob[batsmen[0]]=float(results2[0])
   else:
      outprob[batsmen[0]]=1
   print("\n\n\n")
   print("out_pro",outprob[batsmen[0]],float(results2[0]))
   print("\n\n\n")
'''
'''
t=['Kolkata','Kolkata Knight Riders','Mumbai Indians']
bat1=['RV Uthappa','G Gambhir','MK Pandey','AD Russell','YK Pathan','C Munro','SA Yadav','PP Chawla','JW Hastings','Kuldeep Yadav','GB Hogg']

bowl2=['TG Southee','JJ Bumrah','TG Southee','MJ McClenaghan','TG Southee','MJ McClenaghan','HH Pandya','Harbhajan Singh','J Suchith','Harbhajan Singh','J Suchith','MJ McClenaghan','JJ Bumrah','Harbhajan Singh','TG Southee','Harbhajan Singh','JJ Bumrah','MJ McClenaghan','HH Pandya','JJ Bumrah']

bat2=['RG Sharma','PA Patel','HH Pandya','MJ McClenaghan','JC Buttler','KA Pollard','AT Rayudu','Harbhajan Singh','J Suchith','TG Southee','JJ Bumrah']

bowl1=['AD Russell','JW Hastings','AD Russell','GB Hogg','JW Hastings','GB Hogg','PP Chawla','Kuldeep Yadav','PP Chawla','Kuldeep Yadav','PP Chawla','Kuldeep Yadav','JW Hastings','Kuldeep Yadav','GB Hogg','AD Russell','GB Hogg','JW Hastings','AD Russell','PP Chawla']

t=['Hyderabad','Sunrisers Hyderabad','Kolkata Knight Riders']
bat1=['DA Warner','S Dhawan','MC Henriques','EJG Morgan','DJ Hooda','NV Ojha','A Ashish Reddy','KV Sharma','B Kumar','Mustafizur Rahman','BB Sran']

bowl2=['M Morkel','UT Yadav','M Morkel','UT Yadav','Shakib Al Hasan','UT Yadav','Shakib Al Hasan','AD Russell','SP Narine','AD Russell','SP Narine','AD Russell','SP Narine','PP Chawla','SP Narine','M Morkel','Shakib Al Hasan','M Morkel','UT Yadav','AD Russel']

bat2=['RV Uthappa','G Gambhir','MK Pandey','AD Russell','YK Pathan','Shakib Al Hasan','SA Yadav','PP Chawla','SP Narine','M Morkel','UT Yadav']

bowl1=['B Kumar','BB Sran','B Kumar','BB Sran','Mustafizur Rahman','BB Sran','KV Sharma','MC Henriques','B Kumar','MC Henriques','KV Sharma','Mustafizur Rahman','A Ashish Reddy','Mustafizur Rahman','A Ashish Reddy','BB Sran','B Kumar','Mustafizur Rahman','KV Sharma','MC Henriques']

t=['Hyderabad','Kolkata Knight Riders','Sunrisers Hyderabad']
bat2=['S Dhawan','SP Goswami','KS Williamson','MK Pandey','YK Pathan','CR Brathwaite','Shakib Al Hasan','Rashid Khan','B Kumar','S Kaul','Sandeep Sharma']

bowl1=['N Rana','M Prasidh Krishna','AD Russell','SP Narine','PP Chawla','SP Narine','Kuldeep Yadav','JPR Scantlebury-Searles','Kuldeep Yadav','PP Chawla','Kuldeep Yadav','SP Narine','JPR Scantlebury-Searles','Kuldeep Yadav','AD Russell','M Prasidh Krishna','SP Narine','M Prasidh Krishna','AD Russell','M Prasidh Krishna']

bat1=['CA Lynn','SP Narine','RV Uthappa','KD Karthik','AD Russell','N Rana','Shubman Gill','PP Chawla','JPR Scantlebury-Searles','Kuldeep Yadav','M Prasidh Krishna']

bowl2=['B Kumar','Sandeep Sharma','S Kaul','Shakib Al Hasan','B Kumar','S Kaul','Rashid Khan','CR Brathwaite','Rashid Khan','Shakib Al Hasan','Sandeep Sharma','Shakib Al Hasan','Rashid Khan','S Kaul','B Kumar','Rashid Khan','CR Brathwaite','S Kaul','B Kumar','CR Brathwaite']


t=['Mumbai','Mumbai Indians','Chennai Super Kings']
bat1=['RG Sharma','E Lewis','Ishan Kishan','SA Yadav','HH Pandya','KH Pandya','KA Pollard','JJ Bumrah','MJ McClenaghan','Mustafizur Rahman','M Markande']

bowl2=['DL Chahar','SR Watson','DL Chahar','SR Watson','DL Chahar','SR Watson','Harbhajan Singh','RA Jadeja','Harbhajan Singh','MA Wood','Imran Tahir','DJ Bravo','SR Watson','MA Wood','Imran Tahir','DJ Bravo','MA Wood','DJ Bravo','MA Wood','DJ Bravo']

bat2=['SR Watson','AT Rayudu','SK Raina','KM Jadhav','MS Dhoni','RA Jadeja','DJ Bravo','DL Chahar','Harbhajan Singh','MA Wood','Imran Tahir']

bowl1=['MJ McClenaghan','Mustafizur Rahman','JJ Bumrah','HH Pandya','MJ McClenaghan','HH Pandya','M Markande','JJ Bumrah','M Markande','HH Pandya','M Markande','Mustafizur Rahman','M Markande','Mustafizur Rahman','MJ McClenaghan','JJ Bumrah','HH Pandya','MJ McClenaghan','JJ Bumrah','Mustafizur Rahman']

'''