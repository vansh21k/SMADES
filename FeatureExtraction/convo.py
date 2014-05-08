'''Generates convos from pcap files ##(srcip,destip,proto,timestamp)'''
from operator import itemgetter
import time
from convo_util import *
global sample
global n_max
global n_input_pcaps 
global label
clean_names  = ['p2pbox']
mal_names = ['zeus', 'waledac, gtisc-winobot']
print sys.argv[1]
TIMEOUT = 2000  #standard timeout of 600ms
out_file = open(sys.argv[1] + '_output_'+ str(TIMEOUT)+'_convos','w')
out_file.close()
label = ''
for line in clean_names:
	if line in sys.argv[1]:
		label = line
for line in mal_names:
	if line in sys.argv[1]:
		label = line
if label == '':
	label = 'botnet'

n_max = 0
inp_file = open(sys.argv[1], 'r')
n_input_pcaps = []

def generateConvoAttributes(flow):
    '''Generates attributes for flow(SourceIp,DestIP,TimeStamp,Proto,packet_len,SourcePort, DestPort,reconnects)''' #Number of reconnects ommited
    try:
	if len(flow) < 2: #Ignoring flows with less than 2 packets
    		return 
    	getPacketLevelInfo(flow, label)
    except Exception:
	return

def getDistinctFlags():
    global n_input_pcaps
    n_set = set()
    for line in n_input_pcaps:
        if line[2] == '6':
            if line[7] == 1:
                print "Syn found"
            n_set.add(tuple(line[6:12]))
    print n_set

def getDestPackets(i, dest_ip, source_ip):
    global n_input_pcaps
    #print i, dest_ip, source_ip
    index = i + 1
    prev = []
    for index in range(i+1, len(n_input_pcaps)):
        prev = n_input_pcaps[index]
        if prev[0].strip() == dest_ip and prev[1].strip() == source_ip and prev[-1] == 'unmarked':
            break #found first index
    curr = []
    data = []
    data.append(prev)
    for k in range(index, len(n_input_pcaps)):
        curr = n_input_pcaps[k]
        if  curr[-1] != 'unmarked':
            continue
        if prev[0].strip() == dest_ip and prev[1].strip() == source_ip:
            pass
        else:
            return data 
        prev[-1] = 'marked'
        data.append(prev)
        prev = curr        
    return data

def generateConvos():
    global sample
    global n_max
    if n_max < len(sample):
        n_max = len(sample)
    if sample == []:
        return []
    curr_flow = []
    curr_flow.append(sample[0])
    i = 1
    for i in range(1, len(sample)):
        prev = sample[i-1]
        curr = sample[i]
        if ((float(curr[3]) - float(prev[3])) <= TIMEOUT):
            curr_flow.append(curr)
        else:
            if len(curr_flow) > 0:
                pass
                #out_file_udp.write(','.join(curr_flow[0]) + '\n')
            curr_flow = []
            curr_flow.append(curr)
        prev = curr
    flow_to_send = []
    for item in curr_flow:
        flow_to_send.append(item[0:-2])
    #print flow_to_send
    generateConvoAttributes(flow_to_send)


for line in inp_file:
    #print line
    n_input_pcaps.append(line.strip().split(','))#.extend(['unmarked']))
    n_input_pcaps[-1].append('unmarked')
inp_file.close()

#n_input_pcaps.sort(key = itemgetter(0,1,2))  #Not needed as files are already sorted

'''Generate Conversations'''

prev = []
sample = []
index = 0
prev = n_input_pcaps[index]
for i in range(index + 1,len(n_input_pcaps)):
    curr = n_input_pcaps[i]
    if curr[-1] != 'unmarked':
        continue
    sample.append(prev)
    prev[-1] = 'marked'
    if prev[0].strip() == curr[0].strip() and prev[1].strip() == curr[1].strip():#and ((float(curr[3]) - float(prev[3])) <= UDPTIMEOUT):  #Fix for unidirectional and bidirectional flows
        pass
    else:
        #Time to generate a convo
        #Fix for Bidirecftional bidirectional
        ext_sample = getDestPackets(i, prev[1].strip(), prev[0].strip())
        if len(ext_sample[0]) > 0:
            sample.extend(ext_sample)
        sample = sorted(sample, key = itemgetter(3))
        generateConvos()
        sample = []
        
    prev = curr
sample.append(prev)
sample = sorted(sample, key = itemgetter(3))
generateConvos() #for last flow
print n_max
