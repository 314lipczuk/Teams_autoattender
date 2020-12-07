from selenium import webdriver
import time
import json
import datetime
from selenium.webdriver.common.keys import Keys
import sys





def login(clas, driver):
    driver = webdriver.Chrome()
    #window1 - Yes i want to sign in
    driver.get("https://www.microsoft.com/en-ww/microsoft-365/microsoft-teams/log-in")
    driver.find_element_by_xpath('/html/body/section/div[2]/div/section/div/div[1]/div/div/div/div/div[1]/a').click()
    time.sleep(3)

    #window1 - give email
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_xpath('/html/body/div/form[1]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/input[1]').send_keys(f"{crds[0]}")
    driver.find_element_by_xpath('/html/body/div/form[1]/div/div/div[1]/div[2]/div[2]/div/div/div/div[4]/div/div/div/div/input').click()
    time.sleep(3)

    #window2 - logging for student mail
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[2]/input').send_keys(f"{crds[1]}")
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[4]/span').click()
    time.sleep(3)

    #window3 - dont stay signed in
    driver.find_element_by_xpath('/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input').click()
    time.sleep(3)
    #window4 - yes use the fucking web app
    driver.find_element_by_xpath('/html/body/promote-desktop/div/div/div/div[1]/div[2]/div/a').click()
    time.sleep(3)

    #find a team
    pick_a_card(clas[0][0],driver)

    time.sleep(3)
    print("Searching for a join button")
    #Click on join button
    while( (time_.tm_hour>x[1][1])) and ((time_.tm_hour<=x[2][1] and time_.tm_min<x[2][2]) or time_.tm_hour<x[2][1]):
         try:
             driver.find_element_by_class_name("call-jump-in").click()
             break
         except:
             print("Join button not found")
             time.sleep(60)
    #confirm audio
    print("Found button, continuing")
    time.sleep(3)
    driver.find_element_by_class_name("join-btn").click()
    print("Joined lecture")
    time.sleep(60*90)
    driver.quit()
    driver = None
    print(f"Leaving lecture {time.localtime().tm_hour}:{time.localtime().tm_min}")
    return None


#  TODO (actual one)
#   1.Rework how time works.
#   2.Make setup script to generate 'table' file from team cards in main screen of teams
#   3.Make setup script autmatically obtain dates by parsing chat for scheduled meetings(feels like overengineering, but could be usefull as additional feature)

def pick_a_card(teamlabel,driver):
    path = driver.find_elements_by_class_name("team-card")
    print("Searching for appropriate team out of "+str(len(path)))
    for card in path:
        try:
            if card.get_attribute("data-tid") == teamlabel:
                card.click()
                print("Found card")
        except:
            continue
#read credentials
f = open(".pb.txt", "r")
crds = f.read()
f.close()
crds = crds.split(":",1)
crds[1] = crds[1][0:-1]

#read table
f = open("table", "r")
j = json.load(f)
f.close()
driver = None;
while True:
    print(f"Looking for lecture, {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
    for x in j.values():
        time_ = time.localtime()
        if x[1][0] == time_.tm_wday:
            if ((time_.tm_hour==x[1][1] and time_.tm_min>=x[1][2]) or (time_.tm_hour>x[1][1])) and ((time_.tm_hour<=x[2][1] and time_.tm_min<x[2][2]) or time_.tm_hour<x[2][1]):
                print("Activating...")
                login(x, driver)
    time.sleep(60*5)
