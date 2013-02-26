import os
import sys

def main(argv=None):
    split_me_file_name = argv[1]
    splitted_file_name = argv[2]

    split_me_file = open(split_me_file_name, 'r')
    splitted_file = open(splitted_file_name, 'w')

    previous_score = -1

    for line in split_me_file:
        if not line or line == '\n':
            break
        score = int(line[:-1].split('\t')[1])

        if previous_score == -1:
            previous_score = score
        elif previous_score < score:
            previous_score = score
        else:
            splitted_file.write(str(previous_score) + '\n')
            previous_score = -1

    splitted_file.write(str(previous_score) + '\n')

    split_me_file.close()
    splitted_file.close()

if __name__ == '__main__':
    main(sys.argv)
