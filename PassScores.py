#!/usr/bin/env python

#This will pass random sequences that have already been scored against a
#template. If they pass, they will be written to be saved in the next iteration
#of the entire analysis.

#CURRENT PASS FUNCTION:
#probability = 1 / (score^3 + 1)

#run as "python PassScores.py $1 $2 $3 $4"
#$1 is the maximum number of sequences to pass
#$2 is the file which scores have been written to.
#$3 is the target
#$4 is the save file.

#Written by Aaron Reba

from __future__ import division
import sys
import random

import AddMutation
import MakeMutationNeighbors

#currently passing if equal to template or within 1 base pair of template.
#considering any permutation of the template.

def main(argv=None):
    scored_file_name = argv[2]
    template_file_name = argv[3]
    pass_file_name = argv[4]
    
    scored_file = open(scored_file_name, 'r')
    template_file = open(template_file_name, 'r')
    pass_file = open(pass_file_name, 'w')
    
    try:
        raw_file_name = argv[5]
        raw_file = open(raw_file_name, 'w')
        raw = True
    except:
        raw = False
    
    write_count = 0
    
    top_percentile = 10
    
    template_high_score = 0
    #get the highest template score
    while 1:
        template_line = template_file.readline()
        if not template_line:
            break
        line_score = int(template_line.split(' ')[2])
        if template_high_score < line_score:
            template_high_score = line_score
        template_file.readline()
    template_file.close()
    
    #get the 90th percentile score threshold.
    passed = False
    score_dict = {}
    while 1:
        score_line = scored_file.readline()
        if not score_line:
            break
        
        if 'passed' in score_line:
            passed = True
        
        if 'score:' in score_line:
            if not passed:
                test_score = int(score_line.split(' ')[1])
                if test_score in score_dict.keys():
                    score_dict[test_score] += 1
                else:
                    score_dict[test_score] = 1
            elif passed:
                passed = False
        
    scored_file.seek(0)
    
    
    #go through scores in descending order
    #when the maximum number of scores / 10 have been viewed, break
    scores_viewed = 0
    scores_left = int(argv[1]) / top_percentile
    for score in sorted(score_dict.keys(), reverse=True):
        scores_viewed += score_dict[score]
        if scores_viewed >= int(argv[1]) / top_percentile:
            score_threshold = score
            bottom_threshold_occurances = scores_left
            break
        scores_left -= score_dict[score]
    
    #print bottom_threshold_occurances
    #print score_threshold
    
    previous_write_count = 0
    
    while 1:
        #read score file entry
        title_line = scored_file.readline()
        if not title_line or title_line == '\n':
            break
        
        test_ID = title_line.split(' ')[1]
        
        score_line = scored_file.readline()
        test_score = int(score_line.split(' ')[1])
        
        sequence_line = scored_file.readline()
        
        fold_line = scored_file.readline()
        
        template_line = scored_file.readline()
        
        
        #previously passed, write the entry again
        if 'passed' in test_ID:
            pass_file.write(title_line)
            pass_file.write(score_line)
            pass_file.write(sequence_line)
            pass_file.write(fold_line)
            pass_file.write(template_line)
            
            #do not increment the write count,
            #the only sequences with passed in them are ones generated without
            #amplification.
            #by not incrementing the write count here, it is only incremented
            #on new writes.
            #increment a separate counter
            previous_write_count += 1
            
        else:
            #pass_chance = 1.001
            #if random.random() < pass_chance or\
            
            if test_score > score_threshold or\
            (test_score == score_threshold and\
            0 < bottom_threshold_occurances):
                if test_ID[-1] == '\n':
                    test_ID = test_ID[:-1]
                test_ID = '{0}_passed'.format(test_ID)
                splitTitle = title_line.split(' ')
                splitTitle[1] = test_ID
                newTitle = ' '.join(splitTitle)
                writestring = newTitle
                pass_file.write(writestring)
                
                pass_file.write(score_line)
                pass_file.write(sequence_line)
                pass_file.write(fold_line)
                pass_file.write(template_line)
                
                write_count += 1
                
                if test_score == score_threshold:
                    bottom_threshold_occurances -= 1
                
                if raw:
                    raw_file.write(str(test_score) + '\n')
        
        if write_count == int(argv[1]) / top_percentile:
            break
    
    scored_file.close()
    pass_file.close()
    
    return write_count + previous_write_count

if __name__ == '__main__':
    main(sys.argv)
