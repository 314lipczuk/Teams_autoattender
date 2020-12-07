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
    sign_button = driver.find_element_by_xpath('/html/body/section/div[2]/div/section/div/div[1]/div/div/div/div/div[1]/a')
    sign_button.click()
    time.sleep(3)

    #window1 - give email
    driver.switch_to.window(driver.window_handles[1])
    input_ = driver.find_element_by_xpath('/html/body/div/form[1]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/input[1]')
    input_.send_keys(f"{crds[0]}")
    signin_next = driver.find_element_by_xpath('/html/body/div/form[1]/div/div/div[1]/div[2]/div[2]/div/div/div/div[4]/div/div/div/div/input')
    signin_next.click()
    time.sleep(3)

    #window2 - logging for student mail
    input_ = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[2]/input')
    input_.send_keys(f"{crds[1]}")
    signin_next = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[4]/span')
    signin_next.click()
    time.sleep(3)

    #window3 - dont stay signed in
    input_ = driver.find_element_by_xpath('/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input')
    input_.click()
    time.sleep(3)
    #window4 - yes use the fucking web app
    input_ = driver.find_element_by_xpath('/html/body/promote-desktop/div/div/div/div[1]/div[2]/div/a')
    input_.click()
    time.sleep(3)

    #find a team
    pick_a_card(clas[0][0],driver)

    time.sleep(3)
    time.sleep(1000)
   # print("Searching for a join button")
   # #Click on join button
   # try:
   #     input_ = driver.find_element_by_xpath('//*[@id="toast-container"]/div/div/div[2]/div/button[2]')
   #     input_.click()
   # except:
   #     print("Join button not found")
   #     return None
   # #confirm audio
   # print("Jound button, continuing")
   # time.sleep(3)
   # input_=driver.find_element_by_class_name("ts-calling-join-button")
   # input_.click()
   # time.sleep(3)
   # input_=driver.find_element_by_class_name("join-btn")
   # input_.click()
   # print("Joined lecture")
   # time.sleep(60*90)
   # driver.close()
   # print(f"Leaving lecture {time.localtime().tm_hour}:{time.localtime().tm_min}")
   # return None






#Should no longer be useful, but to be safe...
#teamsdict = {#coords/starttime/endtime
#    'AM_1w':[[2,2],[0,12,15],[0,15,30]],
#    'PPJ_1w':[[2,3],[2,15,45],[2,17,15]],
#    'PPJ_12c1':[[2,4],[3,10,15],[3,11,45]],
#    'PPJ_12c2':[[2,4],[1,10,15],[1,11,45]],
#    'TAK':[[3,3],[0,15,45],[0,17,15]],
#    'HKJ':[[3,4],[2,8,30],[2,10,0]],
#    'WDZ_1w':[[4,2],[2,14,0],[2,15,30]],
#    'WSI_12c':[[4,3],[1,14,0],[1,15,30]],
#    'AM_12c':[[4,4],[1,8,30],[1,10,0]],
#    'WDZ_12c':[[5,2],[4,15,45],[4,17,15]],
#    'test':[["team-2021W_wis_AM_1w_ang"],[0,1,50],[0,19,30]]
#}


#  TODO
#   1.Rework how time works.
#   2.Make setup script to generate 'table' file from team cards in main screen of teams
#   3.Make setup script autmatically obtain dates by parsing chat for scheduled meetings(feels like overengineering, but could be usefull as additional feature)

def pick_a_card(teamlabel,driver):
    path = driver.find_elements_by_class_name("team-card")
    print(path)
    print(len(path))
    for card in path:
        if card.get_attribute("data-tid") == teamlabel:
            card.click()





#read credentials
f = open(".pb", "r")
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
                print('Found lecture up and running')
                login(x, driver)
    time.sleep(60*5)
