from numpy import asarray
import numpy as np
import glob
import pprint
import os
from math import exp
import cPickle
from operator import itemgetter
from collections import defaultdict
import pprint
import time
from operator import itemgetter
start_time = time.time()
path= 'C:\data\\'
path2='C:\data2\\'


num=input("Enter the number of topics")
print(num)

thedictionary = defaultdict(list)
authdictionary = defaultdict(list)
cnf=0
sum1=0
start_time_dictionary=time.time()-start_time
#path='C:\exp\\'
#path2='C:\exp2\\'
thedictionary = defaultdict(list)
authdictionary = defaultdict(list)
author = []
for document_file in glob.glob(os.path.join(path, '*.txt')):
    #print document_file
    f = open('C:\output\\output.txt', 'a')
    f.write(document_file)
    f.write("\n")

    with open(document_file) as f:
        cnf=cnf+1
        file_contents = f.read().lower().split('\n')
        for ath in file_contents:
            if ath != '':
                thedictionary[cnf].append(ath)
                authdictionary[ath].append(cnf)
                author.append(ath)

inDict = defaultdict(list)
f.close()
for cnfr in thedictionary.keys():
    tempDict = defaultdict(int)
    for ath in thedictionary[cnfr]:

        tempDict[ath] +=1
    inDict[cnfr].append(tempDict)
author=list(set(author))

#print("indict")
#print(inDict)
number_of_conference=cnf
number_of_topics=num
number_of_author=len(author)
max_iteration=28
con_topic_prob=defaultdict(list)

for cnfr in inDict.keys():
    temp = np.random.random(size= (1,number_of_topics))
    #print("tEMP")
    #print(temp)
    con_topic_prob[cnfr].append(temp/np.sum(temp))
topic_author_prob=defaultdict(list)

#print("con_topic")
#print(con_topic_prob)

for topic in range(1, number_of_topics+1):
    temp = np.random.random(size= (1, len(author)))
    topic_author_prob[topic].append(temp/np.sum(temp))

topic_prob=defaultdict(list)
for conf in inDict.keys():
    tempDict = defaultdict(list)
    for ath in inDict[conf]:

        for auth in ath.keys():


            temp = np.random.random(size=(1,number_of_topics))

            tempDict[auth].append(temp)
        topic_prob[conf].append(tempDict)
    #print("topic Probability")
    #print(topic_prob[conf][0])

finish_dictionary_time = time.time()-start_time_dictionary
print("time taken for making dictionary")
print(finish_dictionary_time)
start_EM=time.time()

B = 0
for i in range(0,max_iteration):
    #E step
    for conf in inDict.keys():
        for ath in inDict[conf][0].keys():


            indx=author.index(ath)
            den=0
            for top in range(1, number_of_topics+1):
                den +=con_topic_prob[conf][0][0][top-1] * topic_author_prob[top][0][0][indx]
            for top2 in range(1,number_of_topics+1):
                topic_prob[conf][0][ath][0][0][top2-1]= con_topic_prob[conf][0][0][top2-1] * topic_author_prob[top2][0][0][indx]
                prob = topic_prob[conf][0][ath][0][0][top2-1]/den

                topic_prob[conf][0][ath][0][0][top2-1] = prob

    #Mstep
    #Maximising p(w|z)
    for top in range(1, number_of_topics+1):
        temp = 0
        for a in authdictionary.keys():
            det=0
            idx=author.index(a)

            for d in list(set(authdictionary[a])):
                det +=inDict[d][0][a] * topic_prob[d][0][a][0][0][top-1]
            topic_author_prob[top][0][0][idx] = det
            temp +=det
        topic_author_prob[top][0][0]=(topic_author_prob[top][0][0]/temp)

    for conf in inDict.keys():
        temp =0

        for topic2 in range(1, number_of_topics+1):
            det = 0
            for ath in inDict[conf][0].keys():

                det += inDict[conf][0][ath] * topic_prob[conf][0][ath][0][0][topic2-1]
            con_topic_prob[conf][0][0][topic2-1] = det
            temp += det
        con_topic_prob[conf][0][0] = (con_topic_prob[conf][0][0])/temp

#print("printing con_topic: ")
#print(con_topic_prob)
finish_EM=time.time()-start_EM
print("EM Taken:")
print(finish_EM)
start_cluster=time.time()
for c in con_topic_prob.keys():

    temp = (max(con_topic_prob[c][0][0]))

    temp2=np.where(con_topic_prob[c][0][0] == temp)
    #print(temp2[0][0])
    x=str(temp2)
    y=str(temp)
    f = open('C:\output\\output.txt', 'a')
    f.write(x)
    f.write(y)
    f.write("\n")

#Clustering

cluster = defaultdict(list)
tempDict3=defaultdict(list)
#tempDict2=defaultdict(list)
for t in range(1,number_of_topics + 1):
    tempDict2=defaultdict(list)
    sorted_tempDict2 = defaultdict(list)

    for c in con_topic_prob.keys():

        #tempDict3=defaultdict(list)
        temp3 = (max(con_topic_prob[c][0][0]))
        topic_number =(np.where((con_topic_prob[c][0][0]) == temp3))

        if (topic_number[0][0]) == (t-1):
            #print(c)
            #print ("topic")
            #print (topic_number[0][0])
            tempDict2[c].append(temp3)

            # print(tempDict2)
    sorted_tempDict2=dict(sorted(tempDict2.items(),key = itemgetter(1),reverse=True)[:10])
    tempDict3[t].append(sorted_tempDict2)
    x=tempDict3[t][0]
    #print(t)
    #print(x)

print(tempDict3)
    #tempDict2[temp2[0][0]].append(temp3)
#print(tempDict3)


print("clustering done")

for j in tempDict3.keys():
    templist = []
    namelist= []
    print(j,tempDict3[j])
    #j=j+1
    n="topic"+str(j)
    file_name ='C:\output\\%s.txt' %n
    f2 = open(file_name, 'w')
    templist.append(tempDict3[j])
    tem = str(templist)
    #print("TEMPLIST")
    #print(templist)

    for l in templist[0][0].keys():
        #print("lll")
        #print(l)
        m=str(l)

        file_name2="C:\data2\\%s.txt" %m #containing name of conference
        for conf_file in glob.glob(os.path.join(path2, '*.txt')):
            if (conf_file==file_name2):
                with open(file_name2) as f:
                    file_contents2=f.read()
                    name_of_conference=file_contents2.split('\n',1)[0]
                    #print(name_of_conference)
                    namelist.append(name_of_conference)
    #print(namelist)
    tem=str(namelist)
    #print(tem)
    f2.write(tem)

finish_cluster=time.time()-start_cluster
print("Time taken for clustering")
print(finish_cluster)

total_time=time.time()-start_time
print("total time")
print(total_time)