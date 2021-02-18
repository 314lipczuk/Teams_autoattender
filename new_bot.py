from selenium import webdriver
import time
import sqlite3
import sys
class Bot:
    #read credentials
    f = open(".pb.txt", "r")
    crds = f.read()
    f.close()
    crds = crds.split(":",1)
    #crds[1] = crds[1][0:-1]
    head = True
    if("--verbose") in sys.argv:
        head = False
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()

    options.headless = head
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    @staticmethod
    def set_timer(hr=24, min=0):
        hours = hr - time.localtime().tm_hour
        mins = min - time.localtime().tm_min
        t=((hours * 60)+mins)*60
        print('sleeping for ', t ,'seconds')
        time.sleep(t+30)
        return 0

    def setup(self):
        db = sqlite3.connect('table.db')
        cur = db.cursor()
        cur.execute(f"select * from TIMETABLE where day_of_the_week ={time.localtime().tm_wday};")
        res = cur.fetchall()
        cur.close()
        db.close()
        res = list(res)
        for cls in res:
            cls = list(cls)
            cls[0] = cls[3]*60 + cls[4]
        res.sort(key=lambda x: x[0])
        return res

    def loop(self): #Takes res from above and orders when to connect to which class
        while True:
            sched = self.setup()
            while(sched != []):
                self.set_timer(sched[0][3], sched[0][4])
                currentcls = sched.pop(0)
                drv = self.launchTeams()
                self.join(drv,currentcls)
            self.set_timer()

    def launchTeams(self):
        driver = webdriver.Chrome(options=self.options)

        #window1 - Yes i want to sign in
        driver.get("https://www.microsoft.com/en-ww/microsoft-365/microsoft-teams/log-in")
        driver.find_element_by_xpath('/html/body/section/div[2]/div/section/div/div[1]/div/div/div/div/div[1]/a').click()
        time.sleep(3)

        #window1 - give email
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_class_name('text-box').send_keys(f"{self.crds[0]}")
        driver.find_element_by_class_name('ext-button').click()
        time.sleep(3)

        #window2 - logging for student mail
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[2]/input').send_keys(f"{self.crds[1]}")
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[4]/span').click()
        time.sleep(3)

        #window3 - dont stay signed in
        driver.find_element_by_xpath('/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input').click()
        time.sleep(10)
        #window4 - confirm using webapp, if looking for self element gives u error, comment those 2/3 lines
        #driver.find_element_by_xpath('/html/body/promote-desktop/div/div/div/div[1]/div[2]/div/a').click()
        #time.sleep(3)
        #driver.find_element_by_xpath('//*[@id="toast-container"]/div/div/div[2]/div/button[2]').click()
        return driver

    def join(self, driver, curclass):
        path = driver.find_elements_by_class_name("team-card")
        print("Searching for appropriate team out of "+str(len(path)))
        for card in path:
            try:
                if card.get_attribute("data-tid") == curclass[1]:
                    card.click()
                    print("Found team" , curclass[1])
            except:
                continue

        #find a team
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
            time.sleep(curclass[5]*60)
        except:
            print("Fucked up between confirming audio and joining")
        driver.quit()
        print(f"Leaving lecture {time.localtime().tm_hour}:{time.localtime().tm_min}")

if __name__ == "__main__":
    bot = Bot()
    bot.loop()