#!/usr/bin/env python

#parameters:
#$1 is the score file to read
#$2 is the save Directory name
#$3 is the score threshold

import os
import sys
import numpy
import MakeMutationNeighbors

def main(argv=None):
    scoredFile = open(argv[1], 'r')
    saveDir = argv[2]
    threshold = int(argv[3])
    
    while 1:
        scoreLine = scoredFile.readline()
        if not scoreLine:
            break
        
        sequenceName = scoreLine.split(' ')[1]
        
        saveFileName = os.path.join(saveDir, sequenceName)
        
        
    
    scoredFile.close()

if __name__ == '__main__':
    main(sys.argv)