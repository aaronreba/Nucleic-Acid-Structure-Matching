#!/usr/bin/env python

#$1: data file. This should be in the format like so:
#1 1
#2 2
#4 3
#5 5
#6 1
#8 2
#Two columns only. X value on the left. Y value on the right.
#$2: save name
#$3: title
#$4: x label
#$5: y label
#$6: linewidth

import matplotlib.pyplot as plt
import numpy
import sys

def main(argv=None):
    data = numpy.genfromtxt(argv[1], names=('n1', 'n2'))
    
    plt.title(argv[3])
    plt.xlabel(argv[4])
    plt.ylabel(argv[5])
    linewidth = float(argv[6])
    plt.plot(data['n1'], data['n2'], 'g-', linewidth=linewidth)
    plt.savefig(argv[2])
    plt.clf()

if __name__ == '__main__':
    main(sys.argv)
    