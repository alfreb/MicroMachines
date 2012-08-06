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

xmlPath="./images/microMachine.xml"
#imagesPath="/home/alfred/MicroMachines/images/"
mmCount=1000
mmPrefix="mm"
mmPrefixSep="_"

xmlFile=open(xmlPath)
xmlStr=xmlFile.read()

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
    
def connect():
    print "Connecting to Hypervisor"
    conn = libvirt.open(None)
    if conn == None:
        print 'Failed to open connection to the hypervisor'
        sys.exit(1)
    return conn


def deploy():
    conn = connect()
    for mm in mmNames:
    #Put name into xml
        mm_xml=re.sub("<name>.*</name>","<name>"+mm+"</name>",xmlStr)
    #Generate uniquie uuid
        mm_uuid=subprocess.check_output("uuidgen").rstrip()
        print mm+" uuid: "+mm_uuid
    #Put uuid into xml
        mm_xml=re.sub("<uuid>.*</uuid>","<uuid>"+mm_uuid+"</uuid>",mm_xml)
        conn.defineXML(mm_xml)
    conn.close()
        
def stop_1(mm_name,conn):
    mmObj=conn.lookupByName(mm_name)
    if(mmObj.isActive()):
        mmObj.destroy()
        print mm_name+" shutting down"
    else:
        print mm_name+" allready down"

def stop():
    conn=connect()
    for mm in mmNames:
        #thread.start_new_thread(stop_1,(mm,))
        stop_1(mm,conn)
#        print mm+" active: "+str(mmObj.isActive())
    conn.close()

def start():
    conn=connect()
    for mm in mmNames:
        mmObj=conn.lookupByName(mm)
        if(not mmObj.isActive()):
            mmObj.create()
        print mm+" started " #+str(mmObj.isActive())
    conn.close()

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
