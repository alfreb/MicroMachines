#! /usr/bin/python
import sys


sys.stdin.readline()
l=sys.stdin.readline()
t1=l.rstrip().split(";")[2]
for l in sys.stdin:
    arr=l.rstrip().split(";")
    t=int(arr[2])-int(t1)
    print str(t)+","+arr[4]
    
