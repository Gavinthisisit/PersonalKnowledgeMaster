import requests
from crawl_weixin import Spider
# from lxml import etree
# import json
# import time

class ZhiHu(Spider):
    #采集知乎专栏文章标题数据
    def crawl(self):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "cookie": 'SESSIONID=i26zmaNv74HqUt6AVOjDsqeAgHZCZzkDALWYRTKhft7; JOID=U18SBEsWNZ6siFH_QRDix5tcclVfYHLxw9kSkxdiddzLwhWdG71lFMyPV_9GVXGvjWPX9s1wGKj__LIQi3JaKNM=; osd=W1wVCkkeNpmiiln8Rh7gz5hbfFdXY3X_wdERlBlgfd_MzBeVGLprFsSMUPFEXXKog2Hf9cp-GqD8-7wSg3FdJtE=; _xsrf=DKUToyUGBBtLYqZjP9sh1f12dn2obzjO; _zap=dad2c387-0db9-475d-819c-454316e1ccc4; d_c0=ANDeW9AlrRiPTh_Pislk-ZqJ8SgXtZowSNE=|1716716606; tst=r; __zse_ck=001_/4ysJIiy7pwD9bXaPjzd0PWk9mzWhQo0i0C235GVGpYtdk+d/yzAYPSZ5yRO=2L18iTtF=Ubq3tA1p1XbjfiK2wySXtf/mbuqc4hkp8vOFUL8bwgG=LPRTZGUk/DKUim; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1719668076,1720186855,1720445831,1720531543; HMACCOUNT=558E7640EF772C11; z_c0=2|1:0|10:1720531549|4:z_c0|80:MS4xR3ZnOUFBQUFBQUFtQUFBQVlBSlZUV3hiYldkeDV3UW1FVkh5eGZuamppWmNxRTYyZVJyZE9RPT0=|112dd22024bb8d595e6eec107783e14a7c08453ad4aec478beaa716b134fddd0; BEC=d3764731444d280df266d88d1a8361e0; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1720537268; Hm_lvt_bff3d83079cef1ed8fc5e3f4579ec3b3=1720537269; Hm_lpvt_bff3d83079cef1ed8fc5e3f4579ec3b3=1720537269; RT="z=1&dm=zhihu.com&si=4c0a7e9b-cc35-4c44-a42b-37306f111880&ss=lyeip8ue&sl=6&tt=dha&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=rk9z  &ul=t0o6"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        res = requests.get(url=self.url, headers=headers)
        self.html_content = res.text

    def get_content(self):
        self.crawl()
        plain_content = self.html_content_strip(self.html_content)
        return plain_content

if __name__ == '__main__':
    url = "https://zhuanlan.zhihu.com/p/670958880"
    zhihu = ZhiHu(url)
    data = zhihu.get_content()
    # open("../data/zhihu_html.data", "w", encoding='utf-8').write(data)
    # html_str = ""
    # for line in open("../data/zhihu_html.data", "r", encoding='utf-8').readlines():
    #     html_str += line.strip()
    # raw_text = html_content_strip(html_str)
    print(data)
