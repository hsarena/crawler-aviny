# -*- coding: utf-8 -*-
import scrapy
import re
from aviny.items import AvinyItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from newspaper import Article, Config
from bs4 import BeautifulSoup
from scrapy import Selector
import pandas as pd

class VoicesLinkSpider(CrawlSpider):
    name = 'voices-link'
    allowed_domains = ['aviny.com']
    start_urls = ['http://www.aviny.com/Voice']

    rules = (Rule(LinkExtractor(allow=('.*Voice.*','.*voice.*'), deny=('.*Mobile.*','.*mobile.*','\.apk', '\.pdf', '\.zip', '\.jpg', '\.html')), callback='parse_item', follow=True),)

    def parse_item(self, response):
        url = response.url
        page = Article(url)
        page.download()
        page.parse()
        title = page.title
        bs = BeautifulSoup(page.html, features='lxml')
        for t in bs.find_all('table'):
                for l in t.find_all('a', href=True):
                    #if (re.match('\.mp3', l['href']) ) or (re.match('\.wma', l['href'])):
                    tmp = '  ' + l['href'] + '  '
                    l.insert_after(tmp)
                    #else:
                     #   break

        html_str = str(bs)
        df_list = pd.read_html(html_str)
        for i, df in enumerate(df_list):
            #df.to_csv('table {}.csv'.format(title), encoding='utf-8', index=False)
            df.to_json('json {}.json'.format(title))







