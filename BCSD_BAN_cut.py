#!/usr/bin/python
__author__ = 'Edward Guevara'

from sys import argv
import os

if len(argv) != 2:
    print "Usage: python BCSD_BAN_cut.py ListFiles.txt"
    exit(1)

# Open a file
fi = open(argv[1], "r")
print "Name of the file: ", fi.name

for fn in fi.readlines():
    fn = fn.replace('./', '/mnt/BCSD/')
    fo = fn.replace('/mnt/BCSD/', '/home/edarague/BCSD/BAN/')
    if not os.path.exists(os.path.dirname(fo)):
        print 'mkdir -p ' + os.path.dirname(fo)

    #print "Input File: %s" % (fn)
    #print "Output File: %s" % (fo)
    print '\n'

# Close opend file
fi.close()