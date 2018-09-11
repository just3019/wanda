import json
import random
import threading
import tkinter
from tkinter import *
from tkinter import filedialog

import requests
import time

lock = threading.Lock()
place = '丹东'

headers = {
    'Host': 'sop.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'com.dianshang.feifanbp/2.0.1 (iPhone; iOS 11.4; Scale/3.00)',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
}


def log(s):
    print(s)
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)


def write(s):
    f = open(log_path, "a")
    f.write('%s\n' % s.strip())
    f.close()


def get_random():
    ran = random.randint(100000, 999999)
    return str(ran)


def scan(code):
    params = (
        ('', ''),
        ('storeId', '2064055'),
        ('clientType', 'iOS'),
        ('uid', '154240'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10005721'),
        ('loginToken', '1cc92828bce23bb7cd71e437e9604486'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '\u5434\u4E39'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
        ('telephone', '15004154152'),
    )

    data = {
        '_uni_source': '2.2',
        'appType': 'bpMobile',
        'app_time': '13193565337393',
        'app_verification_native': get_random(),
        'certificateno': code,
        'checkDevice': '1',
        'clientAgent': 'iPhone9,2/iOS/11.4.1/1242*2208',
        'clientId': 'xapi_01',
        'clientType': 'iOS',
        'deviceId': '184d19d52857d3628276407b946e367d208c7c5d',
        'loginToken': '1cc92828bce23bb7cd71e437e9604486',
        'merchantId': '10005721',
        'serverVersion': '1',
        'sign': '8f6ae1f653ad69979470552190b6ed34',
        'storeId': '2064055',
        'telephone': '15004154152',
        'uid': '154240',
        'username': '%E5%90%B4%E4%B8%B9',
        'version': '47'
    }

    response = requests.post('https://sop.ffan.com/goods/coupon/queryUnusedCoupons', headers=headers, params=params,
                             data=data)
    print(response.text)

    params1 = (
        ('storeId', '2064055'),
        ('clientType', 'iOS'),
        ('uid', '154240'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10005721'),
        ('loginToken', '1cc92828bce23bb7cd71e437e9604486'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '\u5434\u4E39'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
        ('telephone', '15004154152'),
    )

    data1 = {
        '_uni_source': '2.2',
        'appType': 'bpMobile',
        'app_time': '13198760952423',
        'app_verification_native': get_random(),
        'certificateno': code,
        'clientAgent': 'iPhone9,2/iOS/11.4.1/1242*2208',
        'clientId': 'xapi_01',
        'clientType': 'iOS',
        'deviceId': '184d19d52857d3628276407b946e367d208c7c5d',
        'loginToken': '1cc92828bce23bb7cd71e437e9604486',
        'memberId': '15000000329526285',
        'merchantId': '10005721',
        'serverVersion': '1',
        'sign': 'faf616b5d7c41da54e3635744fd1d3ce',
        'storeId': '2064055',
        'telephone': '15004154152',
        'uid': '154240',
        'userId': '154240',
        'username': '%E5%90%B4%E4%B8%B9',
        'version': '47'
    }

    response = requests.post('https://sop.ffan.com/goods/coupon/checkCoupon', headers=headers, params=params1,
                             data=data1)
    result = response.text
    if json.loads(result)['status'] != 200:
        raise RuntimeError("已验证过")
    print(result)


def openfile():
    r = filedialog.askopenfilename(title='打开文件', filetypes=[('Python', '*.txt'), ('All Files', '*')])
    log("当前操作的文件是：" + r)
    global file_path
    file_path = r


def ui():
    root = tkinter.Tk()
    root.title(place + '核销工具')
    root.geometry('600x800')
    global btn_file
    btn_file = Button(root, text='打开需要核销的文件', command=openfile)
    btn_file.pack()
    label1 = Label(root, text='最少间隔时间：')
    global entry1
    entry1 = Entry(root, width=100)
    label2 = Label(root, text='最大间隔时间：')
    global entry2
    entry2 = Entry(root, width=100)
    label1.pack(expand=YES, fill=X)
    entry1.pack()
    label2.pack(expand=YES, fill=X)
    entry2.pack()
    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, width=400, height=30, yscrollcommand=s1.set)
    label3 = Label(root, text='日志输出')
    label3.pack()
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)
    btn = Button(root, text='开始', command=start)
    btn.pack(expand=YES, fill=X)
    root.mainloop()


def start():
    global th
    th = threading.Thread(target=deal)
    th.setDaemon(True)  # 守护线程
    th.start()


def deal():
    lock.acquire()
    file = open(file_path, 'r')
    index = 0
    t1 = time.time()
    while True:
        try:
            minTime = entry1.get()
            maxTime = entry2.get()
            if minTime == "" or maxTime == "":
                minTime = 10
                maxTime = 180
            index += 1
            mystr = file.readline()
            if not mystr:
                break
            log(str(index) + "  " + mystr)
            code = mystr[mystr.find('info=') + 5: mystr.find('info=') + 17]
            print(code)
            scan(code)
            write(mystr)
            log(str(index) + "个核销成功。")
            print(minTime)
            print(maxTime)
            sleeptime = random.randint(int(minTime), int(maxTime))
            log("本次停顿：" + str(sleeptime))
            time.sleep(sleeptime)
        except RuntimeError as e:
            log(e)
            continue
    t2 = time.time()
    log("总共使用：" + str(t2 - t1))
    file.close()
    lock.release()


if __name__ == '__main__':
    global log_path
    log_path = place + '核销.txt'
    ui()
