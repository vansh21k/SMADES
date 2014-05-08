import sys
from operator import itemgetter
print sys.argv
f = open(sys.argv[1], 'r' )

data = []
for line in f:
	data.append(line.split(','))
f.close()

data = sorted(data, key = itemgetter(0,1,2,3,-2,-1)) #source_ip, dest_ip, proto, timestamp ,source_port, dest_port
g = open (sys.argv[1], 'w')
for line in data:
	test = ','.join(line)
	g.write(test.strip()+ '\n')
g.close()
