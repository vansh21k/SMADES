'''Generates 5 tuple flows from sorted pcap files ##(srcip,destip,proto,timestamp,srcport,destport)'''
import sys
from operator import itemgetter
import time
from flow_util import *
global sample
global label
global n_max
global n_input_pcaps 
UDPTIMEOUT = 2000
TCPTIMEOUT = 2000

n_max = 0
clean_names  = ['p2pbox']
mal_names = ['zeus', 'waledac, gtisc-winobot']
print sys.argv[1]
#inp_file = open('flow_input.csv', 'r') 
inp_file = open(sys.argv[1], 'r')
#out_file = open('_output_flows','w')
out_file = open(sys.argv[1] + '_output_'+ str(UDPTIMEOUT)+'_flows','w')
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
n_input_pcaps = []
#out_file_udp = open('_output_flows_udp','w')
#out_file_tcp = open('_output_flows_tcp','w')
out_file_udp = open(sys.argv[1] + '_output_' + str(UDPTIMEOUT) +'_flows_udp','w')
out_file_tcp = open(sys.argv[1] + '_output_' + str(UDPTIMEOUT) +'_flows_tcp','w')
out_file_udp.close()
out_file_tcp.close()
def generateFlowAttributes(flow):
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

def getDestPackets(i, dest_ip, source_ip, dest_port, source_port,proto):
    global n_input_pcaps
    index = i + 1
    prev = []
    for index in range(i+1, len(n_input_pcaps)):
        prev = n_input_pcaps[index]
        if prev[2] != proto:
            continue
        if prev[0].strip() == dest_ip and prev[1].strip() == source_ip and prev[-3].strip() == dest_port and prev[-2].strip() == source_port and prev[-1] == 'unmarked':
            break #found first index
    curr = []
    data = []
    data.append(prev)
    for k in range(index, len(n_input_pcaps)):
        curr = n_input_pcaps[k]
        if curr[2] != proto or curr[-1] != 'unmarked':
            continue
        if prev[0].strip() == dest_ip and prev[1].strip() == source_ip and prev[-3].strip() == dest_port and prev[-2].strip() == source_port:
            pass
        else:
            return data 
        prev[-1] = 'marked'
        data.append(prev)
        prev = curr        
    return data

def generateUDPFlowsBi():
    '''To generate bi-directional udp flows'''
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
        if ((float(curr[3]) - float(prev[3])) <= UDPTIMEOUT):
            curr_flow.append(curr)
        else:
            if len(curr_flow) > 0:
                pass
            curr_flow = []
            curr_flow.append(curr)
        prev = curr
    flow_to_send = []
    for item in curr_flow:
        flow_to_send.append(item[0:-1])
    	#print flow_to_send[-1]
        #assert False
        
    #print flow_to_send
    #print '*******************************************************************************'
    generateFlowAttributes(flow_to_send)

def generateUDPFlowsUni():
    '''for unidirectional udp flows'''
    global sample
    global n_max
    if n_max < len(sample):
        n_max = len(sample)
    if sample == []:
        return []
    
def generateTCPFlowsUtil(index, sourceIp,destIp,sourcePort,destPort):
    ''' Valid flow generate helper, add code for timeseries evaluation as well'''
    global sample
    number_reconnects = 0
    valid_flow = []
    valid_flowAtoB = []
    valid_FlowBtoA = []
    reset_flag = 6 #Depends on the Tshark command
    syn_flag = 7
    fin_flag = 8 #not really reqd
    ack_flag = 9
    curr = []
    state  = 0
    valid_flow.append(sample[index])
    valid_flowAtoB.append(sample[index])
    for i in range(index + 1,len(sample)):
        curr = sample[i]
        '''if ((float(curr[3]) - float(sample[i-1][3])) <= TCPTIMEOUT):
            #print "special case encountered"
            break
        '''
        if curr[-1] == 'used':
            continue
        if state == 0 and curr[0] == destIp and curr[1] == sourceIp and curr[-3] == destPort and curr[-2] == sourcePort and curr[syn_flag] == '1' and curr[ack_flag] == '1': 
            state = 1
            valid_flow.append(curr)
            valid_FlowBtoA.append(curr)
        elif curr[reset_flag] == '1':
            number_reconnects = number_reconnects + 1
            if curr[0] == sourceIp:
                valid_flow.append(curr)
                valid_flowAtoB.append(curr)
            elif curr[0] == destIp:
                valid_flow.append(curr)
                valid_FlowBtoA.append(curr) 
        elif state == 1 and curr[0] == sourceIp and curr[1] == destIp and curr[-3] == sourcePort and curr[-2] == destPort and curr[ack_flag] == '1':
            state = 2
            valid_flow.append(curr)
            valid_flowAtoB.append(curr)
        elif state == 2 and curr[syn_flag]!=1:
            if curr[0] == sourceIp:
                valid_flow.append(curr)
                valid_flowAtoB.append(curr)
            elif curr[0] == destIp:
                valid_flow.append(curr)
                valid_FlowBtoA.append(curr)
        elif curr[syn_flag] == 1:
            break #Ungraceful exit    but we dont need to monitor exit stage since we distribute flag info to flows as well
        curr[-1] = 'used'
    '''TCP Flow'''        
    '''
    print "VALID FLOW"
    print  len(valid_flow)
    for line in valid_flow:
        print line
    
    print "VALID FLOWATOB"
    print len(valid_flowAtoB)
    for line in valid_flowAtoB:
        print line
    print "VALID FLOWBTOA"
    print len(valid_FlowBtoA)
    for line in valid_FlowBtoA:
        print line
    '''
    flow_to_send = []
    for item in valid_flow:
        curr = []
        curr = item[0:5]
        curr.append(item[-3])
        curr.append(item[-2])
        flow_to_send.append(curr)
  	#print '#####################################'
  	generateFlowAttributes(flow_to_send)
    return number_reconnects  #Number of reconnects no longer used
    
    
def generateTCPFlows():
    '''Validates TCP flows and Extracts attributes needed for further stages'''
    global sample
    global n_max
    reconnects = 0
    if n_max < len(sample):
        n_max = len(sample)
    if sample == []:
        return []
    #reset_flag = 6 #Depends on the Tshark command
    syn_flag = 7
    #fin_flag = 8
    ack_flag = 9
    for i in range(len(sample)):
        if sample[i][-1] == 'used':
            continue
        if sample[i][syn_flag] == '1' and sample[i][ack_flag] != '1':
            sample[i][-1] = 'used'
            #print "Here"
            reconnects = reconnects + generateTCPFlowsUtil(i , sample[i][0], sample[i][1], sample[i][-3], sample[i][-2])
    #print reconnects

for line in inp_file:
    #print line
    n_input_pcaps.append(line.strip().split(','))#.extend(['unmarked']))
    n_input_pcaps[-1].append('unmarked')
inp_file.close()

'''Generate UDP Flows'''

prev = []
sample = []
index = 0
for index in range(0,len(n_input_pcaps)):
    if n_input_pcaps[index][2] == '17':
        break
#print index
prev = n_input_pcaps[index]

for i in range(index + 1,len(n_input_pcaps)):
    curr = n_input_pcaps[i]
    if curr[2] != '17' or curr[-1] != 'unmarked':
        continue
    sample.append(prev)
    prev[-1] = 'marked'
    if prev[0].strip() == curr[0].strip() and prev[1].strip() == curr[1].strip() and prev[-3].strip() == curr[-3].strip() and prev[-2].strip() == curr[-2].strip():#and ((float(curr[3]) - float(prev[3])) <= UDPTIMEOUT):  #Fix for unidirectional and bidirectional flows
        pass
    else:
        #Time to generate a flow
        #Fix for Bidirecftional flows
        ext_sample = getDestPackets(i, prev[1].strip(), prev[0].strip(), prev[-2].strip(), prev[-3].strip(),prev[2].strip())
        if len(ext_sample[0]) > 0:
            sample.extend(ext_sample)
        sample = sorted(sample, key = itemgetter(3))
        generateUDPFlowsBi()
        sample = []
        
    prev = curr
sample.append(prev)
sample = sorted(sample, key = itemgetter(3))
generateUDPFlowsBi() #for last flow
'''Generate TCP Flows'''
prev = []
sample = []
index = 0
for index in range(0,len(n_input_pcaps)):
    if n_input_pcaps[index][2] == '6':
        break
#print index
prev = n_input_pcaps[index]
curr = []

for i in range(index + 1,len(n_input_pcaps)):
    curr = n_input_pcaps[i]
    if curr[2] != '6' or curr[-1] != 'unmarked':
        continue
    prev[-1] = 'marked'
    sample.append(prev)
    if prev[0].strip() == curr[0].strip() and prev[1].strip() == curr[1].strip() and prev[-3].strip() == curr[-3].strip() and prev[-2].strip() == curr[-2].strip():# and ((float(curr[3]) - float(prev[3])) <= TCPTIMEOUT):
        pass
    else:
        #Time to generate a flow
        ext_sample = getDestPackets(i, prev[1].strip(), prev[0].strip(), prev[-2].strip(), prev[-3].strip(),prev[2].strip())
        if len(ext_sample[0]) > 0:
            sample.extend(ext_sample)
        sample = sorted(sample, key = itemgetter(3))
        generateTCPFlows() #sort by timestamp to get flows
        sample = []
    prev = curr
sample.append(prev)
sample = sorted(sample, key = itemgetter(3))
generateTCPFlows() #for last flow
print n_max
