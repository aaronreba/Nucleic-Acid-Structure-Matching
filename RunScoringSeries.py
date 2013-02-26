#!/usr/bin/env python

import runRNAscoring
import HistoPlot
import CheckTarget
import sys
import os

def main(argv=None):
    targetFile = argv[1]
    
    CheckTarget.main([None,
                      targetFile])
    
    target_open = open(targetFile, 'r')
    target_open.readline()
    target = target_open.readline()
    if target[-1] == '\n':
        target = target[:-1]
    
    raw_names = []
    raw_names.append('1mil_100len_best.txt')
    #raw_names.append('1mil_100len_r1.txt')
    #raw_names.append('1mil_100len_r10.txt')
    #raw_names.append('1mil_100len_r100.txt')
    #raw_names.append('1mil_100len_r1000.txt')
    
    test = [None, '30000', '100', targetFile, 'dna', 'b', 'raw', raw_names[0]]
    runRNAscoring.main(test)
    
    #test = [None, '1000000', '100', targetFile, 'dna', 'b', 'r', '1', 'raw', raw_names[1]]
    #runRNAscoring.main(test)
    #
    #test = [None, '1000000', '100', targetFile, 'dna', 'b', 'r', '10', 'raw', raw_names[2]]
    #runRNAscoring.main(test)
    #
    #test = [None, '1000000', '100', targetFile, 'dna', 'b', 'r', '100', 'raw', raw_names[3]]
    #runRNAscoring.main(test)
    #
    #test = [None, '1000000', '100', targetFile, 'dna', 'b', 'r', '1000', 'raw', raw_names[4]]
    #runRNAscoring.main(test)
    
    for name in raw_names:
        HistoPlot.main([None,
                        name,
                        os.path.join('Plots', 'Preliminary', targetFile + name + '.png'),
                        target,
                        'Score',
                        'Score Frequency'
                        ])

if __name__ == '__main__':
    main(sys.argv)
    