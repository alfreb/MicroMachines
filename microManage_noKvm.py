#! /usr/bin/python
#
# Tools to manage large populations of MicroMachines
#
#

import re
import sys
import libvirt
import subprocess
import thread
import datetime
import time

cpuList=range(20,30)
cpuCount=len(cpuList)
mmCount=3
mmPrefix="mm"
mmPrefixSep="_"

# Setting Instance-count from arg1
if len(sys.argv)>2:
    mmCount=sys.argv[1]

    # Setting Instance-name prefix from arg2
    if len(sys.argv)>3:
        mmPrefix=sys.argv[2]


print "Instances: "+mmPrefix+mmPrefixSep+"0 - "+mmPrefix+mmPrefixSep+str(mmCount-1)

mmNames=[]

for mm in range(0,mmCount):
    #New name, based on nr. and prefix
    mm_name=mmPrefix+mmPrefixSep+str(mm)
    mmNames.append(mm_name)

        
def ls():
    screenLs=[]
    try:
        #Will throw exception, due to strange exit statuses
        myStr=subprocess.check_output(["screen","-ls"])
    except Exception as e:
        outs=e.output
        outArr=outs.split("\n")
        for ln in outArr:
            larr=ln.split("\t")
            if(len(larr)==4):
                screenLs.append(larr[1])
    return screenLs
        
vms={}
def start(oncpu=None):
    now=datetime.datetime.now()
    memStart=freemem()
    print "Starting boot at "+str(now)
    print "Free memory is: "+str(memStart)
    lst=ls()
    names=set(map(lambda x:x.split(".")[0],lst))
    i=0
    #Args:
    command="kvm"
    graphics="-nographic"
    mem="1"    
    smp="1,sockets=1,cores=1,threads=1,maxcpus=1"
    net="none"
    cpu="pentium"
    icount="auto" #Virtual instruction counter
    for mm in mmNames:        
        if(mm in names):
            #print mm+" allready running "
            continue
        vms[mm]={} #Create obj. pr. VM
        i+=1
        if(oncpu):
            cpubind=oncpu
        else:
            cpubind=cpuList[i%cpuCount]   
        namearg=mm+",process=proc_"+mm
        #cmd=["screen", "-d", "-m", "-S", mm, "taskset", "-c", str(cpu), command,"-m",mem, "-hda", "microMachine.hda", graphics]
        cmd=["screen", "-d", "-m", "-S", mm,"taskset","-c", str(cpubind),command,"-m",mem, "-hda", "microMachine.hda","-icount",icount, "-cpu",cpu,"-smp",smp,"-net",net,"-name",namearg, graphics]
        #cmd=["screen", "-d", "-m", "-S", mm, "taskset", "-c", str(cpu), "sleep", "1000000"]
    #Generate uniquie uuid
        
        vms[mm]["cmd"]=" ".join(cmd)
        vms[mm]["res"]=subprocess.check_output(cmd)
#        vms[mm]["exit"]=
#        mm_uuid=subprocess.check_output("uuidgen").rstrip()
        
        print "starting "+mm+" on cpu "+str(cpubind)
        
        #Make plottable output
#        print str(i)+"\t"+str(int(time.time()))+"\t"+str(freemem())
        
    print "Done."
    bootCount=len(vms.keys())
    bootTime=datetime.datetime.now()-now
    timePrMm=bootTime/bootCount    
    print "Booted "+str(len(ls()))+" MM's in "+str(bootTime)
    print "Boot-time pr. MM: "+str(timePrMm)
    memStop=freemem()
    memDiff=(memStart-memStop)/1000.0
    print "Memory difference: "+str(memDiff)+" MB"
    print "Mem pr. MM: "+str(memDiff/bootCount)+" MB"

def stop_1(mm_name):
    subprocess.call(["screen","-X","-S",mm_name,"quit"])

def stop():
    lst=ls()
    for mm in lst:
        print "Stopping "+mm
        stop_1(mm)

def undeploy():
    conn=connect()
    for mm in mmNames:
        try:
            mmObj=conn.lookupByName(mm)
            mmObj.undefine()
            print mm+" is undefined"
        except:
            print mm+" does not exist"
    conn.close()
        
def freemem():
    m=subprocess.check_output("free")
    mFree=int(re.split("[\s]*",m.split("\n")[1])[3])
    return mFree
    

def memUsage():
    m1=freemem()
    deploy()
    start()
    m2=freemem()
    print "Memory difference, all started: "+str(m1-m2)+" Kb"
    stop()
    m3=freemem()
    print "Memory difference, all stopped: "+str(m3-m2)+" Kb"
    undeploy()

def moveToCPU(machineName,cpuNr):    
    conn=connect()
    cpuCount=conn.getInfo()[2]
    if not cpuNr<cpuCount:
        raise Exception("Invalid CPU number")
    cpuMap=[False for x in range(0,cpuCount)]
    cpuMap[cpuNr]=True
    mm=conn.lookupByName(machineName)
    mm.pinVcpu(0,tuple(cpuMap))
    conn.close()


def moveAllToCPU(cpuNr):
    conn=connect()
    cpuCount=conn.getInfo()[2]
    if not cpuNr<cpuCount:
        raise Exception("Invalid CPU number")
    cpuMap=[False for x in range(0,cpuCount)]
    cpuMap[cpuNr]=True
    cpuMap=tuple(cpuMap)
    for mm in mmNames:
        mmObj=conn.lookupByName(mm)
        mmObj.pinVcpu(0,cpuMap)
    conn.close()

def distributeOverCPURange(cpuStart,cpuStop):
    conn=connect()
    cpuCount=conn.getInfo()[2]
    if not cpuStop<cpuCount:
        raise Exception("Invalid CPU number")

#memUsage_allOn()
#    print mm_xml

#m0=freemem()
#deploy()
#start()
#m1=freemem()
#print "Memory diff: "+str(m1-m0)+" Kb"
#stop()
#undeploy()
#start()

def make():
    subprocess.call("make")
    deploy();start()

def clean():
    stop();undeploy()



