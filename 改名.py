import os
import time
from moviepy.editor import VideoFileClip
import pytz
import datetime
import exifread
from win32com.propsys import propsys, pscon
import pythoncom
import shutil

m = 0
f = open('tmp.csv','w',encoding='utf8')
for root,dir,file in os.walk('download'):
    for n in file:
        m = m + 1
        path1 = os.path.abspath(os.path.join(root,n))
        properties = propsys.SHGetPropertyStoreFromParsingName(path1)
        dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
        dt = dt.replace(tzinfo=pytz.timezone('UTC'))
        name = dt.strftime('%Y-%m-%d')
        old_path = os.path.join(root,n)
        new_path1 = os.path.join(root,str(name) + n)
        list1 = [old_path,new_path1]
        f.write(','.join(list1) + '\n')
f.close()

