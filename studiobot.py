from selenium import webdriver
import time
import json
import datetime
from selenium.webdriver.common.keys import Keys
import sys
def login(clas):
    global driver  
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
    driver.find_element_by_xpath('//*[@id="toast-container"]/div/div/div[2]/div/button[2]').click()
    if __name__ == "__main__":
        #find a team
        pick_a_card(clas[0][0])

        time.sleep(3)
        print("Searching for a join button")
        #Click on join button
        cnt =0
        while cnt < 10:
            try:
                driver.find_element_by_class_name("call-jump-in").click()
                print("Button found")
                break
            except:
                print("Join button not found. Attempt: ", cnt)
                cnt +=1
                time.sleep(60)
        #confirm audio
        try:
            time.sleep(3)
            driver.find_element_by_class_name("join-btn").click()
            print("Joined lecture")
            time.sleep(60*90)
        except:
            print("Fucked up between confirming audio and joining")
        driver.quit()
        print(f"Leaving lecture {time.localtime().tm_hour}:{time.localtime().tm_min}")
        return None
    else:
        loc = driver
        return loc

#  TODO (actual one)
#   1.Rework how time works.


def pick_a_card(teamlabel):
    path = driver.find_elements_by_class_name("team-card")
    print("Searching for appropriate team out of "+str(len(path)))
    for card in path:
        try:
            if card.get_attribute("data-tid") == teamlabel:
                card.click()
                print("Found team")
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
while __name__ =="__main__":
    print(f"Looking for lecture, {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
    for x in j.values():
        time_ = time.localtime()
        if x[1][0] == time_.tm_wday:
            if ((time_.tm_hour==x[1][1] and time_.tm_min>=x[1][2]) or (time_.tm_hour>x[1][1])) and ((time_.tm_hour<=x[2][1] and time_.tm_min<x[2][2]) or time_.tm_hour<x[2][1]):
                print("Activating...")
                try:
                    login(x)
                except:
                    time.sleep(60)
    time.sleep(60*5)
