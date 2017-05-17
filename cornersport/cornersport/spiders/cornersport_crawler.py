# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from cornersport.items import CornersportItem


class CornersportCrawlerSpider(CrawlSpider):
    name = 'cornersport_crawler'
    allowed_domains = ['cornersport.eu']
    start_urls = ["http://cornersport.eu/zheni/obuvki?p=1&tsvyat=cherven",
                  "http://cornersport.eu/zheni/obuvki?p=1&tsvyat=sin",
                  "http://cornersport.eu/zheni/obuvki?p=1&tsvyat=siv",
                  "http://cornersport.eu/zheni/obuvki?p=1&tsvyat=zelen",
                  "http://cornersport.eu/zheni/obuvki?p=1&tsvyat=kafyav",
                  "http://cornersport.eu/zheni/obuvki?p=1&tsvyat=zhalt",
                  "http://cornersport.eu/zheni/obuvki?p=1&tsvyat=lilav",
                  "http://cornersport.eu/zheni/obuvki?p=1&tsvyat=rozov"]

    rules = (
        Rule(LinkExtractor(allow=(r'zheni/obuvki\?p=(\d|10|11)&tsvyat=byal$',
                                  r'zheni/obuvki\?p=(\d|10|11)&tsvyat=cherven$',
                                  r'zheni/obuvki\?p=(\d|10|11)&tsvyat=sin$',
                                  r'zheni/obuvki\?p=(\d|10|11)&tsvyat=siv$',
                                  r'zheni/obuvki\?p=(\d|10|11)&tsvyat=zelen$',
                                  r'zheni/obuvki\?p=(\d|10|11)&tsvyat=kafyav$',
                                  r'zheni/obuvki\?p=(\d|10|11)&tsvyat=zhalt$',
                                  r'zheni/obuvki\?p=(\d|10|11)&tsvyat=lilav$',
                                  r'zheni/obuvki\?p=(\d|10|11)&tsvyat=rozov$')),
                           callback='parse_item',
                           follow=True),
    )

    def parse_item(self, response):
        for link in response.xpath('//*[@id="main"]/div/div/div[2]/div[2]/div'):
            item = CornersportItem()
            item['gender'] = 'female'
            item['colors'] = (re.search('tsvyat=(.+?)$', response.url).group(1),)
            item['title'] = link.xpath('a[3]/text()').extract()[0]
            item['photo'] = link.xpath('a[1]/img/@src').extract()[0]
            item['link'] = link.xpath('a[3]/@href').extract()[0]
            item['price'] = link.xpath('div/p[2]/span[2]/text()').extract()[0]
            request = scrapy.Request(item['link'], callback=self.parse_url_contents)
            request.meta['item'] = item
            yield request

    def parse_url_contents(self, response):
        item = response.meta['item']
        sizes = response.xpath('//*[@id="allOpptions133"]/li/@data-label').extract()
        item['sizes'] = tuple(map(lambda x: re.search('U(.+?)\s', x).group(1), sizes))
        yield item
