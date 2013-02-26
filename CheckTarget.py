#!/usr/bin/env python

#will add max score of target.
#will overwrite any previous score.
#$1: target file

import sys
import os
import MakeDecodedRNAStaticBinds

def main(argv=None):
    targetFileName = argv[1]
    targetFile = open(targetFileName, 'r')
    noScoreList = []
    currentTarget = 0
    
    tempFile = open('targetTemp.txt', 'w')
    while 1:
        titleTargetLine = targetFile.readline()
        if not titleTargetLine:
            break
        elif titleTargetLine == '\n':
            continue
        
        targetLine = targetFile.readline()
        
        #get max score
        targetSequence = targetLine[:-1]
        parsedTarget = MakeDecodedRNAStaticBinds.main([None,
                                                       targetSequence,
                                                       '-exitparse'])
        
        #making the template into a string
        #the template <2<[2]TGAC>2>
        #would be converted to: "<<**TGAC>>"
        fullTemplateString = ''
        preceeding = False
        proceeding = False
        
        for value in parsedTarget[0]:
            if type(value) == type(''):
                if value == '<':
                    preceeding = True
                elif value == '>':
                    proceeding = True
                else:
                    fullTemplateString += value
            else:
                if preceeding:
                    fullTemplateString += '<' * value
                    preceeding = False
                elif proceeding:
                    fullTemplateString += '>' * value
                    proceeding = False
                else:
                    fullTemplateString += 'N' * value
        
        maxScore = 0
        for character in fullTemplateString:
            if character in 'UGACT':
                maxScore += 2
            elif character in '<RY':
                maxScore += 1
        
        
        tempFile.write('> ')
        if titleTargetLine.split(' ')[1][-1] == '\n':
            tempFile.write(titleTargetLine.split(' ')[1][:-1])
        else:
            tempFile.write(titleTargetLine.split(' ')[1])
        tempFile.write(' {0}\n'.format(maxScore))
        tempFile.write(targetLine)
    
    targetFile.close()
    tempFile.close()
    os.system('mv targetTemp.txt {0}'.format(argv[1]))

if __name__ == '__main__':
    main(sys.argv)
