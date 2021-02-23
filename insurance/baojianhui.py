#-*- coding: utf-8 -*-
from urllib2 import urlopen
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

filename = open(r'.\insurance1.txt', 'a')

url = urlopen("http://www.circ.gov.cn/tabid/5253/ctl/ViewOrg/mid/16658/ItemID/336474/Default.aspx")
soup = BeautifulSoup(url, 'html.parser')

for table in soup.findAll('table')[5:6]:
        for tr in table.findAll('tr')[1:]:
                for td in tr.findAll('td')[0:1]:
                        content = td.get_text().strip()
                        print content
                        filename.write(content)
                        filename.write('\n')




