#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
from bs4 import BeautifulSoup
from Queue import Queue

"""
it is a pity that baidu scholar is wrong:
1.cited itself(it can be used as the end of the program);
2.cited a paper that is later!(this will be dealed later)
"""

class BDXS:
    def __init__(self):
        self.baseURL = "http://xueshu.baidu.com"
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'}
        self.depth = 3 
        
    def getURLByKW(self,kw):
        return self.baseURL + "/s?wd=" + urllib.quote_plus(kw)
    
    def getPageByURL(self,url):
        #perform like the browser
        req = urllib2.Request(url = url,headers = self.headers)
        html = urllib2.urlopen(req)
        return html

    def Parse(self,html):
        soup = BeautifulSoup(html.read(),'html.parser')
        parent = soup.find("div",class_="sc_cite_hint")
        page = soup.find("p",id="page")
        nextpage = None
        if page is not None:
            nextpage = page.find("a",class_="n")
        if parent is not None:
            parent = parent.span.get_text()
        if nextpage is not None:
            if nextpage.get_text() is "下一页>":
                nextpage = self.baseURL + nextpage["href"]
            else:
                nextpage = None
        #get all the paper it lists
        allPapers = []
        for paper in soup.find_all("div",class_="result xpath-log"):
            #every paper has a content and an extra
            dic = {}
            #content
            content = paper.find("div",class_="sc_content")
            dic["name"] = content.find("h3").get_text()
            dic["parent"] = parent
            dic["sc_info"] = content.find("div",class_="sc_info").get_text()
            dic["c_abstract"] = content.find("div",class_="c_abstract").get_text()
            dic["href_cited"] = None
            dic["href_related"] = None
            #extra:be cited and related papers
            extra = paper.find("div",class_="sc_ext")
            #cited(sc_cite)
            cited = extra.find("div",class_="sc_cite")
            if cited.a is not None:
                href_cited = cited.a['href']
                dic["href_cited"] = self.baseURL + href_cited
            #related(sc_other)
            related = extra.find("div",class_="sc_other")
            href_related = related.find("a",class_="c-icon-file-hover")['href']
            dic["href_related"] = self.baseURL + href_related
            allPapers.append(dic)
        return allPapers,nextpage

    #set the depth of the spider(default is 3)
    def setDepth(self,depth):
        self.depth = depth

    #last in first out
    def getLIFO(self,url):
        urlremain = []
        urldepth = []
        urldealed = []
        allPapers = []
        count = 0
        urlremain.append(url)
        urldepth.append(0)
        while len(urlremain) is not 0:
            print count,len(urlremain),len(urldealed)
            count = count + 1
            url = urlremain.pop()
            pdepth = urldepth.pop()
            if pdepth > self.depth:
                continue
            urldealed.append(url)
            html = self.getPageByURL(url)
            tmpPapers,nextpage = self.Parse(html)
            allPapers.extend(tmpPapers)
            for paper in tmpPapers:
                if paper["href_cited"] is not None and paper["href_cited"] not in urlremain and paper["href_cited"] not in urldealed:
                    urlremain.append(paper["href_cited"])
                    urldepth.append(pdepth + 1)
            if nextpage is not None:
                urlremain.append(nextpage)
                urldepth.append(pdepth)
        return allPapers
    
    #first in first out(optional)
    def getFIFO(self,url):
        urlremain = []
        urldealed = []
        allPapers = []
        count = 0
        urlremain.append(url)
        while len(urlremain) is not 0:
            print count,len(urlremain),len(urldealed)
            count = count + 1
            url = urlremain.pop(0)
            urldealed.append(url)
            html = self.getPageByURL(url)
            tmpPapers,nextpage = self.Parse(html)
            allPapers.extend(tmpPapers)
            for paper in tmpPapers:
                if paper["href_cited"] is not None and paper["href_cited"] not in urlremain and paper["href_cited"] not in urldealed:
                    urlremain.append(paper["href_cited"])
            if nextpage is not None:
                urlremain.append(nextpage)        
        return allPapers

if __name__=="__main__":
    """
    #only one page
    #import pdb;pdb.set_trace();
    bdxs = BDXS()
    url = bdxs.getURLByKW("Is DNA a Language?")
    html = bdxs.getPageByURL(url)
    papers = bdxs.Parse(html)
    url = papers[0]["href_cited"]
    html = bdxs.getPageByURL(url)
    allPapers = bdxs.Parse(html)

    for paper in allPapers:
        print "%s:%s"%("name",paper["name"])
        print "%s:%s"%("parent",paper["parent"])
        print "%s:%s"%("sc_info",paper["sc_info"])
        #print "%s:%s"%("href_cited",paper["href_cited"])
        #print "%s:%s"%("href_related",paper["href_related"])
        print "\n"
    """

    #"""
    #get all the pages
    bdxs = BDXS()
    url = bdxs.getURLByKW("Is DNA a Language?")
    html = bdxs.getPageByURL(url)
    papers,nextpage = bdxs.Parse(html)
    url = papers[0]["href_cited"]
    allPapers = bdxs.getLIFO(url)      

    for paper in allPapers:
        print "%s:%s"%("name",paper["name"])
        print "%s:%s"%("sc_info",paper["sc_info"])
        print "%s:%s"%("sc_info",paper["sc_info"])
        #print "%s:%s"%("href_cited",paper["href_cited"])
        #print "%s:%s"%("href_related",paper["href_related"])
        print "\n"
    #"""
    
