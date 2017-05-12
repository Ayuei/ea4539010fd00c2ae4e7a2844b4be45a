import sys

# Account for the fact we can't put everything into the final fold for skipped.
# Solution, create a dictionary with each of the data we will write into each fold and write at the end.

def getOppositeClass(c):
    if c == 'yes':
        return 'no'
    else:
        return 'yes'

in_file = open("pima.csv")
out_file = open("pima-fold.csv", "w+")
data = in_file.read().splitlines()
data_length = len(data)
yes_skipped = []
no_skipped = []
yes_instance = 0; no_instance = 0
tally = []

remainder = len(data) % 10

curr_line = 0
lines_per_fold = int(data_length / 10)

folds = dict()

for i in range(10):
    yes_instance = 0
    no_instance = 0
    curr_fold = 'fold' + str(i + 1)
    folds[curr_fold] = []
    for j in range(lines_per_fold):
        line = data[curr_line]
        class_of_line = line.split(',')[-1]
        if class_of_line == 'yes' and yes_instance < int(lines_per_fold/2):
            folds[curr_fold].append(line)
            yes_instance += 1
        elif class_of_line == 'no' and no_instance < int(lines_per_fold/2):
            folds[curr_fold].append(line)
            no_instance += 1
        else:
            if class_of_line == 'no':
                no_skipped.append(data[curr_line])
            else:
                yes_skipped.append(data[curr_line])
        curr_line += 1
    tally.append([yes_instance, no_instance])

while curr_line < data_length:
    if data[curr_line].split(',')[-1] == 'yes':
        yes_skipped.append(data[curr_line])
    else:
        no_skipped.append(data[curr_line])
    curr_line+=1



for i in range(10):
    yes_instance, no_instance = tally[i]
    while True:
        if yes_instance < int(lines_per_fold/2) and len(yes_skipped) != 0:
            folds['fold'+str(i+1)].append(yes_skipped.pop())
            yes_instance += 1
        elif no_instance < int(lines_per_fold/2) and len(no_skipped) != 0:
            folds['fold' + str(i + 1)].append(no_skipped.pop())
            no_instance += 1
        else:
            break
    while len(folds['fold' + str(i + 1)]) < lines_per_fold:
        if len(yes_skipped) != 0:
            folds['fold' + str(i + 1)].append(yes_skipped.pop())
            yes_instance += 1
        elif len(no_skipped) != 0:
            folds['fold' + str(i + 1)].append(no_skipped.pop())
            no_instance += 1
        else:
            break
    tally[i] = [yes_instance, no_instance]
i = 0
while len(yes_skipped) != 0 or len(no_skipped) != 0:
    if len(yes_skipped) != 0:
        folds['fold' + str(i + 1)].append(yes_skipped.pop())
        tally[i][0] += 1
    else:
        folds['fold' + str(i + 1)].append(no_skipped.pop())
        tally[i][1] += 1
    i+=1

for i in range(10):
    out_file.write("fold" + str(i + 1) + '\n')
    for line in folds["fold" + str(i + 1)]:
        out_file.write(line + '\n')
    out_file.write('\n')