

logfile="stats/deployment_log.csv"


def log(line):
    global __logfile,logfile
    try: 
        __logfile.write(line+"\n")
#        print "Was open"
    except:
        __logfile=open(logfile,"w")
        __logfile.write(line+"\n")
 #       print "was closed"
    print "logging to ",logfile
    __logfile.flush()

def close():
    try:
        __logfile.close()
    except:
        pass



        



