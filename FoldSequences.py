#!/usr/bin/env python

#Assuming an RNAsubopt has been run on a file of sequences, this will modify
#the file to be used in runRNAscoring.py.

#Written by Aaron Reba

import sys
import os
#import CombineFolds

def main(argv=None):
    call_sequence = argv[1]
    population = int(argv[2])
    
    unique_id = argv[3]
    
    full_data = False
    
    specify_final = False
    final_save = None
    
    for option in argv:
        if specify_final:
            final_save = option
            specify_final = False
        
        if option == 'full':
            full_data = True
        elif option == 'final':
            specify_final = True
    
    if final_save == None:
        final_save = 'HighestTestSequences.txt'
    
    call = call_sequence.split(' ')
    
    # < TestSequences.txt > SubOptTestSequences.txt 2> dummy.txt
    
    #split the sequence file (call[-5]) into files of size 20k
    #(2 lines per sequence)
    #Vienna only handles a maximum of ~15k for some reason...
    #Kinfold: 1 at a time
    
    if 'RNAsubopt' in call_sequence:
        i = 0
        sequence_file = open(call[-5], 'r')
        
        temp_call = call
        temp_call[-5] = 'tempseq.txt'
        temp_call[-3] = 'tempsubopt.txt'
        temp_call = ' '.join(temp_call)
        
        #clear the output file
        subopt_file = open('SubOptTestSequences.txt', 'w')
        subopt_file.close()
        print population
        while i < population:
            temp_sequence_file = open('tempseq.txt', 'w')
            j = 0
            while j < 20000:
                sequence_line = sequence_file.readline()
                if not sequence_line:
                    break
                temp_sequence_file.write(sequence_line)
                j += 1
            temp_sequence_file.close()
            print temp_call
            os.system(temp_call)
            
            os.system('cat {0} >> {1}'.format('tempsubopt.txt', 'SubOptTestSequences.txt'))
            
            i += 10000
        sequence_file.close()
        
        subopt_file = open('SubOptTestSequences.txt', 'r')
        
        if '-p' in call:
            sequence_file = open(call[-5], 'r')
            sample = int(call[call.index('-p') + 1])
        
        out_file = open(final_save, 'w')
        
        while 1:
            line = subopt_file.readline()
            
            if not line or len(line) == 1:
                break
            
            if line[0] == '>':
                #always skip next line
                subopt_file.readline()
                
                if '-s' in call:
                    subopt_line = subopt_file.readline()
                    sequence = subopt_line.split(' ')[0]
                    
                    subopt_line = subopt_file.readline()
                    fold = subopt_line.split(' ')[0]
                    
                    out_file.write(line)
                    out_file.write(sequence + '\n')
                    out_file.write(fold + '\n')
                    
                elif '-p' in call:
                    #skip ID
                    sequence_file.readline()
                    
                    sequence = sequence_file.readline()
                    
                    out_file.write(line)
                    out_file.write(sequence)
                    for i in xrange(sample):
                        out_file.write(subopt_file.readline())
        
        subopt_file.close()
        out_file.close()
        if '-p' in call:
            sequence_file.close()
    
    elif 'Kinfold' in call_sequence:
        sequence_file = open(call[-1], 'r')
        
        temp_seq_file_name = str(unique_id) + 'tempseq.txt'
        temp_subopt_file_name = str(unique_id) + 'tempsubopt.txt'
        temp_single_fold_file_name = str(unique_id) + 'tempsingle.txt'
        subopt_file_name = str(unique_id) + 'SubOptTestSequences.txt'
        
        subopt_file = open(subopt_file_name, 'w')
        subopt_file.close()
        
        while 1:
            name_line = sequence_file.readline()
            sequence_line = sequence_file.readline()
            
            if not name_line:
                break
            
            temp_subopt_file = open(temp_subopt_file_name, 'w')
            temp_subopt_file.close()
            
            temp_fold_file = open(temp_seq_file_name, 'w')
            temp_fold_file.write(sequence_line)
            temp_fold_file.close()
            
            temp_call = list(call)
            temp_call.append('>')
            temp_call.append(temp_single_fold_file_name)
            temp_call.append('2>')
            temp_call.append('dummy.txt')
            
            temp_call[-5] = temp_seq_file_name
            
            trajectories = int(temp_call[2][temp_call[2].index('=') + 1:])
            temp_call[2] = '--num=1'
            
            kinfold_seed = int(temp_call[3][7])
            
            temp_call = ' '.join(temp_call)
            #print temp_call
            #it's possible that Kinfold can segfault on certain trajectories.
            #if it does, retry until a trajectory that doesn't segfault is found
            
            for i in xrange(trajectories):
                result = -1
                while result != 0:
                    result = os.system(temp_call)
                    
                    if result != 0:
                        print 'Failure'
                        print 'sequence: {0}'.format(sequence_line)
                        print 'seed: ', '--seed={0}={1}={2}'.format(
                            kinfold_seed,
                            kinfold_seed + 1,
                            kinfold_seed + 2)
                    
                    temp_call = temp_call.split(' ')
                    
                    
                    
                    
                    new_seed = '--seed={0}={1}={2}'.format(
                        kinfold_seed,
                        kinfold_seed + 1,
                        kinfold_seed + 2)
                    kinfold_seed += 1
                    temp_call[3] = new_seed
                    temp_call = ' '.join(temp_call)
                
                
                temp_call = temp_call.split(' ')
                new_seed = '--seed={0}={1}={2}'.format(
                    kinfold_seed,
                    kinfold_seed + 1,
                    kinfold_seed + 2)
                kinfold_seed += 1
                temp_call[3] = new_seed
                temp_call = ' '.join(temp_call)
                
                #write single trajectory to new file
                #append this file to file with all folds
                os.system('cat {0} >> {1}'.format(temp_single_fold_file_name,
                                                  temp_subopt_file_name))
            
            #if os.system(temp_call) != 0:
            #    os.system('echo "{0}" > error/{1}'.format(temp_call, sequence_line[:-1]))
            
            subopt_file = open(subopt_file_name, 'a')
            subopt_file.write(name_line)
            subopt_file.write(sequence_line)
            subopt_file.close()
            
            os.system('sed \'s/\s\+/ /g\' {0} | cut -d " " -f 1-3 >> {1}'.format(
                temp_subopt_file_name,
                subopt_file_name))
            
            
            
        os.system('mv {0} {1}'.format(subopt_file_name, final_save))
        os.remove(temp_seq_file_name)
        os.remove(temp_single_fold_file_name)
        os.remove(temp_subopt_file_name)
        os.system('date')
        #print 'Completed Folding of {0}'.format(sequence_file)
    
if __name__ == '__main__':
    main(sys.argv)
