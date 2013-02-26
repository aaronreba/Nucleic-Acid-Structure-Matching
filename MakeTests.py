#!/usr/bin/env python

structures = ['Structure6.txt',
              'Structure7.txt',
              'Structure8.txt',
              'Structure9.txt',
              'Structure10.txt',
              'StructureBulge.txt']

data = [
    
'100k_folds/10_100t_Sequences.txt',
'100k_folds/1_1t_Sequences.txt',
'100k_folds/3_10t_Sequences.txt',
'100k_folds/5_100t_Sequences.txt',
'100k_folds/6_1t_Sequences.txt',
'100k_folds/8_10t_Sequences.txt',
'100k_folds/10_10t_Sequences.txt',
'100k_folds/2_100t_Sequences.txt',
'100k_folds/3_1t_Sequences.txt',
'100k_folds/5_10t_Sequences.txt',
'100k_folds/7_100t_Sequences.txt',
'100k_folds/8_1t_Sequences.txt',
'100k_folds/10_1t_Sequences.txt',
'100k_folds/2_10t_Sequences.txt',
'100k_folds/4_100t_Sequences.txt',
'100k_folds/5_1t_Sequences.txt',
'100k_folds/7_10t_Sequences.txt',
'100k_folds/9_100t_Sequences.txt',
'100k_folds/1_100t_Sequences.txt',
'100k_folds/2_1t_Sequences.txt',
'100k_folds/4_10t_Sequences.txt',
'100k_folds/6_100t_Sequences.txt',
'100k_folds/7_1t_Sequences.txt',
'100k_folds/9_10t_Sequences.txt',
'100k_folds/1_10t_Sequences.txt',
'100k_folds/3_100t_Sequences.txt',
'100k_folds/4_1t_Sequences.txt',
'100k_folds/6_10t_Sequences.txt',
'100k_folds/8_100t_Sequences.txt',
'100k_folds/9_1t_Sequences.txt']

run_file = open('score2.csh', 'w')

#python ScoreRNA.py Structure9.txt 10k_folds/100t_Sequences.txt 9rep.txt
#Fig3Data/StructureBulge/10k_100t_Scores.txt
#raw Fig3Data/StructureBulge/Raw_10k_100t_Scores.txt
#chrono Fig3Data/StructureBulge/100t_chrono
#rawfold Fig3Data/StructureBulge/100t_rawfold

i = 0
for s in structures:
    for d in data:
        if '100t' in d:
            save_name = '100t'
        elif '10t' in d:
            save_name = '10t'
        else:
            save_name = '1t'
        inum = d.split('_')[1][6:]
        run_file.write(\
'python ScoreRNA.py {0} {1} {2}rep.txt\
 Fig3Data/{5}/100k_{2}_{3}_Scores.txt\
 raw Fig3Data/{5}/Raw_100k_{4}_{3}_Scores.txt\
 chrono Fig3Data/{5}/{4}_{3}_chrono\
 rawfold Fig3Data/{5}/{4}_{3}_rawfold\n'.format(s, d, i, save_name, inum, s[:-4]))
        i += 1
run_file.close()