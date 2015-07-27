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

    def getURLByKW(self,kw):
        return self.baseURL + "/s?wd=" + urllib.quote_plus(kw)
    
    def getPageByURL(self,url):
        html = urllib2.urlopen(url)
        return html

    def Parse(self,html):
        soup = BeautifulSoup(html.read(),'html.parser')
        #get all the paper it lists
        allPapers = []
        for paper in soup.find_all("div",class_="result xpath-log"):
            #every paper has a content and an extra
            dic = {}
            #content
            content = paper.find("div",class_="sc_content")
            dic["name"] = content.find("h3").get_text()
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
        return allPapers

    #last in first out
    def getLIFO(self,url):
        urlremain = []
        urldealed = []
        allPapers = []
        count = 0
        urlremain.append(url)
        while len(urlremain) is not 0:
            print count,len(urlremain),len(urldealed)
            count = count + 1
            url = urlremain.pop()
            urldealed.append(url)
            html = self.getPageByURL(url)
            tmpPapers = self.Parse(html)
            allPapers.extend(tmpPapers)
            for paper in tmpPapers:
                if paper["href_cited"] is not None and paper["href_cited"] not in urlremain and paper["href_cited"] not in urldealed:
                    urlremain.append(paper["href_cited"])
        
        return allPapers
    
    #first in first out
    def getFIFO(self,url):
        urlremain = []
        urldealed = []
        allPapers = []
        count = 0
        urlremain.append(url)
        while len(urlremain) is not 0:
            print count
            count = count + 1
            url = urlremain.pop(0)
            urldealed.append(url)
            html = self.getPageByURL(url)
            tmpPapers = self.Parse(html)
            allPapers.extend(tmpPapers)
            for paper in tmpPapers:
                if paper["href_cited"] is not None and paper["href_cited"] not in urlremain and paper["href_cited"] not in urldealed:
                    urlremain.append(paper["href_cited"])
        
        return allPapers

if __name__=="__main__":
    #"""
    #only one page
    bdxs = BDXS()
    url = bdxs.getURLByKW("Is DNA a Language?")
    html = bdxs.getPageByURL(url)
    allPapers = bdxs.Parse(html)      

    for paper in allPapers:
        print "%s:%s"%("name",paper["name"])
        print "%s:%s"%("sc_info",paper["sc_info"])
        print "%s:%s"%("href_cited",paper["href_cited"])
        print "%s:%s"%("href_related",paper["href_related"])
        print "\n"
    #"""

    """
    #get all the pages
    bdxs = BDXS()
    url = bdxs.getURLByKW("Is DNA a Language?")
    html = bdxs.getPageByURL(url)
    papers = bdxs.Parse(html)
    url = papers[0]["href_cited"]
    allPapers = bdxs.getLIFO(url)      

    for paper in allPapers:
        print "%s:%s"%("name",paper["name"])
        print "%s:%s"%("sc_info",paper["sc_info"])
        print "%s:%s"%("href_cited",paper["href_cited"])
        print "%s:%s"%("href_related",paper["href_related"])
        print "\n"
    """
    
