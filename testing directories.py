#!/usr/bin/env python

import sys
import os

def main(argv=None):
    os.system('cd ..; ls')
    os.system('ls')

if __name__ == '__main__':
    main(sys.argv)
