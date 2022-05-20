from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import notify2
import time
from datetime import datetime



#the begining program notification
notify2.init("starting jobs.py")
n = notify2.Notification("starting jobs.py")
n.show()

#the keywords i'm wanting to search for (you can make them as input)
keywords = ['cyber' , 'Cyber']
#-------------------------------------

#the waiting time until the next search (you can make it as input)
waiting = 600
#-------------------------------------

links = list()
names = list()
places = list()
times = list()


#to make it run in headless mode
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# the link
url = 'https://www.ouedkniss.com/emploi_offres/1?regionIds=alger-16&sexe=sexe-1'


while True :

    #duration checking
    now = datetime.now() # the current time
    now = str(now)

    # open the file and read the last date that been checked
    f = open("date.txt", "r")
    then = f.readline()
    then = str(then)
    f.close()

    # find the time difference between now and the date on the file    
    day_now = re.findall ('.*-.*-([0-9][0-9]?) .*', now)
    day_then = re.findall ('.*-.*-([0-9][0-9]?) .*' , then)
    day_now = int (day_now[0])
    day_then = int (day_then[0])
    day_difference = day_now - day_then

    hour_now = re.findall ('.*-.*-.* ([0-9][0-9]?):.*:.*', now)
    hour_then = re.findall ('.*-.*-.* ([0-9][0-9]?):.*:.*' , then)
    hour_now = int (hour_now[0])
    hour_then = int (hour_then[0])
    hour_difference = hour_now - hour_then

    minute_now = re.findall ('.*-.*-.*:([0-9][0-9]):.*', now)
    minute_then = re.findall ('.*-.*-.*:([0-9][0-9]):.*' , then)
    minute_now = int (minute_now[0])
    minute_then = int (minute_then[0])
    minute_difference = minute_now - minute_then

    difference = 1440 * day_difference + 60 * hour_difference + minute_difference # the final difference
    print (str(difference) + '\n')

    #open the url
    driver = webdriver.Chrome(options=options)
    driver.get (url)

    #get the source page
    soup = driver.page_source

    driver.quit()

    #finding the jobs
    page = BeautifulSoup (soup , "lxml")
    jobs_tmp = page.find_all ('div' , class_ = 'row row--dense')
    jobs = list ()

    for job in jobs_tmp :
        tmp = job.find_all ('div' , class_ = 'col-sm-6 col-md-4 col-12')
        for tm in tmp :
            jobs.append (tm)

    for job in jobs :
        tmp = job.find_all ('a')
        tmp = tmp[0]
        link = tmp['href']
        tmp = tmp.find_all ('div' , class_ = 'px-2 pt-1 pb-2')
        tmp = tmp[0]
        name = tmp.find_all ('h2')
        name = name[0].text
        info = tmp.find_all ('div', class_ = "mt-2 d-flex flex-column flex-gap-1 line-height-1")
        info = info[0].find_all ('span')
        place = info[0].text
        duration = info[1].text
        
        link = link.strip()
        link = "https://www.ouedkniss.com" + link
        name = name.strip()
        place = place.strip()
        duration = duration.strip()
    #--------------------------------------------------------------
        
        
        #the date type in the job duration (minutes, hours ,days)
        confirm = re.findall ('.*y a.*[0-9] (.*)' , duration)
        if len(confirm) == 0 :
            continue
        confirm = confirm[0]
        confirm = confirm.strip()


        #checking if the job is ثxpired
        if difference > 1439 :
            if confirm == 'jour' or confirm == 'jours' :
                check = re.findall ('.*y a ([0-9]?).*', duration)
                check = int (check[0])
                the_difference = int (difference / 1440)
                if check > the_difference :
                    break
        elif difference > 59:
            if confirm == 'heure' or confirm == 'heures':
                check =re.findall ('.*y a environ (.*) heur.*', duration)
                check = int (check[0])
                the_difference = int (difference / 60)
                if check > the_difference :
                    break
        elif difference > 0:
            if confirm == 'minute' or confirm == 'minutes' :
                check =re.findall ('.*y a (.*) minute.*', duration)
                check = int (check[0])
                if check > difference :
                    break


        # notify me if the job title contain the keywords i'm seaching for
        for key in keywords :
            check_job = name.find (key)
            
            if check_job != -1 :
                notify2.init(name)
                n = notify2.Notification(name, link + '\n' + place)
                n.show()
                break
    

    # write the current time in the text file
    f = open("date.txt", "w")
    f.write(now)
    f.close()

    # wait
    time.sleep (waiting)
        

