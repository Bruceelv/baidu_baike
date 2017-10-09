#coding:utf8
try:
    import CPickle
except:
    import pickle
import hashlib

class UrlManager(object):
    def __init__(self):
        #之前的基础爬虫这一步是直接加载集合，现在是加载txt文档
        #如果new_urls.txt已经存在，则加载里面的数据，如果不存在，则返回set()
        self.new_urls = self.load_progress('new_urls.txt')#未爬取的url集合
        self.old_urls = self.load_progress('old_urls.txt')#已爬取的url集合

    def has_new_url(self):
        #跟上一个爬虫一样，这个方法可以不用定义，判断的时候直接调用self.new_url_size()
        return self.new_url_size() != 0

    def get_new_url(self):
        #从new_urls集合中提取一个url链接，待下一次爬取之用
        new_url = self.new_urls.pop()
        #接下来对new_url进行md5值的生产，其实不懂这个函数用法
        m = hashlib.md5()#初始化md5方法
        # new_url = new_url.encode('utf-8')
        m.update(new_url)#加入要生成md5的链接
        self.old_urls.add(m.hexdigest()[8:-8])#貌似是取中间的128位进行存储（总256位）
        return new_url

    #将新的url加入未爬取集合，被下一方法调用
    def add_new_url(self,url):
        if url is None:
            return
        url = url.encode('utf-8')
        m = hashlib.md5()
        m.update(url)
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)

    def save_progress(self,path,data):
        #path:文件路径
        #data:需要保存的数据
        with open(path,'wb') as f:
            pickle.dump(data,f)

    def load_progress(self,path):
        print('[+]从文件加载进度：%s' %path)
        try:
            with open(path,'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print('[!]无进度文件，创建：%s' % path)
        return set()







