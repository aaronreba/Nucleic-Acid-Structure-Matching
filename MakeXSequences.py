import os
import sys
import MakeG

def main(argv=None):
    start = int(argv[1])
    end = int(argv[2])
    step = int(argv[3])
    base_save = argv[4]
    for i in xrange(start, end, step):
        MakeG.main([None, argv[3], '100', '-n', base_save + 'Sequences' + str(i) + '-' + str(i + step - 1) + '.txt', '1', str(i), 'rna'])

if __name__ == '__main__':
    main(sys.argv)
