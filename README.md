# baidu_baike
手写分布式爬虫爬取百度百科相关的词条

Python版本：
2.7.13/3.6.1已做兼容处理，两个版本通用。

本程序为百度百科词条的的爬取，默认是搜索提取与“程序员”有关的1000个词条。
程序的入口在NodeManager.py中url_manager_proc进程，如果需要搜索其他相关的词条，可以把此进程的url变换为所需词条的链接。运行此程序之后，再运行子节点的：SpiderNode.py，即可爬取并存储。

如需爬取其他网页，只需修改2处，
1 程序入口NodeManager.py中url_manager_proc进程链接。
2 子节点spidernode中的HtmlParser.py中的两个方法：_get_new_urls和_get_new_data，前者用于提取所符合需求的URL以待进一步爬取；后者用于提取符合需求的数据。

另外如果爬取的网页需要做反爬虫处理，本程序可以作为扩展，请在子节点的HtmlDownloader.py中添加相关设置。
