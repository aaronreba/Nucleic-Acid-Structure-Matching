import subprocess
import sys

def main(argv=None):
    for i in xrange(100):
        seed = '{0}={1}={2}'.format(i, i + 1, i + 2)
        subprocess.call('echo "{0}" | Kinfold --time=100 --stop --seed={1} > SequenceOverTime/Fold{2}.txt'.format(argv[1], seed, i + 1), shell=True)

if __name__ == '__main__':
    main(sys.argv)
