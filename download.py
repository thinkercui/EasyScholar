#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
from bs4 import BeautifulSoup

"""
it is a pity that baidu scholar is wrong:
1.cited itself;
2.cited a paper that later!
"""

class BDXS:
    def __init__(self):
        self.baseURL = "http://xueshu.baidu.com"

    def getPage(self,kw):
        html = urllib2.urlopen(self.baseURL + "/s?wd=" + urllib.quote_plus(kw))
        return html

    def Parse(self,html):
        soup = BeautifulSoup(html.read(),'html.parser')
        #get all the paper it lists
        allPapers = []
        for paper in soup.find_all("div",class_="result xpath-log"):
            #every paper has a content and a extra
            dic = {}
            #content
            content = paper.find("div",class_="sc_content")
            dic["name"] = content.find("h3").get_text()
            dic["sc_info"] = content.find("div",class_="sc_info").get_text()
            dic["c_abstract"] = content.find("div",class_="c_abstract").get_text()
            dic["href_cited"] = None
            dic["href_related"] = None
            #extra:be cited and relation papers
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

if __name__=="__main__":
    bdxs = BDXS()
    html = bdxs.getPage("Is DNA a Language?")
    allPapers = bdxs.Parse(html)

    for paper in allPapers:
        print "%s:%s"%("name",paper["name"])
        print "%s:%s"%("sc_info",paper["sc_info"])
        print "%s:%s"%("href_cited",paper["href_cited"])
        print "%s:%s"%("href_related",paper["href_related"])
        print "\n"
