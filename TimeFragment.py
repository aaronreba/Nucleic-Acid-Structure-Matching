#!/usr/bin/env python

import os
import sys

def main(argv=None):
    fold_name = argv[1]
    base_save_name = argv[2]
    
    fold_file = open(fold_name, 'r')
    
    title_line = fold_file.readline()
    sequence_line = fold_file.readline()
    
    last_time = -1
    file_number = 0
    
    current_file = open('{0}{1}'.format(file_number, base_save_name), 'w')
    current_file.write(title_line)
    current_file.write(sequence_line)
    
    for fold_line in fold_file:
        split_fold_line = fold_line[:-1].split()
        
        if float(split_fold_line[2]) <= last_time:
            current_file.close()
            file_number += 1
            current_file = open('{0}{1}'.format(file_number, base_save_name), 'w')
            current_file.write(title_line)
            current_file.write(sequence_line)
        
        current_file.write(fold_line)
        last_time = float(split_fold_line[2])
    current_file.close()

if __name__ == '__main__':
    main(sys.argv)