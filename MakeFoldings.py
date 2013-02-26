#!/usr/bin/env python

#python FoldSequences.py
#"Kinfold --time=1000 --num=1 --stop --lmin < sequences/Sequences10001-10100.txt"
#100 0 final folded_sequences_1t/Sequences10001-10100.txt

sfiles = 'Sequences1001-2000.txt  Sequences1-1000.txt  Sequences2001-3000.txt  Sequences3001-4000.txt  Sequences4001-5000.txt  Sequences5001-6000.txt  Sequences6001-7000.txt  Sequences7001-8000.txt  Sequences8001-9000.txt  Sequences9001-10000.txt'.split()


run_file = open('fold10kt.csh', 'w')

#for i in xrange(10):
#    run_file.write('python FoldSequences.py \
#"Kinfold --time=10 --num=1000 --seed=0=1=2 --stop --lmin < sequences/{1}" \
#1000 {0} final 10k_folds/{0}_1000t_Sequences.txt\n'.format(i, sfiles[i]))

for i in xrange(1000):
    run_file.write('python FoldSequences.py \
"Kinfold --time=10 --num=10000 --seed=0=1=2 --stop --lmin < sequences/{2}__{1}" \
10 {0} final 10k_folds/{0}_10000t_Sequences.txt\n'.format(i + 1001, sfiles[int(i / 100)], i % 100 + 1))

run_file.close()
