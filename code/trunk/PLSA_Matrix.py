from numpy import asarray
import numpy as np
from utils import normalize
import glob
import pprint
import os
from math import exp
import cPickle
from operator import itemgetter
import mpmath
from collections import defaultdict
import time

start_time = time.time()


number_of_latent_topics=input("Please Enter the number of topics")   #User given
print(number_of_latent_topics)

path='C:\data2\\' # to be set up before running

sum1=0

thedictionary = defaultdict(list)
doc1=0
start_time_dictionary=time.time()

document_file_list = []
files_list = glob.glob(os.path.join(path, '*.txt'))

for conference_file in files_list:
    #print(conference_file)

    document_file_list.append(conference_file)
    doc1=doc1+1
    with open(conference_file) as f:
            file_contents = f.read().lower().split('\n') # split line on spaces to make a list

    for author_name in (file_contents):

             thedictionary[author_name].append(doc1)

author=[]

for k in thedictionary.keys():
    author.append(k)
#print(len(author))


temp=0
doc_auth = np.zeros([doc1, len(author)])

matrix_doc_author = np.zeros([doc1+1, len(author)], dtype=np.float)


from collections import defaultdict
nesteddict = defaultdict(list)
at=0
doc = 0
authdict=defaultdict(int)
for conference_file in glob.glob(os.path.join(path, '*.txt')):


    with open(conference_file) as f:
            doc=doc+1

            file_contents = f.read().lower().split('\n') # split line on spaces to make a list

            authdict=defaultdict(int)
            for author_name in (file_contents):

                position = author.index(author_name)

                matrix_doc_author[doc][position] += 1

                authdict[author_name] +=1

            nesteddict[doc].append(authdict)

print("diiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")




for i in range(0,doc1):
    for x in range(0, len(author)):
        if(matrix_doc_author[i][x] == 0):
            matrix_doc_author[i][x] = 0.000004# putting a non zero value to the matrix where the entries are zero



        else:
            continue


total_number_conference=doc
number_of_authors= len(author)
max_executions =15




latent_topic_prob=np.zeros([total_number_conference, number_of_authors,number_of_latent_topics], dtype=np.float)


print("Initialize")

conrow_topiccol_prob=np.zeros([total_number_conference,number_of_latent_topics],dtype=np.float)
conrow_topiccol_prob = np.random.random(size=(total_number_conference,number_of_latent_topics))#randomly assigning value
for d_index in range(0, total_number_conference):#normalize for each document
    normalize(conrow_topiccol_prob[d_index])

print("*******************************************************************************************************")
topicrow_authorcol_prob=np.zeros([number_of_latent_topics,number_of_authors], dtype=np.float)
topicrow_authorcol_prob = np.random.random(size=(number_of_latent_topics,number_of_authors))
for z in range(number_of_latent_topics):
    normalize(topicrow_authorcol_prob[z])



print("********************************************************************************************************")
finish_dictionary_time = time.time()-start_time_dictionary
print("time taken for making Matrix data structure")
print(finish_dictionary_time)
start_EM=time.time()

B=0
for i in range(0,max_executions):
    den=0
    for d in range(0,total_number_conference):
        for a in range(0,number_of_authors):
            for z in range(0,number_of_latent_topics):

                    latent_topic_prob[d][a][z] = conrow_topiccol_prob[d][z] * topicrow_authorcol_prob[z][a]
                    den += conrow_topiccol_prob[d][z] * topicrow_authorcol_prob[z][a]

            prob = latent_topic_prob[d][a][z]/den



            latent_topic_prob[d][a][z] = prob



    # M step
    #maximizing p(w|z)


    for z in range(number_of_latent_topics):
        for w in range(0,number_of_authors):
            det = 0
            for d in range(0,total_number_conference):
                det = det+(matrix_doc_author[d, w] * latent_topic_prob[d, w, z])

            topicrow_authorcol_prob[z][w]= det
        normalize(topicrow_authorcol_prob[z])


    #maximizing p(z|d)
    for d in range(0,total_number_conference):
        for z in range(0,number_of_latent_topics):
            dek = 0
            for a in range(0,number_of_authors):
                dek = dek + (matrix_doc_author[d, a] * latent_topic_prob[d, a, z])
            conrow_topiccol_prob[d][z] = dek
        normalize(conrow_topiccol_prob[d])


finish_EM=time.time()-start_EM
print("EM Taken:")
print(finish_EM)



#clustering
start_cluster=time.time()
maxvalue =defaultdict(list)
for i in range(1,doc1):

        temp=conrow_topiccol_prob.argmax(axis=1)
#print("temp")
#print(temp)
k=0
i=0


for j in temp:
        maxvalue[j].append(i)
        i=i+1
print(maxvalue)

tempconflist=defaultdict(list)
for j in maxvalue.keys():
    tempconflist2 = []
    namelist = []

    print(j,maxvalue[j])

    n="topic"+str(j)
    file_name ='C:\output\\%s.txt' %n #output directory should be ready before running
    f2 = open(file_name, 'w')


    tempconflist2.append(maxvalue[j])


    temp = str(tempconflist2)


    for l in tempconflist2[0]:


        l=l+1
        x=len(repr(abs(l)))


        if x==1:
            l="0000"+str(l)
        if x==2:
            l="000"+str(l)
        if x==3:
            l="00"+str(l)
        if x==4:
            l="0"+str(l)

        file_name2="C:\data2\\%s.txt" %l    # to be set up before running



        for conf_file in glob.glob(os.path.join(path, '*.txt')):


            if file_name2 == conf_file:
                with open(conf_file) as f:
                    file_contents2=f.read()
                    name_of_conference=file_contents2.split('\n',1)[0]


                    namelist.append(name_of_conference)

    tem=str(namelist)

    f2.write(tem)
finish_cluster=time.time()-start_cluster
print("Time taken for clustering")
print(finish_cluster)

total_time=time.time()-start_time
print("total time")
print(total_time)
