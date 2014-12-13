#!/usr/bin/python
__author__ = 'Edward Guevara'

from sys import argv
from os import path, system

if len(argv) != 2:
    print "Usage: python BCSD_BAN_cut.py ListFiles.txt"
    exit(1)

# Open a file
fi = open(argv[1], "r")
print "Name of the file: ", fi.name

for fn in fi.readlines():
    fn = fn.replace('./', '/mnt/BCSD/')
    # fo = fn.replace('/mnt/BCSD/', '/home/edarague/BCSD/BAN/')
    fo = path.basename(fn)
    if not path.exists(path.dirname(fo)):
        system('mkdir -p %s' % path.dirname(fo))
        print '... directorio %s creado!' % path.dirname(fo)

    if not path.exists(fo):
        print "... cut file Bangladesh: %s outtemp.nc" % (fn)
        print 'nces -d lat,20.746231,26.631950 -d lon,88.028340,92.680664 %s %s' % (fn, fo)
        system('nces -d lat,20.746231,26.631950 -d lon,88.028340,92.680664 %s %s' % (fn, 'outtemp.nc'))
    else:
        raise Exception('infile not found: %s' % fn)

# Close opend file
fi.close()