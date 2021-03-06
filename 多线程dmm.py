import re
import wget
from queue import Queue
from threading import Thread
import time
import datetime
import requests
q = Queue()
q1 = Queue()
q2 = Queue()
q3 = Queue()
q4 = Queue()

# 定义爬取的页面，不带page,类似https://www.dmm.co.jp/litevideo/-/list/narrow/=/article=keyword/id=4111/n1=DgRJTglEBQ4GpoD6%%2CYyI%%2Cqs_/sort=date,如出现%记得使用%%
page_adr = 'https://www.dmm.co.jp/litevideo/-/list/=/article=maker/id=3152'
# 定义爬取的页数
page_row = 5

def xiazai(q, dirNmae):
    while not q.empty():
        url = q.get()
        print('开始下载：%s' % url)
        num = 0
        while True:
            try:
                num = num + 1
                wget.download(url, out=dirNmae)
                print('剩余队列：%s。下载成功：%s' % (str(q.qsize()), url))
                break
            except Exception as e:
                print('出错%d次' % num)
                print('报错：%s' % e)
                time.sleep(5)
                if num == 5:
                    continue

def paqu(q1, q2):
    while not q1.empty():
        print('开始获取，剩余%d页面！' % q1.qsize())
        home_url = 'https://www.dmm.co.jp/litevideo/-/detail/=/cid='
        url = home_url + q1.get()
        while True:
            try:
                r = requests.get(url, headers={'Connection': 'close'}, verify=False,cookies={'age_check_done':'1'})
                break
            except:
                print("遇到错误，暂停5秒继续")
                time.sleep(5)
                continue
        q2.put(r.text)


def shiping(q3, q4):
    while not q3.empty():
        print('开始爬取视频！剩余%d个' % q3.qsize())
        while True:
            try:
                r = requests.get(q3.get(), headers={'Connection': 'close'}, verify=False,cookies={'age_check_done':'1'})
                break
            except Exception as e:
                print(e)
                print("遇到错误，暂停5秒继续")
                time.sleep(5)
                continue
        q4.put(re.findall('freepv(.*?)mp4', r.text)[0])


# 开始处理cookies
requests.packages.urllib3.disable_warnings()
str1 = ''
str2 = ''

# r = requests.get(page_adr + '/page=%d/' % 1, headers={'Connection': 'close'}, verify=False)
# age_url = re.findall('https://www.dmm.co.jp/age_check/=/declared=yes/(.*?)" class="ageCheck__link ageCheck__link--r18">',r.text)
# if age_url :
#     check_url = "https://www.dmm.co.jp/age_check/=/declared=yes/" + age_url[0]
#     r = requests.get(check_url, verify=False)
#     cookies = r.cookies
#     print(cookies)
for n in range(1, page_row + 1):  # 爬取页面的页数
    print('开始刷新页面：%d' % n)
    # 爬取的url
    r = requests.get(page_adr + '/page=%d/' % n, headers={'Connection': 'close'}, verify=False,cookies={'age_check_done':'1'})
    print(r.text)
    str1 = str1 + r.text
    time.sleep(1)


list2 = re.findall('https://www.dmm.co.jp/litevideo/-/detail/=/cid=(.*?)">', str(str1))
print(list2)
print('总共需要爬取%d个页面' % len(list2))
for n in list2:
    q1.put(n)
tt1 = Thread(target=paqu, args=(q1, q2))
tt2 = Thread(target=paqu, args=(q1, q2))
tt3 = Thread(target=paqu, args=(q1, q2))
tt4 = Thread(target=paqu, args=(q1, q2))
tt5 = Thread(target=paqu, args=(q1, q2))
tt1.start()
tt2.start()
tt3.start()
tt4.start()
tt5.start()
tt1.join()
tt2.join()
tt3.join()
tt4.join()
tt5.join()
print(q2.qsize())
while not q2.empty():
    str2 = str2 + q2.get()
url_list = re.findall('<iframe type="text/html" src="//(.*?)"', str2)
print(url_list)
str3 = ""
print('开始爬取视频地址，总共有%d个视频！' % len(url_list))
mn = 0
mp4_list = []
for n in url_list:
    q3.put('https://' + n)
ttt1 = Thread(target=shiping, args=(q3, q4))
ttt2 = Thread(target=shiping, args=(q3, q4))
ttt3 = Thread(target=shiping, args=(q3, q4))
ttt4 = Thread(target=shiping, args=(q3, q4))
ttt5 = Thread(target=shiping, args=(q3, q4))
ttt1.start()
ttt2.start()
ttt3.start()
ttt4.start()
ttt5.start()
ttt1.join()
ttt2.join()
ttt3.join()
ttt4.join()
ttt5.join()
while not q4.empty():
    mp4_list.append(q4.get())
for n in mp4_list:
    mp4 = n.replace('\\', "")
    mp4_url = 'https://cc3001.dmm.co.jp/litevideo/freepv%smp4' % mp4
    q.put(mp4_url)
time_stamp = datetime.datetime.now()
dirName = time_stamp.strftime('%Y-%m-%d-%H%M%S')
import os

if not os.path.exists(dirName):
    os.mkdir(dirName)
t1 = Thread(target=xiazai, args=(q, dirName))
t2 = Thread(target=xiazai, args=(q, dirName))
t3 = Thread(target=xiazai, args=(q, dirName))
t4 = Thread(target=xiazai, args=(q, dirName))
t5 = Thread(target=xiazai, args=(q, dirName))
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
