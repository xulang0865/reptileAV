import redis
import time
from threading import Thread
import os
import datetime

def create_unique_folder(table_name):
    folder_name = table_name
    count = 1

    while os.path.exists(folder_name):
        folder_name = f"{table_name}_{count}"
        count += 1

    os.mkdir(folder_name)
    return folder_name

time_stamp = datetime.datetime.now()
table_name = time_stamp.strftime('%Y%m%d')

folder_name = create_unique_folder(table_name)
fail_table_name = f'{table_name}_fail'
# 线程数
thread_row = 10
# 连接池
red = redis.ConnectionPool(host='192.168.2.173', port=6379, db=1)
r = redis.Redis(connection_pool=red)


def xiazai():
    while not r.llen(table_name) == 0:
        url = r.lpop(table_name).decode()
        print('开始下载：%s' % url)
        num = 0
        while True:
            try:
                import requests.packages.urllib3.util.ssl_
                requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
                num = num + 1
                # wget.download(url, out=table_name)
                requests.packages.urllib3.disable_warnings()
                file = requests.get(url)
                file_name = url.split('/')[-1]
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, "wb") as f:
                    f.write(file.content)
                print('剩余队列：%s。下载成功：%s' % (str(r.llen(table_name)), url))
                break
            except BaseException as e:
                print('出错%d次' % num)
                print('报错：%s' % e)
                time.sleep(5)
                if num > 5:
                    print(url)
                    r.lpush(fail_table_name, url.encode())
                    break



def download_from_redis():
    # 处理失败任务
    if r.llen(fail_table_name) != 0:
        for n in range(0, r.llen(fail_table_name)):
            value = r.lindex(fail_table_name, n)
            r.lpush(table_name, value)


    # 开始下载任务
    thread_list = []
    for n in range(0, thread_row):
        thread = Thread(target=xiazai, args=())
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    download_from_redis()
