
import re
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
web_page= "http://stats.espncricinfo.com/indian-premier-league-2016/engine/records/averages/batting.html?id=11001;type=tournament"
page = urlopen(web_page)
soup = BeautifulSoup(page,"html.parser")
rows=soup.find_all('tr')
final=[]
rem=[]
head=['Player','Team','Mat','Inns','NO','Runs','HS','Ave','BF','SR','100','50','0','4s','6s']
team=['(Royal Challengers Bangalore)','(Delhi Daredevils)','(Mumbai Indians)','(Kolkata Knight Riders)','(Kings XI Punjab)','(Sunrisers Hyderabad)','(Gujarat Lions)','(Rising Pune Supergiants)']
prev=None
for row in rows:
	cols=row.find_all('td')
	cols=[x.text.strip() for x in cols]
	final.append(cols)
for i in final:
	if len(i)<14 and len(i)!=1:
		rem.append(i)
	if len(i)==1 and i[0] not in team:
		rem.append(i)
	if len(i)==1 and i[0] in team:
		s=str(i[0])	
		s=s[s.find("(")+1:s.find(")")]
		i[0]=s

for i in rem:
	final.remove(i)
for i in final:
	if len(i)>1:
		prev=i
	if len(i)==1:
		prev.insert(1,i[0])
for i in final:
	if len(i)<15:
		final.remove(i)
		
		
#for i in final:
#	if (str(i[9])=='-') :
#		print('0' , end= ' ')
#	else :
#		print(i[9] , end=' ')

with open('bat11.csv', 'w') as csvFile:
	writer = csv.writer(csvFile)
	#writer.writerow(head)
	for i in final:
		if(str(i[7])=='-'):
			i[7]='0'
		if(str(i[9])=='-'):
			i[9]='0'
		row=[i[7],i[9]]
		writer.writerow(row)
csvFile.close()

