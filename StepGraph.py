#!/usr/bin/env python

#$1 scores
#$2 target/template file
#$3 step number

import os
import sys
import matplotlib.pyplot as plt
import numpy
import ScoreRNA
import MakeMutationNeighbors
import HistoPlot
import GetHighestScoreSequences

def main(argv=None):
    scoreFile = open(argv[1], 'r')
    writecount = int(argv[4])
    
    while 1:
        tempScore = open('temp0.txt', 'w')
        scoreLine = scoreFile.readline()
        
        if not scoreLine:
            break
        if writecount == 0:
            break
        
        tempScore.write(scoreLine)
        
        sequenceName = scoreLine.split(' ')[1]
        
        scoreLine = scoreFile.readline()
        score = int(scoreLine.split(' ')[1])
        
        
        sequence = scoreFile.readline()[:-1]
        tempScore.write(sequence)
        fold = scoreFile.readline()[:-1]
        
        scoreFile.readline()
        tempScore.close()
        
        if score <= 2:
            print writecount
            MakeMutationNeighbors.main([None,
                                        'temp0.txt',
                                        'temp1.txt'])
            
            MakeMutationNeighbors.main([None,
                                        'temp1.txt',
                                        'temp2.txt'])
            
            os.system('RNAsubopt -s < temp2.txt > SubOptTestSequences.txt')
            GetHighestScoreSequences.main([None,
                                           'SubOptTestSequences.txt',
                                           'HighestTestSequences.txt',
                                           'temp2.txt'])
            
            ScoreRNA.main([None,
                           'SmallRNA.txt',
                           'HighestTestSequences.txt',
                           'ScoredStep.txt',
                           'RawScore.txt'])
            
            saveto = os.path.join('Plots', sequenceName + '.png')
            
            HistoPlot.main([None,
                            'RawScore.txt',
                            saveto,
                            sequence,
                            'Scores',
                            'Frequency'])
            writecount -= 1

if __name__ == '__main__':
    main(sys.argv)