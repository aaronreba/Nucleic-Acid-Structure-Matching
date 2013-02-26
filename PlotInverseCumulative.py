#!/usr/bin/env python

from __future__ import division

import sys
import os

import numpy
import matplotlib.pyplot as plt
import matplotlib.legend as legend

#parameter format:
#$1: savename
#$2: dir_A,functional_score_A
#$3: dir_B,functional_score_B
#$4:....
#only put spaces between datasets.

def main(argv=None):
    save_name = argv[1]
    
    colors=['r', 'g', 'b', 'y', 'k', 'm']
    colorcycle = 0
    
    score_dirs = []
    functional_scores = []
    
    plt.xscale('log')
    plt.yscale('log')
    
    if argv[2] == 'bin':
        bin = True
    else:
        bin = False
    
    if not bin:
        for arg in argv[2:]:
            score_dir = arg.split(',')[0]
            functional_score = int(arg.split(',')[1])
            
            score_dirs.append(score_dir)
            functional_scores.append(functional_score)
        
        for score_dir, functional_score in zip(score_dirs, functional_scores):
            x_axis = []
            y_axis = []
            
            functional_count = []
            
            
            
            for dirname, dirnames, filenames in os.walk(score_dir):
                for score_file in filenames:
                    full_score_file_name = os.path.join(score_dir, score_file)
                    score_data = numpy.genfromtxt(full_score_file_name, dtype=None, names=('data'))
                    
                    frequency = numpy.bincount(score_data['data'])
                    trajectory_count = sum(frequency)
                    
                    if len(frequency) == functional_score + 1:
                        functional_count.append(frequency[-1])
                    else:
                        functional_count.append(0)
            
            functional_count.sort()
            
            print functional_count
            
            functional_frequency = numpy.bincount(functional_count)
            
            print functional_frequency
            
            current_step = 1
            
            for i, frequency in enumerate(functional_frequency):
                x_axis.append(i / functional_score)
                y_axis.append(current_step)
                
                current_step -= (frequency / len(filenames))
            
            #if len(x_axis) != functional_score:
            #    x_axis.append(1.0)
            #    y_axis.append()
            print score_dir
            print x_axis
            print y_axis
            plt.step(x_axis, y_axis, colors[colorcycle])
            colorcycle += 1
            if colorcycle == len(colors):
                colorcycle = 0
    else:
        plt.plot(1,1)
        lines = []
        #ax = plt.subplot(221)
        for filename in argv[3:]:
            x_axis = []
            y_axis = []
            
            functional_count = numpy.genfromtxt(filename, dtype=None, names=('data'))['data']
            
            functional_count.sort()
            
            functional_frequency = numpy.bincount(functional_count)
            
            current_step = 1
            
            for i, frequency in enumerate(functional_frequency):
                x_axis.append(i / 10000)
                y_axis.append(current_step)
                
                current_step -= (frequency / 10000)
            
            lines.append(plt.plot(y_axis, x_axis, colors[colorcycle], linestyle='steps-pre', label=filename))
            colorcycle += 1
            
            if colorcycle == len(colors):
                colorcycle = 0
        #ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(save_name)
    plt.clf()

if __name__ == '__main__':
    main(sys.argv)