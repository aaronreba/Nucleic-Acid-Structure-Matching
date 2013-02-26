#!/usr/bin/env python

from __future__ import division
import os
import sys
import numpy
import matplotlib.pyplot as plt

def main(argv=None):
    save_as = argv[1]
    
    input_files = []
    max_scores = []
    
    for i in argv[2:]:
        input_files.append(i.split(',')[0])
        max_scores.append(int(i.split(',')[1]))
    
    colors=['r', 'g', 'b', 'y', 'k', 'm']
    colorcycle = 0
    
    plt.yscale('log')
    
    for i, (input_file, max_score) in enumerate(zip(input_files, max_scores)):
        input_data = numpy.genfromtxt(input_file, dtype=None, names=('data'))
        input_bins = numpy.bincount(input_data['data'])
        
        if len(input_bins) == max_score + 1:
            plt.plot(i + 1, input_bins[-1] / len(input_data['data']), colors[colorcycle] + 'o')
        
        colorcycle += 1
        if colorcycle == len(colors):
            colorcycle = 0
    
    plt.xlabel('Structure')
    plt.ylabel('% Perfect Scoring Sequences')
    
    plt.savefig(save_as)
    plt.clf()

if __name__ == '__main__':
    main(sys.argv)