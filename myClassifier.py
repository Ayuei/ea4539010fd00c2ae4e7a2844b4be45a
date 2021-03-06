import sys
import numpy as np
import math

train_file, test_file, classifier = sys.argv[1:4]

flag=False
try:
    flag = sys.argv[4]
except IndexError:
    pass

# DECISION TREE METHODS:


# domains of attributes: used for DT algorithm
# key: index of attribute
# value: list of possible values of attribute
# used to ensure every possible value of each attribute has a branch

attribute_domain = dict()

# Calculate entropy of numpy array with elements in {"yes", "no"}
# expect non-zero example_classes
def entropy(example_classes):
    size = example_classes.size


    class_is_yes = example_classes=="yes" # (array of booleans)
    num_yes = example_classes[class_is_yes].size
    num_no = size - num_yes

    p_yes = num_yes/size
    p_no = num_no/size

    # log_2(0) := 0 for this purpose
    log_p_yes = math.log(p_yes,2) if p_yes != 0 else 0
    log_p_no = math.log(p_no,2) if p_no != 0 else 0

    H = - (p_yes*log_p_yes + p_no*log_p_no)
    return H

# calculate, return reminder of examples with respect to attribute:
# reminder =
# sum over values (P(attribute==value)*entropy(subset of examples where attribute==value)
def reminder(examples, attribute):
    # reminder = sum over values of (P(at=val)*entropy(examples where at=val))
    rem = 0

    num_examples = examples.shape[0]

    #iterate over all possible values of attribute
    for value in attribute_domain[attribute]:
        examples_with_value = examples[examples[:,attribute]==value]
        num_ex_with_value = examples_with_value.shape[0]
        if num_ex_with_value == 0:
            # p_v = 0 and entropy is undefined
            continue
        # probability P(A=value)
        p_v = num_ex_with_value/num_examples


        rem += p_v*entropy(examples_with_value[:,-1])

    return rem


# return string == majority class of given examples ("yes"/"no")
# or None if examples is empty
# examples in format: rows = example, cols = attributes, last col = class
def majorityClass(examples):
    if examples.shape[0]==0:
        return None
    else:
        n_yes = examples[examples[:,-1]=="yes"].shape[0];
        n_no = examples.shape[0]-n_yes
        # "yes" is tiebreaker
        return "yes" if n_yes >= n_no else "no"


# parameters:
# examples: numpy array of examples in format:
#           rows = example, cols = attributes, last col = class
# attributes: list of indices of attributes (column indices)
#
# return:
# attribute with largest information gain
def chooseAttribute(examples, attributes):
    best_attribute = None
    max_gain = 0

    # calculate entropy of given examples
    base_entropy = entropy(examples[:,-1])

    for attribute in attributes:
        info_gain = base_entropy - reminder(examples, attribute)
        if info_gain >= max_gain:
            max_gain = info_gain
            best_attribute = attribute
    return best_attribute


# Might need to reformat a bit
class DecisionTree:

    # takes index of attribute tested at this node as argument
    # attribute = None -> is child
    def __init__(self, attribute=None):
        self.children = dict() # dictionary: attribute_value=key, sub_tree=value
        self.attribute = attribute # attribute tested at root of this tree
        self.is_leaf = True if attribute is None else False
        self.leaf_class = None

    # add child: subtree to follow when self.attribute = value
    def addSubtree(self, value, sub_tree):
        self.children[value] = sub_tree

    # adds leaf value to the tree if self.is_leaf
    def addLeafClass(self, leaf_class):
        if (self.is_leaf):
            self.leaf_class = leaf_class

    # rudimentary recursive print method.
    # need to update for readability
    def printTree(self, leading = ""):
        if self.is_leaf:
            print(leading, "class:",self.leaf_class)
        else:
            attribute = self.attribute
            for att_value, child in self.children.items():
                print(leading, "attribute", attribute, "==", att_value, ":")
                child.printTree(leading+"|  ")


# Create, return a decision tree based on examples
# parameters:
# - examples: numpy array of examples in format:
#           rows = example, cols = attributes, last col = class
# - attributes: list of indices of attributes (column indices)
# - default: majority class of parent node (either "yes" or "no")
def createDT(examples, attributes, default=None):
    # no examples: use default
    num_examples = examples.shape[0]

    if num_examples==0:
        tree = DecisionTree()
        tree.addLeafClass(default)
    # all have same class: use that class
    elif (num_examples == examples[examples[:,-1]==examples[0,-1]].shape[0]):
        tree = DecisionTree()

        tree.addLeafClass(examples[0,-1])
    # no more examples
    elif len(attributes)==0:
        tree = DecisionTree()
        tree.addLeafClass(majorityClass(examples))

    else:
        # decide on attribute to test at this level
        best_attribute = chooseAttribute(examples, attributes)

        # create tree with root testing best_attribute
        tree = DecisionTree(best_attribute)

        # attributes of sub_trees
        atts_without_best = list(attributes) # copy
        atts_without_best.remove(best_attribute)
        sub_default = majorityClass(examples)

        # create subtrees
        for value in attribute_domain[best_attribute]:

            # examples where best_attribute == value
            sub_examples = examples[examples[:,best_attribute]==value]

            sub_tree = createDT(sub_examples, atts_without_best, sub_default)
            tree.addSubtree(value, sub_tree)
    return tree
        # create sub-trees with example sub-sets split by its possible values

    # pseudo code
    # http://puu.sh/vNiO0/d05b24c98b.jpg
    #
    # Information gain definition
    # http://puu.sh/vNiLk/f82ecd39af.jpg

# returns list of classes ("yes" or "no"):
# ith element is class of ith row in test_data, as classified by decision_tree
def DTClassify(decision_tree, test_data):
    classes = []
    # iterate over examples (rows)
    for i in range(test_data.shape[0]):
        example = test_data[i,:];
        # traverse DT:
        tree = decision_tree
        at_leaf = tree.is_leaf
        while (not at_leaf):

            attribute = tree.attribute
            value = str(example[attribute])

            tree = tree.children[value]
            at_leaf = tree.is_leaf

            # time.sleep(0.1)
        classes.append(tree.leaf_class)
    return classes

# # NAIVE BAYES METHODS:



# return probability density that attribute == x
# x: test value of attribute
# mu: mean of attribute for class == yes(/no)
# sigma: stdev for attribute for class == yes(/no)
def probabilityDensity(x, mu, sigma):
    coeff = 1/(sigma*math.sqrt(2*math.pi))
    exponential = math.exp(-((x-mu)**2)/(2*sigma**2))
    return coeff*exponential


# Idea: catalogue mean, stdev for each attribute for class==yes and class==no
# Place in dictionary with key "class"+"attributeindex"+"mu/sigma"
# so mean of 3rd attribute given "yes" would have key "yes4mu"
# train_data: numpy array of training data.
# column<->attributes (last col==class)
# finally, P(class) has key "p"+class_name, e.g. "pyes"

def getStatistics(train_data):

    statistics = dict()

    num_rows = train_data.shape[0]
    num_cols = train_data.shape[1]

    for class_name in ["yes", "no"]:
        # get training data with class==class_name
        class_data = train_data[train_data[:,-1]==class_name]
        statistics["p"+class_name] = class_data.shape[0]/num_rows

        # iterate over non-class columns
        for j in range(num_cols-1):
            column = class_data[:,j].astype(float)

            #  mean
            mu = np.mean(column);

            #gives (xi-mu)**2
            shifted_column_squared = np.square(column-mu)

            # standard deviation
            sigma = math.sqrt(np.sum(shifted_column_squared)/(num_rows-1))

            statistics[class_name + str(j) + "mu"] = mu
            statistics[class_name + str(j) + "sigma"] = sigma

    return statistics


# Runs full Naive Bayes training and testing
# returns list of classes ("yes" or "no"):
# ith element is class of ith row in test_data
def NaiveBayes(train_data, test_data):
    statistics = getStatistics(train_data)

    classes = []

    num_rows = test_data.shape[0]
    num_cols = test_data.shape[1]

    for i in range(num_rows):

        # numerator of Bayes' thm. (P(yes/no|attribute_values)):
        # product of probability densities for each attribute * probability of class
        # init value: probability of class
        yes_numerator = statistics["pyes"]
        no_numerator = statistics["pno"]

        # iterate over attributes
        for j in range(num_cols-1):

           # mean and stdevs of attribute given yes/no
           yes_mu = statistics["yes"+str(j)+"mu"]
           yes_sigma = statistics["yes"+str(j)+"sigma"]
           no_mu = statistics["no"+str(j)+"mu"]
           no_sigma = statistics["no"+str(j)+"sigma"]

           # get probability densities
           att_value = test_data[i,j].astype(float)
           yes_pd = probabilityDensity(att_value, yes_mu, yes_sigma)
           no_pd = probabilityDensity(att_value, no_mu, no_sigma)


           # update numerators
           yes_numerator*=yes_pd
           no_numerator*=no_pd


        # set classes[i].
        # choosing yes as tie-breaker
        classes.append("yes" if yes_numerator >= no_numerator else "no")

    return classes

# GENERIC METHODS


# Returns a 2D numpy array from the given file
# Data type: strings
# Rows: examples. Columns: attributes. Last column: class.
def parseFile(file_name):
    in_file = open(file_name, 'r')
    lines = in_file.read().splitlines()
    num_rows = len(lines)

    rows = [] # list of rows, which are stored as lists

    for i in range(num_rows):
        row = lines[i].split(',')
        rows.append(row)

    return np.array(rows)

def getAccuracy(predicted_classes, actual_classes):
    count = 0
    for p_class, a_class in zip(predicted_classes, actual_classes):
        if p_class == str(a_class): count += 1
    return float(count)/len(actual_classes)*100

def main():

    training_data = parseFile(train_file)
    test_data = parseFile(test_file)
    predicted_classes = []
    dt = object
    # populate classes
    if classifier.lower() == 'nb':
        predicted_classes = NaiveBayes(training_data, test_data)
    elif classifier.lower() == 'dt':
        # fill attribute domain dictionary (assuming training data contains all)
        # iterate over all attributes
        num_cols = training_data.shape[1]
        for j in range (num_cols-1):
            # list of unique values in jth column
            attribute_domain[j] = (np.unique(training_data[:,j])).tolist()
            # create decision tree using training data, based on all examples
        dt = createDT(training_data, range(training_data.shape[1]-1))

        predicted_classes = DTClassify(dt, test_data)
   
    try:
        if flag and classifier.lower() == 'dt': print(dt.printTree())
        #print('\n'.join(predicted_classes))
        #if flag: print('Accuracy: '+"{0:.2f}".format(getAccuracy(predicted_classes, actual_classes=test_data[:,-1]))+"%")

    except Exception:
        pass
        #print('\n'.join(predicted_classes))
        #print('Accuracy: ' + "{0:.2f}".format(getAccuracy(predicted_classes, actual_classes=test_data[:, -1])) + "%")
    print('\n'.join(predicted_classes))

if __name__ == '__main__':
    sys.exit(main())
