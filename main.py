# make it do a search for an item and exstract id
#make it scrape new arrivals page and print out product name and id for each size

import requests
import re
import time
import json
from bs4 import BeautifulSoup
import urllib
from threading import Thread
from Queue import Queue
import argparse
import time

s = requests.Session()
requests.packages.urllib3.disable_warnings()


whatsnew = "https://www.mrporter.com/en-gb/mens/whats-new"

hookheaders = {'Content-Type': 'application/json'}

headers1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
    }





def monitor():
    r = s.get(whatsnew,headers=headers1,verify=False)
    soup = BeautifulSoup(r.text,"lxml")

    word_list = ("Presto",)#TODO CHANGE THIS FOR PRESTOS!

    results = soup.find_all('div', {"class":"designer"})
    print "made by  - https://twitter.com/thebotsmith"
    
    time.sleep(2)
    for result in results:
        if any(word in result.a['title'].lower() for word in word_list):
            product = {}
            title = result.a['title']
            #print result.a['title']
            producturl = "https://www.mrporter.com{}".format(result.a['href'])
            Productcode = (result.a['href'][-13:-6].replace("/",""))
            # print "Product code = {}".format(Productcode)
            # print producturl
            product['url'] = producturl
            product['code'] = Productcode
            print "\n"

            stockmessage =  "{} in stock \n{}".format(title,producturl)

            slackwebhook = ""
            discordwebhook = ""

            print stockmessage

            #POST TO DISCORD
            jsondata = {"content":"presto in stock at {}".format(url)}
            r = requests.post(discordwebhook,json=jsondata,verify=False,headers=hookheaders)

            #POST TO SLACK
            messagepost = {"text":"prestos in stock at {}".format(url)}
            json_data = json.dumps(messagepost)
            req = requests.post(slackwebhook,data=json_data.encode('ascii'),headers={'Content-Type': 'application/json'},verify=False)

            #post to email

            smtp = smtplib.SMTP('smtp.gmail.com:587')
            smtp.ehlo()
            smtp.starttls()
            smtp.login("YOURGMAILRELAY","PASSWORD")
            msg = "presto in stock at {}".format(url)
            msgFrom = ("YOUR GMAIL RELAY")
            msgTo = ("SEND TO EMAIL")
            smtp.sendmail(msgFrom,msgTo,msg)

            #END LOOP, YES THIS IS A SHITTY WAY
            return True

        else:
            print "NOTHING FOUND"
            time.sleep(2)
            s.cookies.clear()
            return False

False = True
while False:
    monitor()
