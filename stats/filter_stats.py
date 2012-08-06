#! /usr/bin/python

# Filter stats from sadf/sar to two-column time-neutral format
# ...just to make the data appear nicely in "plot"

import sys

sys.stdin.readline()
l=sys.stdin.readline()
t1=l.rstrip().split(";")[2]
cpuSum=0
samples=0
for l in sys.stdin:
    samples+=1
    if samples > 990:
        break
    arr=l.rstrip().split(";")
    t=int(arr[2])-int(t1)
    cpuSum+=float(arr[4])
    print str(t)+","+arr[4]
 
print "Average CPU-usage, over "+str(samples)+" samples: "+str(cpuSum/samples)
