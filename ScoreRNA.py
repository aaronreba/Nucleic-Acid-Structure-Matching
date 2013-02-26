#!/usr/bin/env python

#This will score random sequences to the best matching template. One point is
#given for each base in the random sequence that matches the template. One point
#is given for each bind that matches the template's bind as well (excluding .)

#It is assumed the template has the format that would be created by
#"MakeDecodedRNA.py" and the random sequences have the format created by
#"GetHighestScoreSequences.py" 

#$1 is the template file.
#$2 is the random sequence file.
#$3 is the save file.
#$4 is an optional parameter. it is a file that will hold just the scores.

#Written by Aaron Reba

import MakeDecodedRNAStaticBinds

import sys
import csv
import os
import operator

def main(argv=None):
    templateFileName = argv[1]
    testFileName = argv[2]
    templateRepresentationFileName = argv[3]
    writeFileName = argv[4]
    
    
    
    templateFile = open(templateFileName, 'r')
    testFile = open(testFileName, 'r')
    writeFile = open(writeFileName, 'w')
    
    raw = False
    rawFileName = None
    
    rawFold = False
    rawFoldDir = None
    
    chrono = False
    chronoDir = None
    
    threshold = False
    thresholdValue = None
    
    for option in argv[5:]:
        if raw:
            rawFileName = option
            rawFile = open(rawFileName, 'w')
            raw = False
        elif chrono:
            chronoDir = option
            chrono = False
        elif rawFold:
            rawFoldDir = option
            rawFold = False
        elif threshold:
            thresholdValue = option
            threshold = False
        
        if option == 'raw':
            raw = True
        elif option == 'chrono':
            chrono = True
        elif option == 'rawfold':
            rawFold = True
        elif option == 'threshold':
            threshold = True
    
    templates = []
    #each entry in templates is like so:
    #(templateName, templateSequence, length, string representation)
    
    while 1:
        templateLine = templateFile.readline()
        if not templateLine:
            break
        
        templateSequenceName = templateLine.split(' ')[1]
        maxTemplateScore = int(templateLine.split(' ')[2])
        
        templateLine = templateFile.readline()
        templateSequence = templateLine.split(' ')[0]
        
        parsedTemplateInternal = MakeDecodedRNAStaticBinds.main([None,
                                                                 templateSequence,
                                                                 '-exitparse'])
        
        for eachTemplateInternal in parsedTemplateInternal:
            #get string representation
            preceeding = False
            proceeding = False
            fullTemplateString = ''
            for value in eachTemplateInternal:
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
            
            #append new entry
            templates.append((templateSequenceName,
                              templateSequence,
                              len(fullTemplateString),
                              fullTemplateString))
    
    writeTemplateFile = open(templateRepresentationFileName, 'w')
    writeTemplate = lambda x: writeTemplateFile.write('{0}\t{1}\n'.format(x[0], x[3]))
    map(writeTemplate, templates)
    writeTemplateFile.close()
    
    scoreCommand = './ScoreRNA {0} {1} {2}'.format(
        templateRepresentationFileName,
        testFileName,
        writeFileName
        )
    
    if chronoDir != None:
        scoreCommand += ' chrono {0}'.format(chronoDir)
    if rawFoldDir != None:
        scoreCommand += ' rawfold {0}'.format(rawFoldDir)
    if thresholdValue != None:
        scoreCommand += ' threshold {0}'.format(thresholdValue)
    os.system(scoreCommand)
    
    writeFile = open(writeFileName, 'r')
    
    if rawFileName != None:
        for scoreLine in writeFile:
            if scoreLine[:6] == 'score:':
                rawFile.write(scoreLine[7:])
        rawFile.close()
    
    os.remove(templateRepresentationFileName)
    #'''
    #currentRun = 1
    #scoredFoldDict = {}
    #while 1:
    #    testLine = testFile.readline()
    #    titleLine = testLine
    #    
    #    if not testLine:
    #        break
    #    
    #    testSequenceName = testLine.split(' ')[1]
    #    
    #    testLine = testFile.readline()
    #    
    #    if 'score' in testLine:
    #        writeFile.write(titleLine)
    #        writeFile.write(testLine)
    #        writeFile.write(testFile.readline())
    #        writeFile.write(testFile.readline())
    #        writeFile.write(testFile.readline())
    #        bestScore = testLine.split(' ')[1]
    #    else:
    #        testSequence = testLine[:-1]
    #        
    #        bindingList = []
    #        while 1:
    #            previousPosition = testFile.tell()
    #            testLine = testFile.readline()
    #            
    #            if not testLine:
    #                break
    #            
    #            if testLine[0] == '>':
    #                testFile.seek(previousPosition)
    #                break
    #            
    #            testBinding = testLine.split(' ')[0]
    #            
    #            if testBinding[-1] == '\n':
    #                testBinding = testBinding[:-1]
    #                
    #            if testBinding not in bindingList:
    #                bindingList.append(testBinding)
    #        print len(bindingList)
    #        print currentRun
    #        
    #        currentFoldScore = 0
    #        currentCharacterScore = 0
    #        
    #        bestCharacterScore = -1
    #        bestFoldScore = -1
    #        bestTotalScore = -1
    #        
    #        bestSequence = None
    #        bestFold = None
    #        bestScoreIndex = None
    #        
    #        bestTemplate = None
    #        bestTemplateIndex = None
    #        
    #        for eachTemplateIndex, eachTemplate in enumerate(templates):
    #            #there are len(templateSequence) - len(testSequence) + 1 number of
    #            #alignments.
    #            
    #            numOfAlignments = abs(eachTemplate[2] - len(testSequence)) + 1
    #            
    #            if len(testSequence) > eachTemplate[2]:
    #                scoreLength = eachTemplate[2]
    #                
    #                allSequencePatterns = set(
    #                    (testSequence[i:i + eachTemplate[2]], i)\
    #                    for i in xrange(numOfAlignments)
    #                )
    #                allFoldPatterns = [
    #                    (fold[i:i + eachTemplate[2]], i)\
    #                    for i in xrange(numOfAlignments)\
    #                    for fold in bindingList
    #                ]
    #                
    #                allTemplatePatterns = [[eachTemplate[3], 0, eachTemplate[0]]]
    #                
    #            else:
    #                scoreLength = len(testSequence)
    #                
    #                allSequencePatterns = [[testSequence, 0]]
    #                allFoldPatterns = [(fold, 0) for fold in bindingList]
    #                
    #                allTemplatePatterns = set(
    #                    (eachTemplate[3][i:i + len(testSequence)], i, eachTemplate[0])\
    #                    for i in xrange(numOfAlignments)
    #                )
    #            
    #            for template, templateIndex, templateName in allTemplatePatterns:
    #                #character scoring
    #                #print ' ' * templateIndex + template
    #                for sequence, sequenceIndex in allSequencePatterns:
    #                    #print ' ' * sequenceIndex + sequence
    #                    currentCharactescoredrScore = 0
    #                    
    #                    for sequenceCharacter, templateCharacter in zip(sequence, template):
    #                        if sequenceCharacter == templateCharacter:
    #                            currentCharacterScore += 2
    #                        elif templateCharacter == 'Y':
    #                            if sequenceCharacter == 'U' or sequenceCharacter == 'C':
    #                                currentCharacterScore += 1
    #                        elif templateCharacter == 'R':
    #                            if sequscoredenceCharacter == 'A' or sequenceCharacter == 'G':
    #                                currentCharacterScore += 1
    #                    
    #                    if currentCharacterScore > bestCharacterScore:
    #                        bestCharacterScore = currentCharacterScore
    #                    
    #                    for fold, foldIndex in allFoldPatterns:
    #                        if foldIndex != sequenceIndex or len(fold) != len(sequence):
    #                            continue
    #                        
    #                        #the following is not a function call because
    #                        #function calls have huge overheads in Python
    #                        
    #                        #if a subset of a fold is like so:
    #                        #((((.....))))))))
    #                        #with extra () that don't match up,
    #                        #they are replaced with .
    #                        
    #                        hashFoldStack = []
    #                        makePeriods = set()
    #                        
    #                        for hashFoldIndex, hashFoldCharacter in enumerate(fold):
    #                            if hashFoldCharacter == '(':
    #                                hashFoldStack.append(hashFoldIndex)
    #                            elif hashFoldCharacter == ')':
    #                                if len(hashFoldStack) > 0:
    #                                    hashFoldStack.pop()
    #                                else:
    #                                    makePeriods.update([hashFoldIndex])
    #                        
    #                        #add all remaining ( in the stack to makePeriods
    #                        map(lambda x: makePeriods.update([x]), hashFoldStack)
    #                        
    #                        #this is a very long list comprehension for
    #                        #replacing () with . at certain indeces in a string
    #                        hashFold = ''.join(['.' if hashIndex in makePeriods\
    #                                                else hashCharacter\
    #                                                for hashIndex, hashCharacter\
    #                                                in enumerate(fold)])
    #                        
    #                        #and now hashFold is a short, hashable, realistic fold
    #                        
    #                        #print ' ' * foldIndex + fold
    #                        if (hashFold, template) in scoredFoldDict:
    #                            currentFoldScore = scoredFoldDict[(hashFold, template)]
    #                            #print fold, currentFoldScore, sequenceIndex
    #                        else:
    #                            foldStack = []
    #                            templateStack = []
    #                            
    #                            lastFoldIndex = None
    #                            lastTemplateIndex = None
    #                            
    #                            currentFoldScore = 0
    #                            
    #                            for i, (foldCharacter, templateCharacter) in enumerate(zip(hashFold, template)):
    #                                if templateCharacter == '<':
    #                                    templateStack.append((i, len(templateStack)))
    #                                elif templateCharacter == '>':
    #                                    if len(templateStack) > 0:
    #                                        lastTemplate = templateStack.pop()
    #                                
    #                                if foldCharacter == '(':
    #                                    foldStack.append((i, len(foldStack)))
    #                                elif foldCharacter == ')':
    #                                    if len(foldStack) > 0:
    #                                        lastFold = foldStack.pop()
    #                                
    #                                if templateCharacter == '>' and foldCharacter == ')':
    #                                    if lastTemplate != None and lastFold != None:
    #                                        if lastTemplate[0] == lastFold[0] and\
    #                                           len(templateStack) == lastTemplate[1] and\
    #                                           len(foldStack) == lastFold[1]:
    #                                            currentFoldScore += 2
    #                                
    #                                lastTemplate = None
    #                                lastFold = None
    #                            
    #                            scoredFoldDict[(hashFold, template)] = currentFoldScore
    #                        
    #                        if currentFoldScore > bestFoldScore:
    #                            bestFoldScore = currentFoldScore
    #                        
    #                        if currentCharacterScore + currentFoldScore > bestTotalScore:
    #                            bestTotalScore = currentCharacterScore + currentFoldScore
    #                            bestSequence = sequence
    #                            bestFold = fold
    #                            bestScoreIndex = foldIndex
    #                            bestTemplate = template
    #                            bestTemplateIndex = templateIndex
    #                            bestTemplateName = templateName
    #        
    #        writeSequence = ' ' * bestTemplateIndex + testSequence
    #        
    #        #any fold matching the bestFold pattern at the bestTemplateIndex
    #        #will be acceptable for writing.
    #        for fold in bindingList:
    #            #print fold
    #            #print ' ' * bestScoreIndex + fold[bestScoreIndex:bestScoreIndex + len(bestTemplate)]
    #            #print ' ' * bestScoreIndex + bestFold
    #            #print
    #            if fold[bestScoreIndex:bestScoreIndex + len(bestTemplate)] == bestFold:
    #                bestFold = fold
    #                break
    #        else:
    #            #for b in bindingList:
    #            #    print b
    #            #print ' ' * bestTemplateIndex + bestFold
    #            #print testSequence
    #            #print ' ' * bestTemplateIndex + bestSequence
    #            #print bestScoreIndex
    #            #print ' ' * bestScoreIndex + bestTemplate
    #            print 'Internal error.'
    #            raise intentionalcrash
    #        
    #        for eachTemplate in templates:
    #            if bestTemplate == eachTemplate[3][bestTemplateIndex:bestTemplateIndex + len(bestTemplate)]:
    #                bestTemplate = eachTemplate[3]
    #                break
    #        else:
    #            print 'Internal error.'
    #            raise intentionalcrash
    #        
    #        writeFold = ' ' * bestTemplateIndex + bestFold
    #        
    #        writeTemplate = ' ' * bestScoreIndex + bestTemplate
    #        
    #        if writeSequence[-1] != '\n':
    #            writeSequence += '\n'
    #        if writeFold[-1] != '\n':
    #            writeFold += '\n'
    #        if writeTemplate[-1] != '\n':
    #            writeTemplate += '\n'
    #        
    #        if testSequenceName[-1] == '\n':
    #            testSequenceName = testSequenceName[:-1]
    #        writestring = '> {0} scored with the template sequence {1}.\n'.format(
    #            testSequenceName, bestTemplateName)
    #        writeFile.write(writestring)
    #        
    #        writestring = 'score: {0}\n'.format(bestTotalScore)
    #        writeFile.write(writestring)
    #        
    #        writeFile.write(writeSequence)
    #        writeFile.write(writeFold)
    #        writeFile.write(writeTemplate)
    #        
    #        if raw:
    #            writestring = '{0}\n'.format(bestTotalScore)
    #            rawFile.write(writestring)
    #        
    #    currentRun += 1
    #print len(scoredFoldDict.keys())
    #writeFile.close()
    #if raw:
    #    rawFile.close()'''

if __name__ == '__main__':
    main(sys.argv)
