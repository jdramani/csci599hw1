

'''
This Script builds cross correlation matrix from given files.
'''

import os
import math


def compandingfn(l1):
	b = 1.5
	result = []
	n = len(l1)
	for i in range(0,n):
		result.append(pow(float(l1[i]),float(float(1)/float(b))))
	return result

def correlationfactor(x):
	a = float(pow(x,2)) * float(-1)
	b = float(2) * float(pow(0.0375,2))
	y = pow(math.e , float(a / b) )
	return y



## ccmoverall -> Cross Correlation Matrix overall
ccmoverall = [[1 for j in range(0,256)] for i in range(0,256)]
first_flag = 1

## Go Through Each File in a particular directory
for i in os.listdir(os.getcwd()):

	if i == "bfcc.py":
		continue

	## open that file in binary mode and process it
	f = open(i, "rb")
	
	## Initialize array for this file for byte frequency distribution
	bfd = [0 for i in range(0,256)]
	
	## Read bytes one by one until the end of file
	while 1:
		byte = f.read(1)

		if not byte:
			break

		bfd[int(byte,2)-1] += 1
	f.close()
	## Normalize the bfd array

	max1 = max(bfd)
	bfd = [float(i)/float(max1) for i in bfd]

	## Companding
	bfd = compandingfn(bfd)

	## Now loop over to this list and augment this file to overall matrix
	ccm = [[1 for j in range(0,256)] for i in range(0,256)]
	
	if first_flag == 1:
		## 1) Fill the bottom of diagonal
		for i in range(0,256):
			for j in range(0,i+1):
				ccm[i][j] = bfd[i] - bfd[j]

		## 2) set top-left element to 1 (As this is the first file)
		ccm[0][0] = 1

		ccmoverall = ccm[:][:]
		first_flag = 0
		continue
	else:
		## 1) Fill the bottom of diagonal
		for i in range(0,256):
			for j in range(0,i+1):
				ccm[i][j] = bfd[i] - bfd[j]
		
		## 2) Fill the upper side of diagonal
		for i in range(0,255):
			for j in range(i+1, 256):
				ccm[i][j] = correlationfactor(abs(ccm[j][i] - ccmoverall[j][i]))

		## 3) Now add this ccm to ccmoverall to form new ccmoverall
		prev_files = ccmoverall[0][0]
		for i in range(0,256):
			for i in range(0,256):
				ccmoverall[i][j] = float( float(ccmoverall[i][j]) * float(prev_files) + float(ccm[i][j])) / float(prev_files + 1)

		ccmoverall[0][0] = prev_files + 1


## write ccmoverall to csv file...

outfile = open('crosscorr.csv','w')

for i in range(0,256):
	if i != 255:
		outfile.write(str(i) + ',')
	else:
		outfile.write(str(i))
outfile.write('\n')
for i in range(0,256):
	for j in range(0,256):
		if j != 255:
			outfile.write(str(ccmoverall[i][j]) + ',')
		else:
			outfile.write(str(ccmoverall[i][j]))
	if i != 255:
		outfile.write('\n')

outfile.close()







