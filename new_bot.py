from selenium import webdriver
import time
import sqlite3
import sys
import shlex
import datetime
import subprocess
class Bot:
    pulse_channel = 2
    #read credentials
    f = open(".pb.txt", "r")
    crds = f.read()
    f.close()
    crds = crds.split(":",1)
    #crds[1] = crds[1][0:-1]
    head =False
    if("--headless") in sys.argv:
        head = True
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

    def setup(self):
        db = sqlite3.connect('table.db')
        cur = db.cursor()
        cur.execute(f"select * from TIMETABLE where day_of_the_week ={time.localtime().tm_wday};")
        res = cur.fetchall()
        cur.close()
        db.close()
        res = list(res)
        pres_class = None
        for clss in res:
            clss = list(clss)
            print(clss)
            if clss[3] == datetime.datetime.now().hour:
                pres_class = clss
        return pres_class

   # def loop(self): #Takes res from above and orders when to connect to which class
   #     while True:
   #         sched = self.setup()
   #         while(sched != []):
   #             self.set_timer(sched[0][3], sched[0][4])
   #             currentcls = sched.pop(0)
   #             drv = self.launchTeams()
   #             self.join(drv,currentcls)
   #         self.set_timer()

    def start(self):
        clss= self.setup()
        if clss == None:
            print('No class right now')
            quit()
        drv = self.launchTeams()
        self.join(drv, clss)


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
        print(curclass)
        for card in path:
            if card.get_attribute("data-tid") == curclass[1]:
                card.click()
                print("Found team" , curclass[1])

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
            _now = datetime.datetime.now()
            _name =curclass[1]+"_"+str(_now.day) + ":"+str(_now.month)
            _time = curclass[5]*60 - 180
            _command = f"ffmpeg -video_size 924x668 -framerate  20 -f x11grab -i :0.0+0,100 -f pulse -ac {self.pulse_channel} -i 0 -t {_time} {_name}.mkv"
            subprocess.Popen(shlex.split(_command))
            time.sleep(curclass[5]*60)
        except:
            print("Fucked up between confirming audio and joining")
        driver.quit()
        print(f"Leaving lecture {time.localtime().tm_hour}:{time.localtime().tm_min}")

if __name__ == "__main__":
    bot = Bot()
    bot.start()