#coding:utf-8
import re
try:
    import urlparse
except:
    from urllib import parse as urlparse
from bs4 import BeautifulSoup

class HtmlParser(object):
    #爬虫调度器里传入新url和此url里的源码r.text
    def parser(self,page_url,html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url,soup)  # 查找新的url并返回，为set容器，为了去重
        new_data = self._get_new_data(page_url,soup)  # 解析从htmlparser传入的网页源代码，并返回所需数据
        return new_urls,new_data
    def _get_new_urls(self,page_url,soup):
        new_urls = set()
        #查找所有在a标签里满足表达式的href
        links = soup.find_all('a',href=re.compile(r'/item/.*'))
        for link in links:
            new_url = link['href']
            try:
                new_full_url = urlparse.urljoin(page_url,new_url)
            except:
                new_full_url = urlparse.urljoin(page_url.decode('utf-8'), new_url)
            new_urls.add(new_full_url)
        return new_urls
    def _get_new_data(self,page_url,soup):
        data = {}
        data['url'] = page_url
        title = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div',class_='lemma-summary')
        if summary:
            data['summary'] = summary.get_text()
        else:
            data['summary'] = ''
        return data









