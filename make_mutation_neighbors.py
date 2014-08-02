#!/usr/bin/env python

#Given a sequence of RNA, this will find d mutation neighbors of that
#sequence.

import sys
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i',
                        '--in-file',
                        action='store',
                        dest='in_file_name',
                        type=str,
                        required=True,
                        help='File from which to load parent sequence(s)')
    
    parser.add_argument('-o',
                        '--out-file',
                        action='store',
                        dest='out_file_name',
                        default='',
                        type=str,
                        help='File in which to save sequences')
    
    parser.add_argument('-a',
                        '--acid',
                        action='store',
                        dest='acid_type',
                        type=str,
                        choices=['rna', 'dna'],
                        required=True,
                        help='Specify RNA or DNA sequences')
    
    parser.add_argument('-d',
                        '--distance',
                        action='store',
                        dest='distance',
                        type=int,
                        required=True,
                        help='Generate neighbors up to this hamming distance.')
    
    args = parser.parse_args(argv)
    
    in_file_name = args.in_file_name
    out_file_name = args.out_file_name
    acid_type = args.acid_type
    distance = args.distance
    
    in_file = open(in_file_name, 'r')
    
    if out_file_name == '':
        out_file = sys.stdout
    else:
        out_file = open(out_file_name, 'w')
    
    if acid_type == 'rna':
        bases = ('U', 'A', 'G', 'C')
    elif acid_type == 'dna':
        bases = ('T', 'A', 'G', 'C')
    
    generated_neighbor_set = set()
    while 1:
        #python 2.x has dumb scoping rules, so number_of_writes is a length 1
        #list with a single value
        title_line = in_file.readline()
        sequence_line = in_file.readline()
        
        if not title_line:
            break
        
        title = title_line[2:-1] #skipping the '> ' and '\n'
        sequence = sequence_line[:-1] #skipping the '\n'
        
        #generating...
        all_neighbors = []
        all_neighbors.append(sequence)
        
        def get_distance_1_neighbors(sequence):
            distance_1_neighbors = []
            for i, base in enumerate(sequence):
                left_side_sequence = sequence[:i]
                right_side_sequence = sequence[i + 1:]
                mutated_bases =\
                        [
                            template_base
                            for template_base
                            in bases
                            if template_base != base
                        ]
                distance_1_neighbors +=\
                        [
                            ''.join([left_side_sequence, mutated_base, right_side_sequence])
                            for mutated_base
                            in mutated_bases
                        ]
            return distance_1_neighbors
        
        for i in xrange(distance):
            current_neighbors = list(all_neighbors)
            for neighbor in current_neighbors:
                generated_neighbors = get_distance_1_neighbors(neighbor)
                [
                    all_neighbors.append(generated_neighbor)
                    for generated_neighbor
                    in generated_neighbors
                    if generated_neighbor not in all_neighbors
                ]
        
        #writing...
        number_of_writes = [0]
        
        def attempt_to_write(write_sequence):
            #title line
            outstring = '> %s_%i\n' %\
                    (
                        title,
                        number_of_writes[0]
                    )
            out_file.write(outstring)
            
            #sequence line
            outstring = '%s\n' %\
                    (
                        write_sequence
                    )
            out_file.write(outstring)
            
            number_of_writes[0] += 1
        
        map(attempt_to_write, all_neighbors)
    
    in_file.close()
    out_file.close()
    
    #return number_of_writes; legacy?

if __name__ == '__main__':
    main(sys.argv[1:])

