#!/usr/bin/python
__author__ = 'Edward Guevara'

from sys import argv

if len(argv) != 2:
    print "Usage: python BCSD_BAN_cut.py ListFiles.txt"
    exit(1)

# Open a file
fo = open(argv[1], "r")
print "Name of the file: ", fo.name

for line in fo.readlines():
    print "Read Line: %s" % (line)

# Close opend file
fo.close()