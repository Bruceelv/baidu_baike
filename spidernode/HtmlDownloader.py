#coding:utf-8
import requests

#提取网页源代码，通用代码
class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.get(url,headers=headers)
        if r.status_code == 200:#注意这里的200是数字，不能加引号
            r.encoding='utf-8'
            print('网页源码已被提取')
            return r.text
        print('很不幸，源码没有被提取')