__author__ = 'Edward Guevara'
from os import system, path
from sys import argv

if len(argv) != 2:
    print "Usage: python prCopy.py MODEL"
    exit(1)
MODEL = int(argv[1])

for year in range(2006, 2100):
    fs = '/box0_p2/BCSD/%s/rcp85/day/r1i1p1/pr/pr_day_%s_rcp85_r1i1p1_%s.nc' % (MODEL, MODEL, year)
    ft = '/mnt/BCSD/%s/junk/prmm_day_%sMODEL_rcp45_r1i1p1_%s.nc' % (MODEL, MODEL, year)
    if not path.exists(fs):
        print '... copying %s' % ft
        system('cp %s %s' % (fs, ft))
    else:
        print "\n... nothing to do, %s exist!\n" % fs