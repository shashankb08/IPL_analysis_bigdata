import sys
red_output = dict()
for line in sys.stdin:
    line=line.strip().split(":")
    temp_set = set(line[1])
    val_list = list(temp_set)
    red_output[line[0]] = sum(val_list)

key_max = max(red_output.iteritems(), key=operator.itemgetter(1))[0]

print 'Max: ',key_max
print red_output[key_max]