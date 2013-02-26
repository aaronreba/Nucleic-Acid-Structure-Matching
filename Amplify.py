#!/usr/bin/env python

#This will take the sequences that passed and create modified copies to append
#to the new test file.
import os
import random
import sys

def main(argv=None):
    #current method: take those that pass and add a mutation.
    maxPasses = int(argv[1])
    passFileName = argv[2]
    
    mutate = False
    if len(argv) > 3:
        if 'm' in argv[3]:
            mutate = True
            mutationChance = float(argv[4])
    
    passFile = open(passFileName, 'r')
    tempFile = open('temp.txt', 'w')
    
    bases = ('U', 'A', 'G', 'C')
    
    #get the count of the pass file
    passesWritten = 0
    while 1:
        passLine = passFile.readline()
        if not passLine:
            break
        if passLine[0] == '>':
            passesWritten += 1
    passFile.seek(0)
    
    if passesWritten == 0:
        return 0
    
    amplificationsWritten = 0
    
    while amplificationsWritten < maxPasses:
        passFile.seek(0)
        
        copyEntry = random.randint(0, passesWritten - 1)
        
        #os.system('cat {0}'.format(argv[3]))
        #print copyEntry
        
        #skip until the copyEntry'th entry is reached.
        for i in xrange(copyEntry):
            passFile.readline()
            passFile.readline()
            passFile.readline()
            passFile.readline()
            passFile.readline()
        
        entryLine = passFile.readline()
        
        splitEntryLine = entryLine.split(' ')
        passedIndex = splitEntryLine[1].index('_passed')
        lenIDSuffix = len(splitEntryLine[1]) - passedIndex
        passedIndex = entryLine.index('_passed')
        entryLine = entryLine[:passedIndex] + entryLine[passedIndex + lenIDSuffix:]
        
        
        scoreLine = passFile.readline()
        
        sequenceLine = passFile.readline()
        older = sequenceLine[:-1]
        numMutations = 0
        if mutate:
            #roll for mutation
            oldSequence = sequenceLine[:-1]
            newSequence = ''
            for base in oldSequence:
                
                if random.random() < mutationChance:
                    numMutations += 1
                    newBase = base
                    while newBase == base:
                        newBase = bases[random.randint(0, 3)]
                else:
                    newBase = base
                newSequence = '{0}{1}'.format(newSequence, newBase)
            sequenceLine = '{0}\n'.format(newSequence)
        
        if numMutations > 0:
            entryLine = '{0}_{1}M{2}'.format(entryLine[:passedIndex],
                                             numMutations,
                                             entryLine[passedIndex:])
            tempFile.write(entryLine)
            tempFile.write(sequenceLine)
            passFile.readline()
            passFile.readline()
        else:
            tempFile.write(entryLine)
            tempFile.write(scoreLine)
            tempFile.write(sequenceLine)
            tempFile.write(passFile.readline())
            tempFile.write(passFile.readline())
        
        amplificationsWritten += 1
    
    passFile.close()
    tempFile.close()
    
    os.system('mv {0} {1}'.format('temp.txt', argv[2]))
    
    return amplificationsWritten

if __name__ == '__main__':
    main(sys.argv)