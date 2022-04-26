# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 00:51:16 2021

@author: ABC
"""
#__author__ = 'arathi'

import csv
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
# review.csv contains two columns
# first column is the review content (quoted)
# second column is the assigned sentiment (positive or negative)
def load_file():
    with open('dataset.csv',encoding="utf8") as csv_file:
        reader = csv.reader(csv_file,delimiter=",",quotechar='"')
        #reader.next()
       #next(reader1)
      # for row in spamreader:
        data =[]
        target = []
        for row in reader:
            # skip missing data
            print (', '.join(row))
            if row[0] and row[1]:
                data.append(row[0])
                target.append(row[1])

        return data,target

# preprocess creates the term frequency matrix for the review data set
def preprocess():
    data,target = load_file()
    count_vectorizer = CountVectorizer(binary='true')
    data = count_vectorizer.fit_transform(data)
    tfidf_data = TfidfTransformer(use_idf=False).fit_transform(data)

    return tfidf_data

def learn_model(data,target):
    # preparing data for split validation. 60% training, 40% test
    data_train,data_test,target_train,target_test = train_test_split(data,target,test_size=0.4,random_state=43)

    classifier = RandomForestClassifier(max_depth=2, random_state=0)
    classifier.fit(data_train,target_train)
  
    predicted = classifier.predict(data_test)
    evaluate_model(target_test,predicted)
def plot_classification_report(cr, title='Classification report ', with_avg_total=False, cmap=plt.cm.Blues):

    lines = cr.split('\n')

    classes = []
    plotMat = []
    for line in lines[2 : (len(lines) - 3)]:
        #print(line)
        t = line.split()
        # print(t)
        classes.append(t[0])
        v = [float(x) for x in t[1: len(t) - 1]]
        print(v)
        plotMat.append(v)

    if with_avg_total:
        aveTotal = lines[len(lines) - 1].split()
        classes.append('avg/total')
        vAveTotal = [float(x) for x in t[1:len(aveTotal) - 1]]
        plotMat.append(vAveTotal)


    plt.imshow(plotMat, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    x_tick_marks = np.arange(3)
    y_tick_marks = np.arange(len(classes))
    plt.xticks(x_tick_marks, ['precision', 'recall', 'f1-score'], rotation=45)
    plt.yticks(y_tick_marks, classes)
    plt.tight_layout()
    plt.ylabel('Classes')
    plt.xlabel('Measures')
# read more about model evaluation metrics here
# http://scikit-learn.org/stable/modules/model_evaluation.html
def evaluate_model(target_true,target_predicted):
    #print (classification_report(target_true,target_predicted))
    print (classification_report(target_true,target_predicted))
    cm=confusion_matrix(target_true,target_predicted)
    print('True positive = ', cm[0][0])
    print('False positive = ', cm[0][1])
    print('False negative = ', cm[1][0])
    print('True negative = ', cm[1][1])
    spam_caught=cm[1][1]/(cm[1][1]+cm[1][0])
    blocked_hams=cm[0][1]/(cm[0][0]+cm[0][1])
    accuracyvalue=accuracy_score(target_true,target_predicted)
    print ("The accuracy score is {:.2%}".format(accuracy_score(target_true,target_predicted)))
    print ("The Spam Caught is {:.2%}".format(spam_caught))
    print ("The Blocked Ham is {:.2%}".format(blocked_hams))
    plt.figure()
    DayOfWeekOfCall = [1]
    DispatchesOnThisWeekday = [accuracyvalue*100]
    LABELS = ["Accuracy"]
    plt.bar(DayOfWeekOfCall, DispatchesOnThisWeekday, align='center')
    plt.xticks(DayOfWeekOfCall, LABELS) 
    plt.show()
    #plot_classification_report(classification_report(target_true,target_predicted))
def main():
    data,target = load_file()
    tf_idf = preprocess()
    learn_model(tf_idf,target)


main()

