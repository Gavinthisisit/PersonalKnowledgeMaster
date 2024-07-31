from crawl_zhihu import ZhiHu
from crawl_weixin import WeiXin
from typing import Any

class Crawler:
    def __init__(self, url: str):
        self.url = url
        if 'zhihu.com' in url:
            self.loader = ZhiHu(url)
        elif "mp.weixin.qq.com" in url:
            self.loader = WeiXin(url)
        else:
            self.loader = None
    
    def crawl(self):
        if self.loader == None:
            return ""
        plain_content = self.loader.get_content()
        return plain_content

