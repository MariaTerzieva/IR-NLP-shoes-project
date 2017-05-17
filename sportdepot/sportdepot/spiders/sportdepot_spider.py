# -*- coding: utf-8 -*-
import scrapy

from sportdepot.items import SportdepotItem


class SportdepotSpider(scrapy.Spider):
    name = "sportdepot"
    allowed_domains = ["sportdepot.bg"]
    start_urls = ["http://sportdepot.bg/bg/muje-obuvki",]

    def parse(self, response):
        for link in response.xpath('//*[@id="list"]/div'):
            item = SportdepotItem()
            item['title'] = link.xpath('normalize-space(div[3]/div/h5/a/text())').extract()[0]
            item['photo'] = response.urljoin(link.xpath('div[2]/a/img/@src').extract()[0])
            url = response.urljoin(link.xpath('div[3]/div/h5/a/@href').extract()[0])
            request = scrapy.Request(url, callback=self.parse_url_contents)
            request.meta['item'] = item
            yield request

    def parse_url_contents(self, response):
        item = response.meta['item']
        item['link'] = response.url
        prices = tuple(response.xpath('//*[@id="product"]/div[2]/p[1]/text()').extract())
        if len(prices) == 3:
            item['price'] = prices[1]
        else:
            item['price'] = prices[0].strip() 
        item['colors'] = tuple(response.xpath('//*[@id="product"]/div[2]/fieldset/div[1]/ul/li/@title').extract())
        item['sizes'] = tuple(response.xpath('//*[@id="product"]/div[2]/fieldset/div[2]/ul/li/@title').extract())
        item['gender'] = 'male'
        yield item
