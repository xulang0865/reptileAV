from queue import Queue
import requests
import urllib3
import threading
import re
from queue import Queue
import csv

class ThreadNum(threading.Thread):
    def __init__(self, q,q1):
        threading.Thread.__init__(self)
        self.q = q
        self.q1 = q1
    def run(self):
        while not q.empty():
            headers = {'User-Agent': 'User-Agent:Mozilla/5.0','Connection': 'close'}
            page_adr = self.q.get()
            #page_adr = 'https://adultdouga.jp/?search=&page=1&sort=date'
            for n in range(5):
                try:
                    print('我在爬取:'+ page_adr)
                    http = urllib3.PoolManager(headers=headers,timeout = 1);
                    r = http.request('GET',page_adr+"/get")
                    page_str = r.data.decode('Shift_JIS ', "ignore")
                    break
                except Exception as e:
                    continue
            comment = re.compile(r'</td><td(.*?)</div></div>', re.DOTALL)
            class_list = comment.findall(page_str)
            for line in class_list:
                try:
                    httpAdr_tmp = re.findall('.href=\'(.*?)\'"><',line)[0]
                    httpAdr = httpAdr_tmp.replace('./','https://adultdouga.jp/')
                    r1 = http.request('GET',httpAdr+"/get")
                    class_page_str = r1.data.decode('Shift_JIS ', "ignore")
                    av_name = re.findall('<title>(.*?)\.JP</title>',class_page_str)[0]
                    av_mp4 = re.findall('<video src="(.*?)"',class_page_str)[0]
                    av_date = re.findall('\d{4}-\d{2}-\d{2}',line)[0]
                    print(av_name+ '爬取完成')
                    tmpList = [av_name,av_date,httpAdr,av_mp4]
                    self.q1.put(tmpList)
                    print(q1.qsize())
                except Exception as e:
                    continue


if __name__ == '__main__':
    q = Queue()
    q1 = Queue()
    ThreadList = []
    for n in range(1, 7):
        q.put('https://adultdouga.jp/?search=&page=%d&sort=date' % n)
    list1 = []
    for n in range(5):
        n = ThreadNum(q,q1)
        list1.append(n)
    for n in list1:
        n.start()
    for n in list1:
        n.join()
    endList = []
    print(q1.qsize())
    while not q1.empty():
        endList.append(q1.get())
    import xlrd
    import xlwt
    from xlutils.copy import copy
    index = len(endList)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('1')
    for i in range(0, index):
        for j in range(0, len(endList[i])):
            sheet.write(i, j, endList[i][j])
    workbook.save('工作簿.xls')

