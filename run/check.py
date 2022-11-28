
import numpy as np
import math  as m

N = 50
OUTPUT1  =  open("backward_check.txt"      , "w")
OUTPUT2  =  open("forward_check.txt"       , "w")

for i in range(0, 50):
    input1 = "./b" + str(i) + "/b" + str(i) + ".restart.xsc"
    INPUT1 = open(input1, "r")
    lines    = INPUT1.readlines()
    line = lines[2].split()
    steps = line[0]
    if steps != "550000":
        print(f'BACKWARD {i}: {steps}/550000')
        OUTPUT1.write('{}    '.format(i))
        OUTPUT1.write('{}  \n'.format(steps))

for i in range(0, 50):
    input2 = "./f" + str(i) + "/f" + str(i) + ".restart.xsc"
    INPUT2 = open(input2, "r")
    lines    = INPUT2.readlines()
    line = lines[2].split()
    steps = line[0]
    if steps != "550000":
        print(f'FORWARD {i}: {steps}/550000')
        OUTPUT2.write('{}    '.format(i))
        OUTPUT2.write('{}  \n'.format(steps))
