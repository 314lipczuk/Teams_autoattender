from selenium import webdriver
import json
import sys
import time
from studiobot import login
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

###########################
# This script is supposed to set up your credentials file and more importantly, your table file.
# Second one is important, because that's where bot takes info about timestamps from.
# Format of table file is [[date-tid of the team],[day,hour_of_start,minute_of_start],[day,hour_of_end,minute_of_end], ...] converted to json
###########################
table=[]
weekdays = ["Monday", "Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
f = open(".pb.txt", "w")
crds = input("Please input username for ms teams: ")
crds += ":"
crds += input("Please input password: ")
f.write(crds)
f.close()
driver = login(None)
all_cards = driver.find_elements_by_class_name("team-card")
for x in range(len(all_cards)-1):
    print("Chceking card nr: ", x+1)
    cards = driver.find_elements_by_class_name("team-card")
    card = cards[x]
    arr = [[],[],[]]
    name = card.get_attribute("data-tid")
    arr[0].append(name)
    print("Operating on: "+ name)
    card.click()
    time.sleep(10)
    print("Looking for label")
    try:
        label = driver.find_element_by_class_name("time")
    except NoSuchElementException:
        print("No label found for "+name)
        driver.back()
        time.sleep(10)
        continue 
    print("label found: "+ label.text+"\nParsing commences...")
    label = label.text.split(" ")
    if(label[1]!="every"):
        print("format not yet supported")
        driver.back()
        continue
    label=label[2:]
    #setting day 
    for x in range(7):
        if(weekdays[x]==label[0]):
            print("Found day")
            arr[1].append(x)
            arr[2].append(x)
    #setting stating time
    stime = label[1][1:].split(":")
    arr[1].append(int(stime[0]))
    arr[1].append(int(stime[1]))
    #setting ending time
    stime[0] = int(stime[0])+1
    stime[1] = int(stime[1])+30
    if int(stime[1]) >=60:
        stime[0]=int(stime[0])+1
        stime[1]=int(stime[1])-60
    arr[2].append(stime[0])
    arr[2].append(stime[1])
    table.append(arr)
    print(table)
    driver.back()
    time.sleep(10)


tablejson=json.dumps(table)
f = open("tablefile.json","w")
f.write(tablejson)
f.close()
print("All done, check if it's all there")
