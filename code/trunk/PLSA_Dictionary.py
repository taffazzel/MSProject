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


start_time = time.time()                    #capturing the start time of the program
path2= 'C:\data\\'  #input path.To be setup before running




number_of_latent_topics=input("Please Enter the number of topics")   #User given
print(number_of_latent_topics)
max_execution=input("Please enter the upper limit to run EM")
print(max_execution)

thedictionary = defaultdict(list)
authdictionary = defaultdict(list)
cnf=0
sum1=0
start_time_dictionary=time.time()

author = []
for conference_file in glob.glob(os.path.join(path2, '*.txt')):
        with open(conference_file) as f:
            cnf=cnf+1
            file_contents = f.read().lower().split('\n')[1:]
            for ath in file_contents:
                if ath != '':
                    thedictionary[cnf].append(ath)
                    authdictionary[ath].append(cnf)
                    author.append(ath)

inDict = defaultdict(list)
f.close()
for cnfr in thedictionary.keys(): #building the dictionary for each conference
    tempDict = defaultdict(int)
    for ath in thedictionary[cnfr]:
        tempDict[ath] +=1
    inDict[cnfr].append(tempDict)
author=list(set(author))
total_number_of_conference=cnf

number_of_author=len(author)
max_execution=15

conkey_topicval_prob=defaultdict(list)

for cnfr in inDict.keys():  #Normalizing
    temp = np.random.random(size= (1,number_of_latent_topics))
    conkey_topicval_prob[cnfr].append(temp/np.sum(temp))

topickey_authorval_prob=defaultdict(list)

for topic in range(1, number_of_latent_topics+1): # Normalizing
    temp = np.random.random(size= (1, len(author)))
    topickey_authorval_prob[topic].append(temp/np.sum(temp))

latent_topic_prob=defaultdict(list)
for conf in inDict.keys():
    tempDict = defaultdict(list)
    for ath in inDict[conf]:
        for auth in ath.keys():
            temp = np.random.random(size=(1,number_of_latent_topics))
            tempDict[auth].append(temp)
        latent_topic_prob[conf].append(tempDict)

finish_dictionary_time = time.time()-start_time_dictionary
print("time taken for making dictionary")
print(finish_dictionary_time)
start_EM=time.time()   #capturning the system time before starting E-M
#starting E-M
B = 0
for i in range(0,max_execution):
    count = 0;

    B=B+1
    print("B"+str(B))

    # E step
    for conf in inDict.keys():
        for ath in inDict[conf][0].keys():
            indx=author.index(ath)
            den=0
            for top in range(1, number_of_latent_topics+1):
                den +=conkey_topicval_prob[conf][0][0][top-1] * topickey_authorval_prob[top][0][0][indx]
            for top2 in range(1,number_of_latent_topics+1):
                latent_topic_prob[conf][0][ath][0][0][top2-1]= conkey_topicval_prob[conf][0][0][top2-1] * topickey_authorval_prob[top2][0][0][indx]
                probability = latent_topic_prob[conf][0][ath][0][0][top2-1]/den
                latent_topic_prob[conf][0][ath][0][0][top2-1] = probability

    # M step

    for top in range(1, number_of_latent_topics+1):
        temp = 0
        for a in authdictionary.keys():
            det=0
            idx=author.index(a)

            for d in list(set(authdictionary[a])):
                det +=inDict[d][0][a] * latent_topic_prob[d][0][a][0][0][top-1]
            topickey_authorval_prob[top][0][0][idx] = det
            temp +=det
        topickey_authorval_prob[top][0][0]=(topickey_authorval_prob[top][0][0]/temp)
    # maximized P(w|z)

    # M step
    for conf in inDict.keys():
        temp =0

        for topic2 in range(1, number_of_latent_topics+1):
            det = 0
            for ath in inDict[conf][0].keys():

                det += inDict[conf][0][ath] * latent_topic_prob[conf][0][ath][0][0][topic2-1]
            conkey_topicval_prob[conf][0][0][topic2-1] = det
            temp += det
        conkey_topicval_prob[conf][0][0] = (conkey_topicval_prob[conf][0][0])/temp
    # maximized P(z|d)
        if 1.0 in conkey_topicval_prob[conf][0][0]:
            count += 1





    if count == total_number_of_conference: #Coverging point
        print "count = %s " %count
        break;
# E-M finished

finish_EM=time.time()-start_EM  #capturing system and calculting time taken to execute E-M
print("EM Taken:")
print(finish_EM)
start_cluster=time.time()
# sorting
for c in conkey_topicval_prob.keys():
    temp = (max(conkey_topicval_prob[c][0][0]))
    temp2=np.where(conkey_topicval_prob[c][0][0] == temp)
    

#Clustering

cluster = defaultdict(list)
tempDict3=defaultdict(list)

for t in range(1,number_of_latent_topics + 1):
    tempDict2=defaultdict(list)
    sorted_tempDict2 = defaultdict(list)

    for c in conkey_topicval_prob.keys():


        temp3 = (max(conkey_topicval_prob[c][0][0]))
        topic_number =(np.where((conkey_topicval_prob[c][0][0]) == temp3))

        if (topic_number[0][0]) == (t-1):


            tempDict2[c].append(temp3)


    sorted_tempDict2=dict(sorted(tempDict2.items(),key = itemgetter(1),reverse=True)[:10])
    tempDict3[t].append(sorted_tempDict2)
    x=tempDict3[t][0]


print("clustering done")


# writing to local file system
for j in tempDict3.keys():
    templist = []
    namelist= []
    print(j,tempDict3[j])
    n="topic"+str(j)
    file_name ='C:\output\\%s.txt' %n #to be set up before running theprogram
    f2 = open(file_name, 'w')
    templist.append(tempDict3[j])
    tem = str(templist)
    for l in templist[0][0].keys():

        x=len(repr(abs(l)))

        if x==1:
            l="0000"+str(l)
        if x==2:
            l="000"+str(l)
        if l==3:
            l="00"+str(l)
        if l==4:
            l="0"+str(l)

        file_name2="C:\data\\%s.txt" %l #to be set up
        #print("filename_2")
        #print(file_name2)

        for conf_file in glob.glob(os.path.join(path2, '*.txt')):
            #print("CONF")
            #print(conf_file)
            if file_name2 == conf_file:

                with open(conf_file) as f:
                    file_contents2=f.read()
                    name_of_conference=file_contents2.split('\n',1)[0]
                    namelist.append(name_of_conference)
            else:
                continue
    tem=str(namelist)
    f2.write(tem)
# files for each topic ready
finish_cluster=time.time()-start_cluster
print("Time taken for clustering")
print(finish_cluster)

total_time=time.time()-start_time
print("total time")
print(total_time)
