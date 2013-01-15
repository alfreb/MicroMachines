import os
import sys

#Add current directory to import-path     
sys.path.append(os.getcwd())

from microManage import *
import logger
logger.logfile="stats/libvirt_boottest_1000.csv"

DEBUG=False

trace("generating instance names")
generateInstanceNames(1000)

trace("Stopping")
stop()

#trace("Undeploying")
#undeploy()

#trace("Deploying")
#deploy()

trace("Starting")
start()


logger.close()
