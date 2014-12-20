__author__ = 'edarague'

from sys import argv
from os import path, system
from subprocess import call

if len(argv) != 2:
    print "Usage: python tasmin_tasmax_avgyear.py list_monthly.txt"
    exit(1)

# Open a file
fi = open(argv[1], "r")
print "Name of the file: ", fi.name

for fn in fi.readlines():
    fn = fn.replace('./', '/mnt/out_stats/')[:-1]
    fo = fn.replace('.monthly', '')
    if not path.exists(fo):
        print "\n... year summary: %s" % (fn)
        #print 'nces -d lat,20.746231,26.631950 -d lon,88.028340,92.680664 %s %s' % (fn, fo)
        #call('nces -d lat,20.746231,26.631950 -d lon,88.028340,92.680664 %s %s' % (fn, fo), shell=True)
    else:
        raise Exception('infile not found: %s' % fn)

# Close opend file
fi.close()
