#-*- coding: utf-8 -*-
from urllib2 import urlopen
from bs4 import BeautifulSoup
import re

url = urlopen("http://www.circ.gov.cn/tabid/6757/Default.aspx")
#soup = BeautifulSoup(url, 'html.parser')
def get_hiddenvalue(url):

    resu = url.read()
    rex = r'''''<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)"'''
    VIEWSTATE = re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)">', re.I)
    #EVENTVALIDATION = re.findall(rex, resu, re.I)

    #return VIEWSTATE, EVENTVALIDATION
    print VIEWSTATE
test = get_hiddenvalue(url)