import os
import math
import json
from collections import defaultdict

###  Load file type's fingerprint ###

in_file = open("bfa_fp.json","r")
new_dict = json.load(in_file)
in_file.close()

fp = []

for i in range(0,256):
	fp.append(new_dict[i])

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

def correlationfactor(x):
	a = float(pow(x,2)) * float(-1)
	b = float(2) * float(pow(0.0375,2))
	y = pow(math.e , float(a / b) )
	return y

def avgcalc(l1):
	n = len(l1)
	sum1 = 0
	for item in l1:
		sum1 += item
	return float(sum1)/float(n)

finalcf = []
count = 0
## Go Through Each File in a particular directory : TEST
for i in os.listdir(os.getcwd()):
	
	if i == "bfdc.py":
		continue

	## open that file in binary mode and process it
	f = open(i, "rb")
	count += 1
	## Initialize array for this file for byte frequency distribution
	bfd = [0 for i in range(0,256)]
	cf = []

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

	## Compute correlation factor for this file
	cf = [correlationfactor(abs(bfd[i] - fp[i])) for i in range(0,256)]
	finalcf = addtwolists(finalcf,cf)

finalcf = [float(item)/float(count) for item in finalcf]

d = defaultdict(float)

for i in range(0,256):
	d[i] = finalcf[i]

out_file = open("bfcc.json","w")
json.dump(d,out_file, indent=4)
out_file.close()
	
	


























