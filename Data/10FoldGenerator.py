import random
from collections import defaultdict

in_file = open("pima.csv")
out_file = open("pima-fold.pickle", "wb+")
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
	
import pickle

pickle.dump(folds, out_file)
