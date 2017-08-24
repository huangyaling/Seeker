# coding:utf-8
__author__ = 'huangyaling'
import urllib2
import re

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []


    #获取页面代码
    def getPage(self, pageIndex):
        try:
            url = 'https://www.qiushibaike.com/8hr/page/'+str(pageIndex)+'/'
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode=response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u"连接糗事百科失败原因:",e.reason
                return None


    #传入获取到的代码，获取段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败'
            return None
        pattern = re.compile('<div.*?author clearfix">.*?<a.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?<i class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[1])
            pageStories.append([item[0].strip(), text.strip(),item[2].strip()])
        return pageStories

    #加载提取页面内容，加入到列表中
    def loadPage(self):
        if self.enable == True:
            if len(self.stories)<2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    #每敲一次回车加载一条段子
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人：%s\t赞：%s\n%s"%(page, story[0],story[2],story[1])

    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        self.enable=True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pafeStories = self.stories[0]
                nowPage +=1
                del self.stories[0]
                self.getOneStory(pafeStories,nowPage)

spider = QSBK()
spider.start()




