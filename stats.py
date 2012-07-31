import libvirt
import sys

conn = libvirt.open(None)
if conn == None:
    print 'Failed to open connection to the hypervisor'
    sys.exit(1)

try:
    mm1 = conn.lookupByName("mm1")
except:
    print 'Failed to find the main domain'
    sys.exit(1)

print "Domain 0: id %d running %s" % (dom0.ID(), dom0.OSType())
print dom0.info()
