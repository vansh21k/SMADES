''' Computes stats for malicious vs unknown flows based on no of packets and their payload size metrics'''
from operator import itemgetter
zues_input_file = '/media/san1/data_uga/vansh_temp/test/pcap_to_packets/zeus/zeus1-4.pcap.csv'
waledac_input_file = '/media/san1/data_uga/vansh_temp/test/pcap_to_packets/waledac/waledac.pcap.csv'
storm_input_file = '/media/san1/data_uga/vansh_temp/test/pcap_to_packets/storm/gtisc-winobot.20071027.1193508001.pcap.csv'
nugache_input_file = '/media/san1/data_uga/vansh_temp/test/pcap_to_packets/nugache/all.csv'

zues_black_list = {'10.0.2.15':'bot'}
storm_black_list = {'66.154.80.101':'bot','66.154.80.105':'bot','66.154.80.111':'bot','66.154.80.125':'bot', '66.154.83.80': 'bot','66.154.83.107':'bot','66.154.83.113':'bot','66.154.83.138':'bot', '66.154.87.39':'bot', '66.154.87.41':'bot','66.154.87.57':'bot','66.154.87.58':'bot','66.154.87.61':'bot'}
waledac_black_list = {'192.168.58.136':'bot', '192.168.58.137':'bot', '192.168.58.150':'bot'}
nugache_black_list = {'68.198.41.207':'bot','69.168.20.2':'bot', '69.168.20.3':'bot', '69.168.20.4':'bot'}
control_matrix = [[zues_input_file, zues_black_list], [waledac_input_file, waledac_black_list], [storm_input_file, storm_black_list],[nugache_input_file, nugache_black_list]]
names = ['ZUES', 'WALEDAC', 'STORM', 'NUGACHE']
for i in range(len(control_matrix)):
    total_malicious_payload = 0.0
    total_unknown_payload = 0.0
    total_malicious_packets = 0.0
    total_unknown_packets = 0.0
    total_malicious_udp = 0.0 
    total_malicious_tcp = 0.0 
    dict_endpoints = {}
    dict_flows_tcp = {}
    dict_flows_udp = {}
    dict_super_flows = {}
    temp_list_flows_udp =[]
    temp_list_flows_tcp = []
    temp_list_flows = []
    temp_list_superflows = []
    temp_list_endpoints = []
    display_count = 20 
    total_tcp = 0.0
    total_udp = 0.0
    f = open(control_matrix[i][0], 'r')
    for line in f:
        line = line.strip().split(',')
        temp_key_ip = ()
        temp_key_port = () 
        temp_key_flow = ()
        if line[0] < line[1]:
            temp_key_ip = (line[0], line[1])
        else:
            temp_key_ip = (line[1], line[0])
        if line[-2] < line[-1]:
            temp_key_port = (line[-2], line[-1])
        else:
            temp_key_port = (line[-1], line[-2])
        temp_key_flow = temp_key_ip + temp_key_port
        if line[0] in dict_endpoints:
            dict_endpoints[line[0]][0] = dict_endpoints[line[0]][0] + 1
            dict_endpoints[line[0]][1] = dict_endpoints[line[0]][1] + float(line[4])
        else:
            dict_endpoints[line[0]] = [1, float(line[4])]
        if temp_key_ip in dict_super_flows:
            dict_super_flows[temp_key_ip][0] = dict_super_flows[temp_key_ip][0] + 1
            dict_super_flows[temp_key_ip][1] = dict_super_flows[temp_key_ip][0] + float(line[4])
        else:
            dict_super_flows[temp_key_ip] = [1, float(line[4])]
        if line[2] == '17': #UDP FLOW
            total_udp = total_udp + 1
            if (line[0] in control_matrix[i][1]) or (line[1] in control_matrix[i][1]):
                total_malicious_udp = total_malicious_udp + 1
                total_malicious_packets = total_malicious_packets + 1
                total_malicious_payload = total_malicious_payload + float(line[4])     
            else:
                total_unknown_packets = total_unknown_packets + 1
                total_unknown_payload = total_unknown_payload + float(line[4])
            if temp_key_flow in dict_flows_udp:
                dict_flows_udp[temp_key_flow][0] = dict_flows_udp[temp_key_flow][0] + 1
                dict_flows_udp[temp_key_flow][1] = dict_flows_udp[temp_key_flow][1] + float(line[4])
            else: 
                dict_flows_udp[temp_key_flow] = [1, float(line[4])]
        else:
            total_tcp = total_tcp + 1
            if (line[0] in control_matrix[i][1]) or (line[1] in control_matrix[i][1]):
                total_malicious_tcp = total_malicious_tcp + 1
                total_malicious_packets = total_malicious_packets + 1
                total_malicious_payload = total_malicious_payload + float(line[4])
            else:
                total_unknown_packets = total_unknown_packets + 1
                total_unknown_payload = total_unknown_payload + float(line[4])
            if temp_key_flow in dict_flows_tcp:
                dict_flows_tcp[temp_key_flow][0] = dict_flows_tcp[temp_key_flow][0] + 1
                dict_flows_tcp[temp_key_flow][1] = dict_flows_tcp[temp_key_flow][1] + float(line[4])
            else: 
                dict_flows_tcp[temp_key_flow] = [1, float(line[4])]
    for index in dict_endpoints:
            temp_list_endpoints.append([index, dict_endpoints[index][0],dict_endpoints[index][1]])
    for index in dict_flows_tcp:
            temp_list_flows_tcp.append([index, dict_flows_tcp[index][0],dict_flows_tcp[index][1]])
            temp_list_flows.append([index, dict_flows_tcp[index][0],dict_flows_tcp[index][1]])
    for index in dict_flows_udp:
            temp_list_flows_udp.append([index, dict_flows_udp[index][0],dict_flows_udp[index][1]])
            temp_list_flows.append([index, dict_flows_udp[index][0],dict_flows_udp[index][1]])
    for index in dict_super_flows:
            temp_list_superflows.append([index, dict_super_flows[index][0],dict_super_flows[index][1]])
        ##Sorting based on packet lengths and then on number of packets
    temp_list_endpoints = sorted(temp_list_endpoints, key = itemgetter(2,1), reverse=True)
    temp_list_flows = sorted(temp_list_flows, key = itemgetter(2,1), reverse=True)
    temp_list_flows_tcp = sorted(temp_list_flows_tcp, key = itemgetter(2,1), reverse=True)
    temp_list_flows_udp = sorted(temp_list_flows_udp, key = itemgetter(2,1), reverse=True)
    temp_list_superflows = sorted(temp_list_superflows, key = itemgetter(2,1), reverse=True)
    print "Analysis for ", names[i]
    print '%age malicious packets', ((total_malicious_packets/ (total_unknown_packets + total_malicious_packets)) * 100)
    print '%age malicious payload' ,((total_malicious_payload/(total_unknown_payload + total_malicious_payload)) * 100)
    print '%age TCP packets' , (100 *(total_tcp/(total_tcp + total_udp)))
    print '%age UDP packets', (100 *(total_udp/(total_tcp + total_udp)))
    print '%age Malicious TCP in TCP',(100 * (total_malicious_tcp/ (total_tcp)))
    print '%age Malicious UDP in UDP',(100 * (total_malicious_udp/ (total_udp))) 
    print '%age UDP Malicious out of Malicious Packets', ((total_malicious_udp/total_malicious_packets) * 100)
    print '%age TCP Malicious out of Malicious Packets', ((total_malicious_tcp/total_malicious_packets) * 100)
    print 'Top Endpoints'
    it = 1
    for index in temp_list_endpoints:
            if index[0] in control_matrix[i][1]:
                print index, 'MALICIOUS',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            else:
                print index, 'UNKNOWN',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            if it == display_count:
                break
            it = it + 1               
            
    print "Top Conversations"
    it = 1
    for index in temp_list_superflows:
            if index[0][0] in control_matrix[i][1] or index[0][1] in control_matrix[i][1]:
                print index, 'MALICIOUS',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            else:
                print index, 'UNKNOWN',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            if it == display_count:
                break
            it = it + 1               
            
    print 'Top Flows UDP'
    it = 1
    for index in temp_list_flows_udp:
            if index[0][0] in control_matrix[i][1] or index[0][1] in control_matrix[i][1]:
                print index, 'MALICIOUS',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            else:
                print index, 'UNKNOWN',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            if it == display_count:
                break
            it = it + 1               
            
    print 'Top Flows TCP'
    it = 1
    for index in temp_list_flows_tcp:
            if index[0][0] in control_matrix[i][1] or index[0][1] in control_matrix[i][1]:
                print index, 'MALICIOUS',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            else:
                print index, 'UNKNOWN',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            if it == display_count:
                break
            it = it + 1               
            
    print 'Top Flows Overall'
    it = 1
    for index in temp_list_flows:
            if index[0][0] in control_matrix[i][1] or index[0][1] in control_matrix[i][1]:
                print index, 'MALICIOUS', str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            else:
                print index, 'UNKNOWN',str(100*(index[-1]/(total_malicious_payload + total_unknown_payload)))
            if it == display_count:
                break
            it = it + 1               
    print "****************************************************************************"
    f.close()
    
