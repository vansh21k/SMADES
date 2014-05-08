import random
#f = open('big_overall_flows_training_data.arff','w')
g = open('clean_all_convos','r')
training, clean, waledac, storm, zeus = [], [], [], [], []
for line in g:
	line = line.split(',')
	line.pop()
	line.append('CLEAN\n')
	line = ",".join(line)
	clean.append(line)
g.close()
g = open('waledac/waledac.pcap.csv_output_2000_convos', 'r')
for line in g:
	line = line.split(',')
        line.pop()
        line.append('WALEDAC\n')
        line = ",".join(line)
        waledac.append(line)
g.close()
g = open('storm/all_2000_convos_storm', 'r')
for line in g:
	line = line.split(',')
        line.pop()
        line.append('STORM\n')
        line = ",".join(line)
        storm.append(line)
g.close()
g = open('zeus/all_2000_convos_zeus', 'r')
for line in g:
	line = line.split(',')
        line.pop()
        line.append('ZEUS\n')
        line = ",".join(line)
        zeus.append(line)
g.close()
random.shuffle(waledac)
random.shuffle(storm)
random.shuffle(zeus)
random.shuffle(clean)
training.extend(clean[:560000])
training.extend(zeus)
training.extend(storm[:75000])
training.extend(waledac[:75000])
#print len(training)
for line in training:
	print(line.strip())
	

