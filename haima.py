import json
import threading
import time

import requests

URL = "http://www.haima668.com:8008/ActionApi/"
USERNAME = "demon3019"
PASSWORD = "123456"
TOKEN = "zPghzzU%2BTqJbhiYruSiTYry5%2B31hVU/yDr9rBgRI9H5vliniFqmmWtEGI/Gj7cdh"
PID = "521"
# PID = "11147"  # 丙晟科技
UID = "29135"
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


def hm_login(username, password):
    url = URL + "loginIn"
    data = [
        ('uid', username),
        ('pwd', password),
    ]
    response = requests.post(url, data, headers=header_dict, timeout=10).text
    print("[" + threading.current_thread().name + "] " + "登录：" + response)
    r = json.loads(response)
    global TOKEN
    TOKEN = r["Token"]
    global UID
    UID = r["Uid"]
    print(TOKEN)
    print(UID)
    return response


def hm_phone(hm_type, province, pid=PID):
    url = URL + "getMobilenum?uid=%s&pid=%s&token=%s&type=%s&province=%s&nonVirtual=true" % (
        UID, pid, TOKEN, hm_type, province)
    response = requests.post(url, headers=header_dict, timeout=10).text
    # print("获取手机号：" + response)
    if "余额不足，请充值" == response:
        raise RuntimeError("海码余额不足，请充值")
    if "No_Data" == response:
        raise RuntimeError("没有合适号码")
    return response


def hm_sms(phone, timeout, pid=PID):
    url = URL + "getVcodeAndReleaseMobile?mobile=%s&uid=%s&token=%s&author_uid=%s&pid=%s" % (
        phone, UID, TOKEN, USERNAME, pid)
    start = time.time()
    while True:
        response = requests.post(url, headers=header_dict, timeout=10).text
        print("[" + threading.current_thread().name + "] " + response)
        responses = response.split("|")
        end = time.time()
        if (end - start) > timeout:
            hm_black(phone)
            raise RuntimeError("hm_sms获取不到短信")
        if phone in responses:
            hm_black(phone)
            return responses[1]
        time.sleep(5)


def hm_black(phone, pid=PID):
    url = URL + "addIgnoreList?mobiles=%s&token=%s&uid=%s&pid=%s" % (phone, TOKEN, UID, pid)
    response = requests.post(url, headers=header_dict, timeout=10).text
    # print("海码拉黑：" + response)


if __name__ == '__main__':
    # login_result = json.loads(hm_login("wuhai", "wuhai123"))
    # print(str(login_result["Uid"]) + " " + login_result["Token"] + " " + str(login_result["Balance"]) + " " + str(
    #     login_result["UsedMax"]))
    # uid = login_result["Uid"]
    # token = login_result["Token"]
    # print(token)
    phone_result = hm_phone("", "辽宁")
    print(phone_result)
    # # get_code.get_code(phone_result)
    # sms_result = hm_sms(phone_result, 60)
    # hm_black(phone_result)
