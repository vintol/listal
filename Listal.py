#   Listal.py
#   08/11/2016 - 31/03/2019
#   v 1.2.2

import urllib.request, urllib.parse
import http.cookiejar, ssl
import bs4
import queue
import threading
import re
import os
import sys
import argparse
import time

# Scrapers

def get_ipages():
    global IMG, STOP_AT
    while not qq.empty():
        local = threading.local()
        local.url = qq.get()
        local.keep_going = True
        local.skip = False
        if STOP_AT is not None and int(local.url.split('//')[2]) > STOP_AT:continue
        while local.keep_going:
            try:local.html = urllib.request.urlopen(local.url,timeout=10)
            except urllib.error.HTTPError as HERR:
                if HERR.code == 404:
                    local.keep_going = False
                    local.skip = True
                    continue
            except:continue
            if local.html.getcode() == 200:local.keep_going = False
        if local.skip:continue
        local.data = local.html.read()
        local.soup = bs4.BeautifulSoup(local.data,'lxml')
        for each in local.soup.find_all('div','imagewrap-inner'):
            local.img = int(each.a.get('href').strip().split('/')[-1])
            if IMG is None:ipages.append(local.img)
            elif local.img > IMG:ipages.append(local.img)
            elif local.img == IMG:STOP_AT = int(local.url.split('//')[2])
            else:pass

def get_images():
    while not qq.empty():
        local = threading.local()
        local.url = qq.get()
        local.keep_going = True
        local.skip = True
        local.retry = 0
        while local.keep_going and local.retry < 5:
            try:
                local.retry += 1
                local.html = urllib.request.urlopen(local.url,timeout=25)
                if local.html.getcode() == 200:
                    local.keep_going = False
                    local.skip = False
            except urllib.error.HTTPError as HERR:
                if HERR is not None and HERR.code == 404:
                    local.keep_going = False
                    continue
            except:continue
        if local.skip:continue
        for i in range(2):
            try:
                local.data = local.html.read()
                images.append(find_image(local.data))
            except:continue
            break

# Functions

def mksoup(url):
    tmp = urllib.request.urlopen(url)
    return bs4.BeautifulSoup(tmp.read(),"lxml")

def find_image(data):
    return bs4.BeautifulSoup(data,"lxml").find('img','pure-img').get('src').replace("https:","http:")

def post_req():
    tmp = urllib.parse.urlencode({ 'listid' : list_id , 'offset' : offset})
    return urllib.request.urlopen("https://www.listal.com/item-list/",tmp.encode())

def mkqueue(url):
    global no_pics,no_pages
    no_pics  = int(mksoup(url).find('a','picturesbutton').span.text.strip())
    no_pages = no_pics/50
    if no_pages.is_integer():no_pages = int(no_pages)
    else:no_pages = int(no_pages) + 1
    for i in range(int(args.first_page),no_pages+1):qq.put(url+"/pictures//"+str(i))

def enqueue():
    global qq,ipages
    if not qq.empty():print("WARNING : Queue was not empty.")
    qq = queue.Queue()
    ipages = sorted(set(ipages))
    for each in ipages:
        qq.put("http://www.listal.com/viewimage/"+str(each)+"h")

def stop_at(IMG):
    tmp = []
    for each in ipages:
        if each > IMG:tmp.append(each)
    ipages = tmp

def update_progress():
    progress = 100 - int((100*qq.qsize()) / len(ipages))
    pbar = "\r {:0>3}% [{:<50}] ({},{}) ".format(progress, '#'*int((progress/2)), (len(ipages)-qq.qsize()), len(ipages))
    sys.stdout.write(pbar)
    sys.stdout.flush()

def get_listinfo(url):
    global list_type,list_id,list_name,total_pic,offset
    soup = mksoup(url)
    list_type = soup.find(id='customlistitems').get('data-listformat')
    if list_type != "images":
        print("This is not a Image list. Currently listal.dl suppots only Image lists.")
        quit()
    list_id   = int(soup.find(id='customlistitems').get('data-listid'))
    try:list_name = soup.find('div','headertitle').text.strip()
    except AttributeError:list_name = urls.path[6:].replace('-',' ').title()
    total_pic = int(soup.find(id='customlistitems').div.get('data-itemtotal'))
    offset    = int(soup.find('div','loadmoreitems').get('data-offset'))
    for each in soup.find_all('div','imagelistbox'):
        ipages.append(int(each.a.get('href').strip().split('/')[-1]))

def get_list():
    global offset
    while True:
        data = post_req().read()
        for each in sorted(set(re.findall("viewimage\\\/([0-9]{4,10})'" ,data.decode()))):
            ipages.append(int(each))
            offset = offset + 1
        if offset == total_pic:break

def write():
    if urls.path.startswith("/list/"):fhand = open(list_name+".txt",'a')
    else:fhand = open(name+".txt",'a')
    fhand.write("### {} : {} Images\n".format(finished,len(images)))
    for each in images:fhand.write(each+"\n")
    fhand.close()

# Global

qq = queue.Queue()
threads = []
ipages  = []
images  = []
IMG     = None
STOP_AT = None
started = time.time()

# Main

parser = argparse.ArgumentParser(description='Scrape Images from \'listal.com\'.')
parser.add_argument('url', type=str,
                    help='URL to the List or Profile on listal.com.')
parser.add_argument('--from', dest='first_page', type = int, default = None, required = False,
                    help='The profile page no to start scraping images from')
parser.add_argument('--upto', dest='last_page' , type = int, default = None, required = False,
                    help='Scrap images only upto the page no.')
parser.add_argument('--threads', dest='threads', type = int, default = 10, required = False,
                    help='No. of threads to use.')
args = parser.parse_args()

urls = urllib.parse.urlparse(args.url)
if urls.netloc != 'www.listal.com':
    print ("Check the Entered URL.")
    quit()

#CookieJar Initiation
urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())

if urls.path.startswith("/list/"):
    if args.first_page is not None:print("Entered URL is of a list. The '--from' option is ignored.")
    if args.last_page  is not None:print("Entered URL is of a list. The '--upto' option is ignored.")
    get_listinfo(urls.geturl())
    get_list()
else:
    urls = urllib.parse.urlparse(urls.geturl().split('/picture')[0])
    name = urls.path[1:].replace('-',' ').title()
    if args.first_page is None:args.first_page = 1
    if args.last_page is not None:
        for i in range(args.first_page,args.last_page+1):qq.put(args.url+"/pictures//"+str(i))
    else:mkqueue(urls.geturl())
    for n in range(args.threads):
        t = threading.Thread(target=get_ipages)
        threads.append(t)
        t.start()
    for t in threads:t.join()

print("Phase I Complete.",len(ipages),"Images Found.")
print("Time Taken :",time.strftime("%H:%M:%S",time.gmtime(time.time()-started)))
print("Phase II :")
enqueue()
threads.clear()
for n in range(args.threads):
    t = threading.Thread(target=get_images)
    threads.append(t)
    t.start()

while not qq.empty():
    update_progress()
    sys.stdout.flush()
    time.sleep(1)

for t in threads:t.join()

time_taken = time.time() - started
finished   = time.strftime("%d/%m/%Y %H:%M",time.localtime())
write()
print("Time Taken :",time.strftime("%H:%M:%S",time.gmtime(time_taken)))

# END
