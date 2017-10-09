#coding:utf8
import codecs
import time

class DataOutput(object):
    def __init__(self):
        #以时间命名要写入的文件
        self.filepath = 'baike_%s.html'%(time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime()))
        #命名之后就马上写入html头部
        self.output_head(self.filepath)
        self.datas = []

    def store_data(self,data):
        if data is None:
            return
        self.datas.append(data)
        #与基础爬虫不同的是，本爬虫在接收到数据的同时进行存储
        if len(self.datas) > 0:
            self.output_html(self.filepath)

    def output_head(self,path):
        #写入html头
        fout = codecs.open(path,'w',encoding='utf-8')
        fout.write('<html>')
        fout.write('<head><meta charset="utf-8"/></head>')
        fout.write('<body>')
        fout.write('<table>')
        fout.close()

    def output_html(self,path):
        fout = codecs.open(path,'a',encoding='utf-8')#以添加的方式写入
        for data in self.datas[:]:#源码直接迭代self.datas会造成数据丢失一半，所以这里依然以切片形式迭代
            fout.write('<tr>')
            fout.write('<td>%s</td>'%data['url'].decode('utf-8'))#如果对其进行解码的话，需要用decode('utf-8')注意这里有没有等于号哦
            fout.write('<td>%s</td>'%data['title'])#编码的话用encode('utf-8)，
            fout.write('<td>%s</td>'%data['summary'])#解码在Python2都是解为Unicode，在Python3都是解为str
            self.datas.remove(data)
        fout.close()

    #这一步估计到爬虫之后结束的时候才调取
    def ouput_end(self,path):
        #输出html结尾
        fout = codecs.open(path,'a',encoding='utf-8')
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()




