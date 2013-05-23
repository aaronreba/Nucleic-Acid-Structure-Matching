Author: Aaron Reba

Hello!

--------------------------------------------------------------------------------

This project is currently undergoing some heavy code restructuring to make it
easier to use.

--------------------------------------------------------------------------------

This is a set of scripts that can be used to obtain fold patterns from Kinfold,
a library included in the Vienna package, and match them to a specified
structure.

This requires:
* A Unix system.
* Kinfold 1.3 (untested with any other Kinfold version)
* A C++ Compiler
* Python 2.7
* The matplotlib module for Python if you are planning to make graphs using the included scripts.

This package is roughly divided into 3 parts.
* Generating Sequences.
* Folding Sequences.
* Scoring Sequences.

--------------------------------------------------------------------------------

1: Generating Sequences.

Multiple sequences can be randomly generated using ```make_sequences.py```

For example:

```
python make_sequences.py -n 5 -l 50 -a r
```

This would create 5 sequences each 50 bases in length. These sequences would
be printed to the console and would be written with the nucleotide U
instead of T.

The output would look something like this:
```
> Sequence_1
AGCUUAGCGUACGUA...AGGAUCGUACGUACU
> Sequence_2
ACGUACGUAUCUACG...AGCUAGUCGUACUAG
...
```
In this format, the file could be read in using Vienna's packages.
Using FoldSequences.py, the file could also be read in and its sequences folded
using Kinfold.

--------------------------------------------------------------------------------

2: Folding Sequences.

Sequences can be folded using FoldSequences.py. FoldSequences.py requires a call
to Kinfold. An example is like so:
```
python FoldSequences.py "Kinfold --time=10 --num=100 --seed=0=1=2 --stop --lmin < sequences.txt" 500 0 final folded_sequences.txt
```
This will call Kinfold on the file "sequences.txt" and fold the sequences
contained in the file. Kinfold has its own set of parameters and a few of them
must be set for FoldSequences.py to work.
--time specifies the length of time given to the sequence to fold.
--num specifies the number of times a sequence will fold for the desired length
of time.
--seed specifies the seed. I recommend using the same seed every time. After
every time a sequence is folded, each value of the seed increases by 1. In the
first iteration, the seed might be 0=1=2, so in the next it would be 1=2=3. By
checking the number of a sequence in a file, you can obtain the seed used to
generate that folding pattern.
--stop and --lmin are optional parameters. In certain sequences, Kinfold will
crash. Setting these parameters will hopefully avoid the crash. However, if
Kinfold does crash, FoldSequences.py will display a message saying which
sequence failed and the seed that was used. FoldSequences.py will continue
attempting to fold the sequence incrementing the seed as normal until a
successfully folding sequence is found.

After the Kinfold call string, the number of sequences in the file must be
given.

After the number of sequences, a unique string must be given. FoldSequences.py
uses several temporary files. If you want to run FoldSequences.py in the same
directory, then for one call, you might want to specify "1" for this parameter.
In the second call, you might want to specify "2". This avoids any colliding
temporary file names.

Lastly, there is an optional paramter called "final". This specifies where all
of the folded sequences will be written to. By default, this is
HighestTestSequences.txt

--------------------------------------------------------------------------------

3: Scoring Sequences.

Folded sequences can be scored using ScoreRNA.py. ScoreRNA.py requires an
executable named ScoreRNA which can be compiled from ScoreRNA.cpp. It's probably
best to compile using this line:
```g++ -o ScoreRNA ScoreRNA.cpp```

Given a folded sequence file and a target structure, ScoreRNA.py will give
a higher score to sequences with fold patterns that better match the target
structure.

An example target structure:
In structure_1.txt:
```
> structure_1
<<N<<NNNNNN>NN[3]NNN>NNN>>
```
The < and > represent folds from a folding pattern like Vienna's or Kinfold's (
or ). The N represents any nucleotide. The [3] represents a variable length
insertion of 0 to 3 nucleotides. With this structure, the following 3 structures
are generated and scored with sequences that have been specified:
```
<<N<<NNNNNN>NNNNNNNN>NNN>>
<<N<<NNNNNN>NNNNNNN>NNN>>
<<N<<NNNNNN>NNNNNN>NNN>>
<<N<<NNNNNN>NNNNN>NNN>>
```
Multiple structures can be specified in a target file.

Each position of each representation of the target is aligned with each sequence
and each of the sequence's fold patterns.
If a sequence was: ```AGUCAGUCAGUGACUGACUGAUCGUACGACGUACGUAA```
and its fold pattern was: ```((((.......((((....))))...........))))```
then each structure would be aligned and scored like so:
```
((((.......((((....))))...........))))
<<N<<NNNNNN>NNNNNNNN>NNN>>
 <<N<<NNNNNN>NNNNNNNN>NNN>>
  <<N<<NNNNNN>NNNNNNNN>NNN>>
               ...
          <<N<<NNNNNN>NNNNNNNN>NNN>>
           <<N<<NNNNNN>NNNNNNNN>NNN>>
            <<N<<NNNNNN>NNNNNNNN>NNN>>
<<N<<NNNNNN>NNNNNNN>NNN>>
 <<N<<NNNNNN>NNNNNNN>NNN>>
  <<N<<NNNNNN>NNNNNNN>NNN>>
               ...
           <<N<<NNNNNN>NNNNNNN>NNN>>
            <<N<<NNNNNN>NNNNNNN>NNN>>
             <<N<<NNNNNN>NNNNNNN>NNN>>
<<N<<NNNNNN>NNNNNN>NNN>>
 <<N<<NNNNNN>NNNNNN>NNN>>
  <<N<<NNNNNN>NNNNNN>NNN>>
               ...
            <<N<<NNNNNN>NNNNNN>NNN>>
             <<N<<NNNNNN>NNNNNN>NNN>>
              <<N<<NNNNNN>NNNNNN>NNN>>
<<N<<NNNNNN>NNNNN>NNN>>
 <<N<<NNNNNN>NNNNN>NNN>>
  <<N<<NNNNNN>NNNNN>NNN>>
               ...
             <<N<<NNNNNN>NNNNN>NNN>>
              <<N<<NNNNNN>NNNNN>NNN>>
               <<N<<NNNNNN>NNNNN>NNN>>
```
For each set of < and > that align with a corresponding set of ( and )
accounting for depth of the fold, that alignment would receive 1 point.
If a fold was: ```((((.......((((....))))...........))))```
and a target: ```<<..<...><<<......>>.>>>```
This alignment would receive 2 points.

An example call of ScoreRNA.py is like so:
python ScoreRNA.py structure_1.txt folded_sequences.txt 1.txt scored_sequences.txt
structure_1.txt would be the target file.
folded_sequences.txt would be a file generated from FoldSequences.py
1.txt is a temporary file name. It works much in the same way as temporary files
do in FoldSequences.py.
scored_sequences.txt would be the scored file.
It would look like so:
```
> 2s1m_0 scored with the template sequence bulge
score: 10
UGGCCGGGAUCAGCCAUCGCCGCGUGUUGGGCGGUCGACGCCCUAAAGAUACGUAUGCUGCUUCGAGUGUUGGCCUAGAGUGGGGCUCUAGCGUUGCGAA
((((.((......))...))))(((((((((((.....)))))....))))))..(((.(((......(..(((((......))))).))))...)))..
                      <<<<<N<<<<<NNNNN>>>>>NNNNN>>>>>
```
--------------------------------------------------------------------------------

There are multiple optional parameters for ScoreRNA.py.

raw:
It would be called like so:
raw raw_score.txt
at the end of the call to ScoreRNA.py. raw_score.txt would be the file that
will hold the raw scores. The "score: 10" line in the previous example is taken
and simply the 10 is written to raw_score.txt.

rawfold:
It would be called like so:
rawfold raw_folds
at the end of the call to ScoreRNA.py. raw_folds would be a directory created
that will hold files named after sequences. Each file would contain a number of
lines equal to the number of trajectories found. If a sequence had been folded
10 times and it was named seq_1, then inside of raw_folds, there would be a file
named "seq_1.txt". In this file, there would be 10 lines each representing the
highest score found for each trajectory.

threshold:
It would be called like so:
threshold 5
at the end of the call to ScoreRNA.py. Scoring can take a large amount of time.
If only the highest score found for each trajectory or sequence is the aim of
your project, setting a threshold equal to the target's maximum score minus 1
would ignore fold patterns that don't have at least that number of ( and )
characters. This creates a large increase in speed at the cost of ignoring
sequences. This may or may not be a problem for you. The author advises not
using this option with chrono.

chrono:
It would be called like so:
chrono time_dir
at the end of the call to ScoreRNA.py. This option acts a lot like rawfold does.
With the exception of there being at least 1 line for each trajectory rather
than exactly 1 line. As a trajectory's fold pattern is being read and scored,
the current highest score is kept in memory. Whenever this score changes, it is
written to the scoring file holding the sequence. The author advises not using
this option with threshold.

================================================================================

Other included scripts:
There are several .py files that have various functions.

--------------------------------------------------------------------------------

MakeMutationNeighborhood.py and MakeMutationNeighbors.py:
These allow creating all of the n-step mutation neighbors of all of the
sequences in a given file. For example, if there was a file like so:
In sequences.txt:
```
> sequence_1
CA...
```
Then a new file could be created with the 1 step mutation neighbors which would
be like so:
```
> sequence_1_0
CA...
> sequence_1_1
UA...
> sequence_1_2
AA...
> sequence_1_3
GA...
> sequence_1_4
CU...
> sequence_1_5
CG...
> sequence_1_6
CC...
```
Multiple sequences can be included in an initial sequence file. When making
mutation neighbors, each sequence is checked as it is created to make sure that
there are no identical sequences.

MakeMutationNeighbors.py will create only the 1 step mutation neighbors.
MakeMutationNeighborhood.py allows you to specify the number mutation neighbors.

Call MakeMutationNeighbors.py like so:
python MakeMutationNeighbors.py sequences.txt mutation_neighbors.txt
Where the first parameter is your sequence file,
and the second parameter is the file you want to save your mutation neighbors
as.

Call MakeMutationNeighborhood.py like so:
python MakeMutationNeighbors.py sequences.txt n mutation_neighbors.txt
Where the first parameter is your sequence file,
the second parameter is an integer for the number of mutation neighbors,
and the third parameter is the file you want to save your mutation neighbors as.

--------------------------------------------------------------------------------

SequenceFragment.py and TimeFragment.py:
These allow breaking a sequence file or a folded sequence file into smaller
files. This is useful for folding or scoring sequences on multiple processors at
the same time. A file of 1,000,000 sequences may take a long time to fold or
score. Splitting this file into 4 files each with 250,000 sequences may reduce
the folding/scoring time by up to four-fold.

SequenceFragment.py will take a file of only sequences (like one generated from
MakeSequences.py) and divide it.
TimeFragment.py will take a file of a single sequence with multiple trajectories
(like one generated from FoldSequences.py except with only 1 sequence) and
divide each of the trajectories into a new file.

Call SequenceFragment.py like so:
python SequenceFragment.py big_sequences.txt _sequence_fragment.txt n
Where the first parameter is your sequence file,
the second parameter is the base name for the files that will be created,
and the third parameter is an integer for the number of sequences to write to a
file.

Call TimeFragment.py like so:
python TimeFragment.py sequence.txt _sequence_trajectory.txt
Where the first parameter is your sequence file,
and the second parameter is the base name for the files that will be created.

A note on base file names:
If the base name was _sequence_trajectory.txt, and there were 5 trajectories
in the sequence file, the following 5 files would be created:
```
0_sequence_trajectory.txt
1_sequence_trajectory.txt
2_sequence_trajectory.txt
3_sequence_trajectory.txt
4_sequence_trajectory.txt
```

--------------------------------------------------------------------------------

There should be no reason to call these manually:
CheckTarget.py
MakeDecodedRNAStaticBinds.py

