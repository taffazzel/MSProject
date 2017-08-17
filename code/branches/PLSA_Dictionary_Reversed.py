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
from collections import OrderedDict
from matplotlib import pyplot
import matplotlib.cm as cm



start_time = time.time()
#path= 'C:\data\\'
path2='C:\data2\\' # to be set up before running the program
#path='c:\exp\\'

number_of_topics=input("Please Enter the number of topics")
print(number_of_topics)

max_iteration=input("Please Enter the Upper limit to execute E-M")
print(max_iteration)


thedictionary = defaultdict(list)
authdictionary = defaultdict(list)
cnf=0
sum1=0
start_time_dictionary=time.time()

thedictionary = defaultdict(list)
authdictionary = defaultdict(list)
author = []
conferences = []

for conference_file in glob.glob(os.path.join(path2, '*.txt')):

    with open(conference_file) as f:
        cnf=cnf+1
        conferences.append(cnf)


        file_contents = f.read().lower().split('\n')[1:]


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
conferences = list(set(conferences))

number_of_conference=len(conferences)

number_of_author=len(author)



topic_con_prob=defaultdict(list)

for top in range(1,number_of_topics+1):
    temp = np.random.random(size=(1,number_of_conference))
    topic_con_prob[top].append(temp/np.sum(temp))

#print("con_topic")
#print(con_topic_prob)

author_topic_prob=defaultdict(list)
for aut in author:
    temp = np.random.random(size=(1,(number_of_topics)))
    author_topic_prob[aut].append(temp/np.sum(temp))

topic_prob=defaultdict(list)
for conf in inDict.keys():
    tempDict = defaultdict(list)
    for ath in inDict[conf]:

        for auth in ath.keys():

            temp = np.random.random(size=(1,number_of_topics))

            tempDict[auth].append(temp)
        topic_prob[conf].append(tempDict)


finish_dictionary_time = time.time()-start_time_dictionary
print("time taken for making dictionary")
print(finish_dictionary_time)
start_EM=time.time()


for i in range(0,max_iteration):
    #E step


    for conf in inDict.keys():
        for ath in inDict[conf][0].keys():

            indx=conferences.index(conf)
            den=0
            for top in range(1, number_of_topics+1):
                den +=topic_con_prob[top][0][0][indx] * author_topic_prob[ath][0][0][top-1]
            for top2 in range(1,number_of_topics+1):
                topic_prob[conf][0][ath][0][0][top2-1]= topic_con_prob[top2][0][0][indx] * author_topic_prob[ath][0][0][top2-1]
                prob = topic_prob[conf][0][ath][0][0][top2-1]/den

                if (prob == 1):

                    topic_prob[conf][0][ath][0][0][top2-1] = prob


                    break;

    #Mstep
    #Maximising p(w|z)

    for a in authdictionary.keys():
        temp = 0
        for top in range(1, number_of_topics+1):
            det=0
            for d in list(set(authdictionary[a])):
                det +=inDict[d][0][a] * topic_prob[d][0][a][0][0][top-1]
            author_topic_prob[a][0][0][top-1] = det
            temp +=det
        author_topic_prob[a][0][0]=(author_topic_prob[a][0][0]/temp)

    for topic2 in range(1, number_of_topics+1):
        temp =0
        for conf in inDict.keys():
            indx = conferences.index(conf)
            det = 0
            for ath in inDict[conf][0].keys():
                det += inDict[conf][0][ath] * topic_prob[conf][0][ath][0][0][topic2-1]
            topic_con_prob[topic2][0][0][indx] = det
            temp += det
        topic_con_prob[topic2][0][0] = (topic_con_prob[topic2][0][0])/temp



top_conf_updated=defaultdict(list)
sorted_top_conf=defaultdict(list)
conf_dict = defaultdict(int)
conf_dict_sorted = defaultdict(int)

colors = cm.rainbow(np.linspace(0,1,number_of_topics))

for top, c in zip(range(1,number_of_topics +1), colors):
    for conf in inDict.keys():
        indx = conferences.index(conf)
        conf_dict[conf]= topic_con_prob[top][0][0][indx]

    conf_dict_sorted = OrderedDict(sorted(conf_dict.items(), key=lambda x: x[1], reverse = True))
    sorted_top_conf[top].append(conf_dict_sorted)
    print "topic = %i" %top
    #print(sorted_top_conf[top])
    pyplot.scatter(conferences,topic_con_prob[top][0][0],color=c)
    pyplot.plot(conferences,topic_con_prob[top][0][0],color=c)

pyplot.legend(range(1,number_of_topics+1))
pyplot.show()



#############################################################
# sorting
for con in thedictionary.keys():
    temp_prob_cluster=defaultdict(list)
    temp_prob_sorted=defaultdict(list)
    for t in range(1,number_of_topics+1):

        temp3= (max(topic_con_prob[t][0][0]))

        conference_number=(np.where(topic_con_prob[t][0][0]==temp3))

    temp_prob_cluster[t].append(conference_number[0][0])


#print(top_conf_updated)
#sorting done

finish_EM=time.time()-start_EM
print("EM Taken:")
print(finish_EM)


conference_clustering = defaultdict(list)

for c in conferences:
    maxValue = 0
    maxPosition = 0
    indx = conferences.index(c)

    temp_prob={}
    for t in range(1,number_of_topics+1):
        if maxValue <= topic_con_prob[t][0][0][indx]:
            maxValue = topic_con_prob[t][0][0][indx]
            maxPosition = t

    conference_clustering[maxPosition].append(c);

#print("AFTER CLUETERING")
print(conference_clustering)




start_cluster=time.time()
#Clustering



for topic in conference_clustering.keys():
    #print(topic)

    templist = []
    namelist= []
    n="topic"+str(topic)
    file_name='C:\output\\%s.txt'%n
    f2=open(file_name,'a')
    templist.append(conference_clustering[topic])
    for con in templist[0]:


        x=len(repr(abs(con)))

        if x==1:
            con="0000"+str(con)
        if x==2:
            con="000"+str(con)
        if x==3:
            con="00"+str(con)
        if x==4:
            con="0"+str(con)


        file_name2="C:\data2\\%s.txt" %con   # to be set up before running



        for conf_file in glob.glob(os.path.join(path2, '*.txt')):



                if file_name2 == conf_file:

                    with open(conf_file) as f:
                        file_contents2=f.read()



                        name_of_conference=file_contents2.split('\n',1)[0]

                        namelist.append(name_of_conference)
                else:
                    continue

    tem=str(namelist)
    f2.write(tem)



finish_cluster=time.time()-start_cluster
print("Time taken for clustering")
print(finish_cluster)

total_time=time.time()-start_time
print("total time")
print(total_time)

