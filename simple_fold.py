#!/usr/bin/env python

import os
import sys

def main(argv=None):
    sequence_file = open(argv[1], 'r')
    fold_file = open(argv[2], 'w')
    temperature_list = argv[3].split(',')

    i = 0
    for temperature in temperature_list:
        for line in sequence_file:
            if i == 0:
                line = line[:-1] + '_f' + temperature + '\n'
                fold_file.write(line)
                i = 1
            else:
                fold_file.write(line)
                fold_file.write('.' * len(line[:-1]) + ' 0.00 0.00\n')
                rna_pipe = os.popen('echo {0} | RNAfold -T {1} | cut -d " " -f 1'.format(line[:-1], temperature))
                writestring = rna_pipe.readline()
                writestring = rna_pipe.readline()
                if writestring[-1] == '\n':
                    writestring = writestring[:-1]
                writestring = writestring + ' 1.00 0.00\n'
                fold_file.write(writestring)
                i = 0
        sequence_file.seek(0)

    sequence_file.close()
    fold_file.close()

if __name__ == '__main__':
    main(sys.argv)
