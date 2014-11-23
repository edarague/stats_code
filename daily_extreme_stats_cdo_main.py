#!/usr/local/cdat5.2/bin/python

#Set up to use CDO utilities to calculate extremes
#daily downscaled files are in different directories for each variable, scenario and run
#input is one file per year
#some statistics are calculated relative to reference period, all of which must exist.
#For this code, the ref period conincides with the historical period

from sys import exit, argv
from os import path, mkdir

if len(argv) != 2:
    print "Usage: python daily_extreme_stats_cdo_main.py run_list_MODELS.txt"
    exit(1)
import daily_extreme_stats_temp as t_stats
import daily_extreme_stats_precip as p_stats

# var_stat = ['tasmin','tasmax','txx','tnn','gd10','hd18', 'cd18', 'pr', 'cdd', 'r02', 'r5d', 'sdii']
var_stat = ['tasmin', 'tasmax']

# define reference historical period
StRefh = 1950
EnRefh = 1999

# define complete historical period
StRef = 1950
EnRef = 2005

# future periods
StYrs = [2006]
EnYrs = [2099]

# root dir needs to match list of runs below - they need to be located there
RootDir = '/mnt/BCSD'

# input list created by get_run_lists.scr
inlist = './' + str(argv[1])

# land-sea mask
lsm = "./global_0.25deg_LSM.nc"

# read in the list
models = []
scens = []
runs = []
f = open(inlist, 'r')
for line in f.readlines():
    junk = line.split()
    models.append(junk[0])   # like bccr_bcm2_0
    scens.append(junk[1])    # sresa2, sresa1b, sresb1
    runs.append(junk[2])     # entire string like 'run1' must exist for 20c3m too
f.close()

for i in range(len(models)):
    if not path.isdir('/mnt/out_stats/' + models[i]):
        mkdir('/mnt/out_stats/' + models[i])

    # within each directory, subdirectories for each variable: pr, tasmax, tasmin
    ind20 = RootDir + "/" + models[i] + "/historical/day/" + runs[i]
    fn20pr = ind20+"/pr/pr_day_"+models[i]+"_historical_"+runs[i]+"_"
    fn20tx = ind20+"/tasmax/tasmax_day_"+models[i]+"_historical_"+runs[i]+"_"
    fn20tn = ind20+"/tasmin/tasmin_day_"+models[i]+"_historical_"+runs[i]+"_"

    ind21 = RootDir + "/" + models[i] + "/" + scens[i] + "/day/" + runs[i]
    fn21pr = ind21+"/pr/pr_day_"+models[i]+"_"+scens[i]+"_"+runs[i]+"_"
    fn21tx = ind21+"/tasmax/tasmax_day_"+models[i]+"_"+scens[i]+"_"+runs[i]+"_"
    fn21tn = ind21+"/tasmin/tasmin_day_"+models[i]+"_"+scens[i]+"_"+runs[i]+"_"

    ####################################################################################
    # copy_files really just creates soft links to files for existing variables
    # working directory is hardcoded in two py modules.
    # Also, tavg ('tas') is needed for many stats, calculate up front
    t_stats.copy_files(fn20tx, StRef, EnRef, models[i])
    for j in range(len(StYrs)):
        t_stats.copy_files(fn21tx, StYrs[j], EnYrs[j], models[i])
       t_stats.copy_files(fn22tx, StYrs[j], EnYrs[j], models[i])

    t_stats.copy_files(fn20tn, StRef, EnRef, models[i])
    for j in range(len(StYrs)):
        t_stats.copy_files(fn21tn, StYrs[j], EnYrs[j], models[i])
        t_stats.copy_files(fn22tn, StYrs[j], EnYrs[j], models[i])

    t_stats.copy_files(fn20pr, StRef, EnRef, models[i])
    for j in range(len(StYrs)):
        t_stats.copy_files(fn21pr, StYrs[j], EnYrs[j], models[i])
        t_stats.copy_files(fn22pr, StYrs[j], EnYrs[j], models[i])

#    t_stats.CalcTavg(fn20tn, fn20tx, StRef, EnRef, models[i])
#    for j in range(len(StYrs)):
#        t_stats.CalcTavg(fn21tn, fn21tx, StYrs[j], EnYrs[j], models[i])
#        t_stats.CalcTavg(fn22tn, fn22tx, StYrs[j], EnYrs[j], models[i])

    #Monthly mean maximum temperatures
    if 'txavg' in var_stat:
        of = t_stats.TAVG(fn20tx,StRef,EnRef, models[i])
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.TAVG(fn21tx,StYrs[j],EnYrs[j], models[i])
            print "created outfile %s\n" % (of)
            #modify variable name, history, global attributes

    #Monthly mean minimum temperatures
    if 'tnavg' in var_stat:
        of = t_stats.TAVG(fn20tn,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.TAVG(fn21tn,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)
            #modify variable name, history, global attributes

    #Monthly maximum temperatures
    if 'txx' in var_stat:
        of = t_stats.TXX(fn20tx, StRef, EnRef, models[i])
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.TXX(fn21tx, StYrs[j], EnYrs[j], models[i])
            print "created outfile %s\n" % (of)
            #modify variable name, history, global attributes

    #Monthly minimum temperatures
    if 'tnn' in var_stat:
        of = t_stats.TNN(fn20tn,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.TNN(fn21tn,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #90th percentile Tmax - one value per year
    if 'tx90' in var_stat:
        of = t_stats.TX90(fn20tx,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.TX90(fn21tx,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #Generalized version: Pct of time T doesn't exceeds ref pd Nth percentile
    if 'tx90p' in var_stat:
        oftx90p_ref = t_stats.Tref(fn20tx,90,'tasmax',StRefh,EnRefh)
        print "created outfile %s\n" % (oftx90p_ref)
        of = t_stats.TP(fn20tx,90,'tasmax',oftx90p_ref,StRef,EnRef)
        for j in range(len(StYrs)):
            of = t_stats.TP(fn21tx,90,'tasmax',oftx90p_ref,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)
    #Generalized version: Pct of time T doesn't exceeds ref pd Nth percentile
    if 'tx10p' in var_stat:
        oftx90p_ref = t_stats.Tref(fn20tx,10,'tasmax',StRefh,EnRefh)
        print "created outfile %s\n" % (oftx90p_ref)
        of = t_stats.TP(fn20tx,10,'tasmax',oftx90p_ref,StRef,EnRef)
        for j in range(len(StYrs)):
            of = t_stats.TP(fn21tx,10,'tasmax',oftx90p_ref,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #Generalized version: Pct of time T doesn't exceeds ref pd Nth percentile
    if 'tn90p' in var_stat:
        oftx90p_ref = t_stats.Tref(fn20tn,90,'tasmin',StRefh,EnRefh)
        print "created outfile %s\n" % (oftx90p_ref)
        of = t_stats.TP(fn20tn,90,'tasmin',oftx90p_ref,StRef,EnRef)
        for j in range(len(StYrs)):
            of = t_stats.TP(fn21tn,90,'tasmin',oftx90p_ref,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #Generalized version: Pct of time T doesn't exceeds ref pd Nth percentile
    if 'tn10p' in var_stat:
        oftx90p_ref = t_stats.Tref(fn20tn,10,'tasmin',StRefh,EnRefh)
        print "created outfile %s\n" % (oftx90p_ref)
        of = t_stats.TP(fn20tn,10,'tasmin',oftx90p_ref,StRef,EnRef)
        for j in range(len(StYrs)):
            of = t_stats.TP(fn21tn,10,'tasmin',oftx90p_ref,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #Frost days
    if 'fd' in var_stat:
        of = t_stats.FD(fn20tn,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.FD(fn21tn,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)
            
    #Thermal growing season length
    if 'gsl' in var_stat:
        of = t_stats.GSL(fn20tn,fn20tx,lsm,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.GSL(fn21tn,fn21tx,lsm,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)
    
    #Heat wave duration index wrt mean of reference_period
    if 'hwdi' in var_stat:
        oftxnorm_ref = t_stats.TXnorm(fn20tx,StRefh,EnRefh)
        print "created outfile %s\n" % (oftxnorm_ref)
        of = t_stats.HWDI(fn20tx,oftxnorm_ref,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.HWDI(fn21tx,oftxnorm_ref,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #cooling degree days
    if 'cd18' in var_stat:
        of = t_stats.CD18(fn20tg,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.CD18(fn21tg,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #heating degree days
    if 'hd18' in var_stat:
        of = t_stats.HD18(fn20tg,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.HD18(fn21tg,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #growing degree days
    if 'gd10' in var_stat:
        of = t_stats.GD10(fn20tg,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = t_stats.GD10(fn21tg,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)
            
    ###########################################################################

    #Monthly total precip
    if 'ptot' in var_stat:
        of = p_stats.Ptot(fn20pr,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = p_stats.Ptot(fn21pr,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #Consecutive dry days
    if 'cdd' in var_stat:
        of = p_stats.CDD(fn20pr,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = p_stats.CDD(fn21pr,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #Number of wet days > 0.2 mm/d
    if 'r02' in var_stat:
        of = p_stats.R02(fn20pr,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = p_stats.R02(fn21pr,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #Max consec 5 day precip
    if 'r5d' in var_stat:
        of = p_stats.R5D(fn20pr,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = p_stats.R5D(fn21pr,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #Pct of time precip exceeds ref pd 90th percentile (wet day values)
    #calculate % of precip due to this too
    if 'r90p' in var_stat:
        ofpr90_ref = p_stats.R90ref(fn20pr,StRefh,EnRefh)
        print "created outfile %s\n" % (ofpr90_ref)
        of = p_stats.R90P(fn20pr,ofpr90_ref,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = p_stats.R90P(fn21pr,ofpr90_ref,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)
        of = p_stats.R90PTOT(fn20pr,ofpr90_ref,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = p_stats.R90PTOT(fn21pr,ofpr90_ref,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

    #simple daily precip intensity index
    if 'sdii' in var_stat:
        of = p_stats.SDII(fn20pr,StRef,EnRef)
        print "created outfile %s\n" % (of)
        for j in range(len(StYrs)):
            of = p_stats.SDII(fn21pr,StYrs[j],EnYrs[j])
            print "created outfile %s\n" % (of)

#done
