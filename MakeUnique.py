#!/usr/bin/env python

import sys

def main(argv=None):
    scoredFile = open(argv[1], 'r')
    scanScoredFile = open(argv[1], 'r')
    
    newFile = open(argv[2], 'w')
    
    while 1:
        scanScoredFile.seek(0)
        

if __name__ == '__main__':
    main(sys.argv)