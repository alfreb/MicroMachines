import libvirt
import sys

xmlFile=open("/home/alfred/microMachine.xml")
xmlStr=xmlFile.read()

print "Connecting to hypervisor"

conn = libvirt.open(None)
if conn == None:
    print 'Failed to open connection to the hypervisor'
    sys.exit(1)

try:
    mm1 = conn.lookupByName("microMachine")
    try:
        print "Shutting down domain..."
        mm1.destroy()
    except:
        print "Allready shut down"        

    mm1.undefine()    
except:
    print 'Failed to find the domain, defining from XML'

print "(Re)creating from XML..."
conn.defineXML(xmlStr)
mm1=conn.lookupByName("microMachine")
print "Starting..."
mm1.create()
print mm1.info()



#
#print "Domain 0: id %d running %s" % (mm1.ID(), mm1.OST#ype())
#print mm1.info()
