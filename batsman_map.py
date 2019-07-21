import sys
output = dict()
for line in sys.stdin:
    line = line.strip().split(",")
    if line[9] in ['caught','bowled','run out','lbw','caught and bowled']:
        if (line[4],line[6]) in output.keys():
				output[(line[4],line[6])].append('1')
        else:
				output[(line[4],line[6])] = ['1']

for key, value in output.iteritems() :
    print key, value
