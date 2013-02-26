#!/usr/bin/env python

#Given a sequence of RNA, this will find all 1 mutation neighbors of that
#sequence.

#If you want the 2 mutation neighbors of a sequence, run this program twice or
#use MakeMutationNeighborhood.py
#The second time, the input file would be the output file from the first run.
#The sequence file and the save file must be different! You cannot use the same
#file as both parameters!

#run as "python MakeMutationNeighbors.py $1 $2"
#$1 is a file of random sequences in the format of MakeG's output format.
#$2 is the save file.

#Written by Aaron Reba

import sys

def main(argv=None):
    sequenceFileName = argv[1]
    writeFileName = argv[2]
    
    sequenceFile = open(sequenceFileName, 'r')
    writeFile = open(writeFileName, 'w')
    
    numWrites = 0
    
    while 1:
        titleLine = sequenceFile.readline()
        
        if not titleLine:
            break
        
        titleLine = titleLine[2:] #skipping the '> '
        sequence = sequenceFile.readline()[:-1] #skipping the '\n'
        
        #The writing file must be scanned in order to avoid writing the same
        #permutation twice.
        previousWrite = writeFile.tell()
        writeFile.close()
        writeFile = open(writeFileName, 'r')
        foundSequence = False
        
        while 1:
            nextLine = writeFile.readline()
            if not nextLine:
                break
            
            nextLine = writeFile.readline()[:-1]
            if nextLine == sequence:
                foundSequence = True
        
        writeFile = open(writeFileName, 'a')
        writeFile.seek(previousWrite)
        
        if not foundSequence:
            writestring = '> %s_%i\n%s\n' %\
                          (titleLine[:-1],
                           numWrites,
                           sequence)
            writeFile.write(writestring)
            numWrites += 1
        for i in xrange(len(sequence)):
            base = sequence[i]
            
            #getting the bases that the current base isn't
            neighbors = ['U', 'A', 'G', 'C']
            baseIndex = neighbors.index(base)
            neighbors.pop(baseIndex)
            
            for n in neighbors:
                newSequence = sequence[0:i] + n + sequence[i+1:]
                
                previousWrite = writeFile.tell()
                writeFile.close()
                writeFile = open(writeFileName, 'r')
                foundSequence = False
                
                while 1:
                    nextLine = writeFile.readline()
                    if not nextLine:
                        break
                    
                    nextLine = writeFile.readline()[:-1]
                    if nextLine == newSequence:
                        foundSequence = True
                
                writeFile = open(writeFileName, 'a')
                writeFile.seek(previousWrite)
                
                if not foundSequence:
                    writestring = '> %s_%i\n%s\n' %\
                                  (titleLine[:-1],
                                   numWrites,
                                   newSequence)
                    writeFile.write(writestring)
                    numWrites += 1
                
    
    sequenceFile.close()
    writeFile.close()
    
    return numWrites

if __name__ == '__main__':
    main(sys.argv)