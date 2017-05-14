import numpy as np
import math

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
        for j in range(num_cols):
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


# runs full NaiveBayes training and testing
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
N
