import os
import sys
import MakeDecodedRNA

outfilename = sys.argv[1]
infiles = sys.argv[2:]

'''parsedTemplateInternal = MakeDecodedRNAStaticBinds.main([None, templateSequence,'-exitparse'])'''

outfile = open(outfilename, 'w')

for infile in infiles:
    f = open(infile, 'r')
    f.readline()
    struct = f.readline()
    if struct[-1] == '\n':
        struct = struct[:-1]
    os.system('echo "DKLRJLKDJ" > tempfile.txt')
    os.system('echo "{0}" >> tempfile.txt'.format(struct))
    representation = MakeDecodedRNA.main(['', 'tempfile.txt', 'tempfile2.txt', 'exitparse'])
    f.close()
    i = 0
    full_entry = ''
    while 1:
        if i == len(representation):
            break
        entry = representation[i]
        if entry == '>' or entry == '<':
            i += 1
            length = representation[i]
            if entry == '>':
                entry = ')'
            else:
                entry = '('
            next_part = entry * int(length)
        else:
            next_part = '.' * len(entry)
        full_entry = full_entry + next_part
        i += 1
    outfile.write(full_entry + '\n')


outfile.close()
