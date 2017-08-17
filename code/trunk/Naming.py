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
#from nltk.corpus import stopwords
from nltk.corpus import stopwords
from collections import Counter
import re
from itertools import groupby
from collections import OrderedDict


#print(brown.words())
path2='C:\output\\' # to be setup before running
newWord=''
i=0
wordCount={}
stop_words = set(stopwords.words("english"))
stop_words.update(('aaa','bbb','zzz','lll','the','conference','workshop','international','technology',
                   'canada','UK','Germany','china'))


for topic_file in glob.glob(os.path.join(path2, '*.txt')):
    #print("AAA")
    #print(topic_file)
    i=i+1
    wordlist_forfile=[]
    wordlist=[]
    word_count_sorted=defaultdict(int)
    temp=defaultdict(int)

    with open(topic_file) as f:

        for line in f:
            newWord=''
            wordlist= re.findall(r"[\w]+",line)
            wordlist=[word for word in wordlist if not word.isdigit()]



            for word in wordlist:

                if word.lower() not in stop_words:
                    temp[word] += 1

            word_count_sorted = OrderedDict(sorted(temp.items(), key=lambda x: x[1], reverse = True))


    print("before sorting")
    print(temp)
    #print("one file done")
    print("after sorting")
    print(word_count_sorted)

    f4 = open(topic_file,'a')
    word_count_str=str(word_count_sorted)
    f4.write('\n')
    f4.write("The word frequency are here...")
    f4.write(word_count_str+'\n')
    f4.close()
