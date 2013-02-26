#!/usr/bin/env python

#This makes many random sequences given  the number of sequences to make and
#the length of the sequences. The sequences are saved as the given file name.

#$1 is the number of sequences
#$2 is the length of the sequences
#$3 is the name of the file that will hold the previous generations' passed scores
#$4 is the save file name for the newly generated sequences.
#$5 is the number of the current generation

#If $2 is "-f", This will append random sequences of the sequence length in the
#given file until there are $1 sequences.

#If $3 is "-n", this will assume no previous sequences passed.

#Written by Aaron Reba

import os
import random
import sys

def main(argv=None):
    iterations = int(argv[1])
    previousFileName = argv[3]
    newFileName = argv[4]
    genNumber = argv[5]
    seqNumber = argv[6]
    acidType = argv[7]
    
    if argv[2] == '-f' and previousFileName != '-n':
        previousFile = open(previousFileName, 'r')
        
        previousFile.readline()
        previousFile.readline()
        testline = previousFile.readline()
        
        
        length = len(testline) - 1 #subtracting 1 for '\n'
        
        previousFile.seek(0)
        
        count = 0
        while 1:
            testline = previousFile.readline()
            if not testline:
                break
            if testline[0] == '>':
                count += 1
        
        start = count
        
        previousFile.close()
    else:
        length = int(argv[2])
        
        start = 0
    
    newFile = open(newFileName, 'w')
    
    if acidType == 'rna':
        bases = ('U', 'A', 'G', 'C')
    elif acidType == 'dna':
        bases = ('T', 'A', 'G', 'C')
    
    
    for i in xrange(start, iterations):
        writestring = '> testing_{0}_{1}\n'.format(genNumber, int(seqNumber) + i)
        newFile.write(writestring)
        for i in xrange(length):
            newBase = random.randrange(0, 4)
            writeBase = bases[newBase]
            newFile.write(writeBase)
        newFile.write('\n')
    newFile.close()
    
    if start == iterations:
        #this must be an amplification run, set the previous file's name to
        #the new file's name
        os.system('mv {0} {1}'.format(previousFileName, newFileName))
    

if __name__ == "__main__":
    main(sys.argv)
