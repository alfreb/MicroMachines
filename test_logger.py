import os,sys

#Add current directory to import-path     
sys.path.append(os.getcwd())

import logger
logger.logfile="stats/test_run_logger.csv"
logger.log("Let's boot some VM's")
logger.close()
