#!/usr/bin/env python

#This makes many random sequences given  the number of sequences to make and
#the length of the sequences. The sequences are saved as the given file name.

import os
import random
import sys

def main(argv=None):
    iterations = int(argv[1])
    length = int(argv[2])
    saveFileName = argv[3]
    acidType = argv[4]
    
    if acidType == 'rna':
        bases = ('U', 'A', 'G', 'C')
    elif acidType == 'dna':
        bases = ('T', 'A', 'G', 'C')
    
    saveFile = open(saveFileName, 'w')
    
    for i in xrange(iterations):
        writestring = '> testing_{0}\n'.format(i)
        saveFile.write(writestring)
        for i in xrange(length):
            newBase = random.randint(0, 3)
            writeBase = bases[newBase]
            saveFile.write(writeBase)
        saveFile.write('\n')
    saveFile.close()

if __name__ == "__main__":
    main(sys.argv)
