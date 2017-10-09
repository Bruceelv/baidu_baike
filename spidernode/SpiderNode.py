#coding:utf8
from multiprocessing.managers import BaseManager
from HtmlParser import HtmlParser
from HtmlDownloader import HtmlDownloader
import time

t1 = time.time()
class SpiderWork(object):
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        server_addr = '127.0.0.1'
        print('Connect to server %s...'%server_addr)
        #端口和验证口令注意保持与服务进程设置的完全一致
        try:
            self.m = BaseManager(address=(server_addr,8001),authkey='baike')
        except:
            self.m = BaseManager(address=(server_addr, 8001), authkey=b'baike')
        #从网络连接（链接到NodeManager里的分布式管理器）
        self.m.connect()
        #实现第三步：获取Queue的对象即在NodeManager中注册到网络上的queue
        self.task = self.m.get_task_queue()  #代表url_q
        self.result = self.m.get_result_queue()  #代表result_q
        #初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():#因为第一个url已经传入，所以url_q不为空，这个程序被触发
                    url = self.task.get()#取出url，即控制调度器里的url_q队列在这里被取出

                    #在控制调度器里已经说明，如果满足结束条件，则往队列里写入‘end'
                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作。。。')
                        self.result.put({'new_urls':'end','data':'end'})
                        t2 = time.time()
                        print(t2-t1)
                        return
                    try:
                        print('爬虫节点正在解析：%s'%url.encode('utf-8'))
                    except:
                        print('爬虫节点正在解析：%s' % url)
                    content = self.downloader.download(url)
                    print('准备提交给解析管理器')
                    new_urls,data = self.parser.parser(url,content)
                    # 这里是个接口，把提取出的新url和数据放入队列，由控制管理器接收，注意传入的是个字典哦
                    self.result.put({'new_urls':new_urls,'data':data})
            except EOFError as e:
                print(e)
                print('Crawl fali')

if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl()
