import os
import math

#####  4-header  ######
count4 = 4
head4overall = [[0 for i in range(0,256)] for j in range(0,count4)]
first_flag = 1
file_count = 0
## Go Through Each File in a particular directory
for i in os.listdir(os.getcwd()):
	f = open(i, "rb")
	head4 = [[0 for i in range(0,256)] for j in range(0,count4)]
	## Read bytes till count
	for i in range(0,count4):
		byte = f.read(1)
		if byte:
			byte_index = int(byte,2)-1
			head4[i][byte_index] = 1
		else:
			head4[i] = [-1] * 256

	if first_flag == 1:
		head4overall = head4[:][:]
		first_flag = 0
		file_count += 1
		continue
	else:
		for i in range(0,count4):
			for j in range(0,256):
				head4overall[i][j] = float(float(head4overall[i][j]) * file_count + head4[i][j]) / float(file_count + 1)
		file_count += 1
		
		
	f.close()

## write head4overall to csv file...

outfile = open('head4overall.csv','w')

for i in range(0,256):
	if i != 255:
		outfile.write(str(i) + ',')
	else:
		outfile.write(str(i))
outfile.write('\n')
for i in range(0,count4):
	for j in range(0,256):
		if j != 255:
			outfile.write(str(head4overall[i][j]) + ',')
		else:
			outfile.write(str(head4overall[i][j]))
	if i != count4-1:
		outfile.write('\n')

outfile.close()


########  4-Trailer #############

count4 = 4
trail4overall = [[0 for i in range(0,256)] for j in range(0,count4)]
first_flag = 1
file_count = 0
## Go Through Each File in a particular directory
for i in os.listdir(os.getcwd()):
	f = open(i, "rb")
	f.seek(0,2)
	size = f.tell()
	m = count4 -1

	trail4 = [[0 for i in range(0,256)] for j in range(0,count4)]
	while size > 0 and m >= 0:
		size -= 1
		f.seek(size)
		byte = f.read(1)
		if byte:
			byte_index = int(byte,2)-1
			trail4[m][byte_index] = 1
		else:
			trail4[m] = [-1] * 256
		m -= 1

	if first_flag == 1:
		trail4overall = trail4[:][:]
		first_flag = 0
		file_count += 1
		continue
	else:
		for i in range(0,count4):
			for j in range(0,256):
				trail4overall[i][j] = float(float(trail4overall[i][j]) * file_count + trail4[i][j]) / float(file_count + 1)
		file_count += 1
		
		
	f.close()

## write trail4overall to csv file...

outfile = open('trail4overall.csv','w')

for i in range(0,256):
	if i != 255:
		outfile.write(str(i) + ',')
	else:
		outfile.write(str(i))
outfile.write('\n')
for i in range(0,count4):
	for j in range(0,256):
		if j != 255:
			outfile.write(str(trail4overall[i][j]) + ',')
		else:
			outfile.write(str(trail4overall[i][j]))
	if i != count4-1:
		outfile.write('\n')

outfile.close()






































