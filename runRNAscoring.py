#!/usr/bin/env python

#THE WORD TARGET IS INCORRECTLY and INTERCHANGABLY USED WITH TEMPLATE.

#This will run the entire RNA folding analysis.

#$1 is the population size of the random sequences.
#$2 is the length of the sequences.
#$3 is the name of the template file.
#all args after $4 are options. Order does not matter.
#'a 5 m .03' is the same as 'm .03 a 5'
#
#   example:
#   Use a population size of 500, each sequence 50 nucleotides in length,
#   with the target file name of "Target.txt," amplifications enabled
#   for 10 runs, mutations enabled at a chance of .01 per nucleotide, using a
#   random sampling of 15 folds.
#   $ python runRNAscoring.py 500 50 Target.txt a 10 m .01 r 15
#
#   a: amplification enable. If no 'a', passed sequences will not be COPIED
#   when passed to the next generation but still remain in the next generation.
#   proceed by the number of times to iterate.
#
#   m: this will add random mutations to sequences that pass.
#   by default, the chance for a mutation is .002.
#   proceed by the chance for a mutation if desired.
#   enabling this without enabling amplification does nothing.
#
#   r: Use random number of folding of sequences. If there is no 'r', the best
#   fold is taken. If there is an 'r', the next parameter must be the number
#   of sequences to take.
#   proceed by the number of random sequences.
#
#   b: Break after 1 scoring.
#   this is useful for wanting to plot the results after 1 run.
#
#   raw: specifies the raw scoring file name from the last scored sequences.
#   proceed by the name of the raw file you want.
#   by default, this is "RawScore.txt"
#
#   praw: specifies the raw scoring file from the last passed sequences.
#   works in the same manner as raw. by default this is "PRawScore.txt"
#
#   fraw: specifies the full raw scoring file from the entire simulation.
#   works in the same manner as raw. by default this is "AllScores.txt"
#

#target format:
#> name_of_pattern
#TGAC<3<TGACN[4]TGAC>3>TGAC
#> name_of_pattern2
#ACGTACNTCAG[2]<2<[5]>2>

#where <x< marks an opening bind pattern, >x> marks the corresponding bases to
#close that pattern, and [4] marks a variable length insertion of any random
#nucleotides. * means any nucleotide.
#**[2] would mean 2-4 of any nucleotides.

#Written by Aaron Reba

import subprocess
import os
import sys
import time

import CheckTarget
import MakeDecodedRNA
import MakeG
import FoldSequences
import ScoreRNA
import PassScores
import Amplify

def main(argv=None):
    #if a sequence file is specified, the population and length needs to be
    #extracted first.
    if 'isf' in argv:
        #population is # of lines / 2
        #length is length of line #2
        #this is the most disgusting thing i've ever written.
        isfFile = argv[argv.index('isf') + 1]
        prepipe = os.popen('wc {0}'.format(isfFile))
        prepipe = prepipe.readline().lstrip().split(' ')[0]
        argv[1] = str(int(prepipe) / 2)
        prepipe = os.popen('head -n 2 {0}'.format(isfFile))
        print prepipe.readline()
        argv[2] = str(len(prepipe.readline()) - 1)
        prepipe.close()
    
    print 'Starting run:'
    print '{0} Sequences, {1} Length'.format(argv[1], argv[2])
    print
    
    foldTime = 0
    scoreTime = 0
    passTime = 0
    
    CheckTarget.main([None, argv[3]])
    
    print 'Target(s):'
    os.system('cat {0}'.format(argv[3]))
    print
    print
    
    if not os.path.isdir('Stats'):
        os.mkdir('Stats') #what was i going to put in this folder?
    
    #Option parsing
    
    plot = False
    plotSave = None
    
    amplify = False
    amplifications = None
    
    randomSample = False
    randomSampling = None
    
    timing = False
    timeUsing = None
    
    mutate = False
    mutateChance = None
    
    raw = False
    rawName = None
    
    praw = False
    prawName = None
    
    fraw = False
    frawName = None

    sName = False
    sFile = None
    
    temperature = False
    temperatureValue = None
    
    firstBreak = False
    
    dna = False
    
    inputSequenceFile = False
    inputSequenceFileName = None
    
    possibleOptions = ['p', 'a', 'r', 'm', 'b', 'raw', 'praw', 'fraw', 'sname', 'dna', 't', 'isf', 'time']
    
    if len(argv) > 4:
        for option in argv[4:]:
            known = False
            #check previous options that may have been enabled. some options
            #require a name or a number.
            if mutate:
                try:
                    mutateChance = float(option)
                except:
                    mutateChance = .002
                mutate = False
                known = True
                
            elif plot:
                plotSave = option
                plot = False
                known = True
                
            elif randomSample:
                randomSampling = int(option)
                randomSample = False
                known = True
            
            elif timing:
                timeUsing = int(option)
                timing = False
                known = True
            
            elif amplify:
                amplifications = int(option)
                amplify = False
                known = True
                
            elif raw:
                rawName = option
                raw = False
                known = True
                
            elif praw:
                prawName = option
                praw = False
                known = True
                
            elif fraw:
                frawName = option
                fraw = False
                known = True

            elif sName:
                sFile = option
                sName = False
                known = True
            
            elif temperature:
                temperatureValue = int(option)
                temperature = False
                known = True
            
            elif inputSequenceFile:
                inputSequenceFileName = option
                inputSequenceFile = False
                known = True
            
            #check if setting a new option
            if option in possibleOptions:
                known = True
                
                if option == 'p':
                    plot = True
                elif option == 'a':
                    amplify = True
                elif option == 'r':
                    randomSample = True
                elif option == 'time':
                    timing = True
                elif option == 'm':
                    mutate = True
                elif option == 'raw':
                    raw = True
                elif option == 'b':
                    firstBreak = True
                elif option == 'praw':
                    praw = True
                elif option == 'fraw':
                    fraw = True
                elif option == 'dna':
                    dna = True
                elif option == 't':
                    temperature = True
                elif option == 'sname':
                    sName = True
                elif option == 'isf':
                    inputSequenceFile = True
            
            if not known:
                print 'Unknown option: {0}'.format(option)
                return
    
    if rawName == None:
        rawName = 'RawScore.txt'
        print 'Using default raw data file name of "RawScore.txt"'
    else:
        print 'Using raw data file name of "{0}"'.format(rawName)
    
    if prawName == None:
        prawName = 'PRawScore.txt'
        print 'Using default raw data file name of "PRawScore.txt"'
    else:
        print 'Using pass raw data file name of "{0}"'.format(prawName)
    
    if frawName == None:
        frawName = 'AllScores.txt'
        print 'Using default full data file name of "AllScores.txt"'
    else:
        print 'Using full raw data file name of "{0}"'.format(frawName)
    
    if sFile == None:
        sFile = 'ScoredRNA.txt'

    if randomSampling == None:
        print 'Using best fold.'
    else:
        print 'Using random sampling of {0} folds.'.format(randomSampling)
    
    if timeUsing == None:
        print 'Using default time of 50'
        timeUsing = 50
    else:
        print 'Using time of {0}.'.format(timeUsing)

    if temperatureValue == None:
        print 'Using default temperature.'
    else:
        print 'Using temperature of {0}'.format(temperatureValue)
    
    if amplifications == None:
        print 'Not amplifying'
    else:
        print 'Amplifying {0} times.'.format(amplifications)
    
    if not mutate:
        print 'Not mutating.'
    else:
        print 'Mutating.'
    
    if not firstBreak:
        print 'Full scoring run.'
    else:
        print 'Single scoring run.'
    
    if not dna:
        print 'Using RNA sequences.'
        makeType = 'rna'
    else:
        print 'Using DNA sequences.'
        makeType = 'dna'
    
    if inputSequenceFileName == None:
        inputSequenceFileName = 'TestSequences.txt'
        print 'Using randomly generated sequences.'
    else:
        print 'Using specified sequence file {0}.'.format(inputSequenceFileName)
    
    print
    
    #this is used to check scores and passed scores for each run.
    os.system('echo "" > hi.txt')
    
    #simulation begins
    MakeG.main([None,
                argv[1],
                argv[2],
                '-n',
                inputSequenceFileName,
                '1',
                '1',
                makeType])
    
    lastWritten = 0
    currentRun = 1
    
    #initialize files.
    passedFile = open('PassedSequences.txt', 'w')
    passedFile.close()
    frawFile = open(frawName, 'w')
    frawFile.close()
    
    #set up call string
    
    if randomSampling:
        callString = 'Kinfold --time={0} --num={1} --stop'.format(timeUsing, randomSampling)
    else:
        callString = 'RNAsubopt -s'
    
    if dna:
        callString += ' -P dna_mathews2004.par --noconv'
    
    if temperatureValue:
        callString += ' -T {0}'.format(temperatureValue)
    
    print 'Command:', callString
    print
    
    callString += ' < {0} > SubOptTestSequences.txt 2> dummy.txt'.format(inputSequenceFileName)
    
    while 1:
        #####FOLD#####
        
        #os.system('cat TestSequences.txt; echo "f1"')
        #raw_input('')
        
        oldtime = time.time()
        
        FoldSequences.main([None,
                            callString,
                            argv[1]])
        
        
        foldTime += time.time() - oldtime
        
        #os.system('cat PassedSequences.txt; echo "p1"')
        #os.system('cat HighestTestSequences.txt; echo "p2"')
        #raw_input('')
        
        #Append HighestTestSequences to PassedSequences
        os.system('cat HighestTestSequences.txt >> PassedSequences.txt')
        #overwrite HighestTestSequences with PassedSequences and takes its name
        os.system('mv PassedSequences.txt HighestTestSequences.txt')
        
        #####SCORE#####
        #os.system('cat HighestTestSequences.txt; echo "prescore"')
        #raw_input('')
        oldtime = time.time()
        #raw_input('')
        ScoreRNA.main([None,
                       argv[3],
                       'HighestTestSequences.txt',
                       'TargetRepresentation.txt',
                       sFile,
                       'raw',
                       rawName])
        scoreTime += time.time() - oldtime
        
        os.system('echo "{0} {1}" >> {2}'.format(currentRun, 'score', frawName))
        os.system('cat {0} >> {1}'.format(rawName, frawName))
        
        #after the last amplification, the remaining scores are unscored.
        #so when amplification is enabled, this statement breaks after the
        #n + 1 scoring. but they are only amplified n times.
        if amplifications == 0:
            break
        
        #os.system('cat ScoredRNA.txt; echo "Scored"')
        #raw_input('')
        
        if firstBreak:
            break
        
        
        #####PASS#####
        
        oldtime = time.time()
        passesWritten = PassScores.main([None,
                                         argv[1],
                                         sFile,
                                         argv[3],
                                         'PassedSequences.txt',
                                         prawName])
        passTime += time.time() - oldtime
        
        if currentRun == 1:
            passFile = open('PassedSequences.txt', 'r')
            
            rawPassFile = open(prawName, 'w')
            while 1:
                passLine = passFile.readline()
                if not passLine:
                    break
                if 'score:' in passLine:
                    rawPassFile.write(passLine.split(' ')[1])
            
            passFile.close()
            rawPassFile.close()
        
        os.system('echo "{0} {1}" >> {2}'.format(currentRun, 'pass', frawName))
        os.system('cat {0} >> {1}'.format(prawName, frawName))
        
        #os.system('cat PassedSequences.txt; echo "Passed"')
        #raw_input('')
        
        #####AMPLIFY#####
        
        if amplifications != None:
            if passesWritten == 0:
                print 'Failed run. No sequences passed.'
                break
            if mutateChance != None:
                passesWritten = Amplify.main([None,
                                              argv[1],
                                              'PassedSequences.txt',
                                              'm',
                                              mutateChance])
                #take unscored sequences out of passed and create 2 new files
                passFile = open('PassedSequences.txt', 'r')
                testFile = open(inputSequenceFileName, 'w')
                tempPassFile = open('TempPassedSequences.txt', 'w')
                
                while 1:
                    entryCount = 0
                    firstPassLine = passFile.readline()
                    if not firstPassLine:
                        break
                    
                    secondPassLine = passFile.readline()
                    
                    previousPosition = passFile.tell()
                    thirdPassLine = passFile.readline()
                    
                    if not thirdPassLine or thirdPassLine[0] == '>':
                        passFile.seek(previousPosition)
                        testFile.write(firstPassLine)
                        testFile.write(secondPassLine)
                    else:
                        tempPassFile.write(firstPassLine)
                        tempPassFile.write(secondPassLine)
                        tempPassFile.write(thirdPassLine)
                        tempPassFile.write(passFile.readline())
                        tempPassFile.write(passFile.readline())
                
                passFile.close()
                testFile.close()
                tempPassFile.close()
                
                os.system('mv TempPassedSequences.txt PassedSequences.txt')
                #PassedSequences.txt holds scored sequences,
                #TestSequences.txt holds unscored sequences.
                #Renewing is skipped in mutating
                #because it is done in this section.
            else:
                passesWritten = Amplify.main([None,
                                              argv[1],
                                              'PassedSequences.txt',
                                              ''])
        
        #os.system('cat PassedSequences.txt; echo "Amped1"')
        #os.system('cat TestSequences.txt; echo "Amped2"')
        #raw_input('')
        
        if lastWritten != passesWritten:
            lastWritten = passesWritten
            if amplifications == None:
                runstring = 'Run #{0}, Wrote {1} of {2}'.format(currentRun,
                                                                passesWritten,
                                                                argv[1])
                print runstring + '\r',
                sys.stdout.flush()
            
            if amplifications != None:
                pass
            elif passesWritten == int(argv[1]):
                break
        
        #####RENEW#####
        
        if amplifications == None:
            if passesWritten == 0:
                MakeG.main([None,
                            argv[1],
                            argv[2],
                            '-n',
                            inputSequenceFileName,
                            str(currentRun),
                            makeType])
            else:
                MakeG.main([None,
                            argv[1],
                            '-f',
                            'PassedSequences.txt',
                            inputSequenceFileName,
                            str(currentRun),
                            makeType])
        else:
            if currentRun == 1:
                ampMax = amplifications
            amplifications -= 1
            runsLeft = ampMax - amplifications
            runstring = 'Amplification Run #{0} of {1}'.format(runsLeft, ampMax)
            print runstring + '\r',
            sys.stdout.flush()
            if not mutate:
                os.system('echo "" > {0}'.format(inputSequenceFileName))
        currentRun += 1
        
        
        #os.system('cat PassedSequences.txt; echo "Renewed half"')
        #os.system('cat TestSequences.txt; echo "Renewed"')
        #raw_input('')
    
    print
    print 'Complete'
    print
    #print 'fold: {0}\nscore: {1}\n pass: {2}\n'.format(foldTime, scoreTime, passTime)

if __name__ == '__main__':
    main(sys.argv)
