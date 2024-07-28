import json

# -*- coding: UTF-8 -*-
import requests
import time
import pandas as pd
import math
import random
import sys
# 目标url
url = "https://mp.weixin.qq.com/s/Z8BVt7g6rnuAFzoca1fjfg"

def crawl_weixin(url):
    cookie = "_qimei_uuid42=1851a111d071005223d117c4d9e14602fe3c762a52; pac_uid=0_2de2cpCcXnR2J; _qimei_fingerprint=aca24296db4313ba3723fdbbae91fe2c; _qimei_q36=; _qimei_h38=527fca4923d117c4d9e146020200000531851a; RK=jX9BHUFma4; ptcz=8ead7fccb59a8f66442472f6f6d5c92c05855c9079cee2ef4ce476fc62b0d6ed; rewardsn=; wxtokenkey=777; sig_login=h015cc298e83ed0e48ea199dca262258c3d6744123d8cfcd6e0249f39e0249761bd97f6606be68e99dc; _qpsvr_localtk=0.9781630297118207; ua_id=X4rg4KwrfgT7DNrQAAAAAHG1RXyxDtr-rCvYRPSEs3I=; wxuin=20533028037072; uuid=dd1c8cc078648f33b47e5f737da06a69; _clck=1puu7pv|1|fnb|0; cert=ZG_2HRG1gLDuy91x9nRa8kKuoOzmyPoC; sig=h011ffbc362e91373f1d1b4c303c50d26d6c9381c5209e931ba923610f821612df99d4dd4a1ed6fb170; data_bizuin=3909727515; bizuin=3909727515; master_user=gh_f95ed8367143; master_sid=dEJzbGszdThveEN4bnF1Y0VNRnJkVldYQmpzNXFzbjJZYXdTcldsdFZqUXVLMWlnVVNLNXQ0bzRUaWI4d19EX1d1NzVQeGg3MGFEcng0SE93bE9mMzhFQUJuYVZQTkI4WU1QWjdGRGh2eVRyaE1BaW43RWZpRHhIU2xxNm9tWW40akplb2RicHR0c0xMdmdl; master_ticket=b6d8c7047d94826a0d6453e9cabab8e2; media_ticket=aa79342e325bd9710a2e65c3efc4d8b30c161b6b; media_ticket_id=3909727515; data_ticket=QP/SVFhcXXnr2bAYCrdiytMQl2dQrJMTiprO9YAKKvPH2TJb8al0Zj/K9KIgxudq; rand_info=CAESIIpjzg9evSUBO6WgmyIpCqL7KRDk7nyUxyQw3JXm1TWp; slave_bizuin=3909727515; slave_user=gh_f95ed8367143; slave_sid=ZEJHVFVBWDd1aVczOTZualUwNmxmb0E0SEN5U1BQZFlLc3hMMko5dGZpQzhhRHRia1ZJTXVLTlNGX1lHRTBITXVUUlV6UHJNYnBfS1hkT0JQSmJUcTU0NnNSOTNEUnNtYTNSb0hHVU1qZUplUVB6Tk5BcjRMaktvSzdZSTVHSGl4TVBKZUthSHc3aHF3bjNi; _clsk=y65czl|1720534266852|2|1|mp.weixin.qq.com/weheat-agent/payload/record; RT=\"z=1&dm=qq.com&si=59ce57bf-2110-4576-853f-a97ef219b2e2&ss=lyeg6dvr&sl=d&tt=gwx&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1kscc&nu=kpaxjfo&cl=1oi9v\""

    # 使用Cookie，跳过登陆操作

    data = {
        "token": "1615027412",
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": "0",
        "count": "5",
        "query": "",
        "fakeid": "MzIwNDY1NTU5Mg==",
        "type": "9",
    }
    headers = {
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",

        }
    content = requests.get(url, headers=headers, params=data).text
    txt = content
    print(txt)
    open("../LeetCode/weixin_html.json", "w", encoding='utf-8').write(content)


filter_tags = ['style', 'script', '']

def gen_item_map(item_list):
    retval_content = ""
    for item in item_list:
        html_tag = item[0]
        # print(html_tag)
        content = item[1]
        tag = html_tag.split(' ')[0][1:]
        if tag not in filter_tags and content != "":
            # print(tag, "|||", html_tag, ">>>> ", content)
            retval_content = retval_content + content + "\n"
    return retval_content

def html_content_strip(html_str):
    html_str = html_str.replace("\n", "")
    item_map = []
    pre_str = ""
    while html_str != "":
        pre_index = html_str.find("<")
        post_index = html_str.find(">")
        if pre_index != 0:
            plain_text = html_str[:pre_index]
            plain_text = plain_text.replace("&nbsp;", "")
            # print("------", pre_str + ">>>>>>>" + plain_text)
            item_map.append([pre_str, plain_text])
        item_str = html_str[pre_index:post_index + 1]
        pre_str = item_str
        html_str = html_str[post_index + 1:]
    raw_content = gen_item_map(item_map)
    return raw_content

def extract_weixin_content(content):
    content_obj = json.loads(content)
    print(len(content_obj))
    title = content_obj["title"]
    desc = content_obj["desc"]
    html_content = content_obj["content_noencode"]
    print(html_content_strip(html_content))


if __name__ == '__main__':
    for line in open("../LeetCode/weixin_html.json", 'r', encoding='utf-8').readlines():
        # print("||" ,line, "||")
        extract_weixin_content(line.strip())