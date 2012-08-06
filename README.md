Virtual Micro Machines
======================

******* NOTE: ********
This is a static, dedicated branch for CloudCom 2012. 

While the master branch will continue to change, this branch is left as it was at the point of article submission.



RECREATING PLOTS
----------------

Plots in Fig.1 were created with the sysstat package like so:

1. Build the machine:
# cp src/cpu_profile_n.asm microMachine.asm
# make

2. Boot the machine:
# screen -S mm1 taskset -c 3 kvm -hda microMachine.hda -curses

3. Collect and filter statistics:
# sar 1 200 -P 3 -o stats/stats_cpuProfile_n.dat
# sadf -d -T -P 3 stats/stats_cpuProfile_n.dat | stats/filter_stats.py 

The data was then copied into plot: http://plot.micw.eu/


