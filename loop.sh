#!/bin/sh
set -e
discrete=( "pima-discretised-CFS.csv" "pima-indians-diabetes.discrete" )
bayes=( "pima.csv" "pima-CFS.csv" )

for i in ${bayes[@]}
do
	echo "Bayes" $i
	"Anaconda3-4"/python 10FoldGenerator.py $i
	"Anaconda3-4"/python myClassifier.py nb
done

for i in ${discrete[@]}
do
	echo "DT" $i
	"Anaconda3-4"/python 10FoldGenerator.py $i
	"Anaconda3-4"/python myClassifier.py dt
done
