f = open('tmp.csv','r',encoding='utf8')
list1 = ['1']
import os
while 1:
    n = f.readline()
    if not n:
        break
    list1 = n.split(',')
    oldPath = list1[0]
    newPath = list1[1].replace('\n','')
    os.rename(oldPath,newPath)
