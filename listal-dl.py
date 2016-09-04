#
# Listal-dl
#
# v0.21     28/08/2016
#
# Available under GNU GPL v3
#
#    listal-dl  Copyright (C) 2016  Tejas Kumar
#
#    This program comes with ABSOLUTELY NO WARRANTY.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; see file "LICENSE".
#
import urllib.request
from bs4 import *
import queue
import threading
import os
import time

##

class Imager (threading.Thread):
    def __init__(self, threadID, queue, lock, function, store):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = threadID
        self.queue = queue
        self.lock = lock
        self.execution_function = function
        self.output_store = store
    
    def run(self):
        while not self.queue.empty():
            self.lock.acquire()
            self.item = self.queue.get()
            print(self.name,"got item",self.item)
            self.lock.release()
            self.execution_function(self)
            if self.output_store is not None:
                self.lock.acquire()
                self.output_store.append(self.output)
                self.lock.release()
            self.queue.task_done()

#

def ipages(self):
    try:
        self.html = urllib.request.urlopen(self.item,timeout=2)
    except:
        while True:
            try:
                self.html = urllib.request.urlopen(self.item,timeout=5)
                if self.html.getcode() == 200:break
            except:continue
    try:self.html_data = self.html.read()
    except:
        self.lock.acquire()
        self.queue.put(self.item)
        self.lock.release()
        self.output = "\n"
        return
    self.soup = BeautifulSoup(self.html_data,"lxml")
    self.output = []
    for link in self.soup.find_all('a'):
        if link.get('href').startswith("http://www.listal.com/viewimage"):
            self.output.append(link.get('href')+"h")
#

def limages(self):
    try:
        self.html = urllib.request.urlopen(self.item,timeout=2)
    except:
        while True:
            try:
                self.html = urllib.request.urlopen(self.item,timeout=5)
                if self.html.getcode() == 200:break
            except:continue
    try:self.html_data = self.html.read()
    except:
        self.lock.acquire()
        self.queue.put(self.item)
        self.lock.release()
        self.output = "\n"
        return
    self.soup = BeautifulSoup(self.html_data,"lxml")
    self.output = self.soup.find(title=name).get('src')

#

def idownload(self):
    self.iname = self.item.split()[0]
    self.link = self.item.split()[1]
    try:
        self.html = urllib.request.urlopen(self.link,timeout=10)
    except:
        while True:
            try:
                self.html = urllib.request.urlopen(self.link,timeout=100)
                if self.html.getcode() == 200:break
            except:continue
    try:self.html_data = self.html.read()
    except:
        self.lock.acquire()
        self.queue.put(self.item)
        self.lock.release()
        return
    while True:
        try:
            open(self.iname,'wb').write(self.html_data)
        except:continue
        break

#

def pages():
    
    url_name = name.strip().lower().replace(' ','-')
    page_start = int(input("Start at Page No. : "))
    page_end = int(input("End at Page No. : ")) + 1
    no_threads = int(input("No. of Threads:"))
    
    for i in range(page_start,page_end):
        qq.put("http://www.listal.com/"+url_name+"/pictures//"+str(i))
     
    for n in range(no_threads):
        t = Imager("thread-{}".format(n),qq,thlock,ipages,output)
        threads.append(t)
        t.start()
    
    qq.join()
    
    for t in threads:
        t.join()
    
    for bulk in output:
        for link in bulk:
            links.append(link)

# Now Image Pages to Image Links
    
    for each in links:qq.put(each)
    output.clear()
    
    for n in range(no_threads):
        t = Imager("thread-{}".format(n),qq,thlock,limages,output)
        threads.append(t)
        t.start()
    
    qq.join()
    
    for t in threads:
        t.join()
    
    fhand = open("Images",'a')
    for link in output:
        fhand.write(link+"\n")

#

def images_download():
    
    links = open("Images",'r').read().split()
    if len(links) <= 8000:
        for i in range(len(links)):
            qq.put("{} {}".format("D"+str(1001+i)+".jpg",links[i]))
    elif len(links) > 8000:
        for i in range(8000):
            qq.put("{} {}".format("D"+str(1001+i)+".jpg",links[i]))
        for i in range(len(links)-8000):
            qq.put("{} {}".format("E"+str(1001+i)+".jpg",links[8000+i]))
    
    for n in range(int(input("No. of Threads:"))):
        t = Imager("thread-{}".format(n),qq,thlock,idownload,None)
        threads.append(t)
        t.start()
    
    qq.join()
    
    for t in threads:
        t.join()

##

print ("""    listal-dl  Copyright (C) 2016  Tejas Kumar

    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; see file "LICENSE". \n """)

name = input("Name :")
qq = queue.Queue()
thlock = threading.Lock()
threads=[]
output=[]
links=[]

dir_name=name.split()[0]+name.split()[1][0]
dirs = os.listdir(os.getcwd())
if dir_name in dirs:
    print(dir_name,"already exists !")
    os.chdir(dir_name)
    print("Moving to directory :",os.getcwd())
else:
    os.mkdir(dir_name)
    os.chdir(dir_name)
    print("Moving to directory :",os.getcwd())


choise = input (" 0] Get Image Links \n 1] Download Images \n ===> ")
time_started = time.time()
if choise == "0":pages()
elif choise == "1":images_download()
else: print("Try Again.")

time_taken = time.time() - time_started
print("Time Taken = {}:{}:{}".format(str(int(time_taken/3600)).zfill(2),str(int((time_taken%3600)/60)).zfill(2),str(int((time_taken%3600)%60)).zfill(2)))

##