from selenium import webdriver
import json
import sys
import time
from studiobot import login

###########################
# This script is supposed to set up your credentials file and more importantly, your table file.
# Second one is important, because that's where bot takes info about timestamps from
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
cards = driver.find_elements_by_class_name("team-card")
for card in cards:
    arr = [[],[],[]]
    name = card.get_attribute("data-tid")
    arr[0].append(name)
    print("Operating on: "+ name)
    card.click()
    time.sleep(10)
    print("Looking for label")
    label = driver.find_element_by_class_name("time")
    print("label found: "+ label.text+"\nParsing commences...")
    label = label.text.split(" ")[2:]
    #setting day 
    for x in range(7):
        if(weekdays[x]==label[0]):
            print("Found day")
            arr[1].append(x)
            arr[2].append(x)
    #setting stating time
    stime = label[1][1:].split(":")
    print(stime)
    arr[1].append(stime[0])
    arr[1].append(stime[1])
    #setting ending time
    stime[0] = int(stime[0])+1
    stime[1] = int(stime[1])+30
    if int(stime[1]) >=60:
        stime[0]=int(stime[0])+1
        stime[1]=int(stime[1])-60

    arr[2].append(stime[0])
    arr[2].append(stime[1])


    print(arr)
    time.sleep(60*10)
    
    


