#
# Listal Downloader
# vintol.github.io/listal
# v1.2

import urllib.request,ssl
import argparse
import time
import queue
import threading
import os,sys
import better_exceptions
#

# Very Important. 
ssl._create_default_https_context = ssl._create_unverified_context

def download():
    global broken, failed, ls
    while not qq.empty():
        mydata = threading.local()
        mydata.name, mydata.url = qq.get()
        mydata.keep_going, mydata.skip, mydata.retry = (True, False, 0)
        #if mydata.name in ls:continue
        while mydata.keep_going:
            try:mydata.html = urllib.request.urlopen(mydata.url,timeout=120)
            except urllib.error.HTTPError as HERR:
                if HERR.code == 404 or HERR.code == 500:
                    broken += 1
                    mydata.keep_going = False
                    mydata.skip = True
            except:
                mydata.retry += 1
                if mydata.retry > 5:
                    mydata.keep_going = False
                    mydata.skip = True
            break
        if mydata.skip:continue
        while True:
            try:
                mydata.image = mydata.html.read()
                open(mydata.name,'wb').write(mydata.image)
                break
            except:
                mydata.retry += 1
                if mydata.retry > 10:break

def mkqueue():
    global total,ld,ls
    fhand = open(os.path.join(ld,args.fname),'r')
    links = []
    for each in fhand:
        if each.startswith('#') or len(each) < 10:continue
        fname = each.strip().split('/')[-2].zfill(10) + "." + each.strip().split('.')[-1]
        if fname not in ls:links.append((fname,each.strip()))
    for each in sorted(set(links),reverse=True):qq.put(each)
    total = qq.qsize()
    print(str(total),"Files queued for download.")
    fhand.close()

def enqueue():
    if qq.qsize() != 0:print("\n WARNING: Queue was not empty. ")
    for name,url in failed:
        qq.put((name,url))

def init_threads():
    for i in range(args.threads if args.threads < qq.qsize() else qq.qsize()):
        t = threading.Thread(target=download)
        threads.append(t)
        t.start()

def update_progress():
    progress = 100 - int((100*qq.qsize()) / total)
    te = time.strftime("%H:%M:%S",time.gmtime(time.time()-started))
    pbar = "\r {:0>3}% [{:<50}] ({},{}) Time Elapsed : {} ".format(progress, '#'*int((progress/2)), (total-qq.qsize()), total, te)
    sys.stdout.write(pbar)
    sys.stdout.flush()

def check_progress():
    global t1,p1
    t2 = time.time()
    p2 = 100 - int((100*qq.qsize()) / total)
    if t2-t1 < 25:pass
    else:
        if p2 - p1 >0:
            t1 = t2
            p1 = p2
        else:quit()
#

parser = argparse.ArgumentParser(description='Start Tao Downloader.')
parser.add_argument('fname', type=str,
                    help='The File containing list of links.')
parser.add_argument('--dir', dest='directory', type = str, default = None, required = False,
                    help='The directory to download files in.')
parser.add_argument('--threads', dest='threads', type = int, default = 10, required = False,
                    help='No. of threads to use.')
args = parser.parse_args()

#
qq = queue.Queue()
started = time.time()
threads = []
links   = []
failed  = []
broken  = 00
internal_error = 00
ld = os.getcwd()



if args.directory is not None:
    if not os.path.exists(args.directory):os.makedirs(args.directory)
    os.chdir(args.directory)
ls = os.listdir(os.getcwd())
#files = os.listdir(os.getcwd())

mkqueue()
init_threads()
t1, p1 = 0,0
while not qq.empty():
    update_progress()
    time.sleep(5)
    #check_progress()
for t in threads:t.join()

if len(failed) > 0:
    print("\n INFO : Download failed for {} Items. Trying Again ...".format(len(failed)))
    enqueue()
    failed.clear()
    init_threads()
    print("\n INFO:",len(failed),"Downloads Failed.")

print(" \n ============================ \n    Time Taken : {} \n Files Downloaded : {} \n    Failed Downloads\
    : {} \n    Broken Links : {}  \n ===============================================================".format(\
    time.strftime("%H:%M:%S",time.gmtime(time.time()-started)), total-len(failed),len(failed),broken))

#
