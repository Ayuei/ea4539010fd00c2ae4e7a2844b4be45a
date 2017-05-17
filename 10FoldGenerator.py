import random
from collections import defaultdict
import sys
in_file = open(sys.argv[1])
out_file = open("pima-fold.csv", "w+")
data = in_file.read().splitlines()
folds = defaultdict(list)

yes_instances = []; no_instances = []; classes = []
for line in data:
    classes.append(line.split(',')[-1])

for i in range(len(classes)):
    if classes[i] == 'yes':
        yes_instances.append(data[i])
    else:
        no_instances.append(data[i])

random.shuffle(no_instances); random.shuffle(yes_instances)

for i in range(len(yes_instances)):
    folds['fold'+str(i%10+1)].append(yes_instances[i])

for i in range(len(no_instances)):
    folds['fold'+str(i%10+1)].append(no_instances[i])

for i in range(10):
    out_file.write('fold'+str(i+1)+'\n')
    for line in folds['fold'+str(i%10+1)]:
	out_file.write(line+'\n')
    out_file.write('\n')
	
#import pickle

#pickle.dump(folds, out_file)
