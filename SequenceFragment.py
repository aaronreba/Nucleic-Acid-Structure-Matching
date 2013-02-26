#!/usr/bin/env python

import os
import sys

def main(argv=None):
    big_file_name = argv[1]
    tiny_file_base_name = argv[2]
    segment_size = int(argv[3])
    
    big_file = open(big_file_name, 'r')
    tiny_file = open('0{0}'.format(tiny_file_base_name), 'w')
    
    current_sequence = -1
    current_segment = 0
    
    for big_line in big_file:
        if big_line[0] == '>':
            current_sequence += 1
            
            if current_sequence == segment_size:
                current_sequence = 0
                current_segment += 1
                
                tiny_file.close()
                
                tiny_file = open('{0}{1}'.format(current_segment, tiny_file_base_name), 'w')
        tiny_file.write(big_line)
                
    tiny_file.close()
    
    #if current_sequence == 0:
    #    os.remove('{0}{1}'.format(current_segment, tiny_file_base_name))

if __name__ == '__main__':
    main(sys.argv)
