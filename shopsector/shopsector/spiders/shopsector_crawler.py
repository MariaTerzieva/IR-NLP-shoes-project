# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from shopsector.items import ShopsectorItem


class ShopsectorCrawlerSpider(CrawlSpider):
    name = 'shopsector_crawler'
    allowed_domains = ['shopsector.com']
    start_urls = ['http://www.shopsector.com/jeni/obuvki']

    rules = (
        Rule(LinkExtractor(allow=r'jeni/obuvki\?page=(\d|10)$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for link in response.xpath('//*[@id="repeat-white-2"]/div/div'):
            item = ShopsectorItem()
            item['gender'] = 'male'
            item['title'] = link.xpath('div[2]/a/span/text()').extract()[0]
            item['photo'] = response.urljoin(link.xpath('div[1]/a/img/@src').extract()[0])
            item['link'] = response.urljoin(link.xpath('div[2]/a/@href').extract()[0])
            item['price'] = link.xpath('div[3]/span[2]/text()').extract()[0]
            item['sizes'] = tuple(link.xpath('div[5]/span/text()').extract())
            request = scrapy.Request(item['link'], callback=self.parse_url_contents)
            request.meta['item'] = item
            yield request

    def parse_url_contents(self, response):
        item = response.meta['item']
        item['colors'] = (response.xpath(u'//strong[starts-with(text(), \'\u0426\u0412\u042f\u0422\')]/text()').extract()[0][6:],)
        yield item
