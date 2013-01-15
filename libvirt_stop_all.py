import os
import sys

#Add current directory to import-path     
sys.path.append(os.getcwd())

from microManage import *

n=1000;

trace("generating "+str(n)+" instance names")
generateInstanceNames(n)

trace("Stopping")
stop()
