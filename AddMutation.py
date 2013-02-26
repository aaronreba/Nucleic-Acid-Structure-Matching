#!/usr/bin/env python

#Given a string of bases, this will randomly change one base and return the
#new string made

#run as "python AddMutation.py $1"
#$1 is the RNA string to be mutated.

#This returns a python string and does not write to a file.

#Written by Aaron Reba

import sys
import random


def main(argv=None):
    mutateMe = argv[1]
    
    bases = ('U', 'A', 'G', 'C')
    
    newIndex = random.randint(1, len(mutateMe))
    newBase = bases[random.randint(0, 3)]
    
    newSequence = mutateMe[0:newIndex - 1] + newBase + mutateMe[newIndex:]
    
    return newSequence

if __name__ == '__main__':
    main(sys.argv)