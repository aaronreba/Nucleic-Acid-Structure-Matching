#!/usr/bin/env python

import numpy
import os
import sys

def main(argv=None):
    ext_dir = argv[1]
    save_as = argv[2]
    
    for dirname, dirnames, filenames in os.walk(ext_dir):
        for filename in filenames:
            
        
if __name__ == '__main__':
    main(sys.argv)