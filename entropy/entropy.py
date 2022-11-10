
import numpy as np
import math  as m

INPUT   =  open("COM.txt" , "r")

x1 = np.array([])
y1 = np.array([])
z1 = np.array([])

lines    = INPUT.readlines()

for i in range(0, len(lines)):
	
	line = lines[i].split()
	
	x1 = (np.append(x1, float(line[1])))
	y1 = (np.append(y1, float(line[2])))
	z1 = (np.append(z1, float(line[3])))

x1_max =  np.max(x1)
y1_max =  np.max(y1)
z1_max =  np.max(z1)
x1_min =  np.min(x1)
y1_min =  np.min(y1)
z1_min =  np.min(z1)


V    = (x1_max - x1_min) * (y1_max - y1_min) * (z1_max - z1_min)
C0   = 6.023 * 10**(-4)
KbT = (310 * 0.001985875)

print (-1.0 * KbT * np.log(C0 * V))
