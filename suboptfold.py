import sys
import os
import re
seqfile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')
for line in seqfile:
    if line[-1] == '\n':
        line = line[:-1]

    if line[0] == '>':
        outfile.write(line + '\n')
    else:
        outfile.write(line + '\n')
        suboptp = os.popen("echo \"%s\" | RNAsubopt" % line)
        suboptp.readline()
        for subline in suboptp:
            outfile.write('.' * len(line) + ' 0.00 0.00\n')
            if subline[-1] == '\n':
                subline = subline[:-1]
            subline = re.sub(' +', ' ', subline)
            outfile.write(subline + ' 1.00\n')
seqfile.close()
outfile.close()
