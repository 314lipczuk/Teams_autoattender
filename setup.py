from selenium import webdriver
import json
import sys
import time
import sqlite3
from new_bot import join
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def creds():
    f = open(".pb.txt", "w")
    crds = input("Please input username for ms teams: ")
    crds += ":"
    crds += input("Please input password: ")
    f.write(crds)
    f.close()

def setup_database():
    conn = sqlite3.connect('table.db')
    conn.execute('''CREATE TABLE TIMETABLE
                 (label TEXT PRIMARY KEY   NOT NULL,
                  day_of_the_week INT,
                  starting_hour INT,
                  starting_minute INT,
                  lenght INT
                  );''')
    conn.close()

hlp = '''
###########################
# This script is supposed to set up your credentials file and more importantly, your table file.
# Second one is important, because that's where bot takes info about timestamps from.
# Format of table file is [[date-tid of the team],[day,hour_of_start,minute_of_start],[day,hour_of_end,minute_of_end], ...] converted to json
# Default use tries to create a table, if you use -c, it also takes your credentials 
###########################
'''
if sys.argv[1] == ("--creds" or "-c"):
    creds()
elif(sys.argv[1]==("-h" or "--help")):
    print(hlp)
    exit()
elif(sys.argv[1]==("-t" or "--table-setup")):
    setup_database()
    print("Database created")
    exit()
elif(sys.argv[1] == ("--fill-table" or "-f")):
    driver = join()
    table=[]
    weekdays = ["Monday", "Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    all_cards = driver.find_elements_by_class_name("team-card")
    for x in range(len(all_cards)):
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
            time.sleep(10)
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
        driver.back()
        time.sleep(10)

    conn = sqlite3.connect('table.db')
    for record in table:
        conn.execute(f"INSERT INTO TIMETABLE ( label , day_of_the_week, starting_hour, starting_minute, lenght) VALUES ({record[0]},{record[1][0]},{record[1][1]},{record[1][2]},90)")
    conn.commit()
    print("Records created")
    conn.close()
    #legacy solution, test if code above produces desired results and delete   
    tablejson=json.dumps(table)
    f = open("table.json","w")
    f.write(tablejson)
    f.close()
