#coding:utf8
from multiprocessing import Queue,Process
from multiprocessing.managers import BaseManager
import time
from URLManager import UrlManager
from DataOutput import DataOutput

class NodeManager(object):
    def start_manager(self,url_q,result_q):
        #创建一个分布式管理器
        #url_q：url队列
        #result_q：结果队列
        BaseManager.register('get_task_queue',callable=lambda:url_q)
        BaseManager.register('get_result_queue',callable=lambda:result_q)
        #绑定端口8001，设置验证口令‘baike’。这步相当于初始化
        try:
            manager = BaseManager(address=('',8001),authkey='baike')
        except:
            manager = BaseManager(address=('',8001),authkey=b'baike')

        return manager

    #url管理进程
    def url_manager_proc(self,url_q,conn_q,root_url):
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while url_manager.has_new_url():#如果存在未爬取的url，因上一步已经传入url，所以整个程序在此被触发
                #获取新的url
                new_url = url_manager.get_new_url()
                #将新的url添加到队列，发给工作节点，传给spider.py的self.task
                url_q.put(new_url)
                print('old_url=',url_manager.old_url_size())
                #这个爬取的规则跟上一个不一样，上一个是符合要求就爬取，这个是不符合要求就停止
                if (url_manager.old_url_size() > 1000):
                    #通知爬行节点工作结束
                    url_q.put('end')
                    print('控制节点发出结束通知')
                    #调用url管理器的存储url的方法。当爬取规定数量的url之后，把已爬取和未爬取的url进行存储
                    url_manager.save_progress('new_urls.txt',url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt',url_manager.old_urls)
                    return
            #将从result_solve_proc方法获取到的urls添加到url管理器
            #因为conn_q已经在主进程里声明过了为队列，所有如果方法里传入，则基本上可以认为是全局的
            #在下一方法中进行修改，则影响本方法，因下一方法是存储的，所有本方法直接判断是否为空是可以的，无需引用函数
            try:
                if not conn_q.empty():#如果队列不为空
                    urls = conn_q.get()#把所有从新网页里获取的新url提取出来，
                    url_manager.add_new_urls(urls)#并传入url管理器进行存储
            except BaseException as e:
                time.sleep(0.1)

    #数据提取进程
    def result_solve_proc(self,result_q,conn_q,store_q):
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get(True)  # True为默认，如果取不到数据就一直等待
                    if content['new_urls'] == 'end':
                        print('结果分析进程接受通知然后结束！')
                        store_q.put('end')
                        return
                    conn_q.put(content['new_urls'])#content为从爬虫调度器接收过来的，new_urls为新url集合，为set类型
                    store_q.put(content['data'])#data解析出来的数据为dict类型。这步写，store_proc中读
                else:
                    time.sleep(0.1)
            except BaseException as e:
                time.sleep(0.1)

    #数据存储进程
    def store_proc(self,store_q):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程接受通知然后结束！')
                    output.ouput_end(output.filepath)#到此爬虫生命结束，写入html结尾标签
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)
        pass#应该不用写也行

if __name__ == '__main__':
    #程序中这一步是最先执行。首先是初始化4个队列，即创建队列的实例
    url_q = Queue()  # 与子节点通信队列，传入url
    result_q = Queue()  # 与子节点通信队列，传入数据

    store_q = Queue()  # 存储队列，接收子节点传入过来的数据，并进行存储
    conn_q = Queue()  # url中转队列，接收从子节点传入过来的url，并传给urlmanager
    #创建分布式管理器（1初始化NodeManager，2调用分布式管理器方法）
    node = NodeManager()
    manager = node.start_manager(url_q,result_q)

    #创建url管理进程、数据提取进程和数据存储进程
    url_manager_proc = Process(target=node.url_manager_proc,args=(url_q,conn_q,'https://baike.baidu.com/item/%E7%A8%8B%E5%BA%8F%E5%91%98/62748',))
    result_solve_proc = Process(target=node.result_solve_proc,args=(result_q,conn_q,store_q,))
    store_proc = Process(target=node.store_proc,args=(store_q,))

    #启动3个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()

    manager.get_server().serve_forever()












