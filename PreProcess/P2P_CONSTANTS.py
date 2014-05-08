PCAPDATADIR = '/media/san1/data_uga/vansh_temp/test/demo/'
FLOWDATADIR = './jan_flows/'
SUPERFLOWDATADIR = './jan_superflow/'
TRAININGDIR = './training/'
PCAPFILES = 'PcapInputFiles.txt' #Dir with initial pcap
TSHARKOPTIONSFILE = 'TsharkOptions.txt'
FLOWOPTIONS = 'FlowOptions.txt'
FLOWOUTFILE = PCAPDATADIR + 'FLOWDATA'
C_FLOWOUTFILE = PCAPDATADIR + 'COMPLETEFLOWDATA'
FLOWGAP = 1 * 60 * 60
THREADLIMIT = 12
TCP_PROTO = '6'
UDP_PROTO = '17'
UDP_HEADERLENGTH = 8
TCP_HEADERLENGTH = 20
#utility functions
import os
def getCSVFiles(dirname):
	csvfiles = []
	for eachfile in os.listdir(dirname):
		if eachfile.endswith('.csv'):
			csvfiles.append(dirname + eachfile)	
	return csvfiles
