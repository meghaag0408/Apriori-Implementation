"""******************************************************************************************
Name - Megha Agarwal
Roll No - 201506511
Course - M.Tech - CSIS (IInd Year)

                                    APRIORI IMPLEMENTATION

Files Required:

input.csv: Input data file will be a comma separated (.csv) file, containing one transaction 
per line. The location of the input file will be against the key input in the config file. 
 
output.csv: The final output of frequent itemsets and association rules are written in the 
output file provided in config.csv file.


config.csv: 
input,$PATH
output,$PATH
support,value
confidence,value
flag,0 or 1
The values of the support and confidence parameters will lie in the range [0,1].  
if flag==0 : Only frequent items are printed, both otherwise

config.csv has to be in the folder where the code is present.

To run the code : python filename.py
********************************************************************************************"""

import sys
from itertools import chain, combinations
from collections import defaultdict
import math
import csv

#Reading the configuration file
def read_config_file():
    config_information = open('config.csv', 'rb')
    for line in config_information:
        test = line.rstrip('\n').split(',')
        if test[0] == "input":
            inputfilename = test[1]
        elif test[0]=="output":
            outputfilename = test[1]
        elif test[0]=="support":
            support=test[1]
        elif test[0]=="confidence":
            confidence=test[1]
        elif test[0]=="flag":
            flag=test[1]

    return inputfilename, outputfilename, support, confidence, flag

#Creating subsets
def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

#Calculation of intersection of values of dictionary
def calculate_intersection(itemset):
    a = set()
    for item in itemset:
        if len(a) == 0:
            a = a | transaction_information[item]
        else:
            a = a & transaction_information[item]
    return a

#Calculating if the given itemset occurs frequently in the transaction
def calculate_frequent_Items(itemset, transaction_information, minSupport):
    tempset=set()
    b='teststring'
    for item in itemset:
        if type(item)!=type(b):
            intersect = calculate_intersection(item)
            freq = len(intersect)
        else:
            freq = len(transaction_information[item])
        if freq >=minSupport:
            if type(item)==type(b):
                l = []
                l.append(item)
                tempset.add(frozenset(l))
            else:
                tempset.add(item)
    return tempset

#Combining items to make itemsets further
def calculate_join(itemSet, length):
    join = set()
    for i in itemSet:
        for j in itemSet:
            if len(i.union(j))== length:
                join.add(i.union(j))
    return join

"""Main Algorithm : Calculate frequent items and association rules
Calls : calculate_frequent_items function for frequent items
Calculate association rules for every frequent item"""
def appriori_algorithm(transaction_information, minSupport, minConfidence, flag):
    itemset = set(transaction_information.keys())
    result_frequent_set=calculate_frequent_Items(itemset, transaction_information, minSupport)
    result_frequent_set = calculate_frequent_Items(result_frequent_set, transaction_information, minSupport)
        
    k = 1
    frequentitems_final = []
    while(result_frequent_set != set([])):
        frequentitems_final.extend([tuple(item) for item in result_frequent_set])
        result_frequent_set = calculate_join(result_frequent_set, k+1)
        result_frequent_set = calculate_frequent_Items(result_frequent_set, transaction_information, minSupport)
        k = k + 1
    
    associationrules_final = []
    for item in frequentitems_final:
        item = frozenset(item)
        _subsets = map(frozenset, [x for x in subsets(item)])
        for element in _subsets:
            remain = item.difference(element)
            if remain:
                 confidence = float(len(calculate_intersection(item)))/float(len(calculate_intersection(element)))
                 if confidence >= minConfidence:
                     associationrules_final.append((tuple(element), tuple(remain)))

    return frequentitems_final, associationrules_final

#Helper function
def tupletostring(tup):
    string=""
    for i in range(len(tup)):
        if i != len(tup)-1: 
            string=string+tup[i]+","
        else:
            string=string+tup[i]
    return string


#Writing to output file
def gettingoutput(items, rules, outputfilename, flag):
    f = open(outputfilename, "w")
    
    #Writing Frequent ItemSets
    f.write(str(len(items)))
    f.write('\n')
    for item in items:
        templist = list(item)
        for i in range(len(templist)):
            if i != len(templist)-1:
                f.write(templist[i])
                f.write(",")
            else:
                f.write(templist[i])
        f.write('\n')

    #Writing Association Rules
    if(flag=='1'):
        f.write(str(len(rules)))
        f.write('\n')
        for rule in rules:
            pre, post = rule
            to_write = tupletostring(pre)+ " => " + tupletostring(post)
            f.write(to_write)
            f.write('\n')

    f.close()


"""Reading the input file and writing the transaction information
The input information is written to a dictionary of format key:(set)
set contains the transaction number in which the item is appearing"""
def input_information(fname):
    transaction_information=dict()
    count=1
    with open(fname, 'rb') as file_dataset:
        lines = list(csv.reader(file_dataset))
        for transaction in lines:
            if transaction[-1]=='':
                transaction = transaction[0:-1]
            for item in transaction:
                if item in transaction_information:
                    transaction_information[item].add(count)
                else:
                    temp2=set()
                    temp2.add(count)
                    transaction_information[item] = temp2            
            count=count+1

    return transaction_information, count-1

#The main function
if __name__ == "__main__":
    inputfilename, outputfilename, support, confidence, flag = read_config_file()
    
    transaction_information, count = input_information(inputfilename)
    transaction_information_length = len(transaction_information)
    support_final = ((float(support) * float(count)))
    
    items, rules = appriori_algorithm(transaction_information, support_final, float(confidence), flag)
    gettingoutput(items, rules, outputfilename, flag)
