
import numpy as np
import math  as m

N = 50
OUTPUT1  =  open("backward.fepout"      , "w")
OUTPUT2  =  open("forward.fepout"       , "w")

for i in range(0, 50):
	input1 = "./b" + str(i) + "/b" + str(i) + ".fepout"
	INPUT1 = open(input1, "r")
	lines    = INPUT1.readlines()
	for j in range(0, len(lines)):
		line = lines[j]
		if i > 0:
			if j > 1:
				OUTPUT1.write('{}  '.format(line))
		else:
			OUTPUT1.write('{}  '.format(line))
	print (i)

OUTPUT1.close()

for i in range(0, 50):
	input2 = "./f" + str(i) + "/f" + str(i) + ".fepout"
	INPUT2 = open(input2, "r")
	lines    = INPUT2.readlines()
	for j in range(0, len(lines)):
		line = lines[j]
		if i > 0:
			if j > 1:
				OUTPUT2.write('{}  '.format(line))
		else:
			OUTPUT2.write('{}  '.format(line))
	print (i)
OUTPUT2.close()
