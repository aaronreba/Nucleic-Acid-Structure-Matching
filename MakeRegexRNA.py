#!/usr/bin/env python

#This will create a random RNA regular expression. In the save file, the format
#is like so:

#> testing_1
#ACGAT[3]ATCGTACG[2]ACTGACTG[6]GG
#> testing_2
#ACG[3]ATCAAACGACT[4]GACTG[6]GG

#run as "python MakeRegexRNA.py $1 $2 $3"
#$1 is the number of expressions that will be made
#$2 is the length of the expressions (includes wildcard bases, ie. [4])
#$3 is the save file

#Written by Aaron Reba

from __future__ import division

import random
import sys

def main(argv=None):
    #chance for insertion:
    wildcardChance = .03
    
    #insertion length range:
    wildcardLengthRange = [5, 10]
    
    iterations = int(argv[1])
    length = int(argv[2])
    writeFileName = argv[3]
    
    writeFile = open(writeFileName, 'w')
    
    bases = ('T', 'A', 'G', 'C')
    
    for i in xrange(iterations):
        l = 0
        writestring = '> testing_%i\n' % (i + 1)
        writeFile.write(writestring)
        while l < length:
            wildcardRoll = random.random()
            if wildcardRoll < wildcardChance:
                wildcardLength = random.randrange(wildcardLengthRange[0],
                                                  wildcardLengthRange[1])
                if l + wildcardLength > length:
                    #the wildcard length extends past the length of the strand,
                    #set it to go up to the length of the strand.
                    wildcardLength = length - l
                    l = length
                l += wildcardLength
                
                writestring = '[%i]' % (wildcardLength)
                writeFile.write(writestring)
            else:
                newBase = random.randrange(0, 4)
                l += 1
                
                writeBase = bases[newBase]
                writeFile.write(writeBase)
        writeFile.write('\n')
    
    writeFile.close()

if __name__ == "__main__":
    main(sys.argv)

#> testing_1
#[2][2]TTTGATAGCTTGGC[2]
