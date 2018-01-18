#-*- coding:utf-8 -*-
import requests
from lxml import etree
import os
proxys = {'http':'http://127.0.0.1:1080','https':'https://127.0.0.1:1080'}
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}
# url = 'http://www.sis001.com/forum/attachment.php?aid=3017893'
# res = requests.get(url,proxies=proxys,headers=headers,verify=False)
# with open('test.torrent','wb') as f:
#     f.write(res.content)
# print(res.text)

if __name__ == "__main__":
    domain_url = 'http://www.sis001.com/forum/'
    torrentdir = "torrent/"
    #获得具体的torrent所在的页面
    for x in range(30,100):
        torrent_url_list = []
        page_url = 'http://www.sis001.com/forum/forum-58-{page}.html'.format(page=x)
        res = requests.get(page_url,proxies=proxys,headers=headers,verify=False)
        res.encoding = 'utf-8'
        selector = etree.HTML(res.text)
        # print(res.text)
        tables= selector.xpath('//table[@id]')
        tmpurls = tables[-1].xpath('./tbody[@id]/tr/th/span/a/@href')
        # tmpurls = tbody.xpath('./tr/th/span/a/@href')
        torrent_url_list.extend([domain_url+x for x in tmpurls])    #获得具体某个页面的url列表
        #下面是对具体种子页面进行操作，需要保存图片和torrent种子（保存在一个文件夹下）
        for url in torrent_url_list:
            try:
                res = requests.get(url,proxies=proxys,headers=headers,verify=False)
                res.encoding = 'utf-8'
                selector = etree.HTML(res.text)
                div1 = selector.xpath('//div[@class="postmessage defaultpost"]')[0]
                name = div1.xpath('.//dt/a[last()-1]/text()')[0]
                pic_url = div1.xpath('.//img[@onclick]/@src')[0]
                torrent_url = div1.xpath('.//dt/a[last()-1]/@href')[0]
                torrent_url = domain_url+torrent_url
                filedir = os.path.splitext(name)[0]
                filedir = torrentdir + filedir
                if not os.path.exists(filedir):
                    os.makedirs(filedir)

                with open(os.path.join(filedir,'pic.jpg'),'wb') as f:
                    f.write(requests.get(pic_url,proxies=proxys).content)
                with open(os.path.join(filedir,name+".torrent"),'wb') as f:
                    f.write(requests.get(torrent_url,proxies = proxys).content)
            except:
                pass
        # break



