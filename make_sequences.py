#!/usr/bin/env python

#This makes many random sequences given  the number of sequences to make and
#the length of the sequences. The sequences are saved as the given file name.

import random
import sys
import argparse

def main(argv=None):
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-n',
                        '--number',
                        action='store',
                        dest='number_of_sequences',
                        type=int,
                        required=True,
                        help='Number of sequences to generate')
    
    parser.add_argument('-l',
                        '--length',
                        action='store',
                        dest='length',
                        type=int,
                        required=True,
                        help='Length of sequences to generate')
    
    parser.add_argument('-t',
                        '--title',
                        action='store',
                        dest='sequence_title',
                        type=str,
                        default='Sequence',
                        help='Prefixed title of sequences')
    
    parser.add_argument('-f',
                        '--file',
                        action='store',
                        dest='save_file_name',
                        default='',
                        type=str,
                        help='File in which to save sequences')
    
    parser.add_argument('-a',
                        '--acid',
                        action='store',
                        dest='acid_type',
                        type=str,
                        choices='rd',
                        required=True,
                        help='Specify RNA or DNA sequences')
    
    args = parser.parse_args(argv)
    
    number_of_sequences = args.number_of_sequences
    length = args.length
    sequence_title = args.sequence_title
    save_file_name = args.save_file_name
    acid_type = args.acid_type
    
    if save_file_name == '':
        write_to_file = False
    else:
        write_to_file = True
        save_file = open(save_file_name, 'w')
    
    if acid_type == 'r':
        bases = ('U', 'A', 'G', 'C')
    elif acid_type == 'd':
        bases = ('T', 'A', 'G', 'C')
    
    
    for i in xrange(number_of_sequences):
        write_title = '> {0}_{1}\n'.format(sequence_title, i)
        
        write_sequence = ''
        for i in xrange(length):
            new_base = random.randint(0, 3)
            write_sequence += bases[new_base]
        write_sequence += '\n'
        
        if write_to_file:
            save_file.write(write_title)
            save_file.write(write_sequence)
        else:
            print write_title[:-1]
            print write_sequence[:-1]
    
    if write_to_file:
        save_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])

