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
    fo = fn.replace('/mnt/BCSD/', '/home/edarague/BCSD/BAN/')
    if not path.exists(path.dirname(fo)):
        system('mkdir -p %s' % path.dirname(fo))
        print '... directorio %s creado!' % path.dirname(fo)

    #print "Input File: %s" % (fn)
    #print "Output File: %s" % (fo)
    print '\n'

# Close opend file
fi.close()