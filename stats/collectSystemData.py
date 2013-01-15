

procstat=open("/proc/stat")

for line in procstat:
    arr=line.split('\t');
    print arr[0]


