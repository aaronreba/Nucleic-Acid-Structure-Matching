#!/usr/bin/env python

from __future__ import division

import sys
import os
import re
import matplotlib.pyplot as plt

def main(argv=None):
    score_dir = argv[1]
    
    colors = [('#000000'), ('#FF0000'), ('#00FF00'), ('#0000FF'), ('#FFCC00'), ('#FF00FF'), ('#00FFFF'), ('#0066FF'), ('#007700'), ('#CC9999')]
    colorcycle = 0
    maxY = 0
    reached_max = 0
    max_score = 20
    
    for dirname, dirnames, filenames in os.walk(score_dir):
        for filename in filenames:
            if filename[-4:] != '.txt':
                continue
            xAxis = []
            yAxis = []
            fold_file = open(os.path.join(dirname, filename), 'r')
            #time_index = 0
            #total_score = 0
            #num_entries = 0
            while 1:
                fold_line = fold_file.readline()
                if not fold_line or fold_line == '\n':
                    break
                fold = fold_line.split(' ')[0]
                
                try:
                    time = float(re.sub(' +', ' ', fold_line[:-1]).split(' ')[2])
                except:
                    print fold_line
                    raise frownyface
                temp_file = open('tempfold.txt', 'w')
                temp_file.write('> a_sequence\n')
                temp_file.write('z' * len(fold) + '\n')
                temp_file.write(fold + '\n')
                temp_file.close()
                os.system('python ScoreRNA.py StructureBulge.txt tempfold.txt TargetRepresentation.txt ScoredRNA.txt raw1fold.txt')
                
                #if time > time_index + 5:
                #    xAxis.append(time_index)
                #    yAxis.append(total_score / num_entries)
                #    time_index += 5
                #    total_score = 0
                #    num_entries = 0
                
                single_score_file = open('raw1fold.txt', 'r')
                single_score = int(single_score_file.readline()[:-1])
                single_score_file.close()
                
                #total_score += single_score
                #num_entries += 1
                
                #xAxis.append(time_index)
                #yAxis.append(total_score / num_entries)
                xAxis.append(time)
                if len(yAxis) > 0:
                    if yAxis[-1] > single_score:
                        yAxis.append(yAxis[-1])
                    else:
                        yAxis.append(single_score)
                else:
                    yAxis.append(single_score)
                if single_score > maxY:
                    maxY = single_score
            
            if maxY == max_score:
                reached_max += 1
            
            plt.plot(xAxis, yAxis, color=colors[colorcycle])
            colorcycle+=1
            if colorcycle == len(colors):
                colorcycle = 0
    plt.plot(0, maxY + 1)
    plt.xlabel('Time')
    plt.ylabel('Score')
    plt.savefig('SequenceOverTime/Folds.png')
    plt.clf()
    print '{0} out of 100 had a maximum score.'.format(reached_max)

if __name__ == '__main__':
    main(sys.argv)
