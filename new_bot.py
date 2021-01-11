from selenium import webdriver
import time
import sqlite3

#setting up database stuff
db = sqlite3.connect('table.db')
cur = db.cursor()

#read credentials
f = open(".pb.txt", "r")
crds = f.read()
f.close()
crds = crds.split(":",1)
#crds[1] = crds[1][0:-1]

def set_timer(hr=24, min=0):
    hours = hr - time.localtime().tm_hour
    mins = min - time.localtime().tm_min
    t=((hours * 60)+mins)*60
    time.sleep(t)
    
def join(curclass = []):
    driver = webdriver.Chrome()

#    #window1 - Yes i want to sign in
    driver.get("https://www.microsoft.com/en-ww/microsoft-365/microsoft-teams/log-in")
    driver.find_element_by_xpath('/html/body/section/div[2]/div/section/div/div[1]/div/div/div/div/div[1]/a').click()
    time.sleep(3)

    #window1 - give email
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_class_name('text-box').send_keys(f"{crds[0]}")
    driver.find_element_by_class_name('ext-button').click()
    time.sleep(3)

    #window2 - logging for student mail
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[2]/input').send_keys(f"{crds[1]}")
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[4]/span').click()
    time.sleep(3)

    #window3 - dont stay signed in
    driver.find_element_by_xpath('/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input').click()
    time.sleep(10)
    #window4 - yes use the fucking web app
    #driver.find_element_by_xpath('/html/body/promote-desktop/div/div/div/div[1]/div[2]/div/a').click()
    #time.sleep(3)
    driver.find_element_by_xpath('//*[@id="toast-container"]/div/div/div[2]/div/button[2]').click()
    if __name__ == "__main__":
        #find a team
        path = driver.find_elements_by_class_name("team-card")
        print("Searching for appropriate team out of "+str(len(path)))
        for card in path:
            try:
                if card.get_attribute("data-tid") == curclass[0]:
                    card.click()
                    print("Found team")
            except:
                continue

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
            time.sleep(curclass[4]*60)
        except:
            print("Fucked up between confirming audio and joining")
        driver.quit()
        print(f"Leaving lecture {time.localtime().tm_hour}:{time.localtime().tm_min}")
    else:
        print('Using function not on main')
        return driver

    
while __name__ == "__main__":
    clock = time.localtime()
    cur.execute(f"select * from TIMETABLE where day_of_week ={clock.tm_wday};")
    res = cur.fetchall()
    if res == []:
        set_timer()
    bst = res[0]
    for class_ in res:
        if clock.tm_hour <=class_[2] <= bst[2]:
            bst = class_
    set_timer(bst[2], bst[3])
    join(bst)
