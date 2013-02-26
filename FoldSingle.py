import sys
import os

def main(argv=None):
    readme = open('TestSequences.txt', 'r')
    i = 1
    while 1:
        readline = readme.readline()
        if not readline:
            break
        readline = readme.readline()[:-1]
        call = 'Kinfold --num=10 --stop < echo "{0}" > SequenceOverTime/Fold{1}.txt'.format(readline, i)
        print call
        os.system(call)
        i += 1

if __name__ == '__main__':
    main(sys.argv)
