#!/usr/bin/env python

#Given a string representing an RNA regular expression, this will make all
#possible combinations from the expression.

#run as "python MakeDecodedRNA.py $1 $2"
#$1 is the file which has an RNA regular expression.
#$2 is the file which will have the possible combinations of the expression.
#if $2 is "-exitparse" and $1 is a string of a template,
#this will return a parsed version of $1

#Written by Aaron Reba



#
#
#
#This is bugged no more.
#Try the sequence: <1<<1<>1><1<<1<>1>>1>>1>
#
#
#


import sys

def main(argv=None):
    readFileName = argv[1]
    writeFileName = argv[2]
    
    
    if writeFileName == '-exitparse':
        stringbreak = True
    else:
        readFile = open(readFileName, 'r')
        writeFile = open(writeFileName, 'w')
        stringbreak = False
    
    bases = ('T', 'A', 'G', 'C')
    
    while 1:
        if not stringbreak:
            titleLine = readFile.readline()
            dataLine = readFile.readline()
            
            if not titleLine:
                #end of file has been reached.
                break
            
        else:
            dataLine = readFileName
        
        #go through dataLine and see if there are wildcards.
        
        #if there are decode the string into a list
        #like so: ['<3','a',5,6,'atct',3,'gcga','>3']
        #where 5, 6, and 3 are wildcards
        #anything in < is an open binding pattern. > is closed.
        
        possibleDataLines = []
        
        lefts = dataLine.split('[')
        fullSplit = []
        for left in lefts:
            fullSplit.append(left.split(']'))
        
        parsedDataLine = []
        allNumbers = []
        allBinds = []
        for value in fullSplit:
            for subvalue in value:
                if len(subvalue) > 0:
                    if subvalue[-1] == '\n':
                        subvalue = subvalue[:-1]
                    try:
                        parsedDataLine.append(int(subvalue))
                        allNumbers.append(int(subvalue))
                    except:
                        parsedDataLine.append(subvalue)
        
        leftSplit = []
        for value in parsedDataLine:
            try:
                subvalues = value.split('<')
                for subsubvalue in subvalues:
                    if len(subsubvalue) > 0:
                        try:
                            int(subsubvalue)
                            leftSplit.append('<')
                            leftSplit.append(int(subsubvalue))
                            allBinds.append(int(subsubvalue))
                        except:
                            leftSplit.append(subsubvalue)
            except:
                leftSplit.append(value)
        
        bindParsedDataLine = []
        for value in leftSplit:
            try:
                subvalues = value.split('>')
                for subsubvalue in subvalues:
                    if len(subsubvalue) > 0:
                        try:
                            int(subsubvalue)
                            bindParsedDataLine.append('>')
                            bindParsedDataLine.append(int(subsubvalue))
                        except:
                            bindParsedDataLine.append(subsubvalue)
            except:
                bindParsedDataLine.append(value)
        
        possibleDataLines.append(bindParsedDataLine)
        
        
        numbersExist = False
        priorBind = False
        for value in bindParsedDataLine:
            if type(value) == type(''):
                priorBind = False
                if value == '<' or value == '>':
                    priorBind = True
            if type(value) == type(0) and not priorBind:
                numbersExist = True
                break
        
        bindsExist = False
        for value in bindParsedDataLine:
            if type(value) == type(''):
                if value == '<' or value == '>':
                    bindsExist = True
                    break
        
        if not numbersExist and not bindsExist:
            #Only necessary to write 1 string.
            #Write it and quit.
            if stringbreak:
                return [[readFileName]]
            writestring = '%s_%i\n' % (titleLine[:-1], 1)
            writeFile.write(writestring)
            writeFile.write(dataLine)
            return
        
        copyNumbers = list(allNumbers)
        
        
        #go through all numbers and add all possible combos.
        #stop after new append when all numbers are 0 in the copy list.
        
        #have already added the first combination of copies,
        #so decrement the right most value
        
        if numbersExist:
            copyNumbers[-1] -= 1
        
        
        while 1:
            nextPossibleDataLine = []
            copyIndex = 0
            bindIndex = 0
            proceedingBinds = 1
            preceedingBind = False
            proceedingBind = False
            for value in bindParsedDataLine:
                if type(value) == type(''):
                    nextPossibleDataLine.append(value)
                    if value == '<':
                        preceedingBind = True
                    elif value == '>':
                        proceedingBind = True
                elif preceedingBind:
                    preceedingBind = False
                    nextPossibleDataLine.append(value)
                elif proceedingBind:
                    proceedingBind = False
                    nextPossibleDataLine.append(value)
                elif len(copyNumbers) > 0:
                    if copyNumbers[copyIndex] > 0:
                        nextPossibleDataLine.append(copyNumbers[copyIndex])
                    copyIndex += 1
                else:
                    #this only happens on a syntax error from the user.
                    print 'syntax error in input file'
                    print 'you dun goofed'
                    raise the_roof
            
            possibleDataLines.append(nextPossibleDataLine)
            
            if copyNumbers == [0] * len(copyNumbers):
                break
            
            #decrement
            #go through lists in reverse order
            for reversedIndex in xrange(len(copyNumbers) - 1, -1, -1):
                if copyNumbers[reversedIndex] == 0:
                    copyNumbers[reversedIndex] = allNumbers[reversedIndex]
                else:
                    copyNumbers[reversedIndex] -= 1
                    break
        if len(copyNumbers) == 0 and bindsExist:
            #this is a bandaid method.
            #when there are no numbers in the template, then there are 2 copies
            #of the only dataline possible.
            possibleDataLines = [possibleDataLines[0]]
        
        if stringbreak:
            return possibleDataLines
        
        #go through each possible data line
        #write all possible strings with the parsed lines to writeFile
        
        #decode a parsed line's wildcards to iterators.
        #example: ['ata', 3, 2, 'ggc', 2, 'g']
        #to: ['ata', 0, 0, 0, 0, 0, 'ggc', 0, 0, 'g']
        #each write, increment the left most number by 1, when it reaches 4,
        #set it to 0 and add 1 to the number to the right if possible.
        #use the number to index the bases and write a new sequence
        sequencenumber = 1
        for possibleDataLine in possibleDataLines:
            incrementalLine = []
            openBindingLine = []
            closedBindingLine = []
            countIncrements = 0
            preceedingBind = False
            proceedingBind = False
            
            lastBind = None
            #stores whether the last thing looked at was an
            #open or closing bind
            
            addIndex = 0
            unbound = 0
            insertAt = 0
            #go through each value in the data line
            #if it's a string, check if it's a < or > and set the bind flags
            #if it's a number, check if either bind flags are set and add
            #the correct number of 0's.
            #for the bind lists, add the indeces of the binds.
            print possibleDataLine
            for value in possibleDataLine:
                if type(value) == type(''):
                    if preceedingBind:
                        preceedingBind = False
                    elif proceedingBind:
                        proceedingBind = False
                    
                    if value == '<':
                        preceedingBind = True
                    elif value == '>':
                        proceedingBind = True
                    else:
                        incrementalLine.append(value)
                        addIndex += len(value)
                else:
                    for i in xrange(value):
                        incrementalLine.append(0)
                    addIndex += value
                    if not proceedingBind:
                        countIncrements += value
                    if preceedingBind:
                        preceedingBind = False
                        for i in xrange(-value, 0):
                            openBindingLine.append(addIndex + i)
                        lastBind = 'open'
                        unbound += value
                    elif proceedingBind:
                        proceedingBind = False
                        if lastBind == 'close':
                            #insert at the last open bind.
                            for i in xrange(-value, 0):
                                closedBindingLine.insert(insertAt, addIndex + i)
                            insertAt += value
                        else:
                            #insert at the end, or as they say "append"
                            for i in xrange(-1, -value - 1, -1):
                                closedBindingLine.append(addIndex + i)
                        lastBind = 'close'
            
            
            #using a while loop because anything >= 4**16 will crash when
            #using xrange
            #go through the incremental line to create all
            #permutations.
            k = 0
            
            while k < 4 ** countIncrements:
                titlestring = '%s_%i\n' % (titleLine[:-1], sequencenumber)
                print openBindingLine
                print closedBindingLine
                datastring = ''
                preceedingBind = False
                proceedingBind = False
                bindIndex = 0
                
                lineIndex = 0 #keeps track of the index in the final string
                
                
                #go through each value in the incremental line
                for i in xrange(len(incrementalLine)):
                    value = incrementalLine[i]
                    if type(value) == type(''):
                        if value != '<' and\
                        value != '>':
                            #if it the current value is a string, add it unless
                            #it is a < or >
                            datastring += value
                            lineIndex += len(value)
                    else:
                        #if it's a number, see if its index
                        #is in the closed line list
                        if lineIndex in closedBindingLine:
                            closedIndex = closedBindingLine.index(lineIndex)
                            openIndex = openBindingLine[closedIndex]
                            openBindBase = datastring[openIndex]
                            bindIndex += 1
                            #get the complement
                            if openBindBase == 'A':
                                addChar = 'T'
                            elif openBindBase == 'T':
                                addChar = 'A'
                            elif openBindBase == 'C':
                                addChar = 'G'
                            elif openBindBase == 'G':
                                addChar = 'C'
                        #if it isn't, just add the base for this value
                        else:
                            addChar = bases[value]
                        datastring += addChar
                        lineIndex += 1
                        
                datastring += '\n'
                
                writeFile.write(titlestring)
                writeFile.write(datastring)
                
                sequencenumber += 1
                
                nextIncrement = True
                for i in xrange(len(incrementalLine)):
                    if type(incrementalLine[i]) == type(0):
                        if i not in closedBindingLine:
                            if nextIncrement:
                                incrementalLine[i] += 1
                                nextIncrement = False
                                if incrementalLine[i] == 4:
                                    incrementalLine[i] = 0
                                    nextIncrement = True
                    
                    if not nextIncrement:
                        break
                
                k += 1

if __name__ == "__main__":
    main(sys.argv)
