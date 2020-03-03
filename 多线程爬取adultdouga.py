from queue import Queue
import requests
import urllib3
import threading
import re
from queue import Queue


class ThreadNum(threading.Thread):
    def __init__(self, q, q1):
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
            n = 0
            for line in class_list:
                try:
                    n = n + 1
                    httpAdr_tmp = re.findall('.href=\'(.*?)\'"><',line)[0]
                    httpAdr = httpAdr_tmp.replace('./','https://adultdouga.jp/')
                    r1 = http.request('GET',httpAdr+"/get")
                    class_page_str = r1.data.decode('Shift_JIS ', "ignore")
                    av_name = re.findall('<title>(.*?)\.JP</title>',class_page_str)[0]
                    av_mp4 = re.findall('<video src="(.*?)"',class_page_str)[0]
                    av_date = re.findall('\d{4}-\d{2}-\d{2}',line)[0]
                    print(av_name+ '爬取完成')
                    self.q1.put([av_name,av_date,httpAdr,av_mp4])
                except Exception as e:
                    continue


if __name__ == '__main__':
    q = Queue()
    q1 = Queue()
    for n in range(1, 7):
        q.put('https://adultdouga.jp/?search=&page=%d&sort=date' % n)
    for n in range(5):
        n = ThreadNum(q,q1)
        n.start()




#r = requests.get(page_adr, headers={'Host':'adultdouga.jp','Connection':'keep-alive','Cache-Control':'max-age=0','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36','Sec-Fetch-Dest':'document','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'navigate','Sec-Fetch-User':'?1','Referer':'https://adultdouga.jp/','Accept-Encoding':'gzip, deflate, br','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'})
#print(r.text)