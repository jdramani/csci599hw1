import os
import math
import json
from collections import defaultdict()

def addtwolists(l1,l2):
	result = []
	n = len(l1)
	for i in range(0,n):
		result.append(l1[i] + l2[i])

	return result

def compandingfn(l1):
	b = 1.5
	result = []
	n = len(l1)
	for i in range(0,n):
		result.append(pow(float(l1[i]),float(float(1)/float(b))))
	return result

overallbfd = [0 for i in range(0,256)]
count = 0

## Go Through Each File in a particular directory
for i in os.listdir(os.getcwd()):
	
	if i == "bfa.py":
		continue
	## open that file in binary mode and process it
	f = open(i, "rb")
	count += 1
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

	overallbfd = addtwolists(overallbfd,bfd)

overallbfd = [float(overallbfd[i])/float(count) for i in range(0,256)]

d = defaultdict(float)

for i in range(0,256):
	d[i] = overallbfd[i]

out_file = open("bfa.json","w")
json.dump(d,out_file, indent=4)
out_file.close()























