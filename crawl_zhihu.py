# import requests
# import pandas as pd
#
# url = 'https://zhuanlan.zhihu.com/p/670958880?utm_campaign=shareopn&utm_medium=social&utm_psn=1789628512149331969&utm_source=wechat_session&utm_id=0'
# url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true'
# # 构造请求头
# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Host': 'www.zhihu.com',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
#     'Referer': 'https://www.zhihu.com/hot',
#     'Connection': 'keep-alive',
#     'Cookie': '_xsrf=DKUToyUGBBtLYqZjP9sh1f12dn2obzjO; _zap=dad2c387-0db9-475d-819c-454316e1ccc4; d_c0=ANDeW9AlrRiPTh_Pislk-ZqJ8SgXtZowSNE=|1716716606; q_c1=90635e52979c43a99803f687b4d07bb2|1716718720000|1716718720000; tst=r; __zse_ck=001_/4ysJIiy7pwD9bXaPjzd0PWk9mzWhQo0i0C235GVGpYtdk+d/yzAYPSZ5yRO=2L18iTtF=Ubq3tA1p1XbjfiK2wySXtf/mbuqc4hkp8vOFUL8bwgG=LPRTZGUk/DKUim; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1719668076,1720186855,1720445831,1720531543; HMACCOUNT=558E7640EF772C11; z_c0=2|1:0|10:1720531549|4:z_c0|80:MS4xR3ZnOUFBQUFBQUFtQUFBQVlBSlZUV3hiYldkeDV3UW1FVkh5eGZuamppWmNxRTYyZVJyZE9RPT0=|112dd22024bb8d595e6eec107783e14a7c08453ad4aec478beaa716b134fddd0; SESSIONID=U00oJlUUH5eqkf9ZymvTcWeimBIxu9upiu1sbCM5hHH; JOID=Wl4VAUO_d19WCLLMWbWpCGXTnW9J5EFtM0LQnw73TDwladT7BddJ2joGushRYmOmvl9PsXOPPUbDlXmtoWqXExM=; osd=W1wXBku-dV1RALPOW7KhCWfRmmdI5kNqO0PSnQn_TT4nbtz6B9VO0jsEuM9ZY2GkuVdOs3GINUfBl36loGiVFBs=; BEC=4589376d83fd47c9203681b16177ae43; RT="z=1&dm=zhihu.com&si=4c0a7e9b-cc35-4c44-a42b-37306f111880&ss=lyeg2274&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2q5&ul=2po6q&hd=2poab"; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1720536100',
#     'x-ab-pb': 'CgQnB/gMEgIAAA==',
#     'x-requested-with': 'fetch',
#     'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZn490EXtucRFqwHNMUrL8YunpELY0w6SmDggMgBgPD4S1hCS974e1DrNPAQLYlUefii_qr6kxELt0M4PGDwN8gGcYAupMWufIoLVqr4gxrRPOI0cY7HL8qun9g93mFukyigcmebS_FwOYPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTF8Lme9gKSq3_BBOG1UVmggHYFJefYqeYfhO_rTgBSMSMpGYLwqcGYDVfXUSTVHefr_xmBq399qX0jCgKNcr_cCSmi9xYvhoLeXx18qCYEw3Of0NLwuc8TUOpS8tMdCcGuCo8kCp_pbLf6hgO_JVKXwFY2JOLG7VCSXxYqrSBICL_5GxmOg_z6XVxqBLfMvxqYDuf3DOf6GLGhDHCbRxO0qLpTDXfbvxCSAH0BhCmJ4NmRBY8rJwB6MS124SqKuo_ywS8ACtBfqwC8XC9QA3KxCepuuCYXhLyWgNCuwYs',
#     'x-zse-93': '101_3_3.0',
#     'x-api-version': '3.0.76',
#     'x-zse-96': '2.0_CkAT7RdDtmW9PikRDfWa4CZIMx50XeUMQ7r34wP2JRAtFiCKXsSmoxCzrKWi2nJ1'
# }
#
# # 发送请求
# r = requests.get(url, headers=headers)
# print(r.content)
# # 用json接收请求数据
# json_data = r.json()
# print(json_data)


# import requests
# from bs4 import BeautifulSoup
#
# def get_html(url):
#     headers = {
#         'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.text
#     else:
#         return None
#
# def parse_html(html):
#     soup = BeautifulSoup(html, 'lxml')
#     print(soup)
#     items = soup.find_all('div', class_='Listitem')
#     for item in items:
#         print(item)
#         title = item.find('h2').get_text()
#         link = item.find('a')['href']
#         content = item.find('div', class_='RichContentinner').get_text().strip()
#         print(title, link, content)
#
# url = 'https://zhuanlan.zhihu.com/p/193129156'
# html = get_html(url)
# print(html)
# # if html:
# #     parse_html(html)
# # else:
# #     print('获取网页失败')

import requests
from lxml import etree
import json
import time

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "cookie": 'SESSIONID=i26zmaNv74HqUt6AVOjDsqeAgHZCZzkDALWYRTKhft7; JOID=U18SBEsWNZ6siFH_QRDix5tcclVfYHLxw9kSkxdiddzLwhWdG71lFMyPV_9GVXGvjWPX9s1wGKj__LIQi3JaKNM=; osd=W1wVCkkeNpmiiln8Rh7gz5hbfFdXY3X_wdERlBlgfd_MzBeVGLprFsSMUPFEXXKog2Hf9cp-GqD8-7wSg3FdJtE=; _xsrf=DKUToyUGBBtLYqZjP9sh1f12dn2obzjO; _zap=dad2c387-0db9-475d-819c-454316e1ccc4; d_c0=ANDeW9AlrRiPTh_Pislk-ZqJ8SgXtZowSNE=|1716716606; tst=r; __zse_ck=001_/4ysJIiy7pwD9bXaPjzd0PWk9mzWhQo0i0C235GVGpYtdk+d/yzAYPSZ5yRO=2L18iTtF=Ubq3tA1p1XbjfiK2wySXtf/mbuqc4hkp8vOFUL8bwgG=LPRTZGUk/DKUim; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1719668076,1720186855,1720445831,1720531543; HMACCOUNT=558E7640EF772C11; z_c0=2|1:0|10:1720531549|4:z_c0|80:MS4xR3ZnOUFBQUFBQUFtQUFBQVlBSlZUV3hiYldkeDV3UW1FVkh5eGZuamppWmNxRTYyZVJyZE9RPT0=|112dd22024bb8d595e6eec107783e14a7c08453ad4aec478beaa716b134fddd0; BEC=d3764731444d280df266d88d1a8361e0; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1720537268; Hm_lvt_bff3d83079cef1ed8fc5e3f4579ec3b3=1720537269; Hm_lpvt_bff3d83079cef1ed8fc5e3f4579ec3b3=1720537269; RT="z=1&dm=zhihu.com&si=4c0a7e9b-cc35-4c44-a42b-37306f111880&ss=lyeip8ue&sl=6&tt=dha&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=rk9z  &ul=t0o6"',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}


#采集知乎专栏文章标题数据
def get_zhuhu_info(url):
    # data_list = []
    res = requests.get(url=url, headers=headers)
    return res.text
    # for i in res['data']:
    #     try:
    #         data_list = []
    #         title=i['title']
    #         zan_count=i['voteup_count']
    #         comment_count = i['comment_count']
    #         created = time.strftime("%Y-%m-%d", time.localtime(i['created']))
    #         print('标题：',title,'点赞数：',zan_count,'评论数：',comment_count,'时间',created)
    #         data_list.append(title)
    #         data_list.append(zan_count)
    #         data_list.append(comment_count)
    #         data_list.append(created)
    #     except:
    #         print('出错了')
    #         continue


class Doc:
    def __init__(self, title, keywords, content):
        return


filter_tags = ['style', 'script', '']


def gen_item_map(item_list):
    retval_content = ""
    for item in item_list:
        html_tag = item[0]
        # print(html_tag)
        content = item[1]
        tag = html_tag.split(' ')[0][1:]
        if tag not in filter_tags:
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
            # print("------", pre_str + ">>>>>>>" + plain_text)
            item_map.append([pre_str, plain_text])
        item_str = html_str[pre_index:post_index + 1]
        pre_str = item_str
        html_str = html_str[post_index + 1:]
    raw_content = gen_item_map(item_map)
    return raw_content


if __name__ == '__main__':
    # url = "https://zhuanlan.zhihu.com/p/670958880"
    # data = get_zhuhu_info(url)
    # open("./zhihu_html.data", "w", encoding='utf-8').write(data)
    html_str = ""
    for line in open("../LeetCode/zhihu_html.data", "r", encoding='utf-8').readlines():
        html_str += line.strip()
    raw_text = html_content_strip(html_str)
    print(raw_text)
