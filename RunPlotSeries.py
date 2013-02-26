#!/usr/bin/env python

import os
import sys
import HistoPlot

def main(argv=None):
    #target 1
    #best fold
    data = 'fold and temp/data/target1_BestFold37Tempraw.txt,'
    data += 'fold and temp/data/target1_BestFold50Tempraw.txt,'
    data += 'fold and temp/data/target1_BestFold60Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target1_BestFold.png',
            'target1_BestFold',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #1 fold
    data = 'fold and temp/data/target1_1Folds37Tempraw.txt,'
    data += 'fold and temp/data/target1_1Folds50Tempraw.txt,'
    data += 'fold and temp/data/target1_1Folds60Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target1_1Folds.png',
            'target1_1Folds',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #100 folds
    data = 'fold and temp/data/target1_100Folds37Tempraw.txt,'
    data += 'fold and temp/data/target1_100Folds50Tempraw.txt,'
    data += 'fold and temp/data/target1_100Folds60Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target1_100Folds.png',
            'target1_100Folds',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #37 temp
    data = 'fold and temp/data/target1_BestFold37Tempraw.txt,'
    data += 'fold and temp/data/target1_1Folds37Tempraw.txt,'
    data += 'fold and temp/data/target1_100Folds37Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target1_37Temp.png',
            'target1_37Temp',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #50 temp
    data = 'fold and temp/data/target1_BestFold50Tempraw.txt,'
    data += 'fold and temp/data/target1_1Folds50Tempraw.txt,'
    data += 'fold and temp/data/target1_100Folds50Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target1_50Temp.png',
            'target1_50Temp',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #60 temp
    data = 'fold and temp/data/target1_BestFold60Tempraw.txt,'
    data += 'fold and temp/data/target1_1Folds60Tempraw.txt,'
    data += 'fold and temp/data/target1_100Folds60Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target1_60Temp.png',
            'target1_60Temp',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #target 2
    #best fold
    data = 'fold and temp/data/target2_BestFold37Tempraw.txt,'
    data += 'fold and temp/data/target2_BestFold50Tempraw.txt,'
    data += 'fold and temp/data/target2_BestFold60Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target2_BestFold.png',
            'target2_BestFold',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #1 fold
    data = 'fold and temp/data/target2_1Folds37Tempraw.txt,'
    data += 'fold and temp/data/target2_1Folds50Tempraw.txt,'
    data += 'fold and temp/data/target2_1Folds60Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target2_1Folds.png',
            'target2_1Folds',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #100 folds
    data = 'fold and temp/data/target2_100Folds37Tempraw.txt,'
    data += 'fold and temp/data/target2_100Folds50Tempraw.txt,'
    data += 'fold and temp/data/target2_100Folds60Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target2_100Folds.png',
            'target2_100Folds',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #37 temp
    data = 'fold and temp/data/target2_BestFold37Tempraw.txt,'
    data += 'fold and temp/data/target2_1Folds37Tempraw.txt,'
    data += 'fold and temp/data/target2_100Folds37Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target2_37Temp.png',
            'target2_37Temp',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #50 temp
    data = 'fold and temp/data/target2_BestFold50Tempraw.txt,'
    data += 'fold and temp/data/target2_1Folds50Tempraw.txt,'
    data += 'fold and temp/data/target2_100Folds50Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target2_50Temp.png',
            'target2_50Temp',
            'Score',
            'Frequency']
    HistoPlot.main(plot)
    
    #60 temp
    data = 'fold and temp/data/target2_BestFold60Tempraw.txt,'
    data += 'fold and temp/data/target2_1Folds60Tempraw.txt,'
    data += 'fold and temp/data/target2_100Folds60Tempraw.txt'
    plot = [None,
            data,
            'fold and temp/plots/target2_60Temp.png',
            'target2_60Temp',
            'Score',
            'Frequency']
    HistoPlot.main(plot)

if __name__ == '__main__':
    main(sys.argv)
