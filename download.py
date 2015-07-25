#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
from bs4 import BeautifulSoup


class BDXS:
    def __init__(self):
        self.baseURL = "http://xueshu.baidu.com/s?wd="

    def getPage(self,kw):
        html = urllib2.urlopen(self.baseURL + urllib.quote_plus(kw))
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
            #extra:reference papers and relation papers
            extra = paper.find("div",class_="sc_ext")
            #reference
            reference = extra.find("div",class_="sc_cite")
            relation = extra.find("div",class_="sc_other")
            allPapers.append(dic)
        return allPapers

if __name__=="__main__":
    bdxs = BDXS()
    html = bdxs.getPage("Is DNA a Language?")
    allPapers = bdxs.Parse(html)

    for paper in allPapers:
        for key in paper:
            print "%s:%s"%(key,paper[key])
        

