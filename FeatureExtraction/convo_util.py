from math import log
from math import sqrt
from numpy.fft import fft
from numpy import array
import numpy
import sys
from operator import itemgetter
TIME_OUT = '2000'
def get_prime_wave(a, b):
	n_real = float(sum(a))
	n_complex = float(sum(b))
	deg = 0.0
	if n_real == 0.0:
		if n_complex > 0:
			deg = 90.0	
		elif n_complex < 0:
			deg = -90.0	
		else:
			deg = 0.0		
	else:
		deg = numpy.degrees(numpy.arctan(n_complex/ n_real))
	magnitude =  (n_real * n_real) + (n_complex * n_complex)
	return sqrt(magnitude), deg 

def print_fft(sample):
    to_print = ''
    for item in sample[2]:
        if type(item)!=list:
            continue
        to_print = to_print  + '\t' +  str(item[1]) + '\t' + str(item[2]) #+ str(item[0]) + '\t'
    return (str(sample[0]) + '\t' + str(sample[1]) + '\t' + to_print.strip('\t') + '\t' + str(sample[5]) + '\t' + str(sample[-1]))

def remove_values_from_list(the_list):
   return [value for value in the_list if value != 0.0]

def avg_list(sample):
    c_sum = 0.0 
    if len(sample) < 1:
        return 0.0
    for item in sample:
        c_sum = c_sum + item
    return c_sum / len(sample)

def fft_payload_interpolate(x, y):
    net_magnitude = 0.0 
    net_phase = 0.0
    complex_list = []
    real_list = []
    magnitude_list = []
    if len(y) < 1:
        temp = [ [0.0,0.0,0.0]  for x in range(10)]
        real_list = [0.0 for x in range(11)]
        complex_list = [0.0 for x in range(11)]
        return [0.0, 0.0, temp, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    start, end = x[0], x[-1]
    step = 0.001
    temp = []
    i = start
    while(i < end):
        temp.append(numpy.interp(i, x, y))
        i = i + step
    temp.append(numpy.interp(i, x, y))
    a = array(tuple(temp))
    test= fft(a)
    
    temp = []
    for item in test:
	if item.real == 0.0 and item.imag > 0:
		temp.append([item, numpy.abs(item), 90.0])        
	elif item.real == 0.0 and item.imag < 0:
		temp.append([item, numpy.abs(item), -90.0])	
	else:
		temp.append([item, numpy.abs(item), numpy.degrees(numpy.arctan(item.imag/item.real))])
    temp.sort(key = itemgetter(1), reverse = True)
    for item in temp:
        real_list.append(item[0].real)
        complex_list.append(item[0].imag)
        magnitude_list.append(item[1])
    net_magnitude, net_phase = get_prime_wave(real_list, complex_list)
    avg_real = 0.0 #avg_list(real_list)
    avg_complex = 0.0 # avg_list(complex_list)
    avg_magnitude = avg_list(magnitude_list)
    med_real = 0.0 #get_median(real_list)
    med_complex =0.0# get_median(complex_list)
    med_magnitude = get_median(magnitude_list)
    
    if len(temp) < 10:
        while(len(temp) < 10):
            temp.append([0.0,0.0,0.0])
            real_list.append(0.0)
            complex_list.append(0.0)
        return [net_magnitude, net_phase, temp, avg_real, avg_complex, avg_magnitude, med_real, med_complex, med_magnitude]
    else:
        return [net_magnitude, net_phase,temp[0:10], avg_real, avg_complex, avg_magnitude, med_real, med_complex, med_magnitude]


def fft_payload(y):
    net_magnitude = 0.0 
    net_phase = 0.0
    complex_list = []
    real_list = []
    magnitude_list = []
    if len(y) < 1:
        temp = [ [0.0,0.0,0.0]  for x in range(10)]
        real_list = [0.0 for x in range(11)]
        complex_list = [0.0 for x in range(11)]
	net_magnitude, net_phase = 0.0, 0.0 #get_prime_wave(real_list, complex_list)        
	return [0.0, 0.0, temp, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    a = array(tuple(y))
    test= fft(a)
    temp = []
    for item in test:
	if item.real == 0.0 and item.imag > 0:
		temp.append([item, numpy.abs(item), 90.0])        
	elif item.real == 0.0 and item.imag < 0:
		temp.append([item, numpy.abs(item), -90.0])	
	else:
		temp.append([item, numpy.abs(item), numpy.degrees(numpy.arctan(item.imag/item.real))])
    temp.sort(key = itemgetter(1), reverse = True)
    for item in temp:
        real_list.append(item[0].real)
        complex_list.append(item[0].imag)
        magnitude_list.append(item[1])
    net_magnitude, net_phase = get_prime_wave(real_list, complex_list)
    avg_real = 0.0 #avg_list(real_list)
    avg_complex = 0.0 # avg_list(complex_list)
    avg_magnitude = avg_list(magnitude_list)
    med_real = 0.0 #get_median(real_list)
    med_complex =0.0# get_median(complex_list)
    med_magnitude = get_median(magnitude_list)
    if len(temp) < 10:
        while(len(temp) < 10):
            temp.append([0.0,0.0,0.0])
            real_list.append(0.0)
            complex_list.append(0.0)
        return [net_magnitude, net_phase, temp, avg_real, avg_complex, avg_magnitude, med_real, med_complex, med_magnitude]
    else:
        return [net_magnitude, net_phase,temp[0:10], avg_real, avg_complex, avg_magnitude, med_real, med_complex, med_magnitude]

def fft_interarrival(y):
    net_magnitude = 0.0 
    net_phase = 0.0
    complex_list = []
    real_list = []
    magnitude_list = []
    if len(y) < 1:
        temp = [ [0.0,0.0,0.0]  for x in range(10)]
        real_list = [0.0 for x in range(11)]
        complex_list = [0.0 for x in range(11)]
        return [0.0, 0.0, temp, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    a = array(tuple(y))
    test= fft(a)
    temp = []
    for item in test:
	if item.real == 0.0 and item.imag > 0:
		temp.append([item, numpy.abs(item), 90.0])        
	elif item.real == 0.0 and item.imag < 0:
		temp.append([item, numpy.abs(item), -90.0])	
	else:
		temp.append([item, numpy.abs(item), numpy.degrees(numpy.arctan(item.imag/item.real))])
    temp.sort(key = itemgetter(1), reverse = True)
    for item in temp:
        real_list.append(item[0].real)
        complex_list.append(item[0].imag)
        magnitude_list.append(item[1])
    net_magnitude, net_phase = get_prime_wave(real_list, complex_list)
    avg_real = 0.0 #avg_list(real_list)
    avg_complex = 0.0 # avg_list(complex_list)
    avg_magnitude = avg_list(magnitude_list)
    med_real = 0.0 #get_median(real_list)
    med_complex =0.0# get_median(complex_list)
    med_magnitude = get_median(magnitude_list)
    
    if len(temp) < 10:
        while(len(temp) < 10):
            temp.append([0.0,0.0,0.0])
            real_list.append(0.0)
            complex_list.append(0.0)
        return [net_magnitude, net_phase, temp, avg_real, avg_complex, avg_magnitude, med_real, med_complex, med_magnitude]
    else:
        return [net_magnitude, net_phase,temp[0:10], avg_real, avg_complex, avg_magnitude, med_real, med_complex, med_magnitude]


def variance(average, values):
    varience = sum((average - value) ** 2 for value in values) / len(values)
    return varience

def get_median(sample):
    if len(sample) < 1:
        return 0.0
    sample.sort()

    if len(sample) == 2:
        return (sample[0] + sample[1]) / 2
    if sample == []:
        return 0.0
    n = len(sample)
    if n % 2 == 1:
        return sample[n/2]
    else:
        return float(sample[n/2] + sample[ n/2 + 1]) /2.0
     
def huffman_word(sample):
    payload_count = {}
    #print sample
    total = 0.0
    for item in sample:
        total = total + 1.0
        if item in payload_count.keys():
            payload_count[item] = payload_count[item] + 1.0
        else: 
            payload_count[item] = 1.0
    compressed_size = 0.0
    for item in payload_count:
        payload_count[item] = payload_count[item] / total
        compressed_size = compressed_size + ( -1 * payload_count[item] * log(payload_count[item], 2)) 
    compressed_size = (compressed_size * total) + len(payload_count.keys())
    #print ((16.0 * total)/ compressed_size) 
    return ((16.0 * total)/ compressed_size)


def first_packet_size(flow):
    for item in flow:
        if float(item[4]) > 0:
            return float(item[4])
    return 0.0

def max_packet_size(flow):
    c_max = 0.0
    for item in flow:
        if float(item[4]) > c_max:
            c_max = float(item[4])
    return c_max


def getPacketLevelInfo(flow, label):
    #out_file = open('_output_flows','a')
    out_file = open(sys.argv[1] + '_output_' + TIME_OUT + '_convos','a')
    #out_file_udp = open('_output_flows_udp','a')
    #out_file_tcp = open('_output_flows_tcp','a')
    #out_file_udp = open(sys.argv[1] + '_output_convos_udp','a')
    #out_file_tcp = open(sys.argv[1] + '_output_convos_tcp','a')


    fps = first_packet_size(flow)
    mps = max_packet_size(flow)
    source = flow[0][0]
    dest = flow[0][1]
    inter_arrival_sent = []
    inter_arrival_recv = []
    inter_arrival_total = []
    packets_sent = 0.0
    packets_received = 0.0
    inter_total = 0.0
    inter_sent = 0.0
    inter_recv = 0.0
    sending_time = 0.0
    receiving_time = 0.0
    last_sent_time = 0.0
    last_recv_time = 0.0
    t_payload = []
    s_payload = []
    r_payload = []
    variance_total = 0.0
    variance_sent = 0.0
    variance_recv = 0.0
    avg_payload = 0.0
    avg_sent = 0.0
    avg_received = 0.0
    time_start = float(flow[0][3])
    time_end = float(flow[-1][3])
    time_stamps = []
    flow_duration = time_end - time_start
    total_packets = 0.0
    s_flag = 0
    r_flag = 0
    zero_packets_sent = 0
    zero_packets_recv = 0
    for item in flow:
        time_stamps.append(float(item[3]) - time_start)
        if item[0] == source:
            if s_flag == 0:
                s_flag = 1
                last_sent_time = float(item[3])
            else:
                inter_arrival_sent.append(float(item[3]) - last_sent_time)
                inter_arrival_total.append(float(item[3]) - last_sent_time)
                sending_time = sending_time + float(item[3]) - last_sent_time
                last_sent_time = float(item[3])
            packets_sent = packets_sent + 1
            if float(item[4]) == 0.0:
                zero_packets_sent = zero_packets_sent + 1
            t_payload.append(float(item[4]))
            s_payload.append(float(item[4]))
        else:
            if r_flag == 0:
                r_flag = 1
                last_recv_time = float(item[3])
            else:
                inter_arrival_recv.append(float(item[3]) - last_recv_time)
                inter_arrival_total.append(float(item[3]) - last_recv_time)
                receiving_time = receiving_time +  float(item[3]) - last_recv_time
                last_recv_time = float(item[3])
            packets_received = packets_received + 1
            if float(item[4]) == 0.0:
                zero_packets_recv = zero_packets_recv + 1
            t_payload.append(float(item[4]))
            r_payload.append(float(item[4]))
    total_packets = packets_sent + packets_received 
    if (total_packets - zero_packets_sent - zero_packets_recv) > 0:
        avg_payload = sum(t_payload)/(total_packets - zero_packets_sent - zero_packets_recv)
        variance_total = variance(avg_payload, remove_values_from_list(t_payload))
    if total_packets > 0:
        inter_total = (sending_time + receiving_time) / total_packets
    
    if (packets_sent - zero_packets_sent)> 0:
        avg_sent = sum(s_payload)/(packets_sent - zero_packets_sent)
        variance_sent = variance(avg_sent, remove_values_from_list(s_payload))
    if packets_sent > 0:
        inter_sent = sending_time / packets_sent
    
    if (packets_received - zero_packets_recv)> 0:
        avg_received = sum(r_payload)/(packets_received - zero_packets_recv)
        variance_recv = variance(avg_received, remove_values_from_list(r_payload))
    if packets_received > 0:
        inter_recv = receiving_time / packets_received     
    compression = huffman_word(t_payload)
   
    if flow_duration == 0.0:
        return
 
    #print "\TESTING"'''
    final_out = str(source) + '\t' + str(dest) + '\t' + str(flow[0][-2]) + '\t' + str(flow[0][-1]) + '\t' + str(time_start) + '\t' + str(flow_duration)+ '\t' + str(sum(t_payload)) +  '\t' + str(sum(s_payload))  + '\t' + str(sum(r_payload)) + '\t' + str(fps) + '\t' + str(mps) + '\t' + str(float(sum(t_payload)) / flow_duration) +  '\t' + str(float(sum(s_payload))/ flow_duration)  + '\t' + str(float(sum(r_payload))/ flow_duration)+ '\t' + str(get_median(inter_arrival_total)) + '\t' + str(get_median(inter_arrival_sent)) + '\t' + str(get_median(inter_arrival_recv)) \
    + '\t' + str(inter_total) + '\t' + str(inter_sent) + '\t' + str(inter_recv) + '\t' + str(total_packets) + '\t' +  str(packets_sent) +  '\t' + str(packets_received) + '\t'+ str(total_packets/ flow_duration) + '\t' +  str(packets_sent/ flow_duration) +  '\t' + str(packets_received/ flow_duration) + '\t' + str(avg_payload) +  '\t'+ str(avg_sent) +  '\t'+ str(avg_received) \
    + '\t' + str(variance_total) +  '\t'+ str(variance_sent) +  '\t'+ str(variance_recv)  +  '\t'+ str(compression) + '\t' + print_fft(fft_payload(t_payload)) + '\t' + print_fft(fft_interarrival(inter_arrival_total)) + '\t' + label
    final_out = final_out.replace('nan','0.0').replace('\t', ',')
    #print final_out
    out_file.write(final_out + '\n')
   
    out_file.close()
    
