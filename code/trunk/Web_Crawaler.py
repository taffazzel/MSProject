import requests
from bs4 import BeautifulSoup
import re
import sys
import pprint
import numpy
reload(sys)
sys.setdefaultencoding('utf-8')
counter_conference = 0
counter_author = 0

for num in range(0, 95):

    url = "http://dblp.uni-trier.de/db/conf/?pos=" + str(num * 100 + 1)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")


    list = soup.select(".hide-body > ul > li > a")
    length_org=len(list)
    print(length_org)
    for l_org in range(0,length_org):
        for l in list:
            url2 = l['href']
            response2 = requests.get(url2)
            soup2 = BeautifulSoup(response2.text, "html.parser")
            length_conf=soup2.select(".data")
            print("Number of Conferences")
            number_of_conferences = len(length_conf)
            print(number_of_conferences)

            for d in soup2.select(".data"):
                       title = d.select(".title")[0].get_text()
                       url3 = d.select("a")[0]['href']
                       counter_conference = counter_conference + 1
                       filename=str(counter_conference)
                       l = len(filename);
                       if(l == 1):
                            filename = "000000" + filename;
                       elif(l == 2):
                            filename = "00000" + filename;
                       elif(l == 3):
                            filename = "0000" + filename;
                       elif(l == 4):
                            filename = "000" + filename;
                       elif(l == 4):
                            filename = "00" + filename;
                       elif(l == 5):
                            filename = "0" + filename;

                       with open('C:\\Users\\tafaz\\Desktop\\data7\\' + filename + '.txt', 'a') as file:
                            response3 = requests.get(url3);
                            soup3 = BeautifulSoup(response3.text, "html.parser");
                            file.write(title+"\n");
                            for d in soup3.select(".entry > .data"):
                                  for i in d.find_all("span", {"itemprop" : "author"}):
                                       counter_author = counter_author + 1;
                                       file.write(i.get_text() + "\n")

                       print("Conference count: " + str(counter_conference) + " || Total Author count: " + str(counter_author));


