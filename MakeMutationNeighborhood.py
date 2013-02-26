#!/usr/bin/env python

import sys
import os

import MakeMutationNeighbors

def main(argv=None):
    examine_file_name = argv[1]
    num_neighbors = int(argv[2])
    save_file_name = argv[3]
    
    examine_file = open(examine_file_name, 'r')
    
    while 1:
        examine_line = examine_file.readline()
        
        if not examine_line:
            break
        
        if examine_line[0] == '>':
            examine_ID = examine_line.split(' ')[1]
            if examine_ID[-1] == '\n':
                examine_ID = examine_ID[:-1]
            
            #the next lines will either be a "score: x" line or a sequence
            examine_line = examine_file.readline()
            
            if 'score:' in examine_line:
                examine_line = examine_file.readline()
            
            if examine_line[-1] == '\n':
                examine_line = examine_line[:-1]
            
            temp_name = 'neighbortemp.txt'
            temp_file = open(temp_name, 'w')
            temp_file.write('> {0}\n'.format(examine_ID))
            temp_file.write(examine_line + '\n')
            temp_file.close()
            
            #examine_line is now a sequence
            for i in xrange(num_neighbors):
                temp_neighbor_file_name = str(i + 1) + 'neighbortemp.txt'
                
                if i == 0:
                    MakeMutationNeighbors.main([None,
                                                temp_name,
                                                temp_neighbor_file_name])
                    
                else:
                    MakeMutationNeighbors.main([None,
                                                previous_neighbor_file_name,
                                                temp_neighbor_file_name])
                
                previous_neighbor_file_name = temp_neighbor_file_name
            
            os.rename(temp_neighbor_file_name, save_file_name)
            

if __name__ == '__main__':
    main(sys.argv)