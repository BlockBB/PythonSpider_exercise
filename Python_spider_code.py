#__author__ = 'Gang'
# -*- coding:utf-8 -*-
import urllib.request
import urllib.error
import re
import _thread
import time
import readline


class  QSBK:
    def __init__(self):
        #INIT definition
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        #Init header
        self.headers = { 'User-Agent' : self.user_agent }
        # store the fun story in every element
        self.stories = []
        # store parameter  which control if run this process
        self.enable = False
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib.request.Request(url,headers = self.headers)
            response = urllib.request.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode

        except  urllib.error.URLError as e:
             if hasattr(e,"code"):
                print(e.code)
             if hasattr(e,"reason"):
                print(e.reason)
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print("load page fail")
            return  None
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
                         '="content".*?(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
             haveImg = re.search("img",item[2])
             if not haveImg:
                 #Remove whitespace with str.strip()
                pageStories.append([item[0].strip(),item[1].strip(),item[3].strip()])
                #print(item[3])


        return pageStories
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
               pageStories = self.getPageItems(self.pageIndex)
               if pageStories:
                   self.stories.append(pageStories)
                   self.pageIndex +=1

    def getOneStory(self,pageStories,page):
        for story in pageStories:
            #waint user input
            user_input = input()
            #when input enter ,check if it should be load the new page for next time.
            self.loadPage()
            if user_input== "Q":
                self.enable = False
                return
            print("the page is %d\t author is :%s\n content is %s\n and vote number is %s\n"%(page,story[0],story[1],story[2]))
    def start(self):
        print("it is reading QiuShiBaiKe,type enter key to check new story,Q is exit")
        self.enable = True
        #loader a page of content
        self.loadPage()
        #local parameter to control current reading page
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
               #get one page sotry from gloable list
               pageStories = self.stories[0]
               #add one page from current page
               nowPage +=1
               #delete the first element from global list as got it
               del self.stories[0]
               #output this story
               self.getOneStory(pageStories,nowPage)
spider = QSBK()
spider.start()





