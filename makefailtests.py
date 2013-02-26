#!/usr/bin/env python

failrun = open('runfails2.txt', 'w')
allfails = open('allfails.txt', 'r')

failrun.write('#!/bin/bash\n')

while 1:
    line = allfails.readline()
    if line == '\n':
        continue
    if not line:
        break
    sequence = line
    commandline = allfails.readline()
    failrun.write('echo "{0}"; '.format(sequence[:-1]))
    failrun.write('echo "{0}" | '.format(sequence[:-1]))
    failrun.write(commandline[:commandline.index('<') - 1] + '\n')

failrun.close()
allfails.close()
