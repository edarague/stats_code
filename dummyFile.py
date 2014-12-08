__author__ = 'Edward Guevara'
from os import system
from sys import argv

if len(argv) != 4:
    print "Usage: python daily_extreme_stats_cdo_main.py IniYear FinYear TargetPath"
    exit(1)
iniYear = int(argv[1])
finYear = int(argv[2])
TarPath = str(argv[3])

for year in range(iniYear, finYear + 1):
    print '... touch %spr_day_CNRM-CM5_rcp85_r1i1p1_%s.nc' % (TarPath, year)
    system('touch %spr_day_CNRM-CM5_rcp85_r1i1p1_%s.nc' % (TarPath, year))